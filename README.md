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

### F1 Regeln für Captions mit Meldung in der Oberfläche

Für Top text und Bottom text gilt jeweils:

- Enthält der Text Zeichen, die der Font Anton nicht hat (z. B. Emoji), antwortet die API mit 422 und nennt die betroffenen Zeichen.
- Steuerzeichen außer dem Zeilenumbruch → 400.
- Höchstens 200 Zeichen, gezählt vor der Umwandlung in Großbuchstaben (`ß` wird zu `SS`); mehr → 400.
- Ein Zeilenumbruch (`\n`) erzwingt einen Umbruch im Meme. Auf der Seite lässt er sich eingeben.
- Die Seite zeigt jede dieser Meldungen lesbar an.

Heute zeichnet die App Emoji und Steuerzeichen als leere Kästchen und nimmt Texte jeder Länge an; einen Zeilenumbruch kann man auf der Seite nicht eingeben.

### F2 Lesbarkeit beweisen

Weiße Schrift mit schwarzem Rand ist umgesetzt. Offen ist der Nachweis, dass Top text und Bottom text auf schwierigen Hintergründen lesbar sind:

1. reines Weiß
2. reines Schwarz
3. Mittelgrau (`#808080`)
4. fast weißes Gelb oder Creme
5. harte Kante hell | dunkel quer durch den Text
6. Verlauf von Weiß nach Schwarz über die Textbreite
7. Rauschen oder Schachbrett
8. gesättigte rote und blaue Streifen
9. PNG mit transparenter Fläche unter dem Text (setzt F4 voraus)

Jeden Hintergrund mit kurzem Top text und Bottom text und einmal mit langer Caption (setzt F3 voraus). Die Testbilder lassen sich reproduzierbar erzeugen. Ein Mensch hat die Ergebnisbilder einmal abgenommen; weicht ein Meme später davon ab, fällt das auf.

### F3 Lange Captions

Top text und Bottom text werden unabhängig voneinander eingepasst:

- Die Schrift startet bei etwa 1/10 der Bildhöhe.
- Der Text bricht an Wortgrenzen auf etwa 90 % der Bildbreite um.
- Solange der Textblock höher ist als etwa 1/4 des Bilds, wird die Schrift kleiner.
- Untergrenze ist etwa 1/30 der Bildhöhe, mindestens 14 px. Passt der Text dann noch nicht, antwortet die API mit 422 und die Seite zeigt die Meldung.
- Text wird nie stillschweigend abgeschnitten, auch kein einzelnes Wort, das breiter ist als eine Zeile.

Prüffälle: 150 Zeichen auf einem Bild mit 400 × 400 px; ein einzelnes Wort mit 60 Zeichen. Heute läuft ein langer Text in einer Zeile über den Bildrand hinaus.

### F4 PNG und WebP

PNG und WebP werden angenommen und kommen im selben Format zurück; die Transparenz eines PNG bleibt erhalten. Die Seite nimmt beide Formate an. Ein GIF ergibt weiter 415, bis F10 umgesetzt ist.

### F5 Einheitliche Fehler

Jede Fehlerantwort hat das Format `{"error": "…", "message": "…"}`. Fehlt das Bild, antwortet die API mit 400 (heute 422 im Format von FastAPI).

### F6 Uploads nie auf der Platte

Weder Bilddaten noch Caption-Text werden auf die Platte geschrieben, auch nicht im Fehlerfall. Nachgewiesen für: winziges Bild, genau 10 MB, 10 MB + 1 Byte, Upload ohne `Content-Length`, mehrere Dateifelder, kaputtes Bild, Dekompressionsbombe, nicht unterstütztes Format. Heute landet ein Upload über 11 MB in einer temporären Datei.

### F7 Request-ID und Logs ohne Inhalte

- Jede Antwort trägt eine Request-ID im Header `X-Request-ID`, Fehler-JSON auch. Eine mitgeschickte ID (höchstens 64 Zeichen aus `A–Z`, `a–z`, `0–9`, `-`) wird übernommen, sonst erzeugt der Dienst eine.
- Pro Anfrage eine strukturierte Logzeile mit der Form der Anfrage (Format, Bildgröße, Textlängen, Zeiten je Schritt), nie mit Caption-Text, Bilddaten oder Dateinamen.
- Bei etwa 20 parallelen Anfragen trägt jede Logzeile die ID ihrer eigenen Anfrage.
- Nachweis, dass kein Caption-Text und keine Bilddaten in den Logs landen.
- Über die Kommandozeile lässt sich aus einer lokalen Bilddatei ein Meme erzeugen, genau so gezeichnet wie über die API.

### F8 Grenzen und Überlast

- Upload über 10 MB → 413.
- Bild über 25 Megapixel → 422, erkannt bevor das Bild dekodiert wird.
- Das Meme ist an der langen Seite höchstens 1600 px groß.
- Kommen mehr gleichzeitige Anfragen, als der Dienst verarbeiten kann, wartet er einige Sekunden und antwortet dann mit 503 und `Retry-After`, ohne abzustürzen.

### F9 Leistung und Betrieb

- Der Dienst läuft in einem Container mit schreibgeschütztem Dateisystem und besteht dort alle Tests in `e2e/`.
- Antwortzeit p95 unter 300 ms für ein JPEG mit 2 Megapixeln, ohne andere Last.
- 20 parallele Nutzer über 60 s: 0 % Fehler, p95 unter 1 s.
- Unter Last höchstens 300 MB Speicher je Worker-Prozess.
- Ein Bericht stellt die gemessenen Werte diesen Zielen gegenüber und nennt Verfehlungen offen.

### F10 Animierte Memes (optional)

Ein animiertes GIF kommt als animiertes Meme zurück: Caption auf jedem Frame an derselben Stelle, Dauer der Frames und Zahl der Wiederholungen bleiben erhalten. Zu viele Frames (z. B. über 300) → 422.

## Lizenzen

- Die Aufgabe stammt aus der Meme-Generator-Kata in [vanonselenp/agentic-katas](https://github.com/vanonselenp/agentic-katas), Copyright (c) 2026 Peter van Onselen, MIT-Lizenz. Brief und Lizenztext liegen in [`trail-1/kata-meme-generator/`](https://github.com/BoP-haeger/agentic-coding-schule-staffel-1/tree/main/trail-1/kata-meme-generator) im Teilnehmer-Repo.
- Font Anton: Copyright 2020 The Anton Project Authors, SIL Open Font License 1.1, siehe [`assets/fonts/OFL.txt`](assets/fonts/OFL.txt).
