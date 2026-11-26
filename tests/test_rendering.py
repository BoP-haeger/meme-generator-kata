from PIL import Image, ImageChops

from meme_generator.rendering import render_caption


def changed_rows(before: Image.Image, after: Image.Image) -> tuple[int, int]:
    bbox = ImageChops.difference(before, after).getbbox()
    assert bbox is not None
    return bbox[1], bbox[3]


def test_top_text_only_changes_top_band() -> None:
    source = Image.new("RGB", (400, 300), (60, 120, 160))
    top, bottom = changed_rows(source, render_caption(source, "hello", None))
    assert top < 20
    assert bottom < source.height // 4 + 10


def test_bottom_text_only_changes_bottom_band() -> None:
    source = Image.new("RGB", (400, 300), (60, 120, 160))
    top, bottom = changed_rows(source, render_caption(source, None, "hello"))
    assert top > source.height * 3 // 4 - 10
    assert bottom > source.height - 20


def test_render_does_not_modify_source() -> None:
    source = Image.new("RGB", (200, 100), "black")
    render_caption(source, "x", None)
    assert source.getbbox() is None or source.getextrema() == ((0, 0), (0, 0), (0, 0))
