"""Jasper plugin entry point."""

import shutil
import urllib.parse
import webbrowser

VERSION = "0.1.0"

DEFAULT_ENGINE = "https://www.google.com/search?q="
SUPPORTED_BROWSERS = {
    "chrome": ["chrome", "google-chrome", "chrome.exe"],
    "edge": ["msedge", "microsoft-edge", "msedge.exe"],
    "firefox": ["firefox", "firefox.exe"],
}

def _pick_browser(name):
    if not name:
        return None
    key = name.lower()
    if key not in SUPPORTED_BROWSERS:
        return None
    for cand in SUPPORTED_BROWSERS[key]:
        path = shutil.which(cand)
        if path:
            try:
                return webbrowser.get(path)
            except Exception:
                continue
    try:
        return webbrowser.get(key)
    except Exception:
        return None

def register(registry):
    if registry is None:
        return

    def _jasper_cmd(args=None):
        if not args:
            return (
                "jasper help:\n"
                "  jasper search <query>\n"
                "  jasper search <query> --chrome|--edge|--firefox"
            )
        if isinstance(args, (list, tuple)):
            query = " ".join(args)
        else:
            query = str(args)
        return _jasper_search([query])

    def _jasper_search(args=None):
        if not args:
            return "Usage: jasper search <query>"
        if isinstance(args, (list, tuple)):
            query_parts = [a for a in args if not str(a).startswith("--")]
            browser_flag = next((a for a in args if str(a).startswith("--")), None)
            query = " ".join(query_parts)
        else:
            query = str(args)
            browser_flag = None
        url = DEFAULT_ENGINE + urllib.parse.quote_plus(query)
        browser_name = browser_flag.lstrip("-") if browser_flag else None
        browser = _pick_browser(browser_name)
        if browser:
            browser.open(url)
        else:
            webbrowser.open(url)
        return f"Opened: {url}"

    if hasattr(registry, "register_command"):
        registry.register_command("jasper", _jasper_cmd, "Open a browser search")
        registry.register_command("jasper.search", _jasper_search, "Search the web")
