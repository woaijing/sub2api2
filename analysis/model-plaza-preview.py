"""Local-only model plaza fixtures, preview API and Playwright visual checks."""
import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE = os.environ.get("FOXCODE_PREVIEW_URL", "http://127.0.0.1:3001").rstrip("/")
SETTINGS = {
    "site_name": "Sub2API", "site_logo": "", "registration_enabled": True,
    "model_plaza_enabled": True, "model_plaza_require_auth": False,
    "backend_mode_enabled": False, "custom_menu_items": [], "server_utc_offset": "+08:00",
}
USER = {"id": 90001, "username": "Theme Preview", "email": "preview@example.test",
        "role": "user", "status": "active", "balance": 128.5, "concurrency": 5}


def model(name, platform, price=3, mode="token"):
    pricing = {
        "billing_mode": mode, "input_price": price / 1e6, "output_price": price * 5 / 1e6,
        "cache_write_price": price * 1.25 / 1e6, "cache_read_price": price / 10 / 1e6,
        "image_input_price": None, "image_output_price": None,
        "per_request_price": 0.04 if mode == "image" else None, "intervals": [],
    }
    return {"name": name, "platform": platform, "pricing": pricing,
            "official_pricing": {key: pricing[key] for key in [
                "input_price", "output_price", "cache_write_price", "cache_read_price"]}}


def group(group_id, name, platform, models, rate=1, **options):
    return {
        "id": group_id, "name": name, "description": "", "platform": platform,
        "subscription_type": "standard", "rate_multiplier": rate,
        "peak_rate_enabled": False, "peak_start": "14:00", "peak_end": "18:00",
        "peak_rate_multiplier": 1.5, "is_exclusive": False,
        "image_rate_independent": False, "image_rate_multiplier": 1,
        "long_context_pricing_enabled": True, "models": models, **options,
    }


CLAUDE = [model(name, "anthropic", price) for name, price in [
    ("claude-haiku-4-5", 1), ("claude-opus-4-6", 5), ("claude-sonnet-4-6", 3)]]
CLAUDE[2]["pricing"]["intervals"] = [
    {"min_tokens": minimum, "max_tokens": maximum, "input_price": None,
     "input_multiplier": multiplier, "output_price": None, "output_multiplier": multiplier,
     "cache_write_price": None, "cache_read_price": None, "per_request_price": None}
    for minimum, maximum, multiplier in [(0, 200000, 1), (200000, None, 2)]
]
CLAUDE[2]["time_pricing"] = {"timezone": "Asia/Shanghai", "weekdays_only": True,
                            "periods": [{"start_time": "00:00", "end_time": "08:00", "multiplier": 0.5}]}
DATA = {
    "description": "",
    "groups": [
        group(1, "Claude Standard", "anthropic", CLAUDE, 1),
        group(2, "Claude Subscription", "anthropic", CLAUDE, 0.5,
              subscription_type="subscription", peak_rate_enabled=True),
        group(3, "OpenAI Standard", "openai", [model("gpt-5.4", "openai", 2.5),
              model("gpt-5.3-codex", "openai", 1.75), model("gpt-image-1", "openai", mode="image")],
              0.8, image_rate_independent=True, image_rate_multiplier=0.6),
        group(4, "Gemini Standard", "gemini", [model("gemini-3.1-pro", "gemini", 2),
              model("gemini-2.5-flash", "gemini", 0.3)]),
        group(5, "DeepSeek Standard", "deepseek", [model("deepseek-chat", "deepseek", 0.28)], 0.7),
        group(6, "Grok Standard", "grok", [model("grok-4", "grok", 3)]),
        group(7, "Kimi Standard", "kimi", [model("kimi-k2.5", "kimi", 0.6)]),
        group(8, "GLM Standard", "zhipu", [model("glm-5", "zhipu", 1)]),
    ],
}


class PreviewAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        routes = {"/setup/status": {"needs_setup": False, "step": "complete"},
                  "/api/v1/settings/public": SETTINGS, "/api/v1/model-plaza": DATA}
        data = routes.get(path)
        self.send_response(200 if data is not None else 404)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(json.dumps({"code": 0 if data is not None else 404, "data": data}).encode())


