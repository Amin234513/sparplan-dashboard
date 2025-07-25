import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import math
import random
import time

# ===== KONFIGURATION =====
st.set_page_config(
    page_title="NEXUS Wealth",
    page_icon="💫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== DUNKLER HINTERGRUND =====
DARK_BG = """
<style>
:root {
    --primary: #5e17eb;
    --secondary: #2575fc;
    --accent: #00d2ff;
    --dark-bg: #0a081f;
    --card-bg: rgba(20, 15, 45, 0.85);
    --text-light: #f0f4ff;
}

body {
    background: radial-gradient(circle at 10% 20%, var(--dark-bg) 0%, #050417 100%) !important;
    color: var(--text-light) !important;
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: transparent !important;
}

[data-testid="stHeader"] {
    background-color: rgba(10, 8, 25, 0.7) !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--text-light) !important;
}

.st-bq {
    color: var(--text-light) !important;
}

/* Card Styling */
.card {
    background: var(--card-bg) !important;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(94, 23, 235, 0.4);
}

/* Button Styling */
.stButton>button {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none;
    border-radius: 30px;
    padding: 10px 20px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(94, 23, 235, 0.4);
}

/* Tab Styling */
[data-baseweb="tab-list"] {
    gap: 10px;
}

[data-baseweb="tab"] {
    background: rgba(30, 20, 60, 0.5) !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

[data-baseweb="tab"]:hover {
    background: rgba(94, 23, 235, 0.3) !important;
}

[aria-selected="true"] {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    font-weight: bold !important;
}
</style>
"""
st.markdown(DARK_BG, unsafe_allow_html=True)

# ===== SIMULIERTE KI-FUNKTIONALITÄT =====
def get_ai_response(prompt):
    """Simulierte KI-Antworten für Finanzfragen"""
    time.sleep(1)  # Simuliere Denkzeit
    
    finanzwissen = [
        "Für eine solide Basis empfehle ich: 50% MSCI World ETF, 30% Staatsanleihen, 20% Edelmetalle.",
        "Mit 500€ monatlich: 300€ in einen globalen ETF, 100€ in Technologie-ETFs, 100€ als Notfallreserve.",
        "Dein Portfolio sollte zu deiner Risikotoleranz passen. Für konservative Anleger: 70% Anleihen, 30% Aktien.",
        "Zuerst einen Notfallfonds mit 3 Monatsausgaben aufbauen, dann in kostengünstige ETFs investieren.",
        "Die 50-30-20 Regel: 50% des Einkommens für Bedürfnisse, 30% für Wünsche, 20% zum Sparen und Investieren.",
        "Steuern sparen durch Freistellungsauftrag (aktuell 1000€ pro Jahr) und langfristige Haltefristen nutzen.",
        "Für passives Einkommen: Dividenden-ETFs mit mindestens 3% Ausschüttungsrendite und REITs in Betracht ziehen.",
        "Kosten senken durch Neobroker mit 0€ Ordergebühren und ETFs mit TER unter 0.2%."
    ]
    
    return random.choice(finanzwissen)

# ===== HAUPTSECTIONEN =====
def wealth_academy():
    """Wealth Academy Sektion mit Lerninhalten"""
    st.header("📚 Wealth Academy")
    st.subheader("Deine interaktive Finanzschule")
    
    with st.expander("💰 Grundlagen der Geldanlage", expanded=False):
        st.markdown("""
        <div class="card">
        <h3>Lektion 1: Die Macht des Zinseszinses</h3>
        <p><strong>Das achte Weltwunder</strong>: Wie kleine Beträge zu großem Vermögen werden</p>
        <p><strong>Zeit ist Geld</strong>: Warum du heute beginnen solltest</p>
        <p><strong>Praxisbeispiel</strong>: 100€ monatlich bei 7% Rendite</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Beispiel berechnen", key="calc_interest"):
            capital = 100 * (((1 + 0.07/12)**(12*30) - 1) / (0.07/12))
            st.success(f"Ergebnis nach 30 Jahren: **{capital:,.0f}€**")
    
    with st.expander("📈 ETF-Strategien für Einsteiger", expanded=False):
        st.markdown("""
        <div class="card">
        <h3>Die 3 Säulen der ETF-Strategie</h3>
        <ol>
            <li><strong>Diversifikation</strong>: Streuung über Märkte und Sektoren</li>
            <li><strong>Kostenbewusstsein</strong>: TER unter 0.2% anstreben</li>
            <li><strong>Konsistenz</strong>: Monatlich investieren, egal wie der Markt steht</li>
        </ol>
        <p>Beispiel-Portfolio:</p>
        <ul>
            <li>60% MSCI World ETF</li>
            <li>20% Emerging Markets ETF</li>
            <li>15% Technologie-ETF</li>
            <li>5% Nachhaltigkeits-ETF</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🏠 Immobilien vs. Aktien", expanded=False):
        st.markdown("""
        <div class="card">
        <h3>Vergleich der Anlageklassen</h3>
        <table style="width:100%; border-collapse: collapse; margin-top:15px;">
            <tr style="background: rgba(94, 23, 235, 0.2);">
                <th style="padding:10px; text-align:left;">Parameter</th>
                <th style="padding:10px; text-align:left;">Immobilien</th>
                <th style="padding:10px; text-align:left;">Aktien</th>
            </tr>
            <tr>
                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">Renditeerwartung</td>
                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">3-5% p.a.</td>
                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">7-9% p.a.</td>
            </tr>
            <tr>
                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">Liquidität</td>
                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">Niedrig</td>
                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">Hoch</td>
            </tr>
            <tr>
                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">Mindestinvestment</td>
                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">Hoch (>50.000€)</td>
                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">Niedrig (>25€)</td>
            </tr>
            <tr>
                <td style="padding:10px;">Diversifikation</td>
                <td style="padding:10px;">Schwierig</td>
                <td style="padding:10px;">Einfach</td>
            </tr>
        </table>
        <p style="margin-top:15px;">💡 Für die meisten Anleger ist eine Kombination aus beiden sinnvoll!</p>
        </div>
        """, unsafe_allow_html=True)

def ki_assistant():
    """Interaktiver KI-Vermögensassistent"""
    st.header("🤖 NEXUS KI-Assistent")
    st.subheader("Dein persönlicher Finanzberater 24/7")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chatverlauf anzeigen
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Benutzereingabe
    if prompt := st.chat_input("Stelle deine Finanzfrage..."):
        # Benutzernachricht hinzufügen
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # KI-Antwort generieren
        with st.spinner("KI analysiert deine Frage..."):
            ai_response = get_ai_response(prompt)
            
            # KI-Antwort hinzufügen
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            with st.chat_message("assistant"):
                st.markdown(ai_response)

def portfolio_analysis():
    """Portfolio Analyse und Empfehlungen"""
    st.header("📊 Portfolio Analyse")
    
    # Portfolio-Eingabe
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.subheader("Dein aktuelles Portfolio")
            etf = st.slider("ETF-Anteil (%)", 0, 100, 40)
            aktien = st.slider("Einzelaktien (%)", 0, 100, 20)
            krypto = st.slider("Krypto (%)", 0, 100, 10)
            immobilien = st.slider("Immobilien (%)", 0, 100, 20)
            andere = st.slider("Andere (%)", 0, 100, 10)
            
            # Validierung
            total = etf + aktien + krypto + immobilien + andere
            if total != 100:
                st.error(f"Summe muss 100% betragen! Aktuell: {total}%")
    
    with col2:
        st.subheader("Optimierungsvorschlag")
        
        # Portfolio-Daten
        data = {
            "Assetklasse": ["ETF", "Einzelaktien", "Krypto", "Immobilien", "Andere"],
            "Aktuell": [etf, aktien, krypto, immobilien, andere],
            "Empfohlen": [50, 15, 5, 25, 5]
        }
        
        # Diagramm erstellen
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data["Assetklasse"],
            y=data["Aktuell"],
            name="Aktuell",
            marker_color="#5e17eb"
        ))
        fig.add_trace(go.Bar(
            x=data["Assetklasse"],
            y=data["Empfohlen"],
            name="Empfohlen",
            marker_color="#00d2ff"
        ))
        
        fig.update_layout(
            title="Portfolio-Optimierung",
            barmode="group",
            height=400,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Empfehlungen
    with st.container():
        st.subheader("Optimierungsempfehlungen")
        st.markdown("""
        <div class="card">
        <ul>
            <li><strong>ETF-Anteil erhöhen</strong>: Reduziere Einzelaktien um 5%, erhöhe ETFs auf 50%</li>
            <li><strong>Krypto reduzieren</strong>: Maximal 5% für hochriskante Anlagen</li>
            <li><strong>Immobilien diversifizieren</strong>: Betrachte REITs statt direkte Investments</li>
            <li><strong>Notfallfonds prüfen</strong>: 3-6 Monatsausgaben in liquiden Mitteln</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Portfolio optimieren", use_container_width=True):
            st.success("Optimierung durchgeführt! Dein neues Portfolio wurde gespeichert.")

def sparplan_rechner():
    """Sparplan Rechner mit Visualisierung"""
    st.header("💶 Sparplan Rechner")
    st.subheader("Projiziere deine finanzielle Zukunft")
    
    # Eingabefelder
    col1, col2 = st.columns(2)
    with col1:
        monatlich = st.number_input("Monatliche Sparrate (€)", 50, 5000, 300)
        startkapital = st.number_input("Startkapital (€)", 0, 1000000, 5000)
        zeitraum = st.slider("Anlagezeitraum (Jahre)", 5, 40, 20)
    
    with col2:
        rendite = st.slider("Erwartete Rendite p.a. (%)", 1.0, 15.0, 6.5)
        dynamik = st.slider("Jährliche Sparerhöhung (%)", 0.0, 10.0, 2.0)
        inflation = st.slider("Erwartete Inflation p.a. (%)", 0.0, 10.0, 2.0)
    
    # Berechnung
    if st.button("Berechne Vermögensentwicklung", use_container_width=True):
        with st.spinner("Berechne Projektion..."):
            # Daten für die Darstellung
            jahre = list(range(zeitraum + 1))
            vermoegen = [startkapital]
            inflationsbereinigt = [startkapital]
            sparrate = monatlich * 12
            
            for jahr in range(1, zeitraum + 1):
                # Wertentwicklung
                wertentwicklung = vermoegen[-1] * (1 + rendite/100)
                
                # Sparrate mit Dynamik
                jaehrliche_sparrate = sparrate * (1 + dynamik/100)**(jahr-1)
                
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
                line=dict(color="#00d2ff", width=3)
            ))
            fig.add_trace(go.Scatter(
                x=jahre, 
                y=inflationsbereinigt,
                mode="lines+markers",
                name="Inflationsbereinigt",
                line=dict(color="#5e17eb", width=3)
            ))
            
            fig.update_layout(
                title="Vermögensentwicklung",
                xaxis_title="Jahre",
                yaxis_title="Vermögen (€)",
                hovermode="x unified",
                height=500,
                template="plotly_dark"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Ergebnisse anzeigen
            endvermoegen = vermoegen[-1]
            realwert = inflationsbereinigt[-1]
            
            st.success(f"""
            **Ergebnisse nach {zeitraum} Jahren:**
            - Endvermögen nominal: **{endvermoegen:,.0f}€**
            - Kaufkraft (inflationsbereinigt): **{realwert:,.0f}€**
            - Eingezahlte Sparbeiträge: **{(monatlich * 12 * zeitraum):,.0f}€**
            - Zinseszins-Effekt: **{(endvermoegen - startkapital - (monatlich * 12 * zeitraum)):,.0f}€**
            """)

# ===== DASHBOARD =====
def dashboard():
    """Hauptdashboard mit Finanzübersicht"""
    st.title("💫 NEXUS Wealth Dashboard")
    st.subheader("Dein Weg zur finanziellen Freiheit")
    
    # Kurzstatistiken
    col1, col2, col3 = st.columns(3)
    col1.metric("Prognostiziertes Vermögen", "284.500€", "+23%")
    col2.metric("Sparpotential", "85€/Monat", "Optimiert")
    col3.metric("Portfolio-Performance", "+7.2%", "1. Jahr")
    
    # Aktionskarten
    st.subheader("Deine nächsten Schritte")
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.markdown("""
            <div class="card">
            <h3>🔄 Sparplan optimieren</h3>
            <div class="stProgress">
                <div class="stProgressBar" style="width:65%; background:linear-gradient(90deg, #5e17eb, #2575fc); height:10px; border-radius:5px;"></div>
            </div>
            <p>Vervollständige deine Sparplan-Einstellungen</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Jetzt optimieren", key="spar_opt"):
                st.session_state.page = "💶 Sparplan Rechner"
    
    with col2:
        with st.container():
            st.markdown("""
            <div class="card">
            <h3>📚 Finanzwissen erweitern</h3>
            <div class="stProgress">
                <div class="stProgressBar" style="width:30%; background:linear-gradient(90deg, #5e17eb, #2575fc); height:10px; border-radius:5px;"></div>
            </div>
            <p>Beginne mit Modul 1 in der Wealth Academy</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Jetzt lernen", key="learn"):
                st.session_state.page = "📚 Wealth Academy"
    
    # Portfolio-Übersicht
    st.subheader("Dein Portfolio")
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
        color_discrete_sequence=["#5e17eb", "#2575fc", "#00d2ff", "#9c27b0", "#4caf50"]
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ===== HAUPTPROGRAMM =====
if __name__ == "__main__":
    # Session State initialisieren
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Dashboard"
    
    # Seitenleiste für Navigation
    with st.sidebar:
        st.title("NEXUS Wealth")
        st.image("https://cdn.pixabay.com/photo/2016/08/24/14/29/earth-1617121_1280.png", width=80)
        
        # Navigation
        st.subheader("Navigation")
        page_options = {
            "🏠 Dashboard": dashboard,
            "🤖 KI-Assistent": ki_assistant,
            "📊 Portfolio Analyse": portfolio_analysis,
            "💶 Sparplan Rechner": sparplan_rechner,
            "📚 Wealth Academy": wealth_academy
        }
        
        page = st.radio("", list(page_options.keys()))
        
        # Footer
        st.divider()
        st.caption("© 2025 NEXUS Wealth GmbH")
        st.caption("Finanzielles Wohlbefinden durch intelligente Technologie")
    
    # Aktuelle Seite anzeigen
    if page in page_options:
        page_options[page]()
    else:
        dashboard()
