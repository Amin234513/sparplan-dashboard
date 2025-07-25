import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import math
import random
import time

# ===== SCHLICHTES DUNKLES DESIGN =====
st.set_page_config(
    page_title="NEXUS Wealth",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS für schlichtes dunkles Design
DARK_DESIGN = """
<style>
:root {
    --dark-1: #0a0f1f;
    --dark-2: #121a30;
    --dark-3: #1a2540;
    --accent: #2575fc;
    --light-text: #e6f0ff;
}

* {
    font-family: 'Inter', 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--dark-1) !important;
    color: var(--light-text) !important;
}

.stApp {
    background: transparent !important;
    padding-top: 0 !important;
}

/* Header Design */
[data-testid="stHeader"] {
    background-color: rgba(10, 15, 31, 0.95) !important;
    border-bottom: 1px solid rgba(37, 117, 252, 0.2);
}

/* Sidebar Design */
[data-testid="stSidebar"] {
    background-color: var(--dark-2) !important;
    border-right: 1px solid rgba(37, 117, 252, 0.2);
}

/* Main Content */
.main-content {
    padding: 20px 40px;
}

/* Card Design */
.card {
    background-color: var(--dark-3) !important;
    border-radius: 12px !important;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(37, 117, 252, 0.2);
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card:hover {
    border: 1px solid rgba(37, 117, 252, 0.4);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

/* Button Design */
.stButton>button {
    background-color: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.stButton>button:hover {
    background-color: #1c65e0 !important;
    box-shadow: 0 2px 10px rgba(37, 117, 252, 0.3);
}

/* Slider Design */
.stSlider .st-ae {
    background: var(--accent) !important;
}

.stSlider .st-af {
    background: var(--dark-2) !important;
}

/* Progress Bar */
.stProgress > div > div > div {
    background: var(--accent) !important;
}

/* Tabs */
[data-baseweb="tab-list"] {
    gap: 5px;
}

[data-baseweb="tab"] {
    background: var(--dark-3) !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
    border: 1px solid rgba(37, 117, 252, 0.2) !important;
}

[data-baseweb="tab"]:hover {
    background: rgba(37, 117, 252, 0.2) !important;
}

[aria-selected="true"] {
    background: var(--accent) !important;
    color: white !important;
    font-weight: 500 !important;
    border: 1px solid var(--accent) !important;
}

/* Metric Cards */
.metric-card {
    background-color: var(--dark-3) !important;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(37, 117, 252, 0.2);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 5px;
}

.metric-label {
    font-size: 1rem;
    opacity: 0.8;
}

/* Input Fields */
.stTextInput>div>div>input, 
.stNumberInput>div>div>input, 
.stSelectbox>div>div>select {
    background-color: var(--dark-2) !important;
    color: var(--light-text) !important;
    border: 1px solid rgba(37, 117, 252, 0.2) !important;
    border-radius: 8px !important;
    padding: 10px !important;
}

/* Table Styling */
.stDataFrame {
    border: 1px solid rgba(37, 117, 252, 0.2) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* KI-Assistent Panel */
.ki-panel {
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 350px;
    background-color: var(--dark-2);
    border-left: 1px solid rgba(37, 117, 252, 0.3);
    z-index: 100;
    padding: 20px;
    overflow-y: auto;
    transition: transform 0.3s ease;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.2);
    transform: translateX(100%);
}

.ki-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.ki-message {
    background-color: var(--dark-3);
    border-radius: 10px;
    padding: 12px 15px;
    margin-bottom: 15px;
}

.ki-user {
    background-color: rgba(37, 117, 252, 0.15);
    border: 1px solid rgba(37, 117, 252, 0.3);
}

.ki-assistant {
    background-color: var(--dark-3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.ki-input-container {
    position: sticky;
    bottom: 0;
    background: var(--dark-2);
    padding: 15px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.close-btn {
    background: none;
    border: none;
    color: var(--light-text);
    font-size: 1.5rem;
    cursor: pointer;
}

/* KI-Button */
.ki-button {
    position: fixed;
    top: 100px;
    right: 20px;
    z-index: 99;
    background: #2575fc;
    color: white;
    border: none;
    border-radius: 50px;
    padding: 12px 24px;
    font-weight: 500;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.ki-button:hover {
    background: #1c65e0;
    transform: scale(1.05);
}
</style>
"""
st.markdown(DARK_DESIGN, unsafe_allow_html=True)

# ===== FUNKTIONEN =====
def dashboard():
    """Hauptdashboard"""
    with st.container():
        st.title("💎 NEXUS Wealth")
        st.subheader("Dein Finanz-Dashboard")
        
        # Kurzstatistiken
        col1, col2, col3 = st.columns(3)
        col1.markdown("""
        <div class="metric-card">
            <div class="metric-value">284.500€</div>
            <div class="metric-label">Prognostiziertes Vermögen</div>
        </div>
        """, unsafe_allow_html=True)
        
        col2.markdown("""
        <div class="metric-card">
            <div class="metric-value">85€/Monat</div>
            <div class="metric-label">Sparpotential</div>
        </div>
        """, unsafe_allow_html=True)
        
        col3.markdown("""
        <div class="metric-card">
            <div class="metric-value">7.2%</div>
            <div class="metric-label">Portfolio-Performance</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sparplan-Optimierung
        st.subheader("Sparplan Optimierung")
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_savings = st.number_input("Monatliche Sparrate (€)", 50, 5000, 300)
            years = st.slider("Ansparzeit (Jahre)", 5, 40, 15)
            return_rate = st.slider("Erwartete Rendite (%)", 1.0, 15.0, 6.5, 0.1)
            
            # Berechnung
            monthly_return = return_rate / 100 / 12
            months = years * 12
            future_value = monthly_savings * (((1 + monthly_return)**months - 1) / monthly_return)
            
            st.markdown(f"""
            <div class="card">
                <h4>Prognose</h4>
                <div class="metric-value">{future_value:,.0f}€</div>
                <div class="metric-label">Zukünftiges Vermögen</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Diagramm
            growth = []
            for year in range(years + 1):
                months = year * 12
                value = monthly_savings * (((1 + monthly_return)**months - 1) / monthly_return)
                growth.append(value)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(years + 1)),
                y=growth,
                mode="lines+markers",
                name="Vermögensentwicklung",
                line=dict(color="#2575fc", width=3),
                hovertemplate="Jahr %{x}: %{y:,.0f}€"
            ))
            
            fig.update_layout(
                title="Vermögensentwicklung",
                xaxis_title="Jahre",
                yaxis_title="Vermögen (€)",
                template="plotly_dark",
                height=350,
                margin=dict(l=0, r=0, b=0, t=40)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Portfolio-Übersicht
        st.subheader("Portfolio Analyse")
        portfolio_data = pd.DataFrame({
            "Asset": ["ETFs", "Aktien", "Krypto", "Immobilien", "Cash"],
            "Anteil (%)": [45, 20, 15, 15, 5],
            "Rendite (%)": [7.2, 4.5, -2.3, 3.8, 0.5]
        })
        st.dataframe(portfolio_data, use_container_width=True, hide_index=True)
        
        # Assetverteilung
        fig = px.pie(
            portfolio_data, 
            names="Asset", 
            values="Anteil (%)",
            title="Assetverteilung",
            color_discrete_sequence=["#2575fc", "#1c65e0", "#1554b8", "#0e4490", "#073368"]
        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

def sparplan_rechner():
    """Sparplan Rechner"""
    with st.container():
        st.title("📈 Sparplan Rechner")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Eingaben")
            monthly_savings = st.number_input("Monatliche Sparrate (€)", 50, 5000, 300)
            start_capital = st.number_input("Startkapital (€)", 0, 1000000, 5000)
            years = st.slider("Anlagezeitraum (Jahre)", 5, 40, 20)
            return_rate = st.slider("Erwartete Rendite p.a. (%)", 1.0, 15.0, 6.5)
            inflation = st.slider("Erwartete Inflation p.a. (%)", 0.0, 10.0, 2.0)
            savings_increase = st.slider("Jährliche Sparerhöhung (%)", 0.0, 10.0, 2.0)
        
        # Berechnung
        if st.button("Berechnen"):
            with st.spinner("Berechne..."):
                # Daten für die Darstellung
                jahre = list(range(years + 1))
                vermoegen = [start_capital]
                inflationsbereinigt = [start_capital]
                sparrate = monthly_savings * 12
                
                for jahr in range(1, years + 1):
                    # Wertentwicklung
                    wertentwicklung = vermoegen[-1] * (1 + return_rate/100)
                    
                    # Sparrate mit Dynamik
                    jaehrliche_sparrate = sparrate * (1 + savings_increase/100)**(jahr-1)
                    
                    # Neues Vermögen
                    neues_vermoegen = wertentwicklung + jaehrliche_sparrate
                    vermoegen.append(neues_vermoegen)
                    
                    # Inflationsbereinigt
                    inflationsfaktor = (1 - inflation/100)**jahr
                    inflationsbereinigt.append(neues_vermoegen * inflationsfaktor)
                
                # Diagramm erstellen
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=jahre, 
                    y=vermoegen,
                    mode="lines+markers",
                    name="Nominalwert",
                    line=dict(color="#2575fc", width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=jahre, 
                    y=inflationsbereinigt,
                    mode="lines+markers",
                    name="Inflationsbereinigt",
                    line=dict(color="#1c65e0", width=3)
                ))
                
                fig.update_layout(
                    title="Vermögensentwicklung",
                    xaxis_title="Jahre",
                    yaxis_title="Vermögen (€)",
                    hovermode="x unified",
                    height=500,
                    template="plotly_dark"
                )
                
                with col2:
                    st.subheader("Ergebnisse")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Ergebnisse anzeigen
                    endvermoegen = vermoegen[-1]
                    realwert = inflationsbereinigt[-1]
                    
                    st.markdown(f"""
                    <div class="card">
                        <h4>Zusammenfassung</h4>
                        <p>Endvermögen nominal: <strong>{endvermoegen:,.0f}€</strong></p>
                        <p>Kaufkraft (inflationsbereinigt): <strong>{realwert:,.0f}€</strong></p>
                        <p>Eingezahlte Sparbeiträge: <strong>{(monthly_savings * 12 * years):,.0f}€</strong></p>
                        <p>Zinseszins-Effekt: <strong>{(endvermoegen - start_capital - (monthly_savings * 12 * years)):,.0f}€</strong></p>
                    </div>
                    """, unsafe_allow_html=True)

def portfolio_analyse():
    """Portfolio Analyse"""
    with st.container():
        st.title("📊 Portfolio Analyse")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Aktuelles Portfolio")
            etf = st.slider("ETF-Anteil (%)", 0, 100, 45)
            aktien = st.slider("Einzelaktien (%)", 0, 100, 20)
            krypto = st.slider("Krypto (%)", 0, 100, 15)
            immobilien = st.slider("Immobilien (%)", 0, 100, 15)
            andere = st.slider("Andere (%)", 0, 100, 5)
            
            # Validierung
            total = etf + aktien + krypto + immobilien + andere
            if total != 100:
                st.error(f"Summe muss 100% betragen! Aktuell: {total}%")
        
        with col2:
            st.subheader("Optimierungsvorschlag")
            
            # Portfolio-Daten
            data = {
                "Assetklasse": ["ETFs", "Aktien", "Krypto", "Immobilien", "Andere"],
                "Aktuell": [etf, aktien, krypto, immobilien, andere],
                "Empfohlen": [50, 20, 10, 15, 5]
            }
            
            # Diagramm
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=data["Assetklasse"],
                y=data["Aktuell"],
                name="Aktuell",
                marker_color="#2575fc"
            ))
            fig.add_trace(go.Bar(
                x=data["Assetklasse"],
                y=data["Empfohlen"],
                name="Empfohlen",
                marker_color="#1c65e0"
            ))
            
            fig.update_layout(
                title="Portfolio-Optimierung",
                barmode="group",
                template="plotly_dark",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Empfehlungen
            st.markdown("""
            <div class="card">
                <h4>Optimierungsempfehlungen</h4>
                <ul>
                    <li>ETF-Anteil auf 50% erhöhen</li>
                    <li>Krypto auf max. 10% reduzieren</li>
                    <li>Immobilien-Exposure durch REITs erhöhen</li>
                    <li>Notfallfonds prüfen (3-6 Monatsausgaben)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def spar_tipps():
    """Spar-Tipps"""
    with st.container():
        st.title("💡 Spar-Tipps")
        
        # Kategorien
        categories = {
            "Haushalt": [
                "Smart Thermostat installieren - spart bis zu 15% Heizkosten",
                "LED-Beleuchtung komplett umstellen - 80% weniger Stromverbrauch",
                "Wassersparende Duschköpfe nutzen - reduziert Verbrauch um 40%",
                "Energieeffiziente Geräte der Klasse A+++ kaufen",
                "Stromfresser identifizieren mit Energiemonitor"
            ],
            "Einkaufen": [
                "Cashback-Apps wie Shoop nutzen - bis zu 10% zurück",
                "Preisvergleichs-Tools vor jedem Kauf verwenden",
                "Saisonal und regional einkaufen - 30% günstiger",
                "Großpackungen bei häufig genutzten Produkten",
                "Einkaufslisten strikt einhalten - reduziert Impulskäufe"
            ],
            "Finanzen": [
                "Bankgebühren vergleichen und wechseln - bis zu 100€/Jahr sparen",
                "Kreditkarten mit Cashback nutzen",
                "Versicherungen jährlich prüfen und optimieren",
                "Steuererklärung machen - durchschnittlich 1.000€ Rückerstattung",
                "Automatische Sparpläne einrichten - Pay yourself first"
            ]
        }
        
        # Tipp-Kategorien
        selected_category = st.selectbox("Kategorie wählen", list(categories.keys()))
        
        # Tipps anzeigen
        if selected_category:
            tips = categories[selected_category]
            cols = st.columns(2)
            
            for i, tip in enumerate(tips):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="card">
                        <div style="display: flex; align-items: start; gap: 10px;">
                            <div style="font-size: 1.5rem; color: #2575fc;">•</div>
                            <div>
                                <p>{tip}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Personalisierte Empfehlung
        st.markdown("""
        <div class="card">
            <h4>Personalisierte Empfehlung</h4>
            <div style="padding: 15px; background: rgba(37, 117, 252, 0.1); border-radius: 8px; margin-top: 10px;">
                <p>Basierend auf Ihrem Profil könnten Sie <strong>{random.randint(50, 150)}€ pro Monat</strong> sparen durch:</p>
                <ul>
                    <li>{random.choice(["Bankwechsel", "Energieoptimierung", "Versicherungscheck"])}</li>
                    <li>{random.choice(["Steueroptimierung", "Abokündigungen", "Einkaufsoptimierung"])}</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

def investment_strategien():
    """Investment-Strategien"""
    with st.container():
        st.title("🚀 Investment-Strategien")
        
        # Strategien
        strategien = {
            "Konservativ": {
                "risiko": "Niedrig",
                "rendite": "3-5% p.a.",
                "portfolio": "70% Anleihen, 20% ETFs, 10% Cash",
                "beschreibung": "Sicherheitsorientiert mit Fokus auf Kapitalerhalt"
            },
            "Ausgewogen": {
                "risiko": "Mittel",
                "rendite": "5-7% p.a.",
                "portfolio": "50% ETFs, 30% Anleihen, 15% Aktien, 5% Rohstoffe",
                "beschreibung": "Balance zwischen Sicherheit und Wachstum"
            },
            "Wachstum": {
                "risiko": "Hoch",
                "rendite": "7-10% p.a.",
                "portfolio": "70% ETFs, 20% Einzelaktien, 10% Krypto/REITs",
                "beschreibung": "Langfristiges Wachstum mit höherem Risiko"
            }
        }
        
        # Auswahl
        selected_strategy = st.selectbox("Wählen Sie eine Strategie", list(strategien.keys()))
        
        if selected_strategy:
            strat = strategien[selected_strategy]
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h3>{selected_strategy}</h3>
                    <p><strong>Risiko:</strong> {strat["risiko"]}</p>
                    <p><strong>Erwartete Rendite:</strong> {strat["rendite"]}</p>
                    <p><strong>Portfolio:</strong> {strat["portfolio"]}</p>
                    <p><strong>Beschreibung:</strong> {strat["beschreibung"]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Portfolio-Verteilung
                portfolio = {
                    "Asset": [],
                    "Anteil": []
                }
                
                # Parse Portfolio
                parts = strat["portfolio"].split(",")
                for part in parts:
                    asset = part.split("%")[1].strip()
                    anteil = int(part.split("%")[0].strip())
                    portfolio["Asset"].append(asset)
                    portfolio["Anteil"].append(anteil)
                
                # Diagramm
                fig = px.pie(
                    portfolio,
                    names="Asset",
                    values="Anteil",
                    title=f"{selected_strategy} Portfolio",
                    color_discrete_sequence=["#2575fc", "#1c65e0", "#1554b8", "#0e4490"]
                )
                fig.update_layout(template="plotly_dark", height=400)
                st.plotly_chart(fig, use_container_width=True)

def finanzziele():
    """Finanzziele"""
    with st.container():
        st.title("🎯 Finanzziele")
        
        # Zieleingabe
        with st.form("ziel_formular"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Zielname", placeholder="Eigenheim, Altersvorsorge")
                zielbetrag = st.number_input("Zielbetrag (€)", 1000, 10000000, 50000)
                prioritaet = st.selectbox("Priorität", ["Hoch", "Mittel", "Niedrig"])
            
            with col2:
                deadline = st.date_input("Zieldatum", datetime.now() + timedelta(days=365*5))
                aktuell_gespart = st.number_input("Aktuell gespart (€)", 0, 10000000, 5000)
                monatliche_sparrate = st.number_input("Monatliche Sparrate (€)", 0, 5000, 500)
            
            if st.form_submit_button("Ziel speichern"):
                st.success("Ziel gespeichert!")
        
        # Zielübersicht
        if 'ziele' not in st.session_state:
            st.session_state.ziele = []
        
        if st.session_state.ziele:
            st.subheader("Ihre Finanzziele")
            for ziel in st.session_state.ziele:
                with st.container():
                    st.markdown(f"#### {ziel['name']} ({ziel['prioritaet']} Priorität)")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Zielbetrag", f"{ziel['zielbetrag']:,.0f}€")
                        st.metric("Aktueller Stand", f"{ziel['aktuell_gespart']:,.0f}€")
                    
                    with col2:
                        # Fortschrittsbalken
                        progress = min(1.0, ziel['aktuell_gespart'] / ziel['zielbetrag'])
                        st.markdown(f"**Fortschritt** ({progress*100:.1f}%)")
                        st.progress(progress)

# ===== INTELLIGENTE LOKALE KI-FUNKTION =====
def get_ai_response(user_input):
    """Intelligente Finanzberatung ohne externe API"""
    finanzwissen = {
        "sparplan": [
            "Für den Einstieg empfehle ich: 60% MSCI World ETF (IE00B4L5Y983), 20% Emerging Markets (IE00BKM4GZ66), 15% Technologie-ETF (IE00BYVQ8C80), 5% Krypto. Monatlich 300-500€ sparen.",
            "Ein guter Sparplan: 70% MSCI World, 20% Anleihen-ETF, 10% REITs. Mit 500€ monatlich können Sie in 20 Jahren etwa 250.000€ ansparen (bei 6% Rendite).",
            "Sparplan-Optimierung: Verteilen Sie Ihr Investment auf 3 ETFs: Weltaktien (50%), Schwellenländer (30%), Dividenden-ETF (20%)."
        ],
        "etf": [
            "Top ETFs 2024: iShares Core MSCI World (IE00B4L5Y983), Vanguard FTSE All-World (IE00B3RBWM25), Xtrackers MSCI World Technology (IE00BMVB5R75). TER <0.2%.",
            "Günstige ETFs: Amundi Prime Global (LU2089238203) mit 0.05% TER, Xtrackers MSCI World (IE00BK1PV551) mit 0.12% TER.",
            "Dividenden-ETFs: iShares STOXX Global Select Dividend (DE0002635281), Fidelity Global Quality Income (IE00BYXVGX24)."
        ],
        "portfolio": [
            "Portfolio-Optimierung: Erhöhen Sie den ETF-Anteil auf 50-60%, reduzieren Sie Einzelaktien auf 15-20%, halten Sie Krypto unter 10%.",
            "Ein ausgewogenes Portfolio: 50% ETFs, 20% Anleihen, 15% Immobilien (REITs), 10% Edelmetalle, 5% Krypto.",
            "Für Risikobereite: 70% Wachstums-ETFs, 20% Einzelaktien (Tech), 10% Krypto. Für Sicherheit: 60% Anleihen, 30% ETFs, 10% Cash."
        ],
        "kosten": [
            "Kosten senken: Nutzen Sie Neobroker (1€/Sparplan), wählen Sie ETFs mit TER <0.2%, vermeiden Sie aktiv gemanagte Fonds (>1% Gebühren).",
            "Steuern sparen: Nutzen Sie den Sparer-Pauschbetrag von 1000€ pro Jahr, halten Sie Anlagen >1 Jahr für Steuerfreiheit.",
            "Bankkosten: Wechseln Sie zu Direktbanken, die keine Depotgebühren verlangen und günstige Sparpläne anbieten."
        ],
        "einkommen": [
            "Passives Einkommen aufbauen: Investieren Sie in Dividenden-ETFs mit 3-5% Ausschüttung. Bei 200.000€ Investment: 6000-10.000€/Jahr.",
            "REITs für Immobilien-Rendite: Vonovia REIT (DE000A1ML7J1) mit 4-6% Dividende, Realty Income (US7561091049) mit monatlicher Ausschüttung.",
            "Anleihen-ETF für regelmäßiges Einkommen: iShares Global Government Bond (IE00B1FZS798) mit 3-4% Rendite."
        ],
        "allgemein": [
            "Finanziell unabhängig werden: Sparen Sie 25-50% Ihres Einkommens, investieren Sie langfristig in breit gestreute ETFs.",
            "Notfallfonds: Halten Sie 3-6 Monatsausgaben auf einem Tagesgeldkonto bereit. Mindestens 5000€ für unerwartete Ausgaben.",
            "Altersvorsorge: Nutzen Sie staatliche Förderungen wie Riester-Rente, besonders wenn Sie Kinder haben oder niedrige Einkommen."
        ]
    }
    
    # Schlüsselwörter erkennen
    if "sparplan" in user_input.lower():
        return random.choice(finanzwissen["sparplan"])
    elif "etf" in user_input.lower():
        return random.choice(finanzwissen["etf"])
    elif "portfolio" in user_input.lower():
        return random.choice(finanzwissen["portfolio"])
    elif "kosten" in user_input.lower() or "gebühren" in user_input.lower():
        return random.choice(finanzwissen["kosten"])
    elif "einkommen" in user_input.lower() or "dividenden" in user_input.lower():
        return random.choice(finanzwissen["einkommen"])
    else:
        return random.choice(finanzwissen["allgemein"])

def ki_assistent():
    """KI-Assistent in rechter Seitenleiste"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hallo! Ich bin dein NEXUS KI-Assistent für Finanzen. Stelle mir Fragen zu Sparplänen, ETFs, Portfolio-Optimierung oder passivem Einkommen. Wie kann ich dir helfen?"}
        ]
    
    # KI-Assistent Panel
    st.markdown("""
    <div class="ki-panel" id="ki-panel">
        <div class="ki-header">
            <h3>🤖 NEXUS KI-Assistent</h3>
            <button class="close-btn" onclick="document.getElementById('ki-panel').style.transform = 'translateX(100%)';">✕</button>
        </div>
        
        <div class="ki-messages">
    """, unsafe_allow_html=True)
    
    # Chatverlauf anzeigen
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="ki-message ki-user">
                <strong>Du:</strong> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ki-message ki-assistant">
                <strong>KI:</strong> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Benutzereingabe
    st.markdown("""
        </div>
        <div class="ki-input-container">
    """, unsafe_allow_html=True)
    
    user_input = st.text_input("Stelle deine Finanzfrage...", key="ki_input", label_visibility="collapsed")
    
    if user_input:
        # Benutzernachricht hinzufügen
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # KI-Antwort generieren
        with st.spinner("KI denkt nach..."):
            time.sleep(1)
            ai_response = get_ai_response(user_input)
            
            # KI-Antwort hinzufügen
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            # Neu rendern
            st.experimental_rerun()
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== HAUPTPROGRAMM =====
def main():
    # KI-Assistent-Button (bei 100px von oben)
    st.markdown("""
    <button class="ki-button" onclick="document.getElementById('ki-panel').style.transform = 'translateX(0)';">
        🤖 KI-Assistent
    </button>
    """, unsafe_allow_html=True)
    
    # Hauptinhalt
    with st.container():
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # Dashboard
        dashboard()
        
        # Sparplan Rechner
        st.markdown("---")
        sparplan_rechner()
        
        # Portfolio Analyse
        st.markdown("---")
        portfolio_analyse()
        
        # Spar-Tipps
        st.markdown("---")
        spar_tipps()
        
        # Investment-Strategien
        st.markdown("---")
        investment_strategien()
        
        # Finanzziele
        st.markdown("---")
        finanzziele()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # KI-Assistent rendern
    ki_assistent()

if __name__ == "__main__":
    main()
