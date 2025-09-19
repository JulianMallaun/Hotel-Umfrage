
# Befragungs-App (Streamlit)

Diese App bildet den **Befragungsbogen Lastflexibilität – Hotel** digital ab. Sie ist in **Python/Streamlit** umgesetzt.

## Start lokal
1. Python 3.10+ installieren.
2. In dieses Verzeichnis wechseln und Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
3. App starten:
   ```bash
   streamlit run app.py
   ```
4. Den im Terminal angezeigten Link öffnen (z. B. http://localhost:8501) und die Umfrage ausfüllen.

## Weitergabe
- Das Skript kann an Betriebe versendet werden. Ohne Installation empfiehlt sich das **Hosten** (z. B. Streamlit Cloud, lokaler Server, Intranet).
- Ergebnisse können als **CSV** oder **JSON** heruntergeladen werden.

## Export
- Jeder Klick auf „Antworten prüfen und bereitstellen“ erzeugt eine Tabelle, die sich direkt herunterladen lässt.
