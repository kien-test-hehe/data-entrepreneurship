"""Capture the actual aggregate-only Streamlit market overview for the pitch."""
from pathlib import Path
import sys, subprocess, time, urllib.request
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
dest=root/'outputs/mvp';dest.mkdir(parents=True,exist_ok=True)
with (dest/'server.log').open('w') as log:
    p=subprocess.Popen([sys.executable,'-m','streamlit','run','app/app.py','--server.headless','true','--server.port','8501','--browser.gatherUsageStats','false'],cwd=root,stdout=log,stderr=subprocess.STDOUT)
    try:
        for _ in range(60):
            try:
                with urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health',timeout=2) as r:
                    if r.status==200:break
            except Exception:time.sleep(1)
        else:raise RuntimeError('Streamlit did not start')
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1440,'height':980},device_scale_factor=1)
            page.goto('http://127.0.0.1:8501',wait_until='domcontentloaded',timeout=60000)
            page.get_by_text('Historical median asking price',exact=True).wait_for(timeout=60000)
            page.get_by_text('Listing counts are not market share. Prices are historical.',exact=True).wait_for(timeout=60000)
            page.wait_for_function("document.querySelectorAll('img').length >= 2 && Array.from(document.querySelectorAll('img')).every(x=>x.complete && x.naturalWidth > 0)",timeout=60000)
            page.screenshot(path=str(dest/'overview.png'),animations='disabled')
            browser.close()
    finally:
        p.terminate()
        try:p.wait(timeout=10)
        except subprocess.TimeoutExpired:p.kill()
(dest/'server.log').unlink(missing_ok=True)
print('Captured actual Streamlit overview')
