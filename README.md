# ShopScope — See the market. Sell smarter.

**Data Entrepreneurship | English-only startup submission.** Vietnam-first pricing intelligence using the November 2025 Shopee diaper listing collection from Easy Data. 

## Download the submission
The verified aggregate deliverables are published under [reports/](reports/) and [outputs/](outputs/) after a successful build. Alternatively, open [GitHub Actions](https://github.com/kien-test-hehe/data-entrepreneurship/actions/workflows/build.yml), choose the latest successful **Build ShopScope** run, then download **ShopScope-submission**. It contains the executed notebook, evidence JSON, charts, aggregate tables, PowerPoint deck and DOCX report. A successful build is required; a source-only commit is not an analytical result.

## Reproduce locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py
python scripts/run_notebook.py
python scripts/export_office.py
streamlit run app/app.py
```
On Windows activate with .venv\Scripts\activate. If automatic download fails, manually download the six original workbooks from [Kaggle](https://www.kaggle.com/datasets/johnphamed/shopee-diaper-listings-six-markets-november-2025) into data/raw. Do not redistribute raw files or private row-level outputs.

## Deliverables
- notebooks/ShopScope_Data_Analysis.ipynb — source notebook; executed copy in outputs.
- outputs/evidence.json — single source of truth; file hashes, schema, metrics and figure manifest.
- reports/ShopScope_Startup_Pitch.pptx — 22 main slides and 12 appendix slides.
- reports/ShopScope_Business_Report.docx — English consulting-style report.
- app/app.py — local six-screen Streamlit prototype.
- business/validation.md — Test Cards, pilot design and labeling instructions.

All 20 notebook charts (including explicitly labeled external and financial scenarios) are embedded in both documents byte-for-byte. Every EDA chart in the office files comes directly from the executed notebook, and the evidence ID ties both documents to evidence.json. Financial charts are explicit planning scenarios. No interviews, paid pilot, verified matching accuracy or live feed are claimed. The data is a historical filtered snapshot, not an exhaustive market census. Source counters are not transactions; do not infer revenue. Data licensing is unspecified; commercialization requires permission and refreshed feeds. 

Sources: [publisher documentation](https://github.com/JohnPham-easydata/Shopee-Dataset/blob/main/README.md), [VCCI market context](https://en.vcci.com.vn/economic-news/online-retail-sales-in-vietnam-jump-35-to-over-16-bln-in-2025-report-114817), [Metric pricing](https://metric.vn/pricing).
