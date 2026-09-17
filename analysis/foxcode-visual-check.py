"""Local theme QA. Fixtures only exist inside isolated Playwright contexts."""
import json
import os
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

BASE = os.environ.get("FOXCODE_PREVIEW_URL", "http://127.0.0.1:3001").rstrip("/")
OUT = Path(__file__).resolve().parents[1] / "output" / "foxcode-qa"
OUT.mkdir(parents=True, exist_ok=True)
USER = {"id": 90001, "username": "Theme Preview", "email": "preview@example.test",
        "role": "user", "status": "active", "balance": 128.50, "concurrency": 5}
SETTINGS = {"site_name": "Sub2API", "site_logo": "", "site_subtitle": "AI API Gateway",
            "registration_enabled": True, "password_reset_enabled": True,
            "subscription_enabled": False, "payment_enabled": False,
            "model_plaza_enabled": False, "backend_mode_enabled": False,
            "custom_menu_items": [], "home_content": "", "compact_home_enabled": False}
STATS = {"total_api_keys": 4, "active_api_keys": 3, "total_requests": 2841,
         "total_tokens": 4200000, "total_input_tokens": 2100000,
         "total_output_tokens": 500000, "total_cache_creation_tokens": 100000,
         "total_cache_read_tokens": 1500000, "today_requests": 186,
         "today_tokens": 268000, "today_input_tokens": 125000,
         "today_output_tokens": 23000, "today_cache_creation_tokens": 20000,
         "today_cache_read_tokens": 100000, "total_cost": 45.28,
         "total_actual_cost": 22.64, "today_cost": 4.86, "today_actual_cost": 2.43,
         "average_duration_ms": 620, "rpm": 12, "tpm": 18000, "by_platform": []}
TREND = [{"date": f"2026-09-{10+i:02}", "requests": 80 + i*15,
          "input_tokens": 12000 + i*2500, "output_tokens": 4500 + i*500,
          "cache_creation_tokens": 1500 + i*100, "cache_read_tokens": 6500 + i*1000,
          "cost": 2.4, "actual_cost": 1.2} for i in range(7)]
MODELS = [{"model": name, "requests": 50+i*10, "total_tokens": 240000-i*60000,
           "cost": 1.5, "actual_cost": 0.75, "account_cost": 0.5}
          for i, name in enumerate(["claude-sonnet-4-6", "gpt-5.3-codex", "gemini-2.5-pro"])]
GROUPS = [{"group_id": 1, "group_name": "Standard", "requests": 180,
           "total_tokens": 280000, "cost": 2.4, "actual_cost": 1.2}]
ENDPOINTS = [{"endpoint": "/v1/messages", "requests": 150, "total_tokens": 210000,
              "cost": 1.8, "actual_cost": 0.9}]


def fixtures(route):
    path = urlparse(route.request.url).path
    if path == "/setup/status":
        data = {"needs_setup": False, "step": "complete"}
    elif path.endswith("/settings/public"):
        data = SETTINGS
    elif path.endswith("/auth/me"):
        data = USER
    elif path.endswith("/platform-quotas"):
        data = {"platform_quotas": []}
    elif path.endswith("/usage/stats"):
        data = {**STATS, "endpoints": ENDPOINTS, "total_cache_tokens": 1600000}
    elif path.endswith("/dashboard/stats"):
        data = STATS
    elif path.endswith("/dashboard/trend"):
        data = {"trend": TREND}
    elif path.endswith("/dashboard/models"):
        data = {"models": MODELS}
    elif path.endswith("/dashboard/snapshot-v2"):
        data = {"stats": STATS, "trend": TREND, "models": MODELS, "groups": GROUPS,
                "endpoints": ENDPOINTS, "upstream_endpoints": ENDPOINTS,
                "endpoint_paths": ENDPOINTS}
    elif path.endswith(("/announcements", "/subscriptions/active", "/subscriptions/progress", "/groups/available")):
        data = []
    elif path.endswith(("/usage", "/keys", "/usage/errors")):
        data = {"items": [], "total": 0, "page": 1, "page_size": 20, "pages": 0}
    else:
        data = {}
        print("UNMAPPED_FIXTURE", path, flush=True)
    route.fulfill(status=200, content_type="application/json",
                  body=json.dumps({"code": 0, "data": data}))


