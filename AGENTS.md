# Meme Generator

Web-App, die eine Caption (Top text, Bottom text) im Meme-Stil auf ein hochgeladenes Bild schreibt. Python 3.13, FastAPI, Pillow, verwaltet mit uv. Alle Befehle laufen in diesem Ordner. Offene Anforderungen F1 ff.: [`README.md`](README.md#offene-anforderungen).

## Aufbau

| Pfad | Inhalt |
| ---- | ------ |
| `src/meme_generator/app.py` | FastAPI-App: `GET /` (Seite), `POST /memes`, `GET /health` |
| `src/meme_generator/index.html` | Die Seite: eine Datei mit HTML, CSS und JavaScript, ohne Build-Schritt |
| `src/meme_generator/rendering.py` | Zeichnet die Caption auf das Bild |
| `src/meme_generator/fitting.py` | Schriftgröße und Randbreite |
| `src/meme_generator/limits.py` | Grenzwerte; angewendet wird bisher nur `MULTIPART_SPOOL_BYTES` |
| `src/meme_generator/logs.py` | Logger, bisher unbenutzt |
| `assets/fonts/` | Font Anton und seine Lizenz |
| `tests/` | Unit-Tests, ohne Server und Browser |
| `e2e/` | Tests gegen einen echten Server, über HTTP und im Browser (pytest-playwright) |
| `e2e/fixtures/` | Testbilder |

## Aufsetzen

```sh
uv sync
uv run playwright install chromium
```

## Start

```sh
uv run python -m meme_generator
```

Läuft auf <http://127.0.0.1:8000>. Umgebungsvariablen: `MEME_PORT`, `MEME_HOST`, `MEME_DOCS_ENABLED=false` schaltet die Swagger UI unter `/docs` ab.

## Tests

| Befehl | Was |
| ------ | --- |
| `uv run pytest` | Unit-Tests in `tests/` |
| `uv run pytest e2e` | Startet den Server selbst auf einem freien Port, dann HTTP- und Browser-Tests (Chromium, headless) |
| `uv run pytest e2e --video on --output videos --slowmo 500` | Dasselbe, mit einem Video je Browser-Test in `videos/<test>/video.webm`; ohne `--slowmo` fehlt das Ergebnis oft im Video |
| `uv run pytest e2e --headed --slowmo 500` | Browser sichtbar und verlangsamt |
| `uv run ruff check .`, `uv run ruff format --check .`, `uv run pyright` | Lint, Formatierung, Typen (strict) |

- Jeder pytest-Lauf leert zuerst sein Ausgabeverzeichnis (`--output`, Standard `test-results/`), auch `uv run pytest`. Videos deshalb immer mit `--output videos` aufnehmen, sonst löscht der nächste Testlauf sie.
- Die Fixture `base_url` in `e2e/conftest.py` startet den Server. In Browser-Tests öffnet `page.goto("/")` deshalb diesen Server.
- Browser-Tests und Videos haben 800 × 1000 px (`VIEWPORT` in `e2e/conftest.py`): Formular und ein quadratisches Meme passen ohne Scrollen ins Bild.
