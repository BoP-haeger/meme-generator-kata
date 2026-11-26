"""The meme page in a real browser (pytest-playwright)."""

from pathlib import Path

from playwright.sync_api import Page, expect


def test_jpeg_with_top_text_shows_meme(page: Page, jpeg_path: Path) -> None:
    page.goto("/")
    page.get_by_label("Image").set_input_files(jpeg_path)
    page.get_by_label("Top text").fill("hello")
    page.get_by_role("button", name="Create meme").click()

    meme = page.get_by_role("img", name="Meme")
    expect(meme).to_be_visible()
    expect(meme).to_have_js_property("naturalWidth", 800)
