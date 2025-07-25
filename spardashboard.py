import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import math
import random
import time

# ===== MODERNES DUNKLES DESIGN =====
st.set_page_config(
    page_title="NEXUS Wealth",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS für modernes dunkles Design
DARK_DESIGN = """
<style>
:root {
    --primary: #6a11cb;
    --secondary: #2575fc;
    --accent: #00d2ff;
    --dark-1: #0f0c29;
    --dark-2: #1a1935;
    --dark-3: #24243e;
    --light-text: #e6e6ff;
    --success: #00e676;
    --warning: #ffca28;
    --danger: #ff5252;
}

* {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

body {
    background: linear-gradient(to right, var(--dark-1), var(--dark-2)) !important;
    color: var(--light-text) !important;
}

.stApp {
    background: transparent !important;
}

/* Header Design */
[data-testid="stHeader"] {
    background: rgba(15, 12, 41, 0.9) !important;
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(106, 17, 203, 0.3);
}

/* Sidebar Design */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, var(--dark-2), var(--dark-1)) !important;
    border-right: 1px solid rgba(106, 17, 203, 0.3);
}

/* Card Design */
.card {
    background: linear-gradient(145deg, var(--dark-3), var(--dark-2)) !important;
    border-radius: 16px !important;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(106, 17, 203, 0.2);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 12px 40px rgba(106, 17, 203, 0.4);
    border: 1px solid rgba(106, 17, 203, 0.4);
}

/* Button Design */
.stButton>button {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(106, 17, 203, 0.3);
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 25px rgba(106, 17, 203, 0.5);
}

/* Slider Design */
.stSlider .st-ae {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
}

.stSlider .st-af {
    background: var(--dark-3) !important;
}

/* Progress Bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
}

/* Tabs */
[data-baseweb="tab-list"] {
    gap: 8px;
}

[data-baseweb="tab"] {
    background: var(--dark-3) !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
}

[data-baseweb="tab"]:hover {
    background: rgba(106, 17, 203, 0.3) !important;
}

[aria-selected="true"] {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    font-weight: 600 !important;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, rgba(106, 17, 203, 0.25), rgba(37, 117, 252, 0.25)) !important;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(106, 17, 203, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(106, 17, 203, 0.3);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--accent), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.metric-label {
    font-size: 1.1rem;
    opacity: 0.85;
}

/* Floating Animation */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
}

.floating {
    animation: float 6s ease-in-out infinite;
}
</style>
"""
st.markdown(DARK_DESIGN, unsafe_allow_html=True)

# ===== SIMULIERTE KI-FUNKTIONALITÄT =====
def get_ai_response(prompt):
    """Simulierte KI-Antworten für Finanzfragen mit mehr Details"""
    time.sleep(1.5)  # Simuliere Denkzeit
    
    finanzwissen = [
        f"Für deine Situation empfehle ich: 60% MSCI World ETF (ISIN: IE00B4L5Y983), 20% Emerging Markets (ISIN: IE00BKM4GZ66), 15% Technologie-ETF (ISIN: IE00BYVQBR96), und 5% Krypto via ETC. Monatliche Sparrate: {random.randint(200, 800)}€.",
        f"Optimale Sparplan-Aufteilung: {random.randint(40, 60)}% in einen globalen ETF, {random.randint(10, 20)}% in Immobilien-REITs, {random.randint(5, 15)}% in Anleihen, und {random.randint(5, 15)}% in Einzelaktien. Vergiss nicht deinen Notfallfonds!",
        f"Dein Portfolio sollte zu deiner Risikotoleranz passen. Für moderate Anleger: {random.randint(50, 70)}% Aktien-ETFs, {random.randint(20, 30)}% Anleihen, {random.randint(5, 10)}% Edelmetalle, und {random.randint(5, 10)}% Krypto.",
        f"Zuerst einen Notfallfonds mit 3-6 Monatsausgaben aufbauen. Dann investieren: {random.randint(300, 700)}€ monatlich in ETFs. Top-ETFs: iShares Core MSCI World (ISIN: IE00B4L5Y983), Vanguard FTSE All-World (ISIN: IE00B3RBWM25).",
        f"Steuern sparen: Nutze deinen Freistellungsauftrag (1000€ pro Jahr) und halte Investments >1 Jahr für Steuerfreiheit. ETFs mit thesaurierend > ausschüttend für langfristiges Wachstum.",
        f"Für passives Einkommen: Dividenden-ETFs mit 3-5% Ausschüttung (z.B. ISIN: IE00B8GKDB10), REITs mit 4-7% Dividende, und Anleihen-ETFs. Ziel: {random.randint(500, 2000)}€ monatliches passives Einkommen.",
        f"Kosten senken: Nutze Neobroker wie Trade Republic (1€/Sparplan), wähle ETFs mit TER <0.2%, und vermeide aktiv gemanagte Fonds. Jährliche Ersparnis: {random.randint(50, 300)}€.",
        f"Rendite-Boost: Erhöhe deine Sparrate jährlich um {random.randint(3, 10)}%, reinvestiere Dividenden, und nutze Marktdips für Nachkäufe. Potenzieller Renditegewinn: +{random.randint(1, 3)}% p.a."
    ]
    
    return random.choice(finanzwissen)

# ===== DASHBOARD =====
def dashboard():
    """Hauptdashboard mit Finanzübersicht"""
    st.title("💎 NEXUS Wealth")
    st.subheader("Dein intelligenter Weg zur finanziellen Freiheit")
    
    # Kurzstatistiken
    col1, col2, col3 = st.columns(3)
    col1.markdown("""
    <div class="metric-card floating">
        <div class="metric-value">284.500€</div>
        <div class="metric-label">Prognostiziertes Vermögen</div>
        <div style="color: var(--success); font-weight:600;">+23%</div>
    </div>
    """, unsafe_allow_html=True)
    
    col2.markdown("""
    <div class="metric-card floating" style="animation-delay:0.3s">
        <div class="metric-value">85€/Monat</div>
        <div class="metric-label">Sparpotential</div>
        <div style="color: var(--accent); font-weight:600;">Optimiert</div>
    </div>
    """, unsafe_allow_html=True)
    
    col3.markdown("""
    <div class="metric-card floating" style="animation-delay:0.6s">
        <div class="metric-value">7.2%</div>
        <div class="metric-label">Portfolio-Performance</div>
        <div style="color: var(--success); font-weight:600;">1. Jahr</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sparplan-Optimierung
    st.subheader("💸 Sparplan Optimierung")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("### Aktuelle Sparrate")
        current_rate = st.number_input("Monatliche Sparrate (€)", 50, 5000, 300, key="current_rate")
        
        st.markdown("### Ziel-Vermögen")
        target_wealth = st.number_input("Zielbetrag (€)", 10000, 5000000, 250000, key="target_wealth")
    
    with col2:
        # Vermögensentwicklung
        years = st.slider("Zeithorizont (Jahre)", 5, 40, 15)
        return_rate = st.slider("Erwartete Rendite p.a. (%)", 1.0, 15.0, 6.8, 0.1)
        
        # Berechnung
        monthly_return = return_rate / 100 / 12
        months = years * 12
        future_value = current_rate * (((1 + monthly_return)**months - 1) / monthly_return)
        
        # Diagramm
        growth = []
        for year in range(years + 1):
            months = year * 12
            value = current_rate * (((1 + monthly_return)**months - 1) / monthly_return)
            growth.append(value)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(years + 1)),
            y=growth,
            mode="lines+markers",
            name="Prognose",
            line=dict(color="#00d2ff", width=4),
            hovertemplate="Jahr %{x}: %{y:,.0f}€"
        ))
        fig.add_hline(y=target_wealth, line_dash="dash", line_color="#ffca28", 
                      annotation_text="Zielvermögen", annotation_position="bottom right")
        
        fig.update_layout(
            title="Vermögensentwicklung",
            xaxis_title="Jahre",
            yaxis_title="Vermögen (€)",
            template="plotly_dark",
            height=400,
            margin=dict(l=0, r=0, b=0, t=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("### Optimierungsvorschlag")
        optimized_rate = math.ceil(target_wealth / (((1 + monthly_return)**months - 1) / monthly_return))
        difference = optimized_rate - current_rate
        
        st.markdown(f"""
        <div class="card">
            <h4>🚀 Empfohlene Sparrate</h4>
            <div style="font-size:2.5rem; font-weight:700; color:#00d2ff; text-align:center; margin:10px 0;">
                {optimized_rate:,.0f}€
            </div>
            <p style="text-align:center; font-size:1.1rem;">
                {f"+{difference:,.0f}€" if difference > 0 else "Keine Änderung"}
            </p>
            
            <h4>📅 Erreichbares Ziel in</h4>
            <div style="font-size:2rem; font-weight:700; color:#00d2ff; text-align:center; margin:10px 0;">
                {years} Jahren
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sparplan optimieren", key="optimize_plan"):
            st.success(f"Sparplan auf {optimized_rate}€ monatlich aktualisiert!")
    
    # Portfolio-Übersicht
    st.subheader("📊 Portfolio Analyse")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Aktuelle Verteilung")
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
        # Portfolio-Daten
        data = {
            "Assetklasse": ["ETFs", "Aktien", "Krypto", "Immobilien", "Andere"],
            "Aktuell": [etf, aktien, krypto, immobilien, andere],
            "Empfohlen": [50, 15, 5, 25, 5]
        }
        
        # Diagramm
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data["Assetklasse"],
            y=data["Aktuell"],
            name="Aktuell",
            marker_color="#6a11cb"
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
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Empfehlungen
        st.markdown("""
        <div class="card">
            <h4>📈 Optimierungsempfehlungen</h4>
            <ul>
                <li>ETF-Anteil auf 50% erhöhen</li>
                <li>Krypto auf max. 5% reduzieren</li>
                <li>Immobilien-Exposure durch REITs erhöhen</li>
                <li>Notfallfonds prüfen (3-6 Monatsausgaben)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ===== KI-ASSISTENT =====
def ki_assistant():
    """Interaktiver KI-Vermögensassistent"""
    st.title("🤖 NEXUS KI-Assistent")
    st.subheader("Dein persönlicher Finanzberater 24/7")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Beispiel-Fragen
    st.markdown("""
    <div class="card">
        <h4>💡 Beispielfragen:</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
            <div style="background: rgba(106, 17, 203, 0.3); border-radius: 12px; padding: 8px 12px; cursor: pointer;"
                 onclick="document.querySelector('input[aria-label=\\'Stelle deine Finanzfrage...\\']').value = 'Wie mit 500€ monatlich starten?';">
                Wie mit 500€ monatlich starten?
            </div>
            <div style="background: rgba(106, 17, 203, 0.3); border-radius: 12px; padding: 8px 12px; cursor: pointer;"
                 onclick="document.querySelector('input[aria-label=\\'Stelle deine Finanzfrage...\\']').value = 'Welche ETFs sind jetzt am besten?';">
                Welche ETFs sind jetzt am besten?
            </div>
            <div style="background: rgba(106, 17, 203, 0.3); border-radius: 12px; padding: 8px 12px; cursor: pointer;"
                 onclick="document.querySelector('input[aria-label=\\'Stelle deine Finanzfrage...\\']').value = 'Wie erreiche ich 100.000€?';">
                Wie erreiche ich 100.000€?
            </div>
            <div style="background: rgba(106, 17, 203, 0.3); border-radius: 12px; padding: 8px 12px; cursor: pointer;"
                 onclick="document.querySelector('input[aria-label=\\'Stelle deine Finanzfrage...\\']').value = 'Wie optimiere ich mein Portfolio?';">
                Wie optimiere ich mein Portfolio?
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chatverlauf
    chat_container = st.container()
    
    # Benutzereingabe
    if prompt := st.chat_input("Stelle deine Finanzfrage..."):
        # Benutzernachricht hinzufügen
        st.session_state.chat_history.append({
            "role": "user", 
            "content": prompt,
            "time": datetime.now().strftime("%H:%M")
        })
        
        # KI-Antwort generieren
        with st.spinner("KI analysiert deine Frage..."):
            ai_response = get_ai_response(prompt)
            
            # KI-Antwort hinzufügen
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": ai_response,
                "time": datetime.now().strftime("%H:%M")
            })
    
    # Chatverlauf anzeigen
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
                    st.caption(f"Du - {msg['time']}")
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])
                    st.caption(f"NEXUS KI - {msg['time']}")

