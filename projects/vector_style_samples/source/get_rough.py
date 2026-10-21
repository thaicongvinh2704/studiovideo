"""Fetch only the published Rough.js bundle and license from the npm registry."""
from pathlib import Path
import urllib.request,tarfile,io,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.deps'/'roughjs'
OUT.mkdir(parents=True,exist_ok=True)
url='https://registry.npmjs.org/roughjs/-/roughjs-4.6.6.tgz'
data=urllib.request.urlopen(url,timeout=30).read()
with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as package:
 for name in ['package/bundled/rough.cjs.js','package/LICENSE','package/package.json']:
  item=package.extractfile(name)
  if item is None:raise RuntimeError(name)
  (OUT/Path(name).name).write_bytes(item.read())
(OUT/'provenance.json').write_text(json.dumps(dict(url=url,sha256=hashlib.sha256(data).hexdigest(),version='4.6.6'),indent=2),encoding='utf-8')
print('Rough.js bundle ready')
