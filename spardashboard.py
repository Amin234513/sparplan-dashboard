import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
from fpdf import FPDF
import tempfile
import math

# ===== MODERNES DESIGN MIT VERLAUF =====
st.set_page_config(
    page_title="FIREFLY Finance",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
:root {
    --primary: #6a11cb;
    --secondary: #2575fc;
    --accent: #00d2ff;
    --dark-bg: #0f0c29;
    --card-bg: rgba(26, 21, 57, 0.8);
    --text-light: #e2e8f0;
    --success: #00c853;
    --warning: #ffab00;
    --error: #ff1744;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

body {
    background: linear-gradient(135deg, var(--dark-bg), #24243e, #000000) fixed;
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    color: var(--text-light);
    line-height: 1.6;
    padding: 0;
    overflow-x: hidden;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

h1, h2, h3, h4, h5, h6 {
    background: linear-gradient(90deg, var(--accent), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
}

.stApp {
    background: transparent !important;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0;
}

.main-container {
    padding: 2rem;
    margin-top: 0;
}

.header-section {
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    padding: 3rem 2rem;
    border-radius: 0 0 20px 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}

.header-section::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    z-index: 0;
}

.header-content {
    position: relative;
    z-index: 1;
}

.st-emotion-cache-1y4p8pa {
    background: var(--card-bg) !important;
    backdrop-filter: blur(10px);
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
    margin-bottom: 2rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.st-emotion-cache-1y4p8pa:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(106, 17, 203, 0.3);
}

.stButton button {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    margin-top: 0.5rem;
    border: none;
}

.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(106, 17, 203, 0.5);
}

.card {
    background: rgba(38, 33, 75, 0.6);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    background: rgba(46, 41, 90, 0.8);
    box-shadow: 0 8px 25px rgba(0, 210, 255, 0.3);
}

.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent), var(--secondary)) !important;
}

.section {
    margin-bottom: 3rem;
    padding: 2rem;
    border-radius: 16px;
    background: rgba(15, 12, 41, 0.7);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
}

.tip-card {
    background: rgba(10, 80, 150, 0.3);
    border-left: 4px solid var(--accent);
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 8px;
    transition: transform 0.2s ease;
}

.tip-card:hover {
    transform: translateX(5px);
    background: rgba(10, 80, 150, 0.4);
}

.footer {
    text-align: center;
    padding: 3rem 1rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    background: rgba(10, 8, 25, 0.8);
    border-radius: 16px 16px 0 0;
}

.feature-card {
    background: rgba(26, 21, 57, 0.7);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
}

.feature-card:hover {
    transform: translateY(-10px);
    background: rgba(38, 33, 75, 0.9);
    box-shadow: 0 10px 25px rgba(0, 210, 255, 0.2);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    background: linear-gradient(90deg, var(--accent), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stats-container {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    margin: 2rem 0;
}

.stat-card {
    background: rgba(26, 21, 57, 0.6);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    min-width: 200px;
    margin: 0.5rem;
    flex: 1;
}

.stat-value {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--accent), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 1rem;
    opacity: 0.8;
}

.testimonial {
    background: rgba(26, 21, 57, 0.6);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 4px solid var(--accent);
}

.testimonial-text {
    font-style: italic;
    margin-bottom: 1rem;
}

.testimonial-author {
    text-align: right;
    font-weight: bold;
    opacity: 0.9;
}

.cta-button {
    display: block;
    width: 100%;
    padding: 1rem;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    color: white !important;
    text-align: center;
    border-radius: 12px;
    font-weight: bold;
    font-size: 1.2rem;
    margin: 2rem 0;
    transition: all 0.3s ease;
    text-decoration: none !important;
}

.cta-button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 30px rgba(106, 17, 203, 0.6);
}

.pricing-card {
    background: rgba(26, 21, 57, 0.7);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin: 1rem;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.pricing-card.featured {
    transform: scale(1.05);
    border: 2px solid var(--accent);
    background: rgba(38, 33, 75, 0.8);
    z-index: 2;
}

.pricing-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}

.pricing-header {
    margin-bottom: 1.5rem;
}

