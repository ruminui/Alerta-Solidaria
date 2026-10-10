"""E2E browser smoke for local pilot. External tile loading may be unavailable in CI."""
import os, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
proc=subprocess.Popen([sys.executable,str(root/'backend/server.py')],cwd=root,env={**os.environ,'AS_PORT':'18866','AS_DB':str(root/'tests/.smoke_temp.sqlite')},stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=b.new_page(viewport={'width':1365,'height':900},device_scale_factor=1)
        errs=[]
        page.on('pageerror',lambda e: errs.append(str(e)))
        for _ in range(30):
            try: page.goto('http://127.0.0.1:18866',wait_until='domcontentloaded',timeout=1500);break
            except Exception: time.sleep(.1)
        page.wait_for_timeout(1800)
        assert not page.url.startswith('chrome-error:'), 'Browser blocked localhost; run this E2E smoke on an unrestricted developer device'
        assert 'La ayuda empieza' in page.locator('h1').inner_text()
        assert page.locator('#newSOS').is_visible()
        page.locator('#theme').click()
        assert 'theme-ios' in page.locator('body').get_attribute('class')
        page.locator('#accountBtn').click()
        assert page.locator('#authDialog').is_visible()
        page.locator('input[name="alias"]').fill('test_browser')
        page.locator('input[name="password"]').fill('ClaveCompuesta2026')
        page.locator('#register').click()
        page.wait_for_timeout(900)
        assert not page.locator('#authDialog').is_visible(), page.locator('#authError').inner_text()
        page.locator('#offer').click()
        assert page.locator('#postDialog').is_visible()
        page.locator('#postDialog .close').click()
        page.screenshot(path=str(root/'tests/browser_preview.png'),full_page=True)
        assert not errs,errs
        print('BROWSER_SMOKE_PASS title, theme, registration, offer modal. Screenshot saved.')
        b.close()
finally:
    proc.terminate();proc.wait(timeout=6)
    for p in root.glob('tests/.smoke_temp.sqlite*'):p.unlink(missing_ok=True)
