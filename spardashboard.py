import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
from fpdf import FPDF
import tempfile

# ===== SEITENSTRUKTUR =====
st.set_page_config(
    layout="wide", 
    page_title="🚀 FIREFLY - Dein Premium Sparplan", 
    page_icon="✨",
    initial_sidebar_state="expanded"
)

# ===== MODERNES DESIGN MIT VERLAUF =====
st.markdown(f"""
<style>
:root {{
    --primary: #6a11cb;
    --secondary: #2575fc;
    --accent: #00d2ff;
    --dark-bg: #0f0c29;
    --card-bg: rgba(26, 21, 57, 0.8);
    --text-light: #e2e8f0;
}}
body {{
    background: linear-gradient(to right, var(--dark-bg), #24243e, var(--dark-bg)) fixed;
    background-size: 300% 300%;
    animation: gradient 15s ease infinite;
    color: var(--text-light);
    font-family: 'Segoe UI', system-ui, sans-serif;
}}
@keyframes gradient {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
h1, h2, h3, h4, h5, h6 {{
    background: linear-gradient(90deg, var(--accent), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
}}
.stApp {{
    background: transparent !important;
}}
.st-emotion-cache-1y4p8pa {{
    background: var(--card-bg) !important;
    backdrop-filter: blur(10px);
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
}}
.stButton button {{
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}}
.stButton button:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(106, 17, 203, 0.5);
}}
.card {{
    background: rgba(38, 33, 75, 0.6);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}}
.card:hover {{
    transform: translateY(-5px);
    background: rgba(46, 41, 90, 0.8);
    box-shadow: 0 8px 25px rgba(0, 210, 255, 0.3);
}}
.stProgress > div > div {{
    background: linear-gradient(90deg, var(--accent), var(--secondary)) !important;
}}
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
            self.set_font('Arial', 'B', 14)
            self.set_fill_color(106, 17, 203)
            self.cell(0, 10, title, 0, 1, 'L', 1)
            self.ln(4)
            
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
        ("Finanzielle Freiheit erreichen", 6)
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

# ===== SEITEN =====
def dashboard_page():
    st.title("📊 Finanz-Dashboard")
    st.markdown("Ihr zentraler Überblick über Vermögen, Sparziele und Marktentwicklung")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Gesamtvermögen", "124.567 €", "+3.2%")
    with col2:
        st.metric("Monatliche Sparrate", "1.250 €", "Ziel: 1.500 €")
    with col3:
        st.metric("Prognose finanzielle Freiheit", "2038", "12 Jahre")
    
    # Portfolio-Verteilung
    st.subheader("🏆 Portfolio-Verteilung")
    assets = {
        'Aktien-ETFs': 65,
        'Immobilien': 20,
        'Anleihen': 8,
        'Krypto': 5,
        'Edelmetalle': 2
    }
    fig = px.pie(
        names=list(assets.keys()), 
        values=list(assets.values()),
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Sparziel-Fortschritt
    st.subheader("🎯 Sparziel-Fortschritt")
    goals = {
        'Notfallfonds': {'current': 15000, 'target': 20000},
        'Wohnungskauf': {'current': 45000, 'target': 100000},
        'Altersvorsorge': {'current': 29500, 'target': 500000}
    }
    
    for goal, data in goals.items():
        progress = data['current'] / data['target']
        st.markdown(f"**{goal}**")
        st.progress(min(1.0, progress), text=f"{data['current']:,.0f}€ / {data['target']:,.0f}€ ({progress*100:.1f}%)")

def goals_page():
    st.title("🎯 Sparziel-Planung")
    st.markdown("Definieren und verfolgen Sie Ihre finanziellen Meilensteine")
    
    with st.expander("➕ Neues Sparziel hinzufügen", expanded=True):
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
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = days_left / 365,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Jahre bis Ziel"},
                    gauge = {
                        'axis': {'range': [0, 10]},
                        'bar': {'color': "#6a11cb"},
                        'steps': [
                            {'range': [0, 5], 'color': "lightgray"},
                            {'range': [5, 10], 'color': "gray"}],
                    }
                ))
                fig.update_layout(height=200, margin=dict(l=0, r=0, b=0, t=30))
                st.plotly_chart(fig, use_container_width=True)

def ebook_page():
    st.title("📚 Premium Sparguide")
    st.markdown("Ihr persönliches E-Book mit exklusiven Sparstrategien und Finanztipps")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://images.unsplash.com/photo-1545235617-9465d2a55698?auto=format&fit=crop&w=500", 
                caption="FIREFLY Premium Guide")
        
    with col2:
        st.markdown("""
        ### 🔥 Der ultimative Sparguide für finanzielle Freiheit
        
        Dieses exklusive E-Book enthält:
        
        - **7 Säulen der Vermögensbildung** - Fundament für finanziellen Erfolg
        - **Automatisierte Sparsysteme** - Geld arbeiten lassen während Sie schlafen
        - **Steuertricks für Sparer** - Legal mehr behalten
        - **ETF-Strategien 2025** - Top-Performer für Ihr Portfolio
        - **Krisensichere Anlagen** - Schutz für Ihre Investments
        - **FIRE-Strategie** - Finanzielle Unabhängigkeit erreichen
        
        ##### Enthaltene Tools:
        - Sparquote-Rechner
        - FIRE-Erreichbarkeitsanalyse
        - Portfolio-Optimierungscheck
        - Steuerersparnis-Simulator
        """)
        
        # E-Book generieren und Download anbieten
        pdf = generate_ebook()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf_bytes = pdf.output(dest='S').encode('latin1')
            tmpfile.write(pdf_bytes)
            tmpfile.seek(0)
            
            with open(tmpfile.name, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                
        st.download_button(
            label="📥 Jetzt E-Book herunterladen",
            data=f"data:application/pdf;base64,{base64_pdf}",
            file_name="FIREFLY_Premium_Sparguide.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.markdown("---")
    st.subheader("🛠️ Enthaltene Tools")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container():
            st.markdown("### 🔢 Sparquote-Rechner")
            income = st.number_input("Nettoeinkommen (€)", 1000, 20000, 3000)
            expenses = st.number_input("Lebenshaltungskosten (€)", 500, 10000, 1800)
            savings = income - expenses
            savings_rate = savings / income * 100 if income != 0 else 0
            st.metric("Sparquote", f"{savings_rate:.1f}%", f"{savings:,.0f}€")