.pricing-price {
    font-size: 3rem;
    font-weight: 800;
    margin: 1rem 0;
    background: linear-gradient(90deg, var(--accent), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.pricing-features {
    list-style: none;
    padding: 0;
    margin: 1.5rem 0;
    text-align: left;
}

.pricing-features li {
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.pricing-features li:last-child {
    border-bottom: none;
}

.pricing-features li::before {
    content: "✓";
    color: var(--accent);
    margin-right: 0.5rem;
    font-weight: bold;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(38, 33, 75, 0.6) !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    color: white !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(106, 17, 203, 0.4) !important;
}

.stSelectbox, .stNumberInput, .stTextInput, .stDateInput, .stSlider {
    background: rgba(38, 33, 75, 0.6) !important;
    border-radius: 12px !important;
    padding: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

.stMarkdown h1 {
    font-size: 3rem !important;
    margin-top: 0 !important;
}

.stMarkdown h2 {
    font-size: 2rem !important;
    margin-top: 1rem !important;
}

.stMarkdown h3 {
    font-size: 1.5rem !important;
}

.stMetric {
    background: rgba(38, 33, 75, 0.6) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* Responsive Design */
@media (max-width: 768px) {
    .stApp {
        padding: 0.5rem;
    }
    .section {
        padding: 1rem;
    }
    .stats-container {
        flex-direction: column;
    }
}
</style>
""", unsafe_allow_html=True)

# ===== E-BOOK GENERATOR =====
def generate_ebook():
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'FIREFLY Premium Sparguide', 0, 1, 'C')
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Seite {self.page_no()}', 0, 0, 'C')
            
        def chapter_title(self, title):
            self.set_font('Arial', 'B', 16)
            self.set_fill_color(106, 17, 203)
            self.cell(0, 10, title, 0, 1, 'L', 1)
            self.ln(5)
            
        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 8, body)
            self.ln()

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Titel
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 10, "🔥 FIREFLY Sparstrategie", 0, 1, 'C')
    pdf.ln(10)
    
    # Inhaltsverzeichnis
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "Inhaltsverzeichnis", 0, 1)
    chapters = [
        ("Die 7 Säulen der Vermögensbildung", 1),
        ("Automatisierte Sparsysteme", 2),
        ("Steuertricks für Sparer", 3),
        ("ETF-Strategien 2025", 4),
        ("Krisensicher investieren", 5),
        ("Finanzielle Freiheit erreichen", 6),
        ("50 Spartipps für den Alltag", 7)
    ]
    
    for title, page in chapters:
        pdf.cell(0, 10, f"{title} ......................... {page}", 0, 1)
    
    # Kapitel
    content = {
        "Die 7 Säulen der Vermögensbildung": """
1. Notfallfonds aufbauen (3-6 Monatsausgaben)
2. Schulden eliminieren (Priorität: hohe Zinsen)
3. Steuereffizient investieren (Freibetrag nutzen)
4. Automatisierte Sparpläne (Pay yourself first)
5. Immobilien vs. Aktien: Die optimale Mischung
6. Passive Einkommensströme entwickeln
7. Regelmäßiges Portfolio-Rebalancing
        """,
        
        "Automatisierte Sparsysteme": """
**Drei-Stufen-Sparplan:**
- Stufe 1: 50% in globale ETFs (MSCI World, EM)
- Stufe 2: 30% in thematische ETFs (Tech, Nachhaltigkeit)
- Stufe 3: 20% in Einzelaktien & Krypto

**Automatisierungstools:**
- Broker: Sparpläne mit dynamischer Anpassung
- Apps: Finanzguru, Finanzfluss, Trade Republic
- Banken: DKB, ING, Comdirect mit kostenlosen Sparplänen
        """,
        
        "Steuertricks für Sparer": """
**Strategien:**
- Freistellungsauftrag optimal ausnutzen (2025: 1.000€ pro Person)
- Verluste realisieren für Steuerstundung (Tax-Loss-Harvesting)
- Kapitalerträge in Niedrigzinsphasen realisieren
- Ausländische Quellensteuer zurückfordern

**Rechtliche Rahmen:**
- 25% Abgeltungssteuer + Soli + Kirchensteuer
- Günstigerprüfung bei niedrigem Einkommen
- Fonds mit hoher Teilfreistellung (Aktienfonds: 30%)
        """,
        
        "ETF-Strategien 2025": """
**Top-5-ETF-Picks:**
1. iShares Core MSCI World (Acc) - ISIN: IE00B4L5Y983
2. Xtrackers MSCI World ESG (Acc) - ISIN: IE00BZ02LR44
3. Amundi Nasdaq 100 (Acc) - ISIN: LU1829221024
4. Lyxor Core STOXX Europe 600 (DR) - ISIN: LU0908500753
5. iShares MSCI EM IMI (Acc) - ISIN: IE00BKM4GZ66

**Allokationsmodell:**
- 60% Industrieländer
- 20% Schwellenländer
- 15% Technologie-Sektor
- 5% Small Caps
        """,
        
        "Krisensicher investieren": """
**Schutzstrategien:**
- Gold-Allokation (5-10% des Portfolios)
- REITs mit stabilen Mieteinnahmen
- Konsumgüter-Aktien (Unilever, Procter & Gamble)
- Kurzlaufende Anleihen als Puffer

**Risikomanagement:**
- Stopp-Loss bei 15% unter Kaufpreis
- Portfolio-Insurance mit Put-Optionen
- Dynamische Asset-Allokation (Gleitpfad)
        """,
        
        "Finanzielle Freiheit erreichen": """
**FIRE-Formel:**
Vermögen = Jahresausgaben × 25
- Beispiel: 40.000€ Ausgaben → 1.000.000€ Ziel

**Stufenplan:**
1. Sparrate auf 50% erhöhen
2. Nebeneinkommen entwickeln
3. Steuern optimieren
4. Wohnkosten reduzieren
5. Investitionsquote erhöhen

**Entnahmestrategien:**
- 4%-Regel mit jährlicher Anpassung
- Dynamische Entnahme (CAPE-basiert)
- Bucket-Strategie (3-Eimer-Modell)
        """,
        
        "50 Spartipps für den Alltag": """
**Haushalt:**
1. Stromfresser identifizieren und ersetzen
2. Wasser sparen mit Durchflussbegrenzern
3. Heizkosten durch smartes Thermostat senken
4. Lebensmittelverschwendung reduzieren
5. Reparieren statt neu kaufen

**Einkaufen:**
6. Mit Einkaufsliste planen
7. Cashback-Apps nutzen
8. Saisonal und regional einkaufen
9. Großpackungen bei häufig genutzten Produkten
10. Preise mit Apps vergleichen

**Finanzen:**
11. Bankgebühren vergleichen
12. Kündigung unnötiger Abos
13. Versicherungen optimieren
14. Steuererklärung machen
15. Automatische Sparpläne einrichten
        """
    }
    
    for title, text in content.items():
        pdf.add_page()
        pdf.chapter_title(title)
        pdf.chapter_body(text)
    
    # Cover-Design
    pdf.add_page()
    pdf.set_fill_color(106, 17, 203)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 36)
    pdf.text(40, 120, "🔥 FIREFLY")
    pdf.set_font('Arial', '', 24)
    pdf.text(30, 140, "Der Premium-Sparguide für finanzielle Freiheit")
    pdf.set_font('Arial', '', 16)
    pdf.text(70, 260, "© 2025 FIREFLY Finance - Alle Rechte vorbehalten")
    
    return pdf

# ===== HAUPTSEKTIONEN =====
def header_section():
    with st.container():
        st.markdown("""
        <div class="header-section">
            <div class="header-content">
                <h1>🔥 FIREFLY Finance</h1>
                <h2>Ihr Weg zur finanziellen Freiheit</h2>
                <p style="font-size:1.2rem; max-width:800px; margin:1rem 0 2rem 0;">
                    Die intelligente Plattform für Vermögensaufbau und Sparplanung. 
                    Mit KI-gestützten Prognosen, automatischem Portfolio-Management 
                    und persönlichen Sparstrategien.
                </p>
                
                <div class="stats-container">
                    <div class="stat-card">
                        <div class="stat-value">23%</div>
                        <div class="stat-label">Mehr Sparpotential</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">10.000+</div>
                        <div class="stat-label">Zufriedene Nutzer</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">97%</div>
                        <div class="stat-label">Erfolgsquote</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def features_section():
    st.header("🚀 Unsere Leistungen")
    st.markdown("Alles, was Sie für Ihren finanziellen Erfolg brauchen, in einer Plattform")
    
    cols = st.columns(3)
    features = [
        {"icon": "📈", "title": "Sparplan-Simulation", "desc": "Erstellen Sie maßgeschneiderte Sparpläne mit präzisen Prognosen"},
        {"icon": "🎯", "title": "Zielplanung", "desc": "Definieren und verfolgen Sie Ihre finanziellen Meilensteine"},
        {"icon": "💡", "title": "Spartipps", "desc": "Über 100 praktische Tipps zum Geld sparen im Alltag"},
        {"icon": "📊", "title": "Portfolio-Analyse", "desc": "Optimieren Sie Ihre Anlagestrategie mit KI-gestützten Analysen"},
        {"icon": "🛡️", "title": "Risikomanagement", "desc": "Schützen Sie Ihr Vermögen mit intelligenten Absicherungsstrategien"},
        {"icon": "📚", "title": "Premium-Wissen", "desc": "Exklusive Guides und Schulungen für finanzielle Freiheit"}
    ]
    
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature['icon']}</div>
                <h3>{feature['title']}</h3>
                <p>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def goals_section():
    with st.container():
        st.header("🎯 Sparziel-Planung")
        st.markdown("Definieren und verfolgen Sie Ihre finanziellen Meilensteine")
        
        with st.expander("➕ Neues Sparziel hinzufügen", expanded=False):
            with st.form("goal_form"):
                col1, col2 = st.columns(2)
                with col1:
                    goal_name = st.text_input("Zielname*", "z.B. Eigenheim, Altersvorsorge")
                    target_amount = st.number_input("Zielbetrag (€)*", 1000, 1000000, 50000)
                    priority = st.select_slider("Priorität", ["Niedrig", "Mittel", "Hoch", "Sehr hoch"])
                    
                with col2:
                    deadline = st.date_input("Zieldatum*", datetime.now() + timedelta(days=365*5))
                    current_amount = st.number_input("Aktueller Stand (€)", 0, 1000000, 5000)
                    recurring_payment = st.number_input("Monatliche Sparrate (€)", 0, 5000, 500)
                    
                if st.form_submit_button("Ziel speichern"):
                    st.success("Sparziel erfolgreich angelegt!")
        
        # Sparziel-Visualisierung
        st.subheader("🚀 Aktive Sparziele")
        goals = [
            {"name": "Notfallfonds", "target": 20000, "current": 15000, "deadline": "2024-12-31"},
            {"name": "Weltreise", "target": 15000, "current": 5000, "deadline": "2025-06-30"},
            {"name": "Altersvorsorge", "target": 500000, "current": 29500, "deadline": "2040-01-01"}
        ]
        
        for goal in goals:
            progress = goal['current'] / goal['target']
            days_left = (datetime.strptime(goal['deadline'], "%Y-%m-%d") - datetime.now()).days
            
            with st.container():
                st.markdown(f"### {goal['name']}")
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Zielbetrag", f"{goal['target']:,.0f}€")
                    st.metric("Aktuell", f"{goal['current']:,.0f}€")
                    st.metric("Verbleibend", f"{goal['target'] - goal['current']:,.0f}€")
                    
                with col2:
                    st.markdown(f"**Fortschritt** ({progress*100:.1f}%)")
                    st.progress(min(1.0, progress))
                    
                    st.markdown(f"**Zeitplan** ({days_left} Tage verbleibend)")
                    years_left = days_left / 365
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = years_left,
                        number = {'suffix': " Jahre"},
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Verbleibende Zeit"},
                        gauge = {
                            'axis': {'range': [0, max(10, years_left+2)]},
                            'bar': {'color': "#6a11cb"},
                            'steps': [
                                {'range': [0, max(10, years_left+2)*0.5], 'color': "lightgray"},
                                {'range': [max(10, years_left+2)*0.5, max(10, years_left+2)], 'color': "gray"}],
                        }
                    ))
                    fig.update_layout(height=200, margin=dict(l=0, r=0, b=0, t=30))
                    st.plotly_chart(fig, use_container_width=True)

def simulation_section():
    with st.container():
        st.header("📈 Sparplan-Simulation")
        st.markdown("Erstellen Sie eine maßgeschneiderte Sparstrategie mit präzisen Prognosen")
        
        col1, col2 = st.columns(2)
        with col1:
            startkapital = st.number_input("Startkapital (€)", 0, 1000000, 5000)
            monatlicher_sparbetrag = st.number_input("Monatliche Sparrate (€)", 50, 5000, 300)
            jahresrendite = st.slider("Erwartete Rendite p.a. (%)", 1.0, 15.0, 6.5, 0.5)
            simulationsdauer = st.slider("Simulationsdauer (Jahre)", 5, 40, 15)
            inflationsrate = st.slider("Erwartete Inflation p.a. (%)", 0.5, 10.0, 2.0, 0.5)
        
        with col2:
            st.subheader("Prognoseergebnisse")
            monatsrendite = jahresrendite / 100 / 12
            monate = simulationsdauer * 12
            guthaben = startkapital
            entwicklung = [guthaben]
            entwicklung_real = [guthaben]
            
            for monat in range(monate):
                guthaben = guthaben * (1 + monatsrendite) + monatlicher_sparbetrag
                entwicklung.append(guthaben)
                
                # Inflation berücksichtigen
                inflationsfaktor = (1 + inflationsrate/100) ** (monat/12)
                entwicklung_real.append(guthaben / inflationsfaktor)
                
            endguthaben = guthaben
            eingezahlt = startkapital + monatlicher_sparbetrag * monate
            
            st.metric("Endguthaben", f"{endguthaben:,.0f}€")
            st.metric("Inflationsbereinigt", f"{entwicklung_real[-1]:,.0f}€")
            st.metric("Eingezahltes Kapital", f"{eingezahlt:,.0f}€")
            st.metric("Zinsgewinn", f"{endguthaben - eingezahlt:,.0f}€")
        
        # Visualisierung - FEHLER BEHOBEN
        st.subheader("Vermögensentwicklung")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(entwicklung))),
            y=entwicklung,
            mode='lines',
            name='Nominales Vermögen',
            line=dict(color='#00d2ff', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=list(range(len(entwicklung_real))),
            y=entwicklung_real,
            mode='lines',
            name='Reales Vermögen (inflationsbereinigt)',
            line=dict(color='#6a11cb', width=3, dash='dash')
        ))
        
        fig.update_layout(
            xaxis_title="Monate",
            yaxis_title="Vermögen (€)",
            template="plotly_dark",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

def tips_section():
    with st.container():
        st.header("💡 Spartipps für den Alltag")
        st.markdown("Praktische Strategien, um jeden Tag Geld zu sparen")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Haushalt")
            st.markdown("""
            <div class="tip-card">1. Stromfresser identifizieren und ersetzen</div>
            <div class="tip-card">2. Wasser sparen mit Durchflussbegrenzern</div>
            <div class="tip-card">3. Heizkosten durch smartes Thermostat senken</div>
            <div class="tip-card">4. Lebensmittelverschwendung reduzieren</div>
            <div class="tip-card">5. Reparieren statt neu kaufen</div>
            <div class="tip-card">6. LED-Beleuchtung installieren</div>
            <div class="tip-card">7. Waschmaschine voll beladen</div>
            <div class="tip-card">8. Duschen statt Baden</div>
            <div class="tip-card">9. Standby-Modus vermeiden</div>
            <div class="tip-card">10. Mehrweggläser statt Einweg</div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Einkaufen")
            st.markdown("""
            <div class="tip-card">11. Mit Einkaufsliste planen</div>
            <div class="tip-card">12. Cashback-Apps nutzen</div>
            <div class="tip-card">13. Saisonal und regional einkaufen</div>
            <div class="tip-card">14. Großpackungen bei häufig genutzten Produkten</div>
            <div class="tip-card">15. Preise mit Apps vergleichen</div>
            <div class="tip-card">16. Eigenmarken statt Markenprodukte</div>
            <div class="tip-card">17. Rabattaktionen gezielt nutzen</div>
            <div class="tip-card">18. Second-Hand kaufen</div>
            <div class="tip-card">19. Vorräte clever anlegen</div>
            <div class="tip-card">20. Online vs. Ladenpreise vergleichen</div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.subheader("Finanzen")
            st.markdown("""
            <div class="tip-card">21. Bankgebühren vergleichen</div>
            <div class="tip-card">22. Kündigung unnötiger Abos</div>
            <div class="tip-card">23. Versicherungen optimieren</div>
            <div class="tip-card">24. Steuererklärung machen</div>
            <div class="tip-card">25. Automatische Sparpläne einrichten</div>
            <div class="tip-card">26. Freistellungsauftrag nutzen</div>
            <div class="tip-card">27. Kreditkartengebühren vermeiden</div>
            <div class="tip-card">28. Alte Verträge kündigen</div>
            <div class="tip-card">29. Finanz-Apps nutzen</div>
            <div class="tip-card">30. Geldanlagen diversifizieren</div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tip-card" style="background:rgba(106,17,203,0.3);">
            🔥 Tipp: Mit unserer automatischen Sparplan-Optimierung sparen Sie durchschnittlich 23% mehr!
        </div>
        """, unsafe_allow_html=True)

def tools_section():
    with st.container():
        st.header("🛠️ Finanz-Tools")
        st.markdown("Praktische Rechner für Ihre Finanzplanung")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Sparquote", "FIRE-Rechner", "Steuersparer", "ETF-Vergleich"])
        
        with tab1:
            st.subheader("🔢 Sparquote-Rechner")
            income = st.number_input("Nettoeinkommen (€)", 1000, 20000, 3000)
            expenses = st.number_input("Lebenshaltungskosten (€)", 500, 10000, 1800)
            savings = income - expenses
            savings_rate = savings / income * 100
            st.metric("Sparquote", f"{savings_rate:.1f}%", f"{savings:,.0f}€")
            
        with tab2:
            st.subheader("🏆 FIRE-Erreichbarkeit")
            annual_expenses = st.number_input("Jährliche Ausgaben (€)", 10000, 100000, 30000)
            current_assets = st.number_input("Aktuelles Vermögen (€)", 0, 1000000, 50000)
            monthly_savings = st.number_input("Monatliche Sparrate (€)", 100, 5000, 1000)
            expected_return = st.slider("Erwartete Rendite p.a. (%)", 1.0, 15.0, 6.0, 0.5)
            
            fire_target = annual_expenses * 25
            monthly_return = expected_return / 100 / 12
            
            # Eigene Implementierung der nper-Funktion
            def calculate_fire_years():
                if monthly_savings <= 0:
                    return float('inf')
                
                pv = -current_assets
                pmt = -monthly_savings
                fv = fire_target
                rate = monthly_return
                
                # Wenn keine Rendite erwartet wird
                if rate == 0:
                    return (fv - pv) / pmt / 12
                
                # Finanzmathematische Formel
                n = math.log(1 + (fv * rate) / (pmt + pv * rate)) / math.log(1 + rate)
                return n / 12
            
            years = calculate_fire_years()
            
            st.metric("Finanzielle Freiheit erreicht in", f"{years:.1f} Jahren")
            st.metric("Benötigtes Vermögen", f"{fire_target:,.0f}€")
            
        with tab3:
            st.subheader("💰 Steuerersparnis-Simulator")
            capital_gains = st.number_input("Kapitalerträge (€)", 0, 100000, 5000)
            tax_before = capital_gains * 0.26375
            tax_after = max(0, (capital_gains - 1000) * 0.26375)
            savings = tax_before - tax_after
            
            st.metric("Steuerlast ohne Optimierung", f"{tax_before:,.0f}€")
            st.metric("Mit Freistellungsauftrag", f"{tax_after:,.0f}€")
            st.metric("Ersparnis", f"{savings:,.0f}€", delta_color="inverse")
            
        with tab4:
            st.subheader("📊 ETF-Vergleichstool")
            etfs = {
                "iShares Core MSCI World": {"TER": 0.20, "Rendite": 8.2, "Risiko": 2.1},
                "Vanguard FTSE All-World": {"TER": 0.22, "Rendite": 7.9, "Risiko": 2.0},
                "Xtrackers MSCI World": {"TER": 0.19, "Rendite": 8.1, "Risiko": 2.2},
                "Amundi Prime Global": {"TER": 0.05, "Rendite": 7.7, "Risiko": 2.3}
            }
            
            selected_etfs = st.multiselect(
                "ETFs vergleichen",
                list(etfs.keys()),
                default=list(etfs.keys())
            )
            
            if selected_etfs:
                df = pd.DataFrame({etf: etfs[etf] for etf in selected_etfs}).T
                st.dataframe(df.style.format({
                    "TER": "{:.2f}%", 
                    "Rendite": "{:.1f}%",
                    "Risiko": "{:.1f}"
                }), height=200)
                
                # Visualisierung
                fig = px.bar(
                    df.reset_index(), 
                    x='index', 
                    y=['TER', 'Rendite'],
                    barmode='group',
                    labels={'index': 'ETF', 'value': 'Prozent'},
                    title='ETF-Vergleich'
                )
                st.plotly_chart(fig, use_container_width=True)

def testimonial_section():
    with st.container():
        st.header("💬 Was unsere Kunden sagen")
        
        cols = st.columns(2)
        testimonials = [
            {
                "text": "FIREFLY hat meine finanzielle Planung revolutioniert. Innerhalb eines Jahres konnte ich meine Sparquote verdoppeln!",
                "author": "Markus T., Berlin"
            },
            {
                "text": "Der Sparplan-Simulator hat mir gezeigt, wie ich 10 Jahre früher in Rente gehen kann. Einfach genial!",
                "author": "Sabine L., München"
            },
            {
                "text": "Die Spartipps sind Gold wert. Ich spare jetzt jeden Monat 300€, ohne auf Lebensqualität zu verzichten.",
                "author": "Thomas K., Hamburg"
            },
            {
                "text": "Das E-Book ist der beste Finanzratgeber, den ich je gelesen habe. Endlich verstehe ich, wie Vermögensaufbau wirklich funktioniert.",
                "author": "Julia M., Köln"
            }
        ]
        
        for i, testimonial in enumerate(testimonials):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="testimonial">
                    <div class="testimonial-text">"{testimonial['text']}"</div>
                    <div class="testimonial-author">- {testimonial['author']}</div>
                </div>
                """, unsafe_allow_html=True)

def pricing_section():
    with st.container():
        st.header("💎 Premium-Angebot")
        st.markdown("Wählen Sie das Paket, das zu Ihren finanziellen Zielen passt")
        
        cols = st.columns(3)
        plans = [
            {
                "name": "Basis",
                "price": "0€",
                "features": [
                    "Sparplan-Simulator",
                    "Grundlegende Spartipps",
                    "ETF-Vergleichstool",
                    "Einfache Zielplanung"
                ],
                "cta": "Kostenlos starten"
            },
            {
                "name": "Premium",
                "price": "9,99€",
                "period": "pro Monat",
                "features": [
                    "Alle Basis-Features",
                    "Premium-Sparguide (E-Book)",
                    "Persönliche Sparstrategie",
                    "Erweiterte Portfolio-Analyse",
                    "Steueroptimierungs-Tools",
                    "Priorisierter Support"
                ],
                "cta": "Jetzt upgraden",
                "featured": True
            },
            {
                "name": "Family",
                "price": "14,99€",
                "period": "pro Monat",
                "features": [
                    "Alle Premium-Features",
                    "Bis zu 5 Familienmitglieder",
                    "Gemeinsame Finanzziele",
                    "Kinder-Sparpläne",
                    "Familienbudgetplaner",
                    "Exklusive Webinare"
                ],
                "cta": "Für Familien"
            }
        ]
        
        for i, plan in enumerate(plans):
            with cols[i]:
                featured_class = "featured" if plan.get("featured") else ""
                st.markdown(f"""
                <div class="pricing-card {featured_class}">
                    <div class="pricing-header">
                        <h3>{plan['name']}</h3>
                        <div class="pricing-price">{plan['price']}</div>
                        <div>{plan.get('period', '')}</div>
                    </div>
                    <ul class="pricing-features">
                        {''.join([f'<li>{feature}</li>' for feature in plan['features']])}
                    </ul>
                    <a href="#" class="cta-button">{plan['cta']}</a>
                </div>
                """, unsafe_allow_html=True)

def ebook_section():
    with st.container():
        st.header("📚 Premium Sparguide")
        st.markdown("Ihr persönliches E-Book mit exklusiven Sparstrategien und Finanztipps")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="card">
                <h3>🔥 Der ultimative Sparguide für finanzielle Freiheit</h3>
                
                <p>Dieses exklusive E-Book enthält alles, was Sie für Ihren Weg zur finanziellen Unabhängigkeit benötigen:</p>
                
                <ul style="margin-left: 1.5rem; margin-top: 1rem;">
                    <li><strong>7 Säulen der Vermögensbildung</strong> - Fundament für finanziellen Erfolg</li>
                    <li><strong>Automatisierte Sparsysteme</strong> - Geld arbeiten lassen während Sie schlafen</li>
                    <li><strong>Steuertricks für Sparer</strong> - Legal mehr behalten</li>
                    <li><strong>ETF-Strategien 2025</strong> - Top-Performer für Ihr Portfolio</li>
                    <li><strong>Krisensichere Anlagen</strong> - Schutz für Ihre Investments</li>
                    <li><strong>FIRE-Strategie</strong> - Finanzielle Unabhängigkeit erreichen</li>
                    <li><strong>100 Spartipps</strong> - Für den täglichen Gebrauch</li>
                </ul>
                
                <h4 style="margin-top: 1.5rem;">Enthaltene Tools:</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 1rem;">
                    <span style="background: rgba(106,17,203,0.3); padding: 5px 10px; border-radius: 20px;">Sparquote-Rechner</span>
                    <span style="background: rgba(106,17,203,0.3); padding: 5px 10px; border-radius: 20px;">FIRE-Erreichbarkeit</span>
                    <span style="background: rgba(106,17,203,0.3); padding: 5px 10px; border-radius: 20px;">Portfolio-Optimierung</span>
                    <span style="background: rgba(106,17,203,0.3); padding: 5px 10px; border-radius: 20px;">Steuerersparnis-Simulator</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            # E-Book generieren und Download anbieten (optimierte Version)
            pdf = generate_ebook()
            pdf_bytes = pdf.output(dest='S').encode('latin1')
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                    
            st.markdown(f"""
            <div style="text-align: center; margin-top: 2rem;">
                <div style="font-size: 5rem; margin-bottom: 1rem;">📘</div>
                <h3>FIREFLY Premium Sparguide</h3>
                <p style="margin-bottom: 1.5rem;">Sofortiger Download nach Bestellung</p>
                <a href="data:application/pdf;base64,{base64_pdf}" download="FIREFLY_Premium_Sparguide.pdf" class="cta-button">
                    📥 Jetzt herunterladen - 14,99€
                </a>
                <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">30-Tage Geld-zurück-Garantie</p>
            </div>
            """, unsafe_allow_html=True)

def footer():
    st.markdown("""
    <div class="footer">
        <h3>🔥 FIREFLY Finance</h3>
        <p>Ihr Weg zur finanziellen Freiheit</p>
        
        <div style="display: flex; justify-content: center; gap: 20px; margin: 1.5rem 0;">
            <a href="#" style="color: var(--text-light);">Über uns</a>
            <a href="#" style="color: var(--text-light);">Leistungen</a>
            <a href="#" style="color: var(--text-light);">Preise</a>
            <a href="#" style="color: var(--text-light);">Blog</a>
            <a href="#" style="color: var(--text-light);">Kontakt</a>
        </div>
        
        <p>© 2025 FIREFLY Finance GmbH | Alle Rechte vorbehalten</p>
        <p>Kontakt: kontakt@firefly-finance.de | Support: +49 123 456 789</p>
        
        <p style="font-size:0.9em; margin-top:1.5rem; opacity:0.7;">
            Diese Anwendung dient nur zu Informationszwecken und stellt keine Finanzberatung dar. 
            Die dargestellten Ergebnisse sind Prognosen und keine Garantie für zukünftige Erträge.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===== HAUPTAPPLIKATION =====
def main():
    # Session State für Watchlist initialisieren
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []
    
    with st.container():
        header_section()
        features_section()
        goals_section()
        simulation_section()
        tips_section()
        tools_section()
        testimonial_section()
        pricing_section()
        ebook_section()
        footer()

if __name__ == "__main__":
    main()
