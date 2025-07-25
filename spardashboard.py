import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
from fpdf import FPDF
import tempfile
from numpy_financial import nper  # Korrekte Import-Anweisung hinzugefügt

# ===== KONSTANTEN & EINSTELLUNGEN =====
THEME_COLORS = {
    "primary": "#6a11cb",
    "secondary": "#2575fc",
    "accent": "#00d2ff",
    "dark_bg": "#0f0c29",
    "card_bg": "rgba(26, 21, 57, 0.8)",
    "text_light": "#e2e8f0"
}

# ===== MODERNES DESIGN MIT VERLAUF =====
st.markdown(f"""
<style>
:root {{
    --primary: {THEME_COLORS["primary"]};
    --secondary: {THEME_COLORS["secondary"]};
    --accent: {THEME_COLORS["accent"]};
    --dark-bg: {THEME_COLORS["dark_bg"]};
    --card-bg: {THEME_COLORS["card_bg"]};
    --text-light: {THEME_COLORS["text_light"]};
}}
body {{
    background: linear-gradient(to right, var(--dark-bg), #24243e, var(--dark-bg)) fixed;
    background-size: 300% 300%;
    animation: gradient 15s ease infinite;
    color: var(--text-light);
    font-family: 'Segoe UI', system-ui, sans-serif;
    line-height: 1.6;
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
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
}}
.stApp {{
    background: transparent !important;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
}}
.st-emotion-cache-1y4p8pa {{
    background: var(--card-bg) !important;
    backdrop-filter: blur(10px);
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
    margin-bottom: 2rem;
}}
.stButton button {{
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    margin-top: 0.5rem;
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
.section {{
    margin-bottom: 3rem;
}}
.tip-card {{
    background: rgba(10, 80, 150, 0.3);
    border-left: 4px solid var(--accent);
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 0 8px 8px 0;
}}
.footer {{
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.1);
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
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("## 🔥 FIREFLY")
        st.markdown("### Ihr Weg zur finanziellen Freiheit")
    with col2:
        st.markdown("""
        **Die intelligente Plattform für Vermögensaufbau und Sparplanung.**  
        Mit KI-gestützten Prognosen, automatischem Portfolio-Management und persönlichen Sparstrategien.
        """)
    
    st.image("https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=1200", 
             use_column_width=True, caption="Finanzielle Freiheit erreichen mit SMART INVEST")

def goals_section():
    st.header("🎯 Sparziel-Planung")
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
    st.header("📈 Sparplan-Simulation")
    
    col1, col2 = st.columns(2)
    with col1:
        startkapital = st.number_input("Startkapital (€)", 0, 1000000, 5000)
        monatlicher_sparbetrag = st.number_input("Monatliche Sparrate (€)", 50, 5000, 300)
        jahresrendite = st.slider("Erwartete Rendite p.a. (%)", 1.0, 15.0, 6.5, 0.5)
        simulationsdauer = st.slider("Simulationsdauer (Jahre)", 5, 40, 15)
    
    with col2:
        st.subheader("Prognoseergebnisse")
        monatsrendite = jahresrendite / 100 / 12
        monate = simulationsdauer * 12
        guthaben = startkapital
        entwicklung = [guthaben]
        
        for _ in range(monate):
            guthaben = guthaben * (1 + monatsrendite) + monatlicher_sparbetrag
            entwicklung.append(guthaben)
            
        endguthaben = guthaben
        eingezahlt = startkapital + monatlicher_sparbetrag * monate
        
        st.metric("Endguthaben", f"{endguthaben:,.0f}€")
        st.metric("Eingezahltes Kapital", f"{eingezahlt:,.0f}€")
        st.metric("Zinsgewinn", f"{endguthaben - eingezahlt:,.0f}€")
    
    # Visualisierung
    st.subheader("Vermögensentwicklung")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(entwicklung))),
        y=entwicklung,
        mode='lines',
        name='Prognostiziertes Vermögen',
        line=dict(color='#00d2ff', width=3)
    ))
    fig.update_layout(
        xaxis_title="Monate",
        yaxis_title="Vermögen (€)",
        template="plotly_dark",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

def tips_section():
    st.header("💡 50 Spartipps für den Alltag")
    
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
    *Weitere Tipps in unserem Premium-E-Book!*

    <div class="tip-card" style="background:rgba(106,17,203,0.3);">
        🔥 Tipp: Mit unserer automatischen Sparplan-Optimierung sparen Sie durchschnittlich 23% mehr!
    </div>
    """, unsafe_allow_html=True)

def tools_section():
    st.header("🛠️ Finanz-Tools")
    
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
        
        fire_target = annual_expenses * 25
        # Korrekte Verwendung der nper-Funktion aus numpy_financial
        months = nper(0.06/12, -monthly_savings, -current_assets, fire_target)
        years = months / 12
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
            "iShares Core MSCI World": {"TER": 0.20, "Rendite": 8.2},
            "Vanguard FTSE All-World": {"TER": 0.22, "Rendite": 7.9},
            "Xtrackers MSCI World": {"TER": 0.19, "Rendite": 8.1},
            "Amundi Prime Global": {"TER": 0.05, "Rendite": 7.7}
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
                "Rendite": "{:.1f}%"
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

def ebook_section():
    st.header("📚 Premium Sparguide")
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
        - **50 Spartipps** - Für den täglichen Gebrauch
        
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

def footer():
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🔥 FIREFLY - Ihr Weg zur finanziellen Freiheit</p>
        <p>© 2025 FIREFLY Finance | Alle Rechte vorbehalten</p>
        <p>Kontakt: kontakt@firefly-finance.de | Support: +49 123 456 789</p>
        <p style="font-size:0.8em; opacity:0.7;">Diese Anwendung dient nur zu Informationszwecken und stellt keine Finanzberatung dar.</p>
    </div>
    """, unsafe_allow_html=True)

# ===== HAUPTAPPLIKATION =====
def main():
    header_section()
    goals_section()
    simulation_section()
    tips_section()
    tools_section()
    ebook_section()
    footer()

if __name__ == "__main__":
    main()
    
