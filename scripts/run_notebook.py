from pathlib import Path
import nbformat
from nbclient import NotebookClient
root=Path(__file__).resolve().parents[1]
nb=nbformat.read(root/'notebooks/ShopScope_Data_Analysis.ipynb',as_version=4)
out=root/'outputs'; out.mkdir(exist_ok=True)
client=NotebookClient(nb,timeout=600,kernel_name='python3',resources={'metadata':{'path':str(root)}})
client.execute()
nbformat.write(nb,out/'ShopScope_Data_Analysis.executed.ipynb')
print((out/'evidence.json').read_text())
