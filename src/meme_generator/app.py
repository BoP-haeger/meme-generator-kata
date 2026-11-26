import io
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, Response
from PIL import Image, UnidentifiedImageError
from starlette.formparsers import MultiPartParser

from meme_generator.limits import MULTIPART_SPOOL_BYTES
from meme_generator.rendering import load_font, render_caption

MultiPartParser.spool_max_size = MULTIPART_SPOOL_BYTES
INDEX_HTML = Path(__file__).with_name("index.html")


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse({"error": code, "message": message}, status_code=status)


@asynccontextmanager
async def _lifespan(_: FastAPI):
    load_font()
    yield


def create_app() -> FastAPI:
    docs = os.environ.get("MEME_DOCS_ENABLED", "true").lower() != "false"
    app = FastAPI(
        title="Meme Generator",
        lifespan=_lifespan,
        docs_url="/docs" if docs else None,
        redoc_url=None,
        openapi_url="/openapi.json" if docs else None,
    )

    @app.get("/", include_in_schema=False)
    def index() -> HTMLResponse:
        return HTMLResponse(INDEX_HTML.read_text(encoding="utf-8"))

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post(
        "/memes",
        response_model=None,
        responses={200: {"content": {"image/jpeg": {}}, "description": "The Meme"}},
    )
    def create_meme(
        image: Annotated[UploadFile, File(...)],
        top_text: Annotated[str | None, Form()] = None,
        bottom_text: Annotated[str | None, Form()] = None,
    ) -> Response:
        top = (top_text or "").strip()
        bottom = (bottom_text or "").strip()
        if not top and not bottom:
            return _error(400, "caption_missing", "Provide top_text, bottom_text or both.")
        try:
            source = Image.open(io.BytesIO(image.file.read()))
            source.load()
        except (UnidentifiedImageError, OSError):
            return _error(415, "unsupported_image", "The image could not be read.")
        if source.format != "JPEG":
            return _error(415, "unsupported_image", "Only JPEG is supported so far.")
        meme = render_caption(source.convert("RGB"), top, bottom)
        out = io.BytesIO()
        meme.save(out, format="JPEG", quality=90)
        return Response(out.getvalue(), media_type="image/jpeg")

    return app


app = create_app()
