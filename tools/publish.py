"""Publish a Kandy For Scale Captions update into this repository.

Usage (from the repository folder):
  "<KFS python>" -I tools/publish.py <version> <engine_package folder> <signing key file> "What changed"
Then: git add -A && git commit -m "Version X" && git push

Editors' panels check latest.json when they open and install the update automatically.
The signing key file must never be committed to this repository."""
import base64, hashlib, json, sys, zipfile
from pathlib import Path
from cryptography.hazmat.primitives import serialization

REPO = 'rokas-web/kfs-captions-updates'
here = Path(__file__).resolve().parents[1]
version, pkg, keyfile = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
notes = sys.argv[4] if len(sys.argv) > 4 else ''
assert all(x.isdigit() for x in version.split('.')) and version.count('.') == 2, 'Version must look like 1.2.0'
out = here / 'updates'; out.mkdir(exist_ok=True)
z = out / f'kfs-update-{version}.zip'
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for d in ('engine', 'panel'):
        for p in sorted((pkg / d).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and p.name not in ('channel.json', '.DS_Store') and not p.name.endswith('.original'):
                zf.write(p, p.relative_to(pkg).as_posix())
blob = z.read_bytes()
payload = json.dumps(dict(schema=1, version=version, runtime=2, notes=notes, size=len(blob),
                          sha256=hashlib.sha256(blob).hexdigest(),
                          url=f'https://raw.githubusercontent.com/{REPO}/main/updates/{z.name}'))
text = keyfile.read_text()
key = serialization.load_pem_private_key(text[text.index('-----BEGIN'):].encode(), None)
(here / 'latest.json').write_text(json.dumps(dict(payload=payload, signature=base64.b64encode(key.sign(payload.encode())).decode()), indent=2) + '\n')
print('Prepared', z.name, len(blob), 'bytes and latest.json')
