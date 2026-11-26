# Meme Generator

Eine kleine Web-App: Du lädst ein Bild hoch, gibst Top text und Bottom text ein und bekommst das Bild als Meme zurück, in Großbuchstaben, weißer Schrift mit schwarzem Rand, im Font Anton.

## Was die App kann

- Seite unter `/`: JPEG hochladen, Top text, Bottom text oder beides eingeben, „Create meme“. Die Seite zeigt das Meme oder die Fehlermeldung der API.
- API: `POST /memes` mit `multipart/form-data` (`image`, `top_text`, `bottom_text`), Antwort ist das Meme als JPEG. Swagger UI unter `/docs`.
- Fehler kommen als JSON `{"error": "…", "message": "…"}`: ohne Text 400, Bild kein JPEG oder nicht lesbar 415.
- Top text steht am oberen, Bottom text am unteren Rand, in fester Schriftgröße (1/10 der Bildhöhe) und ohne automatischen Umbruch.

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

Dann <http://127.0.0.1:8000> im Browser öffnen. Anderer Port: Umgebungsvariable `MEME_PORT`.

## Testen

```sh
uv run pytest       # Unit-Tests, schnell, ohne Browser
uv run pytest e2e   # startet den Server selbst, testet über HTTP und im Browser
```

### Video aufnehmen

```sh
uv run pytest e2e --video on --output videos --slowmo 500
```

Danach liegt je Browser-Test ein Video in `videos/<test>/video.webm`; es lässt sich z. B. in Chrome oder Firefox abspielen. `--slowmo 500` verlangsamt den Test; ohne fehlt das Ergebnis oft im Video. Dieser Befehl leert `videos/` vorher; andere Testläufe lassen den Ordner in Ruhe.

## Offene Anforderungen

Die offenen Anforderungen stehen als Issues auf GitHub:

- [F1 Regeln für Captions mit Meldung in der Oberfläche](https://github.com/BoP-haeger/meme-generator-kata/issues/1)
- [F2 Lesbarkeit beweisen](https://github.com/BoP-haeger/meme-generator-kata/issues/2)
- [F3 Lange Captions](https://github.com/BoP-haeger/meme-generator-kata/issues/3)
- [F4 PNG und WebP](https://github.com/BoP-haeger/meme-generator-kata/issues/4)
- [F5 Einheitliche Fehler](https://github.com/BoP-haeger/meme-generator-kata/issues/5)
- [F6 Uploads nie auf der Platte](https://github.com/BoP-haeger/meme-generator-kata/issues/6)
- [F7 Request-ID und Logs ohne Inhalte](https://github.com/BoP-haeger/meme-generator-kata/issues/7)
- [F8 Grenzen und Überlast](https://github.com/BoP-haeger/meme-generator-kata/issues/8)
- [F9 Leistung und Betrieb](https://github.com/BoP-haeger/meme-generator-kata/issues/9)
- [F10 Animierte Memes (optional)](https://github.com/BoP-haeger/meme-generator-kata/issues/10)

## Lizenzen

- Die Aufgabe stammt aus der Meme-Generator-Kata in [vanonselenp/agentic-katas](https://github.com/vanonselenp/agentic-katas), Copyright (c) 2026 Peter van Onselen, MIT-Lizenz. Lizenztext: [`LICENSE-agentic-katas`](LICENSE-agentic-katas).
- Font Anton: Copyright 2020 The Anton Project Authors, SIL Open Font License 1.1, siehe [`assets/fonts/OFL.txt`](assets/fonts/OFL.txt).
