"""Smoke test funcional em Chromium, incluindo filtros, navegação e viewport móvel."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'index.html').as_uri()

def run():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        errors=[]
        page=browser.new_page(viewport={'width':1440,'height':900}, device_scale_factor=1)
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto(URL,wait_until='load')
        page.locator('body').wait_for(state='visible')
        page.wait_for_timeout(350)
        assert page.locator('button[data-page="overview"]').count()==1
        assert page.locator('svg').count()>0,'Gráficos SVG não foram renderizados'
        page.locator('#periodo').select_option('6')
        page.locator('button[data-page="trends"]').click()
        assert 'active' in page.locator('button[data-page="trends"]').get_attribute('class')
        page.locator('button[data-page="diagnostics"]').click()
        page.locator('button[data-page="scenarios"]').click()
        page.locator('#scenarioSlider').evaluate("(e)=>{e.value='30';e.dispatchEvent(new Event('input',{bubbles:true}))}")
        page.locator('button[data-page="engineering"]').click()
        page.locator('#resetFilters').click()
        page.set_viewport_size({'width':390,'height':844})
        assert page.locator('.sidebar .menu').is_visible(), 'Navegação horizontal móvel não está visível'
        page.locator('button[data-page="overview"]').click()
        assert 'active' in page.locator('button[data-page="overview"]').get_attribute('class')

        assert not errors,'Erros de JavaScript: '+repr(errors)
        browser.close()
        print('OK: navegação, filtros e responsividade testados com Chromium')

if __name__=='__main__':
    run()
