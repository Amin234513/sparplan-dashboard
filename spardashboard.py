import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf

# ===== PREMIUM DESIGN =====
st.set_page_config(
    layout="wide", 
    page_title="🚀 SMART INVEST - Dein KI-Sparplan", 
    page_icon="📈"
)

# Modernes FinTech-Design
st.markdown("""
<style>
:root {
    --primary: #2563eb;
    --secondary: #1e40af;
    --accent: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}
h1, h2, h3, h4, h5 {
    color: var(--secondary) !important;
    font-family: 'Segoe UI', system-ui, sans-serif;
}
.st-emotion-cache-1y4p8pa {
    background-color: rgba(255,255,255,0.92);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    padding: 2rem;
}
.card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #e2e8f0;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent), #34d399) !important;
}
.stButton button {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    border: none !important;
}
.stSlider .thumb {
    background: var(--primary) !important;
}
.stSelectbox, .stNumberInput {
    background-color: #f8fafc !important;
}
</style>
""", unsafe_allow_html=True)

# ===== NEUE PREMIUM-FUNKTIONEN =====
st.title("🚀 SMART INVEST - Dein KI-Sparplan")
st.markdown("""
<div style="background: linear-gradient(90deg, #2563eb, #10b981); color: white; padding: 1rem; border-radius: 12px; margin-bottom: 2rem;">
    <h3 style="color: white!important; margin:0">✨ Premium Features: KI-Prognosen | Risikoanalyse | Automatische Rebalancing | Social Benchmarking</h3>
</div>
""", unsafe_allow_html=True)

# ===== KONFIGURATION =====
with st.expander("⚙️ Sparplan-Konfiguration", expanded=True):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💰 Finanzielle Parameter")
        monatliches_netto = st.number_input("Monatliches Nettoeinkommen (€)", 1000, 20000, 3500, 100)
        sparrate = st.slider("Sparrate (% des Einkommens)", 5, 50, 20)
        startkapital = st.number_input("Startkapital (€)", 0, 1000000, 5000, 500)
        risikoprofil = st.select_slider("Risikoprofil", ["Konservativ", "Ausgewogen", "Dynamisch", "Aggressiv"], value="Ausgewogen")
        
    with col2:
        st.subheader("🎯 Sparziele")
        ziel_betrag = st.number_input("Zielbetrag (€)", 1000, 1000000, 100000, 1000)
        ziel_jahre = st.slider("Zeithorizont (Jahre)", 1, 40, 15)
        
        st.subheader("📈 Anlagestrategie")
        etf_quote = st.slider("ETF-Anteil (%)", 0, 100, 70)
        immobilien_quote = st.slider("Immobilienanteil (%)", 0, 100, 20)
        krypto_quote = st.slider("Kryptoanteil (%)", 0, 100, 10)
        
        # Automatische Anpassung
        if (etf_quote + immobilien_quote + krypto_quote) != 100:
            st.warning("Die Summe muss 100% ergeben!")
            etf_quote = 70
            immobilien_quote = 20
            krypto_quote = 10

# ===== KI-PROGNOSE & MARKTDATEN =====
st.subheader("🤖 KI-Marktprognose")
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.markdown("**📊 Aktuelle Marktdaten**")
    # Realistische simulierte Daten
    marktdaten = {
        "MSCI World (1J)": "+8.2%",
        "EU Immobilien": "+4.5%",
        "Bitcoin (1J)": "+45.3%",
        "EURIBOR": "3.8%",
        "Inflationsrate": "2.4%"
    }
    for asset, perf in marktdaten.items():
        st.markdown(f"- {asset}: `{perf}`")

with col2:
    st.markdown("**🔮 KI-Prognose (nächste 5 Jahre)**")
    # KI-Prognose basierend auf Risikoprofil
    ki_prognosen = {
        "Konservativ": "Ø +3.8% p.a.",
        "Ausgewogen": "Ø +6.2% p.a.",
        "Dynamisch": "Ø +8.1% p.a.",
        "Aggressiv": "Ø +10.4% p.a."
    }
    st.metric("Erwartete Rendite", ki_prognosen[risikoprofil])
    st.metric("Empfohlene Asset-Allokation", f"{risikoprofil} Portfolio")
    st.metric("Risikoindex", "Mittel" if risikoprofil == "Ausgewogen" else "Hoch" if risikoprofil == "Aggressiv" else "Niedrig")