# ===== SPAR-TIPPS =====
def spar_tipps():
    """Intelligente Spartipps mit personalisierten Empfehlungen"""
    st.title("💡 Intelligente Spartipps")
    st.subheader("Maximiere dein Sparpotential in allen Lebensbereichen")
    
    # Kategorien
    categories = {
        "🏠 Haushalt": [
            "Smart Thermostat installieren - spart bis zu 15% Heizkosten",
            "LED-Beleuchtung komplett umstellen - 80% weniger Stromverbrauch",
            "Wassersparende Duschköpfe nutzen - reduziert Verbrauch um 40%",
            "Energieeffiziente Geräte der Klasse A+++ kaufen",
            "Stromfresser identifizieren mit Energiemonitor"
        ],
        "🛒 Einkaufen": [
            "Cashback-Apps wie Shoop nutzen - bis zu 10% zurück",
            "Preisvergleichs-Tools vor jedem Kauf verwenden",
            "Saisonal und regional einkaufen - 30% günstiger",
            "Großpackungen bei häufig genutzten Produkten",
            "Einkaufslisten strikt einhalten - reduziert Impulskäufe"
        ],
        "💰 Finanzen": [
            "Bankgebühren vergleichen und wechseln - bis zu 100€/Jahr sparen",
            "Kreditkarten mit Cashback nutzen",
            "Versicherungen jährlich prüfen und optimieren",
            "Steuererklärung machen - durchschnittlich 1.000€ Rückerstattung",
            "Automatische Sparpläne einrichten - Pay yourself first"
        ],
        "📈 Investitionen": [
            "Kostenlose Sparpläne bei Neobrokern nutzen",
            "Steuerfreistellungsauftrag optimal ausnutzen",
            "ETF-Portfolio mit max. 0.2% TER zusammenstellen",
            "Regelmäßiges Rebalancing - 1x jährlich",
            "Dividendenstrategie für passives Einkommen"
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
                    <div style="display: flex; align-items: start; gap: 15px;">
                        <div style="font-size: 2rem; background: linear-gradient(90deg, var(--primary), var(--accent));
                             -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                            {i+1}
                        </div>
                        <div>
                            <h4 style="margin-top: 0;">{tip.split(" - ")[0]}</h4>
                            <p>{tip.split(" - ")[1] if " - " in tip else ""}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Personalisierte Empfehlung
    st.markdown("""
    <div class="card">
        <h3>⭐ Personalisierte Empfehlung</h3>
        <div style="display: flex; align-items: center; gap: 20px; padding: 15px; background: rgba(106, 17, 203, 0.2); border-radius: 12px;">
            <div style="font-size: 3rem;">💡</div>
            <div>
                <h4 style="margin: 0;">Basierend auf deinem Profil</h4>
                <p style="margin: 5px 0 0 0; font-size: 1.1rem;">
                    Du könntest 
                    <span style="color: var(--accent); font-weight: 600;">{random.randint(50, 150)}€ pro Monat</span> 
                    sparen durch:
                </p>
                <ul>
                    <li>{random.choice(["Bankwechsel", "Energieoptimierung", "Versicherungscheck", "Abokündigungen"])}</li>
                    <li>{random.choice(["Steueroptimierung", "Cashback-Nutzung", "Großeinkäufe"])}</li>
                </ul>
            </div>
        </div>
        <div style="text-align: center; margin-top: 15px;">
            <button style="background: linear-gradient(90deg, var(--primary), var(--accent));
                        color: white; border: none; border-radius: 50px; padding: 12px 28px;
                        font-weight: 600; font-size: 1.05rem; cursor: pointer;">
                Sparplan optimieren
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== WEALTH ACADEMY =====
def wealth_academy():
    """Interaktive Finanzbildung"""
    st.title("📚 Wealth Academy")
    st.subheader("Baue dein Finanzwissen auf - Schritt für Schritt")
    
    # Module
    modules = [
        {
            "title": "💰 Grundlagen der Geldanlage",
            "level": "Anfänger",
            "progress": 35,
            "icon": "💰",
            "content": """
            ### Lektion 1: Die Macht des Zinseszinses
            - **Das achte Weltwunder**: Wie kleine Beträge zu großem Vermögen werden
            - **Zeit ist Geld**: Warum du heute beginnen solltest
            - **Praxisbeispiel**: 
                - 100€ monatlich bei 7% Rendite
                - Ergebnis nach 30 Jahren: **122.000€**
            
            **Interaktive Aufgabe:**
            Berechne, wie viel 150€ monatlich bei 6% Rendite in 25 Jahren werden.
            """
        },
        {
            "title": "📈 ETF-Strategien",
            "level": "Mittel",
            "progress": 20,
            "icon": "📈",
            "content": """
            ### Die 3 Säulen der ETF-Strategie
            1. **Diversifikation**: Streuung über Märkte und Sektoren
            2. **Kostenbewusstsein**: TER unter 0.2% anstreben
            3. **Konsistenz**: Monatlich investieren, egal wie der Markt steht
            
            **Top-ETFs 2024:**
            - MSCI World (ISIN: IE00B4L5Y983)
            - NASDAQ-100 (ISIN: IE00B53SZB19)
            - Global Clean Energy (ISIN: IE00B1XNHC34)
            """
        },
        {
            "title": "🏠 Immobilien vs. Aktien",
            "level": "Mittel",
            "progress": 10,
            "icon": "🏠",
            "content": """
            | Parameter          | Immobilien       | Aktien           |
            |--------------------|------------------|------------------|
            | Renditeerwartung   | 3-5% p.a.        | 7-9% p.a.        |
            | Liquidität         | Niedrig          | Hoch             |
            | Mindestinvestment  | Hoch (>50.000€)  | Niedrig (>25€)   |
            | Arbeitsaufwand     | Hoch             | Niedrig          |
            | Diversifikation    | Schwierig        | Einfach          |
            
            💡 Für die meisten Anleger ist eine Kombination aus beiden sinnvoll!
            """
        }
    ]
    
    # Module anzeigen
    for module in modules:
        with st.expander(f"{module['icon']} {module['title']} - {module['level']} - {module['progress']}% abgeschlossen", expanded=False):
            st.markdown(f"<div class='card'>{module['content']}</div>", unsafe_allow_html=True)
            
            if "Berechne" in module["content"]:
                col1, col2 = st.columns([1, 3])
                with col1:
                    capital = st.number_input("Monatliche Sparrate (€)", 50, 2000, 150, key=f"capital_{module['title']}")
                    years = st.slider("Jahre", 5, 40, 25, key=f"years_{module['title']}")
                    rate = st.slider("Rendite p.a. (%)", 1.0, 15.0, 6.0, 0.1, key=f"rate_{module['title']}")
                
                if st.button("Berechnen", key=f"btn_{module['title']}"):
                    monthly_rate = rate / 100 / 12
                    months = years * 12
                    result = capital * (((1 + monthly_rate)**months - 1) / monthly_rate)
                    st.success(f"Ergebnis nach {years} Jahren: **{result:,.0f}€**")

# ===== SIDEBAR NAVIGATION =====
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="background: linear-gradient(90deg, var(--accent), var(--secondary));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 5px;">NEXUS</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Wealth Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page_options = {
        "📊 Dashboard": dashboard,
        "🤖 KI-Assistent": ki_assistant,
        "💡 Spar-Tipps": spar_tipps,
        "📚 Wealth Academy": wealth_academy
    }
    
    page = st.radio("Navigation", list(page_options.keys()))
    
    # Fortschrittsbalken
    st.divider()
    st.markdown("### Dein Fortschritt")
    st.markdown("Finanzielle Freiheit")
    st.progress(65)
    st.caption("65% erreicht")
    
    # Community
    st.divider()
    st.markdown("### Community")
    col1, col2 = st.columns(2)
    col1.metric("Mitglieder", "12.458")
    col2.metric("Aktive", "3.892")
    
    # Footer
    st.divider()
    st.caption("© 2025 NEXUS Wealth GmbH")
    st.caption("Dein Weg zur finanziellen Freiheit")

# ===== HAUPTPROGRAMM =====
if __name__ == "__main__":
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Aktuelle Seite anzeigen
    if page in page_options:
        page_options[page]()
