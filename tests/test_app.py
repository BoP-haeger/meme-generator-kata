import io
from collections.abc import Iterator

import httpx
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from meme_generator.app import create_app


@pytest.fixture
def client() -> Iterator[httpx.Client]:
    with TestClient(create_app()) as test_client:
        yield test_client


def jpeg_bytes() -> bytes:
    out = io.BytesIO()
    Image.new("RGB", (200, 100), "teal").save(out, format="JPEG")
    return out.getvalue()


def test_health(client: httpx.Client) -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_root_serves_the_meme_page(client: httpx.Client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "/memes" in response.text


def test_meme_without_caption_is_400(client: httpx.Client) -> None:
    response = client.post("/memes", files={"image": ("a.jpg", jpeg_bytes())})
    assert response.status_code == 400
    assert response.json()["error"] == "caption_missing"


@pytest.fixture
def docs_off_client(monkeypatch: pytest.MonkeyPatch) -> Iterator[httpx.Client]:
    monkeypatch.setenv("MEME_DOCS_ENABLED", "false")
    with TestClient(create_app()) as test_client:
        yield test_client


def test_docs_can_be_disabled(docs_off_client: httpx.Client) -> None:
    assert docs_off_client.get("/docs").status_code == 404
    assert docs_off_client.get("/openapi.json").status_code == 404
