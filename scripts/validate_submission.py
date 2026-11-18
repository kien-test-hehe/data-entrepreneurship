from pathlib import Path
import json, hashlib, zipfile
from pptx import Presentation
from docx import Document
import nbformat
from streamlit.testing.v1 import AppTest
root=Path(__file__).resolve().parents[1]
out=root/'outputs'; reports=root/'reports'
e=json.loads((out/'evidence.json').read_text())
assert len(e['files'])==6 and e['raw_observations']==24896 and e['unique_listings']==19686
assert e['vn_listings']==4956 and e['vn_shops']==1017
assert len(e['figures'])==20 and all((out/'figures'/x).stat().st_size>1000 for x in e['figures'])
nb=nbformat.read(out/'ShopScope_Data_Analysis.executed.ipynb',as_version=4)
assert all(c.execution_count is not None and not any(x.output_type=='error' for x in c.outputs) for c in nb.cells if c.cell_type=='code')
p=reports/'ShopScope_Startup_Pitch.pptx'; d=reports/'ShopScope_Business_Report.docx'
assert len(Presentation(p).slides)==34 and len(Document(d).inline_shapes)==20
eid=hashlib.sha256((out/'evidence.json').read_bytes()).hexdigest()[:12]
expected={hashlib.sha256((out/'figures'/n).read_bytes()).hexdigest() for n in e['figures']}
for file,folder in [(p,'ppt/media/'),(d,'word/media/')]:
    with zipfile.ZipFile(file) as z:
        assert z.testzip() is None
        imgs={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith(folder) and n.endswith('.png')}
        assert imgs==expected,(file.name,len(imgs),len(expected),len(expected-imgs))
        assert any(eid.encode() in z.read(n) for n in z.namelist() if n.endswith('.xml'))
# Exercise each actual app screen with the locally generated private analysis table.
app=AppTest.from_file(str(root/'app/app.py'),default_timeout=30).run()
assert not app.exception, app.exception
for view in ['Product explorer','Competitor analysis','Price intelligence','Opportunity finder','Pricing advisor']:
    app.sidebar.radio[0].set_value(view).run()
    assert not app.exception,(view,app.exception)
print('PASS: source counts, executed notebook, 20 identical chart assets in both Office files, evidence ID and six MVP screens.')
