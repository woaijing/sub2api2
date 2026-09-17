"""Public page QA with isolated local fixtures; never submits to a real backend."""
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

BASE = os.environ.get('FOXCODE_PREVIEW_URL', 'http://127.0.0.1:3001').rstrip('/')
OUT = Path(__file__).resolve().parents[1] / 'output' / 'public-pages-qa'
OUT.mkdir(parents=True, exist_ok=True)
SETTINGS = {
    'site_name': 'Sub2API', 'site_logo': '', 'site_subtitle': 'AI API Gateway',
    'registration_enabled': True, 'password_reset_enabled': True,
    'email_verify_enabled': False, 'model_plaza_enabled': True,
    'model_plaza_require_auth': False, 'backend_mode_enabled': False,
    'custom_menu_items': [], 'compact_home_enabled': False, 'home_content': '',
    'doc_url': 'https://docs.example.test/', 'registration_email_suffix_whitelist': [],
}
report = {}


def context_for(browser, width, locale='zh', overrides=None):
    settings = {**SETTINGS, **(overrides or {})}
    context = browser.new_context(viewport={'width': width, 'height': 1000 if width >= 1024 else 900}, locale='zh-CN' if locale == 'zh' else 'en-US')
    context.add_init_script("if (!localStorage.getItem('theme')) localStorage.setItem('theme', 'light'); localStorage.setItem('locale', " + json.dumps(locale) + ");")
    requests = []

    def handle(route):
        request = route.request
        path = urlparse(request.url).path
        if not request.url.startswith(BASE + '/'):
            route.abort()
            return
        if request.resource_type == 'document':
            response = route.fetch()
            html = response.text()
            injection = '<script>window.__APP_CONFIG__=' + json.dumps(settings) + ';</script>'
            html = re.sub(r'<script>window\.__APP_CONFIG__=.*?</script>', '', html, flags=re.S)
            route.fulfill(response=response, body=html.replace('</head>', injection + '</head>'))
        elif path == '/setup/status':
            route.fulfill(json={'code': 0, 'data': {'needs_setup': False, 'step': 'complete'}})
        elif path == '/api/v1/settings/public':
            route.fulfill(json={'code': 0, 'data': settings})
        elif path in ('/api/v1/auth/login', '/api/v1/auth/register'):
            requests.append({'path': path, 'body': request.post_data_json})
            route.fulfill(status=400, json={'code': 400, 'message': 'Local preview: sample rejection'})
        elif path.startswith('/api/'):
            route.fulfill(json={'code': 0, 'data': []})
        else:
            route.continue_()

    context.route('**/*', handle)
    return context, requests


def capture(page, name):
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.wait_for_timeout(150)
    metrics = page.evaluate("""() => ({
      width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
      brokenImages: [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src),
      headings: [...document.querySelectorAll('h1')].map(e => e.innerText),
      background: getComputedStyle(document.body).backgroundColor,
      missingTranslations: /brand\\.[a-zA-Z]/.test(document.body.innerText),
      hiddenText: [...document.querySelectorAll('.hero-copy h1, .auth-form h1, .studio-modes button, .hero-actions a')]
        .filter(e => e.scrollWidth > e.clientWidth + 1).map(e => e.innerText)
    })""")
    assert metrics['width'] >= metrics['scrollWidth'], (name, metrics)
    assert not metrics['brokenImages'], (name, metrics)
    assert not metrics['missingTranslations'], (name, metrics)
    assert not metrics['hiddenText'], (name, metrics)
    assert len(metrics['headings']) == 1, (name, metrics)
    page.screenshot(path=str(OUT / (name + '.png')), full_page=True, animations='disabled')
    report[name] = metrics


with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    for locale, widths in [('zh', [1440, 1024, 768, 390, 320]), ('en', [1440, 390])]:
        for width in widths:
            context, requests = context_for(browser, width, locale)
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            for route in ['home', 'login', 'register']:
                page.goto(BASE + '/' + route, wait_until='networkidle')
                page.locator('h1').wait_for()
                capture(page, f'{route}-{width}-{locale}-light')
                page.locator('.theme-button').click()
                assert page.locator('html.dark').count() == 1
                capture(page, f'{route}-{width}-{locale}-dark')
                page.locator('.theme-button').click()
                if route == 'home':
                    assert page.locator('.hero-actions a').first.get_attribute('href') == '/register'
                    for index, endpoint in [(1, '/v1/messages'), (2, '/v1/images/generations'), (0, '/v1/responses')]:
                        page.locator('.studio-modes button').nth(index).click()
                        assert endpoint in page.locator('.studio-bottom code').inner_text()
                    if width < 1024:
                        page.locator('.mobile-navigation summary').click()
                        page.locator('.mobile-navigation-links a[href="#start"]').click()
                        assert not page.locator('.mobile-navigation').get_attribute('open')
                else:
                    page.locator('#password').fill('local-fixture-only')
                    toggle = page.locator('button[aria-pressed]')
                    toggle.click()
                    assert page.locator('#password').get_attribute('type') == 'text'
                    toggle.click()
                    assert page.locator('#password').get_attribute('type') == 'password'
            assert not errors, errors
            if width == 1440 and locale == 'zh':
                for route in ['login', 'register']:
                    page.goto(BASE + '/' + route, wait_until='networkidle')
                    page.locator('#email').fill('visual@example.test')
                    page.locator('#password').fill('local-fixture-only')
                    page.locator('button[type=submit]').click()
                    page.get_by_text('Local preview: sample rejection').first.wait_for()
                assert [r['path'] for r in requests] == ['/api/v1/auth/login', '/api/v1/auth/register']
                assert all(r['body']['email'] == 'visual@example.test' for r in requests)
            context.close()

    for label, settings in [
        ('closed', {'registration_enabled': False}),
        ('private-models', {'model_plaza_require_auth': True}),
        ('oauth-invite', {'github_oauth_enabled': True, 'google_oauth_enabled': True, 'invitation_code_enabled': True, 'promo_code_enabled': True}),
        ('agreement', {'login_agreement_enabled': True, 'login_agreement_mode': 'checkbox', 'login_agreement_revision': 'qa', 'login_agreement_documents': [{'key': 'terms', 'title': 'Example terms', 'content': 'Local fixture agreement.'}]}),
    ]:
        context, _ = context_for(browser, 390, overrides=settings)
        page = context.new_page()
        if label == 'closed':
            page.goto(BASE + '/home', wait_until='networkidle')
            assert page.locator('.hero-actions a').first.get_attribute('href') == '/login'
            page.goto(BASE + '/register', wait_until='networkidle')
            assert page.locator('form').count() == 0
            capture(page, 'register-closed')
        elif label == 'private-models':
            page.goto(BASE + '/home', wait_until='networkidle')
            assert page.locator('a[href="/model-plaza"]').count() == 0
        else:
            page.goto(BASE + '/register', wait_until='networkidle')
            if label == 'oauth-invite':
                assert page.locator('#invitation_code').count() == 1
                assert page.locator('#promo_code').count() == 1
                assert page.get_by_role('button', name='GitHub', exact=False).count() == 1
                assert page.get_by_role('button', name='Google', exact=False).count() == 1
            capture(page, 'register-' + label)
        context.close()
    browser.close()

(OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'screenshots': len(report), 'report': str(OUT / 'report.json'), 'status': 'passed'}))
