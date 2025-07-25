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
import time  # Fehlenden Import hinzugefügt

# ===== REVOLUTIONÄRES DESIGN =====
st.set_page_config(
    page_title="NEXUS Wealth",
    page_icon="💫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dynamisches Farbdesign
primary_color = "#5e17eb"
secondary_color = "#2575fc"
accent_color = "#00d2ff"
dark_bg = "#0a081f"
card_bg = "rgba(20, 15, 45, 0.85)"
text_light = "#f0f4ff"

# CSS mit korrigierten geschweiften Klammern
st.markdown(f"""
<style>
:root {{
    --primary: {primary_color};
    --secondary: {secondary_color};
    --accent: {accent_color};
    --dark-bg: {dark_bg};
    --card-bg: {card_bg};
    --text-light: {text_light};
    --success: #00e676;
    --warning: #ffca28;
    --error: #ff5252;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}}

body {{
    background: radial-gradient(circle at 10% 20%, var(--dark-bg) 0%, #050417 100%);
    color: var(--text-light);
    line-height: 1.7;
    padding: 0;
    overflow-x: hidden;
}}

.stApp {{
    background: transparent !important;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0;
}}

.header-section {{
    background: linear-gradient(135deg, var(--primary), #1a0b47);
    padding: 4rem 2rem;
    border-radius: 0 0 30px 30px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
}}

.header-section::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 30%, rgba(255,255,255,0.1) 0%, transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(94,23,235,0.2) 0%, transparent 40%);
    z-index: 0;
}}

.header-content {{
    position: relative;
    z-index: 2;
    text-align: center;
}}

h1 {{
    font-size: 4rem !important;
    background: linear-gradient(90deg, var(--accent), #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900 !important;
    margin-bottom: 1rem !important;
    text-shadow: 0 5px 15px rgba(0,0,0,0.2);
}}

h2 {{
    font-size: 2.2rem !important;
    background: linear-gradient(90deg, var(--text-light), #d1d8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
    margin-bottom: 2rem !important;
}}

.section-title {{
    font-size: 2.5rem;
    text-align: center;
    margin: 3rem 0 2rem;
    background: linear-gradient(90deg, var(--accent), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
    display: inline-block;
    width: 100%;
}}

.section-title::after {{
    content: "";
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, var(--accent), var(--primary));
    border-radius: 2px;
}}

.feature-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}}

.feature-card {{
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    overflow: hidden;
    position: relative;
}}

.feature-card::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: linear-gradient(90deg, var(--accent), var(--primary));
}}

.feature-card:hover {{
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255,255,255,0.15);
}}

.feature-card h3 {{
    font-size: 1.8rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.feature-card h3 .icon {{
    font-size: 2rem;
    background: linear-gradient(90deg, var(--accent), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.stats-container {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin: 3rem 0;
}}

.stat-card {{
    background: linear-gradient(145deg, rgba(94,23,235,0.2), rgba(37,117,252,0.2));
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    min-width: 250px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
}}

.stat-card:hover {{
    transform: scale(1.05);
}}

.stat-value {{
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--accent), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}}

.stat-label {{
    font-size: 1.1rem;
    opacity: 0.9;
    letter-spacing: 0.5px;
}}

.cta-button {{
    display: inline-block;
    padding: 1rem 2.5rem;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    color: white !important;
    text-align: center;
    border-radius: 50px;
    font-weight: bold;
    font-size: 1.2rem;
    margin: 1.5rem 0;
    transition: all 0.3s ease;
    text-decoration: none !important;
    border: none;
    cursor: pointer;
    box-shadow: 0 5px 15px rgba(94,23,235,0.3);
}}

.cta-button:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(94,23,235,0.4);
}}

.tab-container {{
    background: var(--card-bg);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}}

.visualization-card {{
    background: linear-gradient(145deg, rgba(20,15,45,0.8), rgba(30,20,60,0.8));
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}}

.progress-container {{
    background: rgba(30,20,60,0.6);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}}

.progress-container::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: var(--progress-width, 0%);
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    opacity: 0.15;
    transition: width 1s ease;
}}

.tip-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}}

.tip-card {{
    background: linear-gradient(145deg, rgba(20,15,45,0.8), rgba(30,20,60,0.8));
    border-radius: 15px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    border-left: 4px solid var(--accent);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}}

.tip-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,210,255,0.2);
}}

.tip-card h4 {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}}

.tip-card h4 .icon {{
    color: var(--accent);
    font-size: 1.5rem;
}}

.footer {{
    text-align: center;
    padding: 3rem 1rem;
    margin-top: 4rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    background: rgba(10, 8, 25, 0.8);
    border-radius: 30px 30px 0 0;
}}

/* Animations mit korrigierten Klammern */
@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }}
    100% {{ transform: translateY(0px); }}
}}

.floating {{
    animation: float 4s ease-in-out infinite;
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .feature-grid {{
        grid-template-columns: 1fr;
    }}
    
    .stats-container {{
        flex-direction: column;
    }}
    
    h1 {{
        font-size: 2.5rem !important;
    }}
    
    h2 {{
        font-size: 1.8rem !important;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ===== REVOLUTIONÄRE FUNKTIONEN =====

def generate_wealth_plan():
    """Generiert einen personalisierten Vermögensplan als PDF"""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'NEXUS Wealth Plan', 0, 1, 'C')
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Seite {self.page_no()}', 0, 0, 'C')
            
        def chapter_title(self, title):
            self.set_font('Arial', 'B', 16)
            self.set_fill_color(94, 23, 235)
            self.cell(0, 10, title, 0, 1, 'L', 1)
            self.ln(5)
            
        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 8, body)
            self.ln()

    pdf = PDF()
    pdf.add_page()
    
    # Titel
    pdf.set_font('Arial', 'B', 28)
    pdf.cell(0, 10, "NEXUS Wealth Plan", 0, 1, 'C')
    pdf.ln(15)
    
    # Inhalte
    chapters = {
        "Finanzielle Freiheitsstrategie": """
Ihr Weg zur finanziellen Unabhängigkeit in 3 Phasen:

Phase 1: Fundament schaffen (1-3 Jahre)
- Notfallfonds aufbauen (6 Monatsausgaben)
- Hochzins-Schulden eliminieren
- Grundlegende Sparroutine etablieren

Phase 2: Vermögenswachstum (3-10 Jahre)
- Diversifiziertes Portfolio aufbauen
- Sparrate systematisch erhöhen
- Passive Einkommensquellen entwickeln

Phase 3: Erhalt & Genuss (10+ Jahre)
- Entnahmestrategie implementieren
- Steuereffizientes Portfolio-Management
- Lebensstil anpassen
        """,
        
        "Ihr Investment-Fahrplan": """
**Aktuelle Allokation:**
- 50% Welt-ETFs
- 20% Immobilien-REITs
- 15% Technologie-Sektor
- 10% Anleihen
- 5% Rohstoffe

**Optimierte Allokation:**
- 55% Welt-ETFs (+5%)
- 15% Immobilien-REITs (-5%)
- 15% Technologie-Sektor
- 10% Anleihen
- 5% Nachhaltigkeitsfonds (neu)

**Begründung:**
- Höhere Wachstumschancen durch stärkere Gewichtung globaler Märkte
- Reduzierung volatiler Immobilienanteile
- Neue Nachhaltigkeitskomponente für zukunftssichere Investitionen
        """,
        
        "Monatlicher Aktionsplan": """
1. Sparrate erhöhen von 500€ auf 650€ (+30%)
2. Neue Sparpläne einrichten:
   - 350€ in MSCI World ETF
   - 150€ in Nachhaltigkeits-ETF
   - 100€ in Technologie-ETF
   - 50€ in Anleihenfonds

3. Kostenoptimierung:
   - Bankgebühren sparen: 8€/Monat
   - Versicherungen optimieren: 15€/Monat
   - Abos kündigen: 12€/Monat

4. Bildung:
   - Finanzbuchführungskurs beginnen
   - 2 Finanzbücher pro Quartal lesen
        """
    }
    
    for title, text in chapters.items():
        pdf.add_page()
        pdf.chapter_title(title)
        pdf.chapter_body(text)
    
    return pdf

def ai_wealth_assistant():
    """Interaktiver KI-Vermögensassistent"""
    with st.expander("💬 NEXUS KI-Assistent - Frag mich alles zu deinen Finanzen", expanded=True):
        st.info("""
        **Ich bin dein persönlicher KI-Finanzassistent.**  
        Stelle mir Fragen wie:
        - Wie kann ich meine Sparrate optimieren?
        - Welche ETFs sind jetzt interessant?
        - Wie erreiche ich meine finanziellen Ziele schneller?
        """)
        
        question = st.text_input("Stelle deine Frage:", placeholder="Wie kann ich mit 500€ monatlich starten?")
        
        if st.button("Analyse anfordern", use_container_width=True):
            with st.spinner("KI analysiert deine Situation..."):
                time.sleep(2)
                
                responses = [
                    "Basierend auf deinen Angaben empfehle ich eine Aufteilung in 60% globale ETFs, 30% Technologie-ETFs und 10% Emerging Markets. Beginne mit kostengünstigen Sparplänen bei einem Neobroker.",
                    "Für dein Budget von 500€ monatlich schlage ich vor: 300€ in einen MSCI World ETF, 100€ in einen NASDAQ-100 ETF und 100€ in einen nachhaltigen Aktienfonds. Vergiss nicht, einen Notfallfonds aufzubauen!",
                    "Deine aktuelle Strategie ist solide, aber ich empfehle eine stärkere Diversifikation. Betrachte zusätzlich REITs für Immobilienexposure und Edelmetalle als Sicherheit. Ein 70/20/10 Portfolio könnte besser zu deiner Risikotoleranz passen."
                ]
                
                st.success(f"**KI-Empfehlung:** {random.choice(responses)}")

def financial_health_check():
    """Echtzeit-Finanzgesundheitscheck mit visuellem Scoring"""
    with st.container():
        st.subheader("📊 Finanzgesundheits-Check")
        st.write("Analysiere deine aktuelle finanzielle Situation in 5 Schlüsselbereichen")
        
        categories = {
            "Sparrate": {"current": 15, "target": 20},
            "Notfallfonds": {"current": 3, "target": 6},
            "Verschuldung": {"current": 25, "target": 10},
            "Investitionen": {"current": 35, "target": 50},
            "Diversifikation": {"current": 40, "target": 70}
        }
        
        cols = st.columns(5)
        for i, (category, values) in enumerate(categories.items()):
            with cols[i]:
                score = min(100, int((values['current'] / values['target']) * 100))
                st.metric(category, f"{values['current']} von {values['target']}")
                st.progress(score/100)
        
        # Gesamtscore berechnen
        total_score = sum([min(100, int((v['current'] / v['target']) * 100)) for v in categories.values()]) // 5
        health_levels = {
            80: ("Exzellent", "var(--success)"),
            60: ("Gut", "#4CAF50"),
            40: ("Durchschnittlich", "var(--warning)"),
            20: ("Schwach", "#FF9800"),
            0: ("Kritisch", "var(--error)")
        }
        
        for level, (label, color) in health_levels.items():
            if total_score >= level:
                health_label, health_color = label, color
                break
        
        st.markdown(f"""
        <div style="text-align:center; margin:2rem 0;">
            <h3>Gesamtbewertung: <span style="color:{health_color}">{health_label}</span></h3>
            <div style="font-size:3rem; font-weight:800; color:{health_color}; margin:0.5rem 0;">{total_score}/100</div>
            <p style="max-width:600px; margin:0 auto;">{random.choice([
                "Solide Basis, aber noch Luft nach oben bei Diversifikation",
                "Starker Notfallfonds, aber Sparrate kann optimiert werden",
                "Gute Investitionsquote, reduziere deine Verschuldung"
            ])}</p>
        </div>
        """, unsafe_allow_html=True)

def wealth_projection():
    """Interaktive Vermögensprojektion mit mehreren Szenarien"""
    with st.container():
        st.subheader("🚀 Vermögensprognose")
        st.write("Erkunde verschiedene Zukunftsszenarien für deine Finanzen")
        
        col1, col2 = st.columns(2)
        with col1:
            current_wealth = st.number_input("Aktuelles Vermögen (€)", 0, 10000000, 25000)
            monthly_savings = st.number_input("Monatliche Sparrate (€)", 0, 10000, 500)
            investment_return = st.slider("Erwartete Rendite p.a. (%)", 1.0, 15.0, 6.5, 0.5)
            years = st.slider("Projektionszeitraum (Jahre)", 5, 40, 15)
            inflation = st.slider("Erwartete Inflation p.a. (%)", 0.5, 10.0, 2.0, 0.5)
        
        # Szenarien berechnen
        scenarios = {
            "Optimistisch": investment_return * 1.3,
            "Standard": investment_return,
            "Konservativ": investment_return * 0.7,
            "Hochinflation": investment_return - inflation * 1.5
        }
        
        projections = {}
        months = years * 12
        monthly_return = investment_return / 100 / 12
        
        for scenario, rate in scenarios.items():
            wealth = current_wealth
            growth = [wealth]
            monthly_scenario_rate = rate / 100 / 12
            
            for month in range(months):
                wealth = wealth * (1 + monthly_scenario_rate) + monthly_savings
                growth.append(wealth)
            
            projections[scenario] = growth
        
        # Visualisierung
        fig = go.Figure()
        colors = [accent_color, primary_color, "#00e676", "#ffca28"]
        
        for i, (scenario, growth) in enumerate(projections.items()):
            fig.add_trace(go.Scatter(
                x=list(range(len(growth))),
                y=growth,
                mode='lines',
                name=scenario,
                line=dict(color=colors[i], width=3),
                hovertemplate="<b>%{x} Monate</b><br>%{y:,.0f}€"
            ))
        
        fig.update_layout(
            title="Vermögensentwicklung in verschiedenen Szenarien",
            xaxis_title="Monate",
            yaxis_title="Vermögen (€)",
            template="plotly_dark",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

def goal_planner():
    """Dynamischer Zielplaner mit Fortschrittsvisualisierung"""
    with st.container():
        st.subheader("🎯 Finanzziele planen")
        
        goals = st.session_state.get("goals", [])
        
        with st.expander("➕ Neues Ziel hinzufügen", expanded=False):
            with st.form("goal_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Zielname*", placeholder="Eigenheim, Altersvorsorge")
                    target = st.number_input("Zielbetrag (€)*", 1000, 10000000, 50000)
                    priority = st.select_slider("Priorität", ["Niedrig", "Mittel", "Hoch", "Sehr hoch"])
                    
                with col2:
                    deadline = st.date_input("Zieldatum*", datetime.now() + timedelta(days=365*3))
                    current = st.number_input("Aktuell gespart (€)", 0, 10000000, 5000)
                    monthly = st.number_input("Monatliche Sparrate (€)", 0, 5000, 500)
                    
                if st.form_submit_button("Ziel speichern"):
                    goals.append({
                        "name": name,
                        "target": target,
                        "current": current,
                        "monthly": monthly,
                        "deadline": deadline.strftime("%Y-%m-%d"),
                        "priority": priority
                    })
                    st.session_state.goals = goals
                    st.success("Ziel gespeichert!")
        
        if goals:
            st.write("### Deine Finanzziele")
            for goal in goals:
                progress = min(1.0, goal['current'] / goal['target'])
                days_left = (datetime.strptime(goal['deadline'], "%Y-%m-%d") - datetime.now()).days
                monthly_needed = max(0, (goal['target'] - goal['current']) / max(1, days_left/30.44))
                
                with st.container():
                    st.markdown(f"#### {goal['name']} ({goal['priority']} Priorität)")
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric("Zielbetrag", f"{goal['target']:,.0f}€")
                        st.metric("Aktueller Stand", f"{goal['current']:,.0f}€")
                        st.metric("Monatlich benötigt", f"{monthly_needed:,.0f}€")
                    
                    with col2:
                        st.markdown(f"**Fortschritt** ({progress*100:.1f}%)")
                        st.progress(progress)
                        
                        st.markdown(f"**Zeitplan** ({days_left} Tage verbleibend)")
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=days_left/365,
                            number={'suffix': " Jahre"},
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={
                                'axis': {'range': [0, max(5, days_left/365 + 2)]},
                                'bar': {'color': primary_color},
                                'steps': [
                                    {'range': [0, max(5, days_left/365 + 2)*0.3], 'color': "#4CAF50"},
                                    {'range': [max(5, days_left/365 + 2)*0.3, max(5, days_left/365 + 2)*0.7], 'color': "#FFC107"},
                                    {'range': [max(5, days_left/365 + 2)*0.7, max(5, days_left/365 + 2)], 'color': "#F44336"}],
                            }
                        ))
                        fig.update_layout(height=200, margin=dict(l=0, r=0, b=0, t=0))
                        st.plotly_chart(fig, use_container_width=True)

def smart_saving_tips():
    """Intelligente Spartipps mit personalisierten Empfehlungen"""
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
        ],
        "Investitionen": [
            "Kostenlose Sparpläne bei Neobrokern nutzen",
            "Steuerfreistellungsauftrag optimal ausnutzen",
            "ETF-Portfolio mit max. 0.2% TER zusammenstellen",
            "Regelmäßiges Rebalancing - 1x jährlich",
            "Dividendenstrategie für passives Einkommen"
        ]
    }
    
    with st.container():
        st.subheader("💡 Intelligente Spartipps")
        st.write("Personalisiert basierend auf deinem Profil")
        
        # Tipp-Kategorien anzeigen
        selected_category = st.selectbox("Kategorie auswählen", list(categories.keys()))
        
        if selected_category:
            tips = categories[selected_category]
            
            st.write(f"### Top-Tipps für {selected_category}")
            for i, tip in enumerate(tips):
                st.markdown(f"""
                <div class="tip-card">
                    <h4><span class="icon">✔</span> Tipp #{i+1}</h4>
                    <p>{tip}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Personalisierte Empfehlung
        st.markdown(f"""
        <div style="margin-top:2rem; padding:1.5rem; background: linear-gradient(145deg, rgba(94,23,235,0.2), rgba(37,117,252,0.2)); border-radius:15px;">
            <h4>⭐ Personalisierte Empfehlung</h4>
            <p>{random.choice([
                "Basierend auf deinen Angaben könntest du durch Bankwechsel ca. 80€ pro Jahr sparen.",
                "Dein Energieverbrauch ist überdurchschnittlich - ein Smart Home System könnte 15% reduzieren.",
                "Deine Versicherungen sind nicht optimal - eine Analyse könnte 200€/Jahr sparen.",
                "Du hast noch keinen Freistellungsauftrag hinterlegt - hol dir 1.000€ steuerfrei!"
            ])}</p>
        </div>
        """, unsafe_allow_html=True)

# ===== HAUPTSEKTIONEN =====

def hero_section():
    """Hero-Bereich mit Haupt-CTA"""
    with st.container():
        st.markdown("""
        <div class="header-section">
            <div class="header-content">
                <h1>NEXUS Wealth</h1>
                <h2>Dein Weg zur finanziellen Freiheit</h2>
                
                <p style="font-size:1.2rem; max-width:800px; margin:2rem auto;">
                    Die intelligente Plattform für Vermögensaufbau, Sparplanung und finanzielle Bildung. 
                    Mit KI-gestützter Analyse, automatischem Portfolio-Management und 
                    persönlichen Strategien für finanzielle Unabhängigkeit.
                </p>
                
                <button class="cta-button">Jetzt kostenlos starten</button>
                
                <div class="stats-container">
                    <div class="stat-card floating">
                        <div class="stat-value">23%</div>
                        <div class="stat-label">Mehr Sparpotential</div>
                    </div>
                    <div class="stat-card floating" style="animation-delay:0.5s">
                        <div class="stat-value">10.000+</div>
                        <div class="stat-label">Zufriedene Nutzer</div>
                    </div>
                    <div class="stat-card floating" style="animation-delay:1s">
                        <div class="stat-value">97%</div>
                        <div class="stat-label">Erfolgsquote</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def features_section():
    """Innovative Features im Grid-Layout"""
    with st.container():
        st.markdown('<div class="section-title">Revolutionäre Funktionen</div>', unsafe_allow_html=True)
        
        features = [
            {
                "icon": "🤖",
                "title": "KI-Vermögensassistent",
                "desc": "24/7 persönliche Beratung durch unseren KI-Finanzexperten",
                "color": primary_color
            },
            {
                "icon": "📊",
                "title": "Echtzeit-Finanzcheck",
                "desc": "Umfassende Analyse deiner finanziellen Gesundheit mit Handlungsempfehlungen",
                "color": secondary_color
            },
            {
                "icon": "🚀",
                "title": "Vermögensprojektion",
                "desc": "Interaktive Simulation verschiedener Zukunftsszenarien für deine Finanzen",
                "color": accent_color
            },
            {
                "icon": "🎯",
                "title": "Zielplaner",
                "desc": "Definiere und verfolge deine finanziellen Meilensteine mit dynamischen Plänen",
                "color": "#9C27B0"
            },
            {
                "icon": "💡",
                "title": "Intelligente Spartipps",
                "desc": "Personalisiertes Sparpotenzial in allen Lebensbereichen",
                "color": "#FF9800"
            },
            {
                "icon": "📚",
                "title": "Wealth Academy",
                "desc": "Interaktive Lernmodule für finanzielle Bildung und Investment-Wissen",
                "color": "#4CAF50"
            }
        ]
        
        st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
        for feature in features:
            st.markdown(f"""
            <div class="feature-card">
                <h3><span class="icon">{feature['icon']}</span> {feature['title']}</h3>
                <p>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main_sections():
    """Hauptfunktionalitäten der App"""
    with st.container():
        st.markdown('<div class="section-title">Dein Finanz-Dashboard</div>', unsafe_allow_html=True)
        
        ai_wealth_assistant()
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "💰 Finanzcheck", 
            "🚀 Vermögensprognose", 
            "🎯 Zielplanung", 
            "💡 Sparpotenzial"
        ])
        
        with tab1:
            financial_health_check()
        
        with tab2:
            wealth_projection()
        
        with tab3:
            goal_planner()
        
        with tab4:
            smart_saving_tips()

def wealth_academy():
    """Interaktive Lernsektion für finanzielle Bildung"""
    with st.container():
        st.markdown('<div class="section-title">Wealth Academy</div>', unsafe_allow_html=True)
        st.write("Interaktive Lernmodule für deine finanzielle Bildung")
        
        modules = [
            {"title": "Grundlagen der Geldanlage", "progress": 35, "icon": "📈"},
            {"title": "ETF-Strategien für Einsteiger", "progress": 20, "icon": "📊"},
            {"title": "Steuern sparen für Investoren", "progress": 10, "icon": "💰"},
            {"title": "Immobilien vs. Aktien", "progress": 5, "icon": "🏠"},
            {"title": "Passives Einkommen aufbauen", "progress": 0, "icon": "🔄"}
        ]
        
        for module in modules:
            with st.expander(f"{module['icon']} {module['title']} - {module['progress']}% abgeschlossen", expanded=False):
                st.progress(module['progress']/100)
                
                if module['title'] == "Grundlagen der Geldanlage":
                    st.write("""
                    **Lektion 1: Die Macht des Zinseszinses**
                    - Wie aus kleinen Beträgen Vermögen wird
                    - Der wichtigste Faktor: Zeit
                    - Praxisbeispiel: 100€ monatlich bei 7% Rendite
                    
                    **Interaktive Aufgabe:**
                    Berechne, wie viel 100€ monatlich bei 7% Rendite in 30 Jahren werden.
                    """)
                    
                    if st.button("Lösung anzeigen", key="zins_aufgabe"):
                        capital = 100 * (((1 + 0.07/12)**(12*30) - 1) / (0.07/12))
                        st.success(f"Ergebnis: {capital:,.0f}€")
                
                st.button(f"Modul fortsetzen: {module['title']}", use_container_width=True)

def footer_section():
    """Footer-Bereich mit Abschlussinformationen"""
    st.markdown("""
    <div class="footer">
        <h3>NEXUS Wealth</h3>
        <p>Dein Partner für finanzielle Freiheit</p>
        
        <div style="display: flex; justify-content: center; gap: 20px; margin: 1.5rem 0;">
            <a href="#" style="color: var(--text-light);">Über uns</a>
            <a href="#" style="color: var(--text-light);">Leistungen</a>
            <a href="#" style="color: var(--text-light);">Preise</a>
            <a href="#" style="color: var(--text-light);">Blog</a>
            <a href="#" style="color: var(--text-light);">Kontakt</a>
        </div>
        
        <p>© 2025 NEXUS Wealth GmbH | Alle Rechte vorbehalten</p>
        <p>Kontakt: kontakt@nexus-wealth.de | Support: +49 123 456 789</p>
        
        <p style="font-size:0.9em; margin-top:1.5rem; opacity:0.7;">
            Diese Anwendung dient nur zu Informationszwecken und stellt keine Finanzberatung dar. 
            Die dargestellten Ergebnisse sind Prognosen und keine Garantie für zukünftige Erträge.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===== HAUPTAPPLIKATION =====
def main():
    # Initialisiere Session State
    if 'goals' not in st.session_state:
        st.session_state.goals = []
    
    # App-Struktur
    hero_section()
    features_section()
    main_sections()
    wealth_academy()
    footer_section()

if __name__ == "__main__":
    main()
