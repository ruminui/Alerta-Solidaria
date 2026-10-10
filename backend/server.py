"""Alerta Solidaria community coordination API. Pilot only, not a dispatch system.
Python 3.11+ stdlib. Same-origin, opt-in and no public exact coordinates.
"""
from __future__ import annotations
import hashlib, hmac, json, math, os, re, secrets, sqlite3, threading, time, urllib.request, uuid
from collections import defaultdict, deque
from contextlib import contextmanager
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
DB = Path(os.environ.get('AS_DB', str(ROOT / 'alerta.db')))
HOST = os.environ.get('AS_HOST', '127.0.0.1')
PORT = int(os.environ.get('PORT', os.environ.get('AS_PORT', '8765')))
MAPS_KEY = os.environ.get('GOOGLE_MAPS_BROWSER_KEY', '').strip()
MAX_BODY = 12_000
POST_LIFETIME_SECONDS = 72 * 60 * 60
CHAT_LIFETIME_SECONDS = 24 * 60 * 60
REPORT_LIFETIME_SECONDS = 30 * 24 * 60 * 60
KINDS = {'necesito', 'ofrezco'}
CATEGORIES = {'rescate', 'agua', 'alimentos', 'medicamentos', 'refugio', 'transporte', 'donaciones', 'otros'}
STATUS = {'abierto', 'resuelto'}
lock = threading.Lock()
rates = defaultdict(deque)
quake_cache = {'until': 0, 'data': None}
prune_due = 0
USGS = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson'