def check():
    from playwright.sync_api import sync_playwright
    out = Path(__file__).resolve().parents[1] / "output" / "model-plaza-qa"
    out.mkdir(parents=True, exist_ok=True)
    report = {}

    def capture(page, name):
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.wait_for_timeout(300)
        page.screenshot(path=str(out / (name + ".png")), full_page=not name.endswith("-details"), animations="disabled")
        metrics = page.evaluate("""() => ({
          width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
          background: getComputedStyle(document.body).backgroundColor,
          cards: document.querySelectorAll('.plaza-model-card').length,
          brokenImages: [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src),
          clipped: [...document.querySelectorAll('.plaza-model-card h2, .plaza-model-card dd, nav a')]
            .filter(e => e.scrollWidth > e.clientWidth + 1).map(e => e.textContent)
        })""")
        assert metrics["scrollWidth"] <= metrics["width"], (name, metrics)
        assert not metrics["brokenImages"], (name, metrics)
        assert not metrics["clipped"], (name, metrics)
        report[name] = metrics

    def fixture(route):
        path = urlparse(route.request.url).path
        data = {"/api/v1/auth/me": USER, "/api/v1/announcements": [],
                "/api/v1/subscriptions/active": [], "/api/v1/subscriptions/progress": []}.get(path, {})
        route.fulfill(status=200, content_type="application/json", body=json.dumps({"code": 0, "data": data}))

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        for width, height, device in [(1440, 1000, "desktop"), (768, 1024, "tablet"), (390, 844, "mobile"), (320, 740, "small-mobile")]:
            context = browser.new_context(viewport={"width": width, "height": height}, locale="zh-CN")
            context.add_init_script("localStorage.setItem('theme','light');localStorage.setItem('locale','zh');")
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(BASE + "/model-plaza", wait_until="networkidle")
            page.locator("article").first.wait_for()
            assert page.locator("article").count() == 12
            capture(page, device + "-light")
            page.locator("nav button[aria-label]").click()
            assert page.locator("html.dark").count() == 1
            capture(page, device + "-dark")
            page.locator("nav button[aria-label]").click()
            page.get_by_role("button", name="CLAUDE", exact=True).click()
            assert page.locator("article").count() == 3
            page.locator("input[type=search]").fill("SONNET")
            assert page.locator("article").count() == 1
            page.locator("article button[aria-expanded]").click()
            assert page.locator("article li").count() == 2
            capture(page, device + "-expanded")
            page.locator("article li button").first.click()
            page.get_by_role("dialog").wait_for()
            assert page.locator(".plaza-pricing-table tbody tr").count() == 2
            capture(page, device + "-details")
            page.keyboard.press("Escape")
            page.get_by_role("dialog").wait_for(state="hidden")
            assert page.locator("article li button").first.evaluate("e => e === document.activeElement")
            page.locator("input[type=search]").fill("no-such-model")
            assert page.locator("article").count() == 0
            capture(page, device + "-empty")

            page.locator("input[type=search]").fill("")
            page.locator(".category-button").first.click()
            page.locator("select").first.select_option("3")
            page.locator("select").nth(1).select_option("0.6")
            assert page.locator("article").count() == 1
            assert "gpt-image-1" in page.locator("article").inner_text()

            page.route("**/api/v1/model-plaza**", lambda route: route.fulfill(status=500, content_type="application/json", body='{"code":500,"message":"fixture error"}'))
            page.reload(wait_until="networkidle")
            page.get_by_role("alert").wait_for()
            capture(page, device + "-error")
            page.unroute("**/api/v1/model-plaza**")
            page.get_by_role("alert").get_by_role("button").click()
            page.locator("article").first.wait_for()
            assert page.locator("article").count() == 12

            if device in ("desktop", "mobile"):
                context.route("**/api/v1/auth/**", fixture)
                context.route("**/api/v1/announcements**", fixture)
                context.route("**/api/v1/subscriptions/**", fixture)
                page.evaluate("""user => {
                  localStorage.setItem('auth_token', 'local-preview-only');
                  localStorage.setItem('auth_user', JSON.stringify(user));
                  localStorage.setItem('user_guide_90001_user_v4_interactive', 'true');
                }""", USER)
                page.goto(BASE + "/model-plaza?embedded=1", wait_until="networkidle")
                page.locator("article").first.wait_for()
                capture(page, device + "-embedded")
            if device == "small-mobile":
                long_model = model("custom" + "VeryLongModelName" * 6, "custom")
                stress_data = {"description": "", "groups": [group(90, "VeryLongGroupName" * 6, "custom", [long_model])]}
                page.route("**/api/v1/model-plaza**", lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps({"code": 0, "data": stress_data})))
                page.goto(BASE + "/model-plaza", wait_until="networkidle")
                page.locator("article button[aria-expanded]").click()
                capture(page, device + "-long-names")
                page.locator("article li button").click()
                page.get_by_role("dialog").wait_for()
                capture(page, device + "-long-name-details")
            assert not errors, errors
            context.close()
        browser.close()
    (out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8082)
    args = parser.parse_args()
    if args.serve:
        print("Local sample API on 127.0.0.1:" + str(args.port), flush=True)
        ThreadingHTTPServer(("127.0.0.1", args.port), PreviewAPI).serve_forever()
    else:
        check()
