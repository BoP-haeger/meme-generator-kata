# Meme Generator

Web-App und API, die eine Caption im Meme-Stil auf ein Bild schreibt: Top text oben, Bottom text unten, in Großbuchstaben, weiße Schrift mit schwarzem Rand, im Font Anton.

Die Social-Media-Agentur des ZDF erstellt damit Memes für ihre Kanäle. Bilder und Texte sollen nicht auf fremden Meme-Seiten landen, denn viele Bilder sind nur für die eigenen Kanäle lizenziert. Deshalb hat die Agentur einen eigenen Generator, und sie ist auf ihn angewiesen.

Der Dienst ist über einen ersten Stand nie hinausgekommen. Was er heute kann, steht unter [Was der Dienst kann](#was-der-dienst-kann). Der letzte Entwickler ist nicht mehr dabei. Die offene Arbeit hat er als Issues mit Priorität hinterlegt, siehe [Offene Arbeit](#offene-arbeit). Neue Entwickler kommen als Externe dazu und arbeiten in einem Fork, siehe [Mitarbeiten](#mitarbeiten).

## Was der Dienst kann

- Seite unter `/`: JPEG hochladen, Top text, Bottom text oder beides eingeben, „Create meme“. Die Seite zeigt das Meme oder die Fehlermeldung der API.
- API: `POST /memes` mit `multipart/form-data` (`image`, `top_text`, `bottom_text`). Antwort ist das Meme als JPEG, so groß wie das Originalbild. Swagger UI unter `/docs`.
- `GET /health` antwortet mit `{"status": "ok"}`.
- Fehler kommen als JSON `{"error": "…", "message": "…"}`: ohne Text 400 (`caption_missing`), auch wenn beide Texte nur aus Leerzeichen bestehen; Bild kein JPEG oder nicht lesbar 415 (`unsupported_image`). Ausnahme: Fehlt das Bild, antwortet FastAPI mit 422 im eigenen Format `{"detail": […]}`.
- Top text steht am oberen, Bottom text am unteren Rand, in fester Schriftgröße (1/10 der Bildhöhe, mindestens 14 px) und ohne automatischen Umbruch.

## Aufsetzen

Du brauchst [uv](https://docs.astral.sh/uv/getting-started/installation/). Python 3.13 lädt uv bei Bedarf selbst.

```sh
uv sync
uv run playwright install chromium
```

Der zweite Befehl lädt Chromium für die Browser-Tests (Download etwa 300 MB, auf der Platte etwa 600 MB). Unter Linux: `uv run playwright install --with-deps chromium`.

## Starten

```sh
uv run python -m meme_generator
```

Dann <http://127.0.0.1:8000> im Browser öffnen.

| Umgebungsvariable | Standard | Wirkung |
| ----------------- | -------- | ------- |
| `MEME_PORT` | `8000` | Port |
| `MEME_HOST` | `127.0.0.1` | Adresse, an die der Server bindet |
| `MEME_DOCS_ENABLED` | `true` | `false` schaltet `/docs` und `/openapi.json` ab |

## Testen

```sh
uv run pytest                            # Unit-Tests in tests/, schnell, ohne Browser
uv run pytest e2e                        # startet den Server selbst, testet über HTTP und im Browser
uv run pytest e2e --headed --slowmo 500  # dasselbe, Browser sichtbar und verlangsamt
```

Lint, Formatierung und Typen (pyright im Modus strict):

```sh
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

### Video aufnehmen

```sh
uv run pytest e2e --video on --output videos --slowmo 500
```

Danach liegt je Browser-Test ein Video in `videos/<test>/video.webm`; es lässt sich z. B. in Chrome oder Firefox abspielen. `--slowmo 500` verlangsamt den Test; ohne fehlt das Ergebnis oft im Video. Dieser Befehl leert `videos/` vorher; andere Testläufe lassen den Ordner in Ruhe.

## Offene Arbeit

Die offene Arbeit steht als Issues in `BoP-haeger/meme-generator-kata`, Issue-Nummer = F-Nummer. Die Priorität steht als Label am Issue, von `Prio 1` (höchste) bis `Prio 4` (niedrigste). Maßgeblich sind die Labels, nicht diese Liste.

| Prio | Issue |
| ---- | ----- |
| 1 | [F3 Lange Captions](https://github.com/BoP-haeger/meme-generator-kata/issues/3) |
| 2 | [F1 Regeln für Captions mit Meldung in der Oberfläche](https://github.com/BoP-haeger/meme-generator-kata/issues/1) |
| 2 | [F6 Uploads nie auf der Platte](https://github.com/BoP-haeger/meme-generator-kata/issues/6) |
| 3 | [F2 Lesbarkeit beweisen](https://github.com/BoP-haeger/meme-generator-kata/issues/2) |
| 3 | [F4 PNG und WebP](https://github.com/BoP-haeger/meme-generator-kata/issues/4) |
| 3 | [F5 Einheitliche Fehler](https://github.com/BoP-haeger/meme-generator-kata/issues/5) |
| 3 | [F8 Grenzen und Überlast](https://github.com/BoP-haeger/meme-generator-kata/issues/8) |
| 4 | [F7 Request-ID und Logs ohne Inhalte](https://github.com/BoP-haeger/meme-generator-kata/issues/7) |
| 4 | [F9 Leistung und Betrieb](https://github.com/BoP-haeger/meme-generator-kata/issues/9) |
| 4 | [F10 Animierte Memes (optional)](https://github.com/BoP-haeger/meme-generator-kata/issues/10) |

Aktueller Stand mit Labels:

```sh
gh issue list -R BoP-haeger/meme-generator-kata
```

## Mitarbeiten

1. Repo auf GitHub forken und den Fork klonen.
2. Änderungen in einem Branch machen.
3. Pull Request gegen `main` stellen und darin auf das Issue verweisen.

In einem Fork sind Issues auf GitHub standardmäßig abgeschaltet. Lesen auch aus dem Fork: `gh issue view <n> -R BoP-haeger/meme-generator-kata`.

## Lizenzen

- Die Aufgabe stammt aus der Meme-Generator-Kata in [vanonselenp/agentic-katas](https://github.com/vanonselenp/agentic-katas), Copyright (c) 2026 Peter van Onselen, MIT-Lizenz. Lizenztext: [`LICENSE-agentic-katas`](LICENSE-agentic-katas).
- Font Anton: Copyright 2020 The Anton Project Authors, SIL Open Font License 1.1, siehe [`assets/fonts/OFL.txt`](assets/fonts/OFL.txt).

Fiktives Szenario für eine Schulung. Es besteht keine Verbindung zum ZDF.
