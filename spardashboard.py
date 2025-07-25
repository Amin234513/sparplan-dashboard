import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ===== Streamlit Konfiguration =====
st.set_page_config(
    layout="wide",
    page_title="🚀 SMART INVEST - Dein KI-Sparplan",
    page_icon="📈"
)

# ===== Stil (schlichter Hintergrund) =====
st.markdown("""
<style>
body {
    background-color: #f8fafc;
}
[data-testid="stAppViewContainer"] {
    background-color: #f8fafc;
}
h1, h2, h3, h4, h5 {
    color: #1e3a8a;
}
.st-emotion-cache-1y4p8pa {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}
</style>
""", unsafe_allow_html=True)

# ===== App-Titel =====
st.title("🚀 SMART INVEST - Dein KI-Sparplan")

# ===== Parameter-Eingabe =====
with st.sidebar:
    st.header("📋 Deine Eingaben")

    netto = st.number_input("Monatliches Nettoeinkommen (€)", 1000, 20000, 3000, 100)
    sparrate = st.slider("Sparquote (%)", 5, 80, 20)
    startkapital = st.number_input("Startkapital (€)", 0, 1000000, 10000, 1000)
    zielbetrag = st.number_input("Zielbetrag (€)", 1000, 1000000, 150000, 1000)
    laufzeit = st.slider("Anlagedauer (Jahre)", 1, 40, 20)
    profil = st.selectbox("Risikoprofil", ["Konservativ", "Ausgewogen", "Dynamisch", "Aggressiv"])

    etf = st.slider("ETF-Anteil (%)", 0, 100, 70)
    immobilien = st.slider("Immobilien-Anteil (%)", 0, 100, 20)
    krypto = st.slider("Krypto-Anteil (%)", 0, 100, 10)

    if etf + immobilien + krypto != 100:
        st.warning("Die Summe muss 100% ergeben.")
        st.stop()

# ===== Renditen nach Profil =====
renditen = {
    "Konservativ": 0.035,
    "Ausgewogen": 0.06,
    "Dynamisch": 0.08,
    "Aggressiv": 0.10
}
jahresrendite = renditen[profil]
monatsrendite = jahresrendite / 12
sparbetrag = netto * sparrate / 100

# ===== Sparplan-Simulation =====
guthaben = startkapital
entwicklung = [guthaben]

for monat in range(1, laufzeit * 12 + 1):
    guthaben *= (1 + monatsrendite)
    guthaben += sparbetrag
    entwicklung.append(guthaben)

daten = pd.DataFrame({
    "Monat": pd.date_range(datetime.today(), periods=len(entwicklung), freq='M'),
    "Vermögen (€)": entwicklung
})

# ===== Charts =====
st.subheader("📈 Vermögensentwicklung")
fig = px.line(daten, x="Monat", y="Vermögen (€)", title="Prognose deines Vermögens")
fig.add_hline(y=zielbetrag, line_dash="dash", line_color="green", annotation_text="Zielbetrag")
st.plotly_chart(fig, use_container_width=True)

# ===== Portfolio-Anzeige =====
st.subheader("📊 Portfolio-Zusammensetzung")
pie = go.Figure(data=[go.Pie(
    labels=["ETFs", "Immobilien", "Krypto"],
    values=[etf, immobilien, krypto],
    hole=0.4
)])
pie.update_layout(margin=dict(t=0, b=0))
st.plotly_chart(pie, use_container_width=True)

# ===== Ergebnis-Report =====
st.subheader("📑 Ergebnis & Empfehlung")
st.metric("Endvermögen", f"{entwicklung[-1]:,.0f} €")
st.metric("Zielbetrag erreicht?", "✅" if entwicklung[-1] >= zielbetrag else "❌")

bericht = f"""
# SMART INVEST - Bericht

## Ausgangslage
- Nettoeinkommen: {netto} €
- Sparquote: {sparrate}% = {sparbetrag:.2f} €/Monat
- Startkapital: {startkapital} €

## Ziel
- Zielbetrag: {zielbetrag} €
- Laufzeit: {laufzeit} Jahre
- Risikoprofil: {profil}
- Erwartete Jahresrendite: {jahresrendite*100:.2f}%

## Portfolio
- ETFs: {etf}%
- Immobilien: {immobilien}%
- Krypto: {krypto}%

## Ergebnis
- Endvermögen: {entwicklung[-1]:,.0f} €
- Ziel erreicht: {"✅ Ja" if entwicklung[-1] >= zielbetrag else "❌ Nein"}
"""

st.download_button("📥 Bericht herunterladen", data=bericht, file_name="smart_invest_bericht.md", mime="text/markdown")
