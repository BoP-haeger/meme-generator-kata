"""Walking skeleton: a JPEG with Top text over HTTP."""

import io
from typing import cast

import httpx
from PIL import Image, ImageChops

JPEG_NOISE = 30


def band_changed(before: Image.Image, after: Image.Image, top: int, bottom: int) -> bool:
    box = (0, top, before.width, bottom)
    diff = ImageChops.difference(before.convert("L").crop(box), after.convert("L").crop(box))
    # JPEG re-encoding shifts pixels slightly everywhere; text changes them a lot.
    _, strongest = cast(tuple[int, int], diff.getextrema())
    return strongest > JPEG_NOISE


def test_health(client: httpx.Client) -> None:
    assert client.get("/health").status_code == 200


def test_jpeg_with_top_text_returns_meme_with_text_in_top_band(
    client: httpx.Client, jpeg: bytes
) -> None:
    response = client.post(
        "/memes", files={"image": ("a.jpg", jpeg, "image/jpeg")}, data={"top_text": "hello"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    meme = Image.open(io.BytesIO(response.content))
    source = Image.open(io.BytesIO(jpeg))
    assert meme.format == "JPEG"
    assert meme.size == source.size
    assert band_changed(source, meme, 0, meme.height // 4)
    assert not band_changed(source, meme, meme.height // 4 + 20, meme.height)
