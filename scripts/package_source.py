#!/usr/bin/env python3
"""Reproducible code-only ZIP. Excludes runtime databases and local credentials."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'ALERTA_SOLIDARIA_2026/'
ROOT_FILES = {'README.md','LICENSE','SECURITY.md','CONTRIBUTING.md','.gitignore'}
DIRECTORIES = {'app','backend','native','deploy','tests','docs','.github','scripts'}
EXCLUDED_SUFFIXES = {'.db','.sqlite','.sqlite3','.env','.key','.pem','.p12','.p8','.pfx'}
EXCLUDED_NAMES = {'MANIFEST.json','SHA256SUMS.txt','.DS_Store','__pycache__','.pytest_cache','.git','.venv','node_modules'}

def eligible(p: Path) -> bool:
    parts = p.relative_to(ROOT).parts
    if any(s in EXCLUDED_NAMES or s.startswith('.env') for s in parts):
        return False
    if p.suffix.lower() in EXCLUDED_SUFFIXES or p.name.endswith(('-wal','-shm')):
        return False
    return (len(parts)==1 and p.name in ROOT_FILES) or parts[0] in DIRECTORIES

def generate(target: Path) -> None:
    files={str(p.relative_to(ROOT)).replace('\\','/'):p.read_bytes() for p in ROOT.rglob('*') if p.is_file() and eligible(p)}
    assert 'backend/server.py' in files and 'LICENSE' in files, 'missing essential files'
    digests={name:hashlib.sha256(data).hexdigest() for name,data in sorted(files.items())}
    manifest={'project':'Alerta Solidaria','status':'RESEARCH_ONLY_NO_GO','file_count_excluding_manifest':len(files),
              'sha256_by_path':digests,'distribution':'source code only; local DB and secrets excluded'}
    files['MANIFEST.json']=(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
    files['SHA256SUMS.txt']=''.join(f'{hashcode}  {name}\n' for name,hashcode in digests.items()).encode()
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(PREFIX+name,(2026,10,10,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,data)

def verify(source: Path) -> None:
    with zipfile.ZipFile(source) as z:
        assert z.testzip() is None
        m=json.loads(z.read(PREFIX+'MANIFEST.json'))
        assert len(m['sha256_by_path'])==m['file_count_excluding_manifest']
        names=z.namelist()
        assert not any(n.endswith(('.db','.sqlite','.sqlite3','.env','.pem','.key')) for n in names)
        for name,digest in m['sha256_by_path'].items():
            assert hashlib.sha256(z.read(PREFIX+name)).hexdigest()==digest,name

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--check',action='store_true')
    ap.add_argument('--output',default='ALERTA_SOLIDARIA_CODE_ONLY.zip')
    args=ap.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            test=Path(tmp)/'code-only.zip';generate(test);verify(test)
        print('PASS: code-only ZIP, manifest, hashes, sensitive-file exclusions')
    else:
        out=Path(args.output);generate(out);verify(out)
        print(f'PASS: {out}, sha256={hashlib.sha256(out.read_bytes()).hexdigest()}')
if __name__=='__main__':main()