@contextmanager
def connection():
    db = sqlite3.connect(DB, timeout=8)
    try:
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA busy_timeout=8000')
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    with connection() as db:
        db.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS users(
          id TEXT PRIMARY KEY, alias TEXT UNIQUE NOT NULL, salt TEXT NOT NULL,
          hash TEXT NOT NULL, created INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions(
          hash TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), expires INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS posts(
          id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), kind TEXT NOT NULL,
          category TEXT NOT NULL, description TEXT NOT NULL, status TEXT NOT NULL,
          latitude REAL NOT NULL, longitude REAL NOT NULL,
          public_lat REAL NOT NULL, public_lon REAL NOT NULL, created INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS chat(
          id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id),
          zone TEXT NOT NULL, body TEXT NOT NULL, created INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS reports(
          id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id),
          target_type TEXT NOT NULL, target_id TEXT NOT NULL, reason TEXT NOT NULL,
          created INTEGER NOT NULL);
        CREATE INDEX IF NOT EXISTS post_created_idx ON posts(created);
        CREATE INDEX IF NOT EXISTS chat_zone_idx ON chat(zone, created);
        ''')
        db.execute('UPDATE posts SET latitude=public_lat, longitude=public_lon '
                   'WHERE latitude!=public_lat OR longitude!=public_lon')
        cleanup(db)


def cleanup(db):
    now=int(time.time())
    db.execute('DELETE FROM posts WHERE created < ?', (now-POST_LIFETIME_SECONDS,))
    db.execute('DELETE FROM chat WHERE created < ?', (now-CHAT_LIFETIME_SECONDS,))
    db.execute('DELETE FROM reports WHERE created < ?', (now-REPORT_LIFETIME_SECONDS,))
    db.execute('DELETE FROM sessions WHERE expires <= ?', (now,))


def prune_expired():
    global prune_due
    now=time.monotonic()
    with lock:
        if now < prune_due:
            return
        with connection() as db:
            cleanup(db)
        prune_due=now+300


def pass_hash(password, salt):
    return hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=2**14, r=8, p=1).hex()


def public_location(value):
    """Round to ~1 km grid. Exact coordinates are not persisted."""
    return round(float(value), 2)


def zone(lat, lon):
    return f'{round(float(lat), 1):.1f},{round(float(lon), 1):.1f}'


def check_coords(lat, lon):
    if type(lat) not in (int, float) or type(lon) not in (int, float):
        raise ValueError('Coordenadas numéricas requeridas')
    if not math.isfinite(lat) or not math.isfinite(lon) or not -90 <= lat <= 90 or not -180 <= lon <= 180:
        raise ValueError('Coordenadas fuera de rango')
    return float(lat), float(lon)


def current_user(header):
    parts = (header or '').split(' ', 1)
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    hashed = hashlib.sha256(parts[1].encode()).hexdigest()
    with connection() as db:
        row = db.execute('SELECT u.id,u.alias FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.hash=? AND s.expires>?', (hashed, int(time.time()))).fetchone()
        return dict(row) if row else None


def read_quakes():
    with lock:
        if quake_cache['until'] > time.monotonic() and quake_cache['data'] is not None:
            return quake_cache['data']
    req = urllib.request.Request(USGS, headers={'User-Agent': 'AlertaSolidaria/0.2 (USGS public feed)'})
    with urllib.request.urlopen(req, timeout=7) as response:
        body = response.read(1_000_001)
        if len(body) > 1_000_000:
            raise ValueError('Fuente demasiado grande')
    data = json.loads(body)
    events = []
    for item in data.get('features', [])[:500]:
        p = item.get('properties') or {}
        coords = (item.get('geometry') or {}).get('coordinates') or []
        if len(coords) < 2:
            continue
        events.append({'id': str(item.get('id', '')), 'mag': p.get('mag'), 'place': p.get('place'),
                       'time': p.get('time'), 'url': p.get('url'), 'lat': coords[1], 'lon': coords[0],
                       'source': 'USGS', 'status': p.get('status')})
    result = {'source': 'USGS', 'source_url': USGS, 'retrieved_at': int(time.time()),
              'disclaimer': 'Registro posterior al sismo; NO es alerta temprana ni predicción.',
              'events': events}
    with lock:
        quake_cache.update(until=time.monotonic() + 100, data=result)
    return result


class Handler(BaseHTTPRequestHandler):
    server_version = 'AlertaSolidaria/0.2'

    def log_message(self, fmt, *args):
        # Avoid logging paths/locations/personal data by default.
        pass

    def send_json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Robots-Tag', 'noindex, nofollow')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "frame-ancestors 'none'")
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path):
        mime = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png'}.get(path.suffix, 'application/octet-stream')
        body = path.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mime + ('; charset=utf-8' if mime.startswith('text') else ''))
        self.send_header('Cache-Control', 'no-store' if path.name == 'index.html' else 'public, max-age=120')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Robots-Tag', 'noindex, nofollow')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def body_json(self):
        length = int(self.headers.get('Content-Length', '0'))
        if length <= 0 or length > MAX_BODY:
            raise ValueError('Cuerpo ausente o demasiado grande')
        data = json.loads(self.rfile.read(length))
        if not isinstance(data, dict):
            raise ValueError('Formato inválido')
        return data

    def auth(self):
        user = current_user(self.headers.get('Authorization'))
        if not user:
            self.send_json(401, {'error': 'Registrate o iniciá sesión para publicar'})
        return user

    def limited(self, max_per_minute=20):
        ip = self.client_address[0]
        # This is deliberately per-process; replace with redis/perimeter gateway for internet deployment.
        now = time.monotonic()
        with lock:
            d = rates[ip]
            while d and d[0] < now - 60:
                d.popleft()
            if len(d) >= max_per_minute:
                return True
            d.append(now)
            return False

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        if path == '/api/health':
            return self.send_json(200, {'ok': True, 'mode': 'pilot', 'public_dispatch': False})
        if path == '/api/config':
            return self.send_json(200, {'maps_key': MAPS_KEY, 'pilot': True, 'emergency_number': '911', 'maps_provider': 'Google Maps' if MAPS_KEY else 'OpenStreetMap fallback'})
        if path == '/api/me':
            u = current_user(self.headers.get('Authorization'))
            return self.send_json(200, {'user': u})
        if path == '/api/posts':
            with connection() as db:
                rows = db.execute('''SELECT p.id,p.kind,p.category,p.description,p.status,p.public_lat AS lat,
                    p.public_lon AS lon,p.created,u.alias FROM posts p JOIN users u ON p.user_id=u.id
                    WHERE p.status='abierto' AND p.created>=? ORDER BY p.created DESC LIMIT 150''',
                    (int(time.time())-POST_LIFETIME_SECONDS,)).fetchall()
            return self.send_json(200, {'posts': [dict(r) for r in rows], 'location_precision': 'aproximada ~1 km',
                'post_lifetime_hours': POST_LIFETIME_SECONDS // 3600, 'retrieved_at': int(time.time())})
        if path == '/api/chat':
            v = parse_qs(url.query).get('zone', [''])[0]
            if not re.fullmatch(r'-?\d{1,2}\.\d,-?\d{1,3}\.\d', v):
                return self.send_json(400, {'error': 'Zona inválida'})
            with connection() as db:
                rows = db.execute('''SELECT c.id,c.body,c.created,u.alias FROM chat c JOIN users u ON c.user_id=u.id
                    WHERE c.zone=? AND c.created>=? ORDER BY c.created DESC LIMIT 80''',
                    (v, int(time.time())-CHAT_LIFETIME_SECONDS)).fetchall()
            return self.send_json(200, {'zone': v, 'messages': [dict(r) for r in reversed(rows)],
                'message_lifetime_hours': CHAT_LIFETIME_SECONDS // 3600})
        if path == '/api/earthquakes':
            try:
                return self.send_json(200, read_quakes())
            except Exception:
                return self.send_json(503, {'error': 'Fuente USGS no disponible; comprobar el sitio oficial directamente', 'source_url': USGS})
        if path == '/':
            path = '/index.html'
        allowed = {'/index.html', '/app.css', '/app.js', '/manifest.json', '/icon.svg', '/sw.js'}
        if path in allowed:
            return self.send_file(ROOT / 'app' / path[1:])
        return self.send_json(404, {'error': 'No encontrado'})

    def do_POST(self):
        if self.limited():
            return self.send_json(429, {'error': 'Demasiadas solicitudes. Reintentá en un minuto.'})
        path = urlparse(self.path).path
        try:
            b = self.body_json()
            if path in ('/api/auth/register', '/api/auth/login'):
                alias, pwd = str(b.get('alias', '')).strip(), str(b.get('password', ''))
                if not re.fullmatch(r'[a-zA-ZÀ-ÿ0-9_\-. ]{3,35}', alias) or len(pwd) < 10 or len(pwd) > 128:
                    raise ValueError('Alias de 3 a 35 caracteres y contraseña de 10 o más')
                with connection() as db:
                    if path.endswith('register'):
                        salt = secrets.token_hex(16)
                        try:
                            user_id = uuid.uuid4().hex
                            db.execute('INSERT INTO users VALUES(?,?,?,?,?)', (user_id,alias,salt,pass_hash(pwd,salt),int(time.time())))
                            db.commit()
                        except sqlite3.IntegrityError:
                            return self.send_json(409, {'error': 'El alias ya está registrado'})
                    row = db.execute('SELECT * FROM users WHERE alias=?', (alias,)).fetchone()
                    if not row or not hmac.compare_digest(pass_hash(pwd,row['salt']),row['hash']):
                        return self.send_json(401, {'error': 'Credenciales incorrectas'})
                    token = secrets.token_urlsafe(32)
                    expires = int(time.time()) + 7 * 86400
                    db.execute('INSERT INTO sessions VALUES(?,?,?)', (hashlib.sha256(token.encode()).hexdigest(),row['id'],expires))
                    db.commit()
                return self.send_json(200, {'token': token, 'alias': alias, 'expires': expires})
            user = self.auth()
            if not user:
                return
            if path == '/api/posts':
                kind, cat = b.get('kind'), b.get('category')
                desc = str(b.get('description', '')).strip()
                if kind not in KINDS or cat not in CATEGORIES or not 12 <= len(desc) <= 450:
                    raise ValueError('Completá tipo, categoría y detalle (12 a 450 caracteres)')
                lat, lon = check_coords(b.get('lat'), b.get('lon'))
                ident = uuid.uuid4().hex
                with connection() as db:
                    db.execute('INSERT INTO posts VALUES(?,?,?,?,?,?,?,?,?,?,?)', (ident,user['id'],kind,cat,desc,'abierto',lat,lon,public_location(lat),public_location(lon),int(time.time())))
                    db.commit()
                return self.send_json(201, {'id': ident, 'posted': True, 'public_location': 'aproximada', 'warning':'Esto NO contacta automáticamente a emergencias'})
            if path == '/api/chat':
                lat, lon = check_coords(b.get('lat'),b.get('lon'))
                body = str(b.get('message', '')).strip()
                if not 2 <= len(body) <= 280:
                    raise ValueError('Mensaje de 2 a 280 caracteres')
                z = zone(lat,lon)
                with connection() as db:
                    db.execute('INSERT INTO chat VALUES(?,?,?,?,?)', (uuid.uuid4().hex,user['id'],z,body,int(time.time())))
                    db.commit()
                return self.send_json(201, {'posted': True, 'zone': z})
            if path == '/api/posts/resolve':
                ident = str(b.get('id', ''))
                with connection() as db:
                    count = db.execute("UPDATE posts SET status='resuelto' WHERE id=? AND user_id=?", (ident, user['id'])).rowcount
                    db.commit()
                return self.send_json(200 if count else 404, {'updated': bool(count)})
            if path == '/api/reports':
                if b.get('target_type') not in ('post','chat') or not re.fullmatch(r'[a-f0-9]{32}',str(b.get('target_id',''))):
                    raise ValueError('Publicación inválida')
                reason = str(b.get('reason','')).strip()
                if not 10 <= len(reason) <= 350:
                    raise ValueError('Explicá el motivo de 10 a 350 caracteres')
                with connection() as db:
                    db.execute('INSERT INTO reports VALUES(?,?,?,?,?,?)', (uuid.uuid4().hex,user['id'],b['target_type'],b['target_id'],reason,int(time.time())))
                    db.commit()
                return self.send_json(201, {'reported': True, 'note': 'Requiere revisión humana; este piloto no tiene equipo de moderación activo'})
            return self.send_json(404, {'error': 'No encontrado'})
        except (ValueError, KeyError, json.JSONDecodeError, OverflowError) as err:
            return self.send_json(400, {'error': str(err)})
        except sqlite3.Error:
            return self.send_json(500, {'error': 'Error de persistencia'})


def serve():
    # Avoid accidental public hosting of experimental safety-related software.
    if HOST not in ('127.0.0.1', 'localhost', '::1') and os.environ.get('AS_REMOTE_PILOT_ACK') != 'I_UNDERSTAND_NOT_FOR_EMERGENCIES':
        raise RuntimeError('Piloto sólo loopback. Para pruebas de red aislada: AS_REMOTE_PILOT_ACK=I_UNDERSTAND_NOT_FOR_EMERGENCIES')
    init_db()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'Alerta Solidaria PILOTO: http://{HOST}:{PORT} - NO usar como sistema oficial de emergencias', flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()

if __name__ == '__main__':
    serve()
