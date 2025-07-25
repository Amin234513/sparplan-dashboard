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
        
        # Visualisierung
        st.subheader("Vermögensentwicklung")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(entwicklung))),
            y=entwicklung,
            mode='lines',
            name='Nominales Vermögen',
            line=dict(color='#00d2ff', width=3)
        ))  # Hier wurde die fehlende schließende Klammer hinzugefügt
        
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
