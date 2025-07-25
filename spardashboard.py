import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
from fpdf import FPDF
import math
import random
import time
import openai

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
</style>
"""
st.markdown(DARK_BG, unsafe_allow_html=True)

# ===== KI-FUNKTIONALITÄT =====
def get_ai_response(prompt):
    """Holt eine KI-Antwort von der OpenAI API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du bist ein Finanzberater, der Nutzern bei Investitionen und Sparplänen hilft."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"KI-Fehler: {str(e)}. Bitte versuche es später erneut."

# ===== HAUPTSECTIONEN =====
def wealth_academy():
    """Wealth Academy Sektion mit Lerninhalten"""
    st.header("📚 Wealth Academy")
    st.subheader("Deine interaktive Finanzschule")
    
    with st.expander("💰 Grundlagen der Geldanlage", expanded=False):
        st.markdown("""
        ### Lektion 1: Die Macht des Zinseszinses
        - **Das achte Weltwunder**: Wie kleine Beträge zu großem Vermögen werden
        - **Zeit ist Geld**: Warum du heute beginnen solltest
        - **Praxisbeispiel**: 
            - 100€ monatlich bei 7% Rendite
            - Ergebnis nach 30 Jahren: **122.000€**
        """)
        
        if st.button("Beispiel berechnen", key="calc_interest"):
            capital = 100 * (((1 + 0.07/12)**(12*30) - 1) / (0.07/12))
            st.success(f"Ergebnis: {capital:,.0f}€")
    
    with st.expander("📈 ETF-Strategien für Einsteiger", expanded=False):
        st.markdown("""
        ### Die 3 Säulen der ETF-Strategie
        1. **Diversifikation**: Streuung über Märkte und Sektoren
        2. **Kostenbewusstsein**: TER unter 0.2% anstreben
        3. **Konsistenz**: Monatlich investieren, egal wie der Markt steht
        
        ```python
        # Beispiel-Portfolio
        portfolio = {
            "MSCI World": 60,
            "Emerging Markets": 20,
            "Technologie-ETF": 15,
            "Nachhaltigkeits-ETF": 5
        }
        ```
        """)
    
    with st.expander("🏠 Immobilien vs. Aktien", expanded=False):
        st.markdown("""
        | Parameter          | Immobilien       | Aktien           |
        |--------------------|------------------|------------------|
        | Renditeerwartung   | 3-5% p.a.        | 7-9% p.a.        |
        | Liquidität         | Niedrig          | Hoch             |
        | Mindestinvestment  | Hoch (>50.000€)  | Niedrig (>25€)   |
        | Arbeitsaufwand     | Hoch             | Niedrig          |
        | Diversifikation    | Schwierig        | Einfach          |
        """)
        st.info("💡 Für die meisten Anleger ist eine Kombination aus beiden sinnvoll!")

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
        st.subheader("Dein aktuelles Portfolio")
        etf = st.number_input("ETF-Anteil (%)", 0, 100, 40)
        aktien = st.number_input("Einzelaktien (%)", 0, 100, 20)
        krypto = st.number_input("Krypto (%)", 0, 100, 10)
        immobilien = st.number_input("Immobilien (%)", 0, 100, 20)
        andere = st.number_input("Andere (%)", 0, 100, 10)
        
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
    st.subheader("Optimierungsempfehlungen")
    st.markdown("""
    - **ETF-Anteil erhöhen**: Reduziere Einzelaktien um 5%, erhöhe ETFs auf 50%
    - **Krypto reduzieren**: Maximal 5% für hochriskante Anlagen
    - **Immobilien diversifizieren**: Betrachte REITs statt direkte Investments
    - **Notfallfonds prüfen**: 3-6 Monatsausgaben in liquiden Mitteln
    """)
    
    if st.button("🚀 Portfolio optimieren"):
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
    if st.button("Berechne Vermögensentwicklung"):
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

def main_navigation():
    """Hauptnavigation der App"""
    st.sidebar.title("NEXUS Wealth")
    st.sidebar.image("https://cdn.pixabay.com/photo/2017/01/08/21/37/flame-1964066_1280.png", width=80)
    
    page = st.sidebar.radio("Navigation", [
        "🏠 Dashboard", 
        "🤖 KI-Assistent", 
        "📊 Portfolio Analyse", 
        "💶 Sparplan Rechner",
        "📚 Wealth Academy"
    ])
    
    # Seiteninhalt basierend auf Auswahl
    if page == "🏠 Dashboard":
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
            with st.container(border=True):
                st.markdown("### 🔄 Sparplan optimieren")
                st.progress(65)
                st.caption("Vervollständige deine Sparplan-Einstellungen")
                if st.button("Jetzt optimieren", key="spar_opt"):
                    st.session_state.page = "💶 Sparplan Rechner"
        
        with col2:
            with st.container(border=True):
                st.markdown("### 📚 Finanzwissen erweitern")
                st.progress(30)
                st.caption("Beginne mit Modul 1 in der Wealth Academy")
                if st.button("Jetzt lernen", key="learn"):
                    st.session_state.page = "📚 Wealth Academy"
        
        # Portfolio-Übersicht
        st.subheader("Dein Portfolio")
        portfolio_data = {
            "Asset": ["ETFs", "Aktien", "Krypto", "Immobilien", "Cash"],
            "Anteil (%)": [45, 20, 15, 15, 5],
            "Rendite (%)": [7.2, 4.5, -2.3, 3.8, 0.5]
        }
        st.dataframe(portfolio_data, use_container_width=True)
        
    elif page == "🤖 KI-Assistent":
        ki_assistant()
    elif page == "📊 Portfolio Analyse":
        portfolio_analysis()
    elif page == "💶 Sparplan Rechner":
        sparplan_rechner()
    elif page == "📚 Wealth Academy":
        wealth_academy()

# ===== HAUPTPROGRAMM =====
if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Dashboard"
    
    # API Key für OpenAI (ersetze mit deinem eigenen Schlüssel)
    openai.api_key = st.secrets.get("OPENAI_API_KEY", "dein-api-key-hier")
    
    # Hauptnavigation aufrufen
    main_navigation()
    
    # Footer
    st.divider()
    st.caption("© 2025 NEXUS Wealth GmbH | Finanzielles Wohlbefinden durch intelligente Technologie")
