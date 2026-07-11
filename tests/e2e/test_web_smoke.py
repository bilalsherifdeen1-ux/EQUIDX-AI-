"""
Placeholder Playwright-style e2e smoke test outline for the web dashboard.

Not wired into CI by default (would require a browser runtime + the full
stack running) — kept here as a starting point per the roadmap item
"Add end-to-end (Playwright) tests for the web dashboard."

To actually run this, install playwright (`pip install playwright &&
playwright install chromium`) and remove the skip marker.
"""
import pytest

pytest.skip(
    "E2E browser tests require Playwright + a running stack; see docstring.",
    allow_module_level=True,
)


def test_marketing_page_loads_and_shows_disclaimer():
    # from playwright.sync_api import sync_playwright
    # with sync_playwright() as p:
    #     browser = p.chromium.launch()
    #     page = browser.new_page()
    #     page.goto("http://localhost:3000")
    #     assert "Research prototype" in page.content()
    #     browser.close()
    ...
