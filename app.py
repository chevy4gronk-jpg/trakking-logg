
import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

DATAFIL = Path("data/trakking_logg.xlsx")

st.set_page_config(
    page_title="Tråkkeloggen",
    layout="centered"
)

st.title("🚜 Tråkkeloggen")

# Last eller opprett data
if DATAFIL.exists():
    df = pd.read_excel(DATAFIL)
    df["Dato"] = pd.to_datetime(df["Dato"])
else:
    df = pd.DataFrame(columns=[
        "Dato", "Sjåfør",
        "Maskin_ut_timer", "Maskin_inn_timer",
        "Kjøretid_timer",
        "Strekning",
        "Olje_ok", "Veske_ok", "Visuell_kontroll_ok",
        "Merknader"
    ])

# Faner – mobilvennlig
tab1, tab2 = st.tabs(["➕ Ny tur", "📊 Månedsrapport"])

# --------------------
# NY TUR
# --------------------
with tab1:
    with st.form("ny_tur", clear_on_submit=True):
        sjafor = st.selectbox(
            "Sjåfør",
            ["Thomas", "Sjåfør 2", "Sjåfør 3"]
        )

        dato = st.date_input(
            "Dato",
            value=date.today()
        )

        ut = st.number_input(
            "Maskin ut (timer)",
            min_value=0.0,
            step=0.1
        )

        inn = st.number_input(
            "Maskin inn (timer)",
            min_value=0.0,
            step=0.1
        )

        strekning = st.text_input("Strekning")

        olje = st.checkbox("Oljenivå OK", value=True)
        veske = st.checkbox("Veskenivå OK", value=True)
        visuell = st.checkbox("Visuell kontroll OK", value=True)

        merknad = st.text_area("Merknad (valgfri)", height=80)

        lagre = st.form_submit_button("💾 Lagre tur")

    if lagre:
        kjoretid = max(0, inn - ut)

        ny_rad = {
            "Dato": dato,
            "Sjåfør": sjafor,
            "Maskin_ut_timer": ut,
            "Maskin_inn_timer": inn,
            "Kjøretid_timer": kjoretid,
            "Strekning": strekning,
            "Olje_ok": olje,
            "Veske_ok": veske,
            "Visuell_kontroll_ok": visuell,
            "Merknader": merknad
        }

        df = pd.concat([df, pd.DataFrame([ny_rad])], ignore_index=True)
        df.to_excel(DATAFIL, index=False)

        st.success(f"Turen er lagret – {kjoretid:.1f} t")

# --------------------
# MÅNEDSRAPPORT
# --------------------
with tab2:
    if df.empty:
        st.info("Ingen registrerte turer ennå.")
    else:
        df["År"] = df["Dato"].dt.year
        df["Måned"] = df["Dato"].dt.month

        valgt_ar = st.selectbox(
            "År",
            sorted(df["År"].unique(), reverse=True)
        )

        valgt_maned = st.selectbox(
            "Måned",
            sorted(df[df["År"] == valgt_ar]["Måned"].unique())
        )

        filtrert = df[
            (df["År"] == valgt_ar) &
            (df["Måned"] == valgt_maned)
        ]

        st.subheader("⏱️ Timer per sjåfør")

        summering = (
            filtrert
            .groupby("Sjåfør")["Kjøretid_timer"]
            .sum()
            .reset_index()
            .rename(columns={"Kjøretid_timer": "Timer"})
        )

        st.dataframe(summering, use_container_width=True)

        st.subheader("📋 Alle turer denne måneden")
        st.dataframe(
            filtrert.drop(columns=["År", "Måned"]),
            use_container_width=True
        )https://docs.google.com/spreadsheets/d/1pv7F8aSYibs4iOJrrgsrX8BAi1eD_s47/edit?usp=drivesdk&ouid=117944760349150711944&rtpof=true&sd=true
