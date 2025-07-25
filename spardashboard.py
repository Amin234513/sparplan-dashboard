import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import tempfile
import io

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
    # Einfacher Dummy-PDF-Bytes-String, damit der Download funktioniert, ohne fpdf zu benötigen
    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Count 1 /Kids [3 0 R] >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n50 150 Td\n(🔥 FIREFLY Premium Sparguide) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000061 00000 n \n0000000112 00000 n \n0000000207 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n306\n%%EOF"
    return pdf_bytes


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
        
        pdf_bytes = generate_ebook()

        st.download_button(
            label="📥 Jetzt E-Book herunterladen",
            data=pdf_bytes,
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
            savings_rate = savings / income * 100
            st.metric("Sparquote", f"{savings_rate:.1f}%", f"{savings:,.0f}€")
    
    with col2:
        with st.container():
            st.markdown("### 🏆 FIRE-Erreichbarkeit")
            annual_expenses = st.number_input("Jährliche Ausgaben (€)", 10000, 100000, 30000)
            current_assets = st.number_input("Aktuelles Vermögen (€)", 0, 1000000, 50000)
            monthly_savings = st.number_input("Monatliche Sparrate (€)", 100, 5000, 1000)
            
            fire_target = annual_expenses * 25
            years = np.nper(0.06/12, -monthly_savings, -current_assets, fire_target) / 12
            st.metric("Finanzielle Freiheit erreicht in", f"{years:.1f} Jahren")
    
    with col3:
        with st.container():
            st.markdown("### 💰 Steuerersparnis-Simulator")
            capital_gains = st.number_input("Kapitalerträge (€)", 0, 100000, 5000)
            tax_before = capital_gains * 0.26375
            tax_after = max(0, (capital_gains - 1000) * 0.26375)
            savings = tax_before - tax_after
            
            st.metric("Steuerlast ohne Optimierung", f"{tax_before:,.0f}€")
            st.metric("Mit Freistellungsauftrag", f"{tax_after:,.0f}€")
            st.metric("Ersparnis", f"{savings:,.0f}€", delta_color="inverse")

# ===== HAUPTAPPLIKATION =====
pages = {
    "📊 Dashboard": dashboard_page,
    "🎯 Sparziele": goals_page,
    "📚 Premium Sparguide": ebook_page
}

# Seitenauswahl in der Sidebar
with st.sidebar:
    st.title("🔥 FIREFLY")
    page = st.radio("Navigation", list(pages.keys()))
    
    st.markdown("---")
    st.markdown("### Dein Fortschritt")
    st.progress(0.65, text="Finanzielle Freiheit: 65%")
    st.caption("🔥 12 von 18 Meilensteinen erreicht")
    
    st.markdown("---")
    st.markdown("### 🔔 Benachrichtigungen")
    st.info("🎉 Sparziel 'Notfallfonds' erreicht!")
    st.warning("⚠️ Portfolio-Rebalancing empfohlen")
    st.info("💡 Neues E-Book-Kapitel verfügbar: Steuertricks")

# Aktive Seite anzeigen
pages[page]()
