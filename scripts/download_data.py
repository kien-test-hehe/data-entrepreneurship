"""Fetch the exact release from Kaggle; fall back to publisher's public Drive."""
from pathlib import Path
import urllib.request, zipfile, tempfile, subprocess, sys
root=Path(__file__).resolve().parents[1]/'data'/'raw'
root.mkdir(parents=True,exist_ok=True)
if len(list(root.rglob('*.xlsx')))==6:
    print('Six workbooks already present.'); sys.exit(0)
url='https://www.kaggle.com/api/v1/datasets/download/johnphamed/shopee-diaper-listings-six-markets-november-2025'
try:
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/'data.zip'
        with urllib.request.urlopen(url,timeout=120) as r,p.open('wb') as f:
            import shutil
            shutil.copyfileobj(r,f)
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.lower().endswith('.xlsx') and not n.startswith('__MACOSX'):
                    dest=root/Path(n).name
                    dest.write_bytes(z.read(n))
except Exception as e:
    print('Kaggle download unsuccessful:',type(e).__name__,str(e)[:300])
if len(list(root.rglob('*.xlsx')))!=6:
    subprocess.run([sys.executable,'-m','gdown','--folder','https://drive.google.com/drive/folders/1-ynfBFXTlHJ6S4Hq52QEjfs0xSjga-N-','-O',str(root)],check=True)
assert len(list(root.rglob('*.xlsx')))==6, 'Place six original workbooks in data/raw manually.'
