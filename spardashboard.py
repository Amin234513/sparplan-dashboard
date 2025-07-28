import math
from datetime import datetime

def sparplan_rechner():
    # Benutzereingaben
    netto_gehalt = float(input("Monatliches Netto-Gehalt (€): "))
    fixkosten = float(input("Monatliche Fixkosten (Miete, Versicherungen etc., €): "))
    lebenshaltung = float(input("Durchschnittliche Lebenshaltungskosten (€): "))
    
    # Berechnungen
    verfügbar = netto_gehalt - fixkosten - lebenshaltung
    if verfügbar <= 0:
        print("\n⚠️ Warnung: Deine Ausgaben übersteigen dein Einkommen! Bitte passe deine Eingaben an.")
        return
    
    # Sparzieleingabe
    print("\n===== SPARZIELE DEFINIEREN =====")
    sparziele = []
    prozent_summe = 0
    ziel_id = 1
    
    while True:
        print(f"\nSparziel #{ziel_id}:")
        name = input("  Bezeichnung (z.B. 'Notgroschen', 'Urlaub'): ")
        zielbetrag = float(input("  Zielbetrag (€): "))
        priorität = int(input("  Priorität (1=hoch, 2=mittel, 3=niedrig): "))
        
        sparziele.append({
            'name': name,
            'zielbetrag': zielbetrag,
            'priorität': priorität,
            'aktuell': 0.0
        })
        
        ziel_id += 1
        if input("Weiteres Sparziel hinzufügen? (j/n): ").lower() != 'j':
            break
    
    # Budgetverteilung nach Priorität
    PRIORITÄTSFAKTOR = {1: 0.5, 2: 0.35, 3: 0.15}
    for ziel in sparziele:
        anteil = PRIORITÄTSFAKTOR[ziel['priorität']]
        ziel['monatlich'] = verfügbar * anteil
    
    # Monatliche Simulation
    print("\n" + "="*50)
    print(f"START SPARPLAN ({datetime.now().strftime('%d.%m.%Y')})")
    print("="*50)
    
    monat = 0
    ziele_erreicht = 0
    gespart_insgesamt = 0
    
    while ziele_erreicht < len(sparziele):
        monat += 1
        print(f"\n📅 Monat {monat}:")
        
        # Sparfortschritt berechnen
        for ziel in sparziele:
            if ziel['aktuell'] < ziel['zielbetrag']:
                ziel['aktuell'] += ziel['monatlich']
                gespart_insgesamt += ziel['monatlich']
                
                # Visualisierung
                prozent = (ziel['aktuell'] / ziel['zielbetrag']) * 100
                bar_length = int(prozent // 5)
                progress_bar = '▓' * bar_length + '░' * (20 - bar_length)
                
                print(f"  [{progress_bar}] {ziel['name']}: {ziel['aktuell']:.2f}€/{ziel['zielbetrag']}€ ({min(prozent, 100):.1f}%)")
                
                if ziel['aktuell'] >= ziel['zielbetrag']:
                    ziele_erreicht += 1
                    überschuss = ziel['aktuell'] - ziel['zielbetrag']
                    print(f"  🎉 Ziel erreicht! Überschuss: {überschuss:.2f}€")
        
        # Frühzeitiger Abbruch bei allen Zielen erreicht
        if ziele_erreicht == len(sparziele):
            break
    
    # Zusammenfassung
    jahre = monat / 12
    print("\n" + "="*50)
    print("💶 FINANZBERICHT")
    print("="*50)
    print(f"Gesparte Summe: {gespart_insgesamt:.2f}€")
    print(f"Benötigte Zeit: {monat} Monate ({jahre:.1f} Jahre)")
    print(f"Monatliche Sparrate: {verfügbar:.2f}€")
    print("\nEinzelziele:")
    for ziel in sparziele:
        monate_ziel = math.ceil(ziel['zielbetrag'] / ziel['monatlich'])
        print(f"  - {ziel['name']}: {monate_ziel} Monate")

# Programmstart
if __name__ == "__main__":
    print("""
    █▀ ▄▀█ █▀▄▀█ █▀█ █▀▀ █▀▀
    ▄█ █▀█ █░▀░█ █▄█ █▄▄ ██▄
    
    Willkommen zum Sparplan-Rechner!
    """)
    sparplan_rechner()
