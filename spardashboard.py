import streamlit as st
import plotly.express as px
import pandas as pd

# === FANCY DESIGN-KONFIGURATION (Anpassbar) ===
THEME = "midnight_blue"  # Optionen: aurora_purple, emerald_green, sunset_orange
BACKGROUND_IMAGE = [url=https://ibb.co/Jwr9zKp7][img]https://i.ibb.co/dwkRQrp2/b5836dd4-2e59-486c-8ca0-cec79457ebd3.jpg[/img][/url]  # Optional

# === DASHBOARD-AUFBAU ===
st.set_page_config(layout="wide", page_title="💰 Finanz-Magie", page_icon="✨")

# Custom CSS für "Wow-Effekt"
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;800&display=swap');
body {{ 
    font-family: 'Montserrat', sans-serif; 
    background: url('{BACKGROUND_IMAGE}') no-repeat center center fixed;
    background-size: cover;
}}
.stMetricContainer {{ 
    background: rgba(25, 25, 35, 0.7) !important; 
    border-radius: 15px !important;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
}}
.stProgress > div > div {{ 
    background-image: linear-gradient(to right, #00d2ff, #3a7bd5) !important; 
}}
</style>
""", unsafe_allow_html=True)

# === INTERAKTIVER INPUT-BEREICH ===
with st.sidebar:
    st.header("🎛️ Deine Parameter")
    einkommen = st.number_input("Monatseinkommen (€)", min_value=0, value=2500, step=100)
    fixkosten = st.number_input("Fixkosten (€)", min_value=0, value=1200, step=100)
    sparen = st.number_input("Sparziel pro Monat (€)", min_value=0, value=450, step=50)
    spartage = st.slider("Spartarget (Monate)", 1, 60, 12)

# === AUTOMATISCHE BERECHNUNGEN ===
verfuegbar = einkommen - fixkosten
sparquote = (sparen / einkommen) * 100
erreicht = min(sparen * spartage, 10000)  # Beispiel-Logik

# === VISUALISIERUNGEN MIT PLOTLY (Fancy Charts) ===
# 1. Sparfortschritt (Animierter Balken)
df_progress = pd.DataFrame({
    "Phase": ["Erreicht", "Verbleibend"],
    "Betrag": [erreicht, 10000 - erreicht]
})
fig1 = px.bar(df_progress, x='Betrag', y='Phase', orientation='h', 
             color='Phase', color_discrete_sequence=['#00cc96', '#ff6699'],
             title="<b>🏆 Sparziel-Fortschritt</b>")
fig1.update_layout(showlegend=False, hovermode=False)

# 2. Mittelverwendung (3D-Tortendiagramm)
labels = ['Fixkosten', 'Sparen', 'Verfügbar']
values = [fixkosten, sparen, verfuegbar - sparen]
fig2 = px.pie(values=values, names=labels, hole=0.4,
             title="<b>💸 Geldfluss-Tornado</b>",
             color_discrete_sequence=px.colors.qualitative.Pastel)

# === DASHBOARD-AUSGABE ===
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💰 Verfügbar pro Monat", f"{verfuegbar}€")
with col2:
    st.metric("📈 Sparquote", f"{sparquote:.1f}%")
with col3:
    st.metric("🎯 Ziel erreicht", f"{erreicht}€")

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
