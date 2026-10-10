"""Deterministic API tests; no Internet, no earthquakes fabricated."""
import importlib.util, json, math, tempfile, threading, unittest, time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer

FILE = Path(__file__).resolve().parents[1] / 'backend' / 'server.py'
spec = importlib.util.spec_from_file_location('alerta_backend', FILE)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class APITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        server.DB = Path(cls.tmp.name) / 'test.sqlite'
        server.init_db()
        cls.http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:' + str(cls.http.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.tmp.cleanup()

    def req(self, path, payload=None, token=None):
        h = {'Content-Type': 'application/json'}
        if token:
            h['Authorization'] = 'Bearer ' + token
        req = Request(self.base + path, data=json.dumps(payload).encode() if payload is not None else None,
                      headers=h, method='POST' if payload is not None else 'GET')
        try:
            with urlopen(req, timeout=5) as r:
                return r.status, json.loads(r.read())
        except HTTPError as e:
            return e.code, json.loads(e.read())

    def test_00_health(self):
        code, data = self.req('/api/health')
        self.assertEqual(code, 200)
        self.assertFalse(data['public_dispatch'])

    def test_01_auth_and_public_location(self):
        code, data = self.req('/api/auth/register', {'alias': 'vecino_test', 'password':'ClaveMuyLarga123'})
        self.assertEqual(code, 200)
        token = data['token']
        code, data = self.req('/api/posts', {'kind':'necesito','category':'agua','description':'Necesitamos agua potable para el refugio', 'lat':8.91234,'lon':-79.51234})
        self.assertEqual(code,401)
        code, data = self.req('/api/posts', {'kind':'necesito','category':'agua','description':'Necesitamos agua potable para el refugio', 'lat':8.91234,'lon':-79.51234}, token)
        self.assertEqual(code,201)
        ident = data['id']
        code, data = self.req('/api/posts')
        self.assertEqual(data['posts'][0]['lat'],8.91)
        self.assertEqual(data['posts'][0]['lon'],-79.51)
        self.assertNotIn('latitude', data['posts'][0])
        self.assertNotIn('longitude', data['posts'][0])
        self.assertNotIn('user_id', data['posts'][0])
        code, data = self.req('/api/posts/resolve', {'id':ident}, token)
        self.assertEqual(code,200)
        self.assertTrue(data['updated'])
        code, data = self.req('/api/posts')
        self.assertFalse(data['posts'])

    def test_02_chat_and_bad_coords(self):
        code, data = self.req('/api/auth/login', {'alias':'vecino_test','password':'ClaveMuyLarga123'})
        self.assertEqual(code,200)
        token=data['token']
        code, data = self.req('/api/posts', {'kind':'ofrezco','category':'donaciones','description':'Tengo mantas disponibles para el centro','lat': 100,'lon':-79},token)
        self.assertEqual(code,400)
        code, data = self.req('/api/chat', {'message':'Tengo un refugio disponible','lat':8.91,'lon':-79.51},token)
        self.assertEqual(code,201)
        self.assertEqual(data['zone'],'8.9,-79.5')
        code, data = self.req('/api/chat?zone=8.9%2C-79.5')
        self.assertEqual(code,200)
        self.assertEqual(len(data['messages']),1)
        self.assertEqual(data['messages'][0]['body'],'Tengo un refugio disponible')
        code, data = self.req('/api/chat?zone=<script>')
        self.assertEqual(code,400)

    def test_03_failed_password(self):
        code, data = self.req('/api/auth/login', {'alias':'vecino_test','password':'Incorrecta123'})
        self.assertEqual(code,401)

    def test_04_static_content(self):
        with urlopen(self.base+'/', timeout=5) as r:
            self.assertEqual(r.status,200)
            self.assertIn(b'ALERTA',r.read())

    def test_06_non_finite_coordinates_rejected(self):
        for pair in [(math.nan, -79.5), (8.9, math.inf), (math.inf, -79.5)]:
            with self.subTest(pair=pair):
                with self.assertRaisesRegex(ValueError, 'fuera de rango'):
                    server.check_coords(*pair)
        with self.assertRaises(ValueError):
            server.check_coords(True, -79.5)

    def test_07_old_posts_hidden_from_public_map(self):
        with server.connection() as db:
            row=db.execute('SELECT id FROM posts LIMIT 1').fetchone()
            if not row:
                self.skipTest('Falta dato previo')
            db.execute('UPDATE posts SET status=?,created=? WHERE id=?',
                       ('abierto',int(time.time())-server.POST_LIFETIME_SECONDS-1,row['id']))
            db.commit()
        code, data=self.req('/api/posts')
        self.assertEqual(code,200)
        self.assertEqual(data['post_lifetime_hours'],72)
        self.assertTrue(all(p['id']!=row['id'] for p in data['posts']))

    def test_08_old_chat_hidden_from_public_zone(self):
        with server.connection() as db:
            row=db.execute('SELECT id FROM chat LIMIT 1').fetchone()
            self.assertIsNotNone(row)
            db.execute('UPDATE chat SET created=? WHERE id=?',
                       (int(time.time())-server.CHAT_LIFETIME_SECONDS-1,row['id']))
            db.commit()
        code,data=self.req('/api/chat?zone=8.9%2C-79.5')
        self.assertEqual(code,200)
        self.assertEqual(data['message_lifetime_hours'],24)
        self.assertEqual(data['messages'],[])

    def test_09_headers_and_offline_guidance(self):
        with urlopen(self.base+'/', timeout=5) as r:
            self.assertEqual(r.headers['X-Robots-Tag'],'noindex, nofollow')
            self.assertIn('Plan rápido si se corta Internet', r.read().decode('utf-8'))

    def test_05_zone(self):
        self.assertEqual(server.zone(8.94,-79.54), '8.9,-79.5')
        self.assertEqual(server.public_location(-79.51234), -79.51)

if __name__=='__main__': unittest.main(verbosity=2)
