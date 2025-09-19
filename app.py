
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Befragung Lastflexibilität – Hotel", page_icon="🧭", layout="wide")

# ---------- Meta ----------
st.title("Befragung Lastflexibilität – Hotel")
st.caption("Masterarbeit – Intelligente Energiesysteme | ca. 20–30 Minuten")

with st.sidebar:
    st.header("Legende & Anleitung")
    st.write(
        """
        **So füllen Sie den Fragebogen aus:**
        - **Vorhanden** → Gerät im Hotel vorhanden?
        - **Leistung (kW)** → wenn bekannt eintragen
        - **Bewertung der Kriterien** je Gerät (1–4):
            - **Modulation**: Wie fein lässt sich die Leistung anpassen?
            - **Dauer**: Wie lange kann die Leistung verändert werden?
            - **Rebound**: Gibt es einen Nachholeffekt nach der Anpassung?
            - **Betriebsfenster**: Wie frei ist der Betrieb zeitlich gestaltbar?
        
        **Skala (1–4):**
        1 = gering/rigide (z. B. <10 %, <15 min, ≥24 h, sehr starker Rebound)  
        2 = moderat (10–25 %, 15–45 min, 1–8 h, starker Rebound)  
        3 = gut (25–40 %, 45–120 min, 30–60 min, geringer Rebound)  
        4 = hoch/frei (≥40 %, ≥2 h, ≤15 min, kaum Rebound)
        """
    )
    st.info("Ihre Angaben werden anonymisiert und ausschließlich zu wissenschaftlichen Zwecken verwendet.")

# ---------- Consent ----------
with st.expander("Einverständniserklärung", expanded=True):
    st.write("""Mit Ihrer Teilnahme erklären Sie sich einverstanden, dass Ihre Angaben freiwillig erfolgen,
    anonymisiert und ausschließlich zu wissenschaftlichen Zwecken verwendet werden und nicht auf einzelne Hotels oder Personen zurückgeführt werden können.""")
    consent = st.checkbox("Ich habe die Informationen verstanden und bin mit der Teilnahme einverstanden.")

# ---------- Stammdaten ----------
st.subheader("Stammdaten")
col1, col2, col3, col4 = st.columns(4)
hotel = col1.text_input("Hotel")
bereich = col2.text_input("Bereich/Abteilung")
position = col3.text_input("Position")
datum = col4.date_input("Datum", value=date.today())

name = st.text_input("Name (optional)")

# ---------- Skalenbeschriftungen ----------
scale_labels = {
    "Modulation": ["1 (<10 %)", "2 (10–25 %)", "3 (25–40 %)", "4 (≥40 %)"],
    "Dauer": ["1 (<15 min)", "2 (15–45 min)", "3 (45–120 min)", "4 (≥2 h)"],
    "Rebound": ["1 (sehr stark)", "2 (stark)", "3 (gering)", "4 (kaum)"],
    "Betriebsfenster": ["1 (rigide)", "2 (begrenzt)", "3 (breit)", "4 (frei)"],
}

# ---------- Gerätekatalog ----------
catalog = [
    # A) Küche
    ("A1) Kühlung/Kälte", [
        "Walk-in Kühlraum",
        "Walk-in Tiefkühlraum",
        "Kühltische/Unterbaukühler",
        "Getränke-/Flaschenkühler",
        "Eismaschine",
        "Kühlanlagenzentrale",
    ]),
    ("A2) Gargeräte/Wärme", [
        "Kombidämpfer",
        "Konvektomat/Backofen",
        "Fritteuse",
        "Induktionsherd",
        "Kippbratpfanne",
        "Bain-Marie/Warmhalten",
        "Salamander",
    ]),
    ("A3) Geschirr- und Spülbereich", [
        "Haubenspülmaschine",
        "Bandspülmaschine",
    ]),
    ("A4) Lüftung", [
        "Küchenabluft (Haubenlüftung)",
    ]),
    # B) Wellness / Spa / Pool
    ("B1) Sauna/Wärme", [
        "Finnische Sauna",
        "Biosauna",
    ]),
    ("B2) Dampfbad", [
        "Dampfsauna",
    ]),
    ("B3) Pools/Wassertechnik", [
        "Pool-Umwälzpumpe",
    ]),
    ("B4) Lüftung/Entfeuchtung", [
        "Schwimmbad Abluft",
        "Schwimmbad Luftentfeuchtung",
    ]),
    # C) Zimmer & Allgemeinbereiche
    ("C1) Beleuchtung", [
        "Zimmerbeleuchtung",
        "Reklame/Aussenbeleuchtung",
    ]),
    ("C2) Vertikale Förderung/Garage", [
        "Aufzüge",
    ]),
    ("C3) Laundry/Sonstiges", [
        "Waschmaschinen",
        "Trockner",
        "Wallbox (EV-Ladepunkte)",
    ]),
]