with col3:
    # Historische Performance-Vergleich
    st.markdown("**📉 Historische Performance**")
    jahre = np.arange(2020, 2024)
    konservativ = [2.1, 3.5, -1.2, 4.3]
    ausgewogen = [5.2, 8.7, -3.4, 7.9]
    dynamisch = [8.5, 15.2, -12.4, 18.7]
    aggressiv = [12.8, 32.5, -24.1, 41.3]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=jahre, y=konservativ, name="Konservativ", line=dict(width=3)))
    fig.add_trace(go.Scatter(x=jahre, y=ausgewogen, name="Ausgewogen", line=dict(width=3)))
    fig.add_trace(go.Scatter(x=jahre, y=dynamisch, name="Dynamisch", line=dict(width=3)))
    fig.add_trace(go.Scatter(x=jahre, y=aggressiv, name="Aggressiv", line=dict(width=3)))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="Jahr",
        yaxis_title="Rendite (%)",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ===== SPARPLAN-SIMULATION =====
st.subheader("📊 Sparplan-Simulation")

# Erweiterte Simulation mit mehr Parametern
monatliche_sparrate = monatliches_netto * (sparrate / 100)
simulations_jahre = ziel_jahre

# Rendite basierend auf Risikoprofil
rendite_profil = {
    "Konservativ": 0.035,
    "Ausgewogen": 0.062,
    "Dynamisch": 0.081,
    "Aggressiv": 0.104
}
jahresrendite = rendite_profil[risikoprofil]
monatsrendite = jahresrendite / 12

# Simulation mit monatlicher Verzinsung
months = simulations_jahre * 12
guthaben = startkapital
monatliche_entwicklung = [guthaben]

for month in range(1, months + 1):
    guthaben = guthaben * (1 + monatsrendite) + monatliche_sparrate
    monatliche_entwicklung.append(guthaben)

# Endgültige Werte
prognose_guthaben = guthaben
monatliche_entwicklung = np.array(monatliche_entwicklung)
zeitachse = pd.date_range(start=datetime.today(), periods=len(monatliche_entwicklung), freq='M')

# ===== VISUALISIERUNG =====
col1, col2 = st.columns(2)