def capture(page, name):
    page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)
    return page.evaluate("""() => ({
      width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
      background: getComputedStyle(document.body).backgroundColor,
      brokenImages: [...document.images].filter(i=>!i.complete || i.naturalWidth===0).map(i=>i.src),
      canvases: [...document.querySelectorAll('canvas')].map(c=>{
        const p=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
        let painted=0,brand=0;
        for(let i=0;i<p.length;i+=4){if(p[i+3])painted++;if(p[i]===217&&p[i+1]===119&&p[i+2]===87&&p[i+3]>200)brand++;}
        return {width:c.width,height:c.height,painted,brand};
      })
    })""")


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    report = {}
    for width, height, device in [(1440, 1000, "desktop"), (390, 844, "mobile")]:
        context = browser.new_context(viewport={"width": width, "height": height}, locale="zh-CN")
        context.route(BASE + "/api/**", fixtures)
        context.route("**/setup/status", fixtures)
        context.add_init_script("window.__APP_CONFIG__=" + json.dumps(SETTINGS) + ";")
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(BASE + "/login", wait_until="networkidle")
        page.evaluate("localStorage.setItem('theme','light');document.documentElement.classList.remove('dark')")
        page.locator("input[type=email]").focus()
        page.wait_for_timeout(250)
        report[f"login-{device}-light"] = capture(page, f"login-{device}-light")
        page.evaluate("document.documentElement.classList.add('dark')")
        report[f"login-{device}-dark"] = capture(page, f"login-{device}-dark")
        page.evaluate("""user => {
          localStorage.setItem('auth_token','local-visual-fixture');
          localStorage.setItem('auth_user',JSON.stringify(user));
          localStorage.setItem('user_guide_90001_user_v4_interactive','true');
          localStorage.setItem('theme','light');
        }""", USER)
        page.goto(BASE + "/dashboard", wait_until="networkidle")
        page.locator("canvas").first.wait_for()
        # sub2api2-specific navigation must survive the theme transplant.
        assert page.locator('.sidebar a[href="/infinite-canvas"]').count() == 1
        assert page.locator('.sidebar a[href="/ip-allowlist"]').count() == 1
        page.wait_for_timeout(500)
        report[f"dashboard-{device}-light"] = capture(page, f"dashboard-{device}-light")
        if device == "mobile":
            page.locator("header button[aria-label]").first.click()
        page.locator(".sidebar .mt-auto button").first.click()
        if device == "mobile":
            page.locator("div.fixed.inset-0.z-30").click(position={"x": width-10, "y": 100})
        page.wait_for_timeout(500)
        report[f"dashboard-{device}-dark"] = capture(page, f"dashboard-{device}-dark")
        page.goto(BASE + "/usage", wait_until="networkidle")
        page.wait_for_timeout(1200)
        report[f"usage-{device}-dark"] = capture(page, f"usage-{device}-dark")
        page.evaluate("document.documentElement.classList.remove('dark')")
        page.wait_for_timeout(250)
        report[f"usage-{device}-light"] = capture(page, f"usage-{device}-light")
        page.evaluate("localStorage.removeItem('auth_token');localStorage.removeItem('auth_user');localStorage.setItem('theme','light')")
        page.goto(BASE + "/home", wait_until="networkidle")
        report[f"home-{device}-light"] = capture(page, f"home-{device}-light")
        page.goto(BASE + "/key-usage", wait_until="networkidle")
        report[f"key-usage-{device}-light"] = capture(page, f"key-usage-{device}-light")
        report[f"errors-{device}"] = errors
        context.close()
    browser.close()
    print(json.dumps(report, indent=2), flush=True)
    (OUT / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    assert not report['errors-desktop'] and not report['errors-mobile'], "Runtime errors"
    for key, result in report.items():
        if key.startswith('errors-'):
            continue
        assert result['scrollWidth'] <= result['width'], f"Overflow: {key}"
        assert not result['brokenImages'], f"Broken image: {key}"
        if key.startswith('dashboard-'):
            assert len(result['canvases']) == 2, f"Missing charts: {key}"
            assert all(c['painted'] > 500 and c['brand'] > 0 for c in result['canvases']), f"Blank chart: {key}"
        if key.startswith('usage-'):
            assert len(result['canvases']) == 4, f"Missing distribution chart: {key}"