responses = []
st.markdown("---")
st.subheader("Bewertung der Geräte")

def render_device(section_key: str, device_name: str):
    key_prefix = f"{section_key}::{device_name}"

    cols = st.columns([1.2, 1, 1, 1, 1, 1.2])
    vorhanden = cols[0].checkbox("Vorhanden", key=f"{key_prefix}::vorhanden")
    leistung = None
    if device_name == "Zimmerbeleuchtung":
        betten = cols[1].number_input("Bettenanzahl", min_value=0, step=1, key=f"{key_prefix}::betten")
    else:
        leistung = cols[1].number_input("Leistung (kW)", min_value=0.0, step=0.1, format="%.1f", key=f"{key_prefix}::leistung")

    mod = cols[2].selectbox("Modulation", scale_labels["Modulation"], index=None, placeholder="Bitte wählen", key=f"{key_prefix}::mod")
    dur = cols[3].selectbox("Dauer", scale_labels["Dauer"], index=None, placeholder="Bitte wählen", key=f"{key_prefix}::dur")
    reb = cols[4].selectbox("Rebound", scale_labels["Rebound"], index=None, placeholder="Bitte wählen", key=f"{key_prefix}::reb")
    win = cols[5].selectbox("Betriebsfenster", scale_labels["Betriebsfenster"], index=None, placeholder="Bitte wählen", key=f"{key_prefix}::win")

    # Pack to a dict when any field is touched
    d = {
        "section": section_key,
        "geraet": device_name,
        "vorhanden": bool(vorhanden),
        "leistung_kw": None if device_name == "Zimmerbeleuchtung" else (leistung if leistung is not None else None),
        "bettenanzahl": (betten if device_name == "Zimmerbeleuchtung" else None),
        "modulation": mod,
        "dauer": dur,
        "rebound": reb,
        "betriebsfenster": win,
    }
    responses.append(d)

# Render sections
for sec, devices in catalog:
    st.markdown(f"### {sec}")
    for dev in devices:
        with st.container(border=True):
            render_device(sec, dev)

# ---------- Submit ----------
st.markdown("---")
valid_meta = hotel.strip() != "" and bereich.strip() != "" and position.strip() != ""
if not consent:
    st.warning("Bitte Einverständnis bestätigen.")
if not valid_meta:
    st.warning("Bitte Hotel, Bereich/Abteilung und Position angeben.")

submitted = st.button("Antworten prüfen und bereitstellen")
if submitted and consent and valid_meta:
    df = pd.DataFrame(responses)
    # add meta
    df.insert(0, "hotel", hotel)
    df.insert(1, "bereich", bereich)
    df.insert(2, "position", position)
    df.insert(3, "datum", str(datum))
    df.insert(4, "name", name)

    st.success("Antworten erfasst. Sie können die Daten unten herunterladen.")
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    json_str = df.to_json(orient="records", force_ascii=False).encode("utf-8")
    st.download_button("CSV herunterladen", csv, file_name="befragung_antworten.csv", mime="text/csv")
    st.download_button("JSON herunterladen", json_str, file_name="befragung_antworten.json", mime="application/json")

    st.caption("Tipp: Mehrere Einreichungen können später in Excel/Power BI zusammengeführt werden.")
else:
    st.caption("Wenn Sie alles ausgefüllt haben, klicken Sie auf „Antworten prüfen und bereitstellen“.")