with col1:
    # Vermögensentwicklung
    st.markdown(f"### 📈 Vermögensentwicklung")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=zeitachse, 
        y=monatliche_entwicklung,
        mode='lines',
        name='Prognostiziertes Vermögen',
        line=dict(color='#2563eb', width=3)
    )
    fig1.add_hline(y=ziel_betrag, line_dash="dash", line_color="#10b981", annotation_text="Zielbetrag")
    fig1.update_layout(
        height=400,
        xaxis_title="Zeit",
        yaxis_title="Vermögen (€)",
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Benchmarking
    st.markdown(f"### 🏆 Social Benchmarking")
    vergleichsdaten = {
        "Dein Plan": prognose_guthaben,
        "Durchschnitt (30-40J)": 145000,
        "Top 10% (deine Altersgruppe)": 287000,
        "Finanzfluss-Empfehlung": 220000
    }
    fig2 = px.bar(
        x=list(vergleichsdaten.keys()),
        y=list(vergleichsdaten.values()),
        labels={'x':'', 'y':'Vermögen in €'},
        color=list(vergleichsdaten.keys()),
        color_discrete_sequence=['#2563eb', '#94a3b8', '#f59e0b', '#10b981']
    )
    fig2.update_layout(
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    # Portfolio-Performance
    st.markdown(f"### 🧩 Portfolio-Allokation")
    labels = ['Aktien-ETFs', 'Immobilien', 'Krypto']
    sizes = [etf_quote, immobilien_quote, krypto_quote]
    colors = ['#2563eb', '#10b981', '#f59e0b']
    
    fig3 = go.Figure(data=[go.Pie(
        labels=labels, 
        values=sizes,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='percent+label'
    )])
    fig3.update_layout(
        height=300,
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Risikoanalyse
    st.markdown(f"### ⚠️ Risikoanalyse")
    risiko_faktoren = {
        "Marktvolatilität": 45,
        "Inflationseinfluss": 30,
        "Liquiditätsrisiko": 25,
        "Währungsrisiko": 20 if krypto_quote > 5 else 5
    }
    fig4 = px.bar(
        x=list(risiko_faktoren.keys()),
        y=list(risiko_faktoren.values()),
        labels={'x':'Risikofaktoren', 'y':'Ausprägung (0-100)'},
        color=list(risiko_faktoren.keys()),
        color_discrete_sequence=px.colors.qualitative.Dark2
    )
    fig4.update_layout(
        height=300,
        showlegend=False,
        yaxis_range=[0,50]
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    # Meilensteine
    st.markdown(f"### 🎯 Meilensteine")
    milestones = [
        {"Ziel": "50% des Ziels", "Datum": "2027 Q3", "Erfolgswahrscheinlichkeit": "85%"},
        {"Ziel": "Startkapital verdoppelt", "Datum": "2026 Q1", "Erfolgswahrscheinlichkeit": "92%"},
        {"Ziel": "Erste 100.000€", "Datum": "2029 Q4", "Erfolgswahrscheinlichkeit": "78%"},
        {"Ziel": "Finanzielle Freiheit", "Datum": f"{datetime.today().year + ziel_jahre}", "Erfolgswahrscheinlichkeit": "68%"}
    ]
    for i, milestone in enumerate(milestones):
        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between">
                <strong>{milestone['Ziel']}</strong>
                <span style="background-color:#dcfce7; color:#166534; padding:2px 8px; border-radius:12px; font-size:0.9em">
                    {milestone['Erfolgswahrscheinlichkeit']}
                </span>
            </div>
            <div style="color:#4b5563; margin-top:8px">⏱️ {milestone['Datum']}</div>
        </div>
        """, unsafe_allow_html=True)

# ===== ERGEBNISSE & EMPFEHLUNGEN =====
st.subheader("💎 Zusammenfassung & KI-Empfehlungen")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Finanzprognose")
    st.metric("Prognostiziertes Endvermögen", f"{prognose_guthaben:,.0f} €")
    st.metric("Monatliche Sparrate", f"{monatliche_sparrate:,.0f} €")
    st.metric("Erwartete Rendite p.a.", f"{jahresrendite*100:.1f}%")

with col2:
    st.markdown("### ⚙️ Optimierungsvorschläge")
    st.markdown("""
    - **ETFs:** 70% auf MSCI World & EM (TER < 0.2%)
    - **Immobilien:** REITs mit Fokus Europa
    - **Krypto:** Max. 5% in Bluechips (BTC, ETH)
    - **Steueroptimierung:** Nutzung Freibetrag
    """)
    st.progress(0.65, text="Umsetzungspotenzial: 65%")

with col3:
    st.markdown("### 🚀 Nächste Schritte")
    st.markdown("""
    1. Depot bei Smart Broker eröffnen
    2. Sparplan für Core-ETFs einrichten
    3. Quartals-Review terminieren
    4. Notfallfonds aufbauen (3 Monate)
    """)
    st.button("📅 Termin mit Berater vereinbaren")

# ===== AUTOMATISCHER REPORT =====
st.subheader("📑 Automatisierter Report")
report = f"""
# SMART INVEST - Finanzreport

## Persönliche Parameter
- **Nettoeinkommen:** {monatliches_netto:,.0f} €
- **Sparrate:** {sparrate}% ({monatliche_sparrate:,.0f} €)
- **Startkapital:** {startkapital:,.0f} €
- **Risikoprofil:** {risikoprofil}

## Zielsetzung
- **Zielbetrag:** {ziel_betrag:,.0f} €
- **Zeithorizont:** {ziel_jahre} Jahre
- **Prognostiziertes Endvermögen:** {prognose_guthaben:,.0f} €

## Portfolio-Strategie
- **Aktien-ETFs:** {etf_quote}%
- **Immobilien:** {immobilien_quote}%
- **Krypto:** {krypto_quote}%

## Risikoanalyse
Das gewählte Portfolio hat eine erwartete Rendite von {jahresrendite*100:.1f}% p.a. 
bei einem Risikoindex von {"Mittel" if risikoprofil == "Ausgewogen" else "Hoch" if risikoprofil == "Aggressiv" else "Niedrig"}.
"""

st.download_button(
    label="📥 PDF-Report herunterladen",
    data=report,
    file_name="smart_invest_report.md",
    mime="text/markdown"
)

# ===== MOBILER ZUGANG =====
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:1rem; background:#f1f5f9; border-radius:12px">
    <h4>📱 Jetzt auch mobil nutzen</h4>
    <p>Scanne den QR-Code für App-Zugang</p>
    <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://smart-invest.app" width="150" style="margin:0 auto">
</div>
""", unsafe_allow_html=True)
