import math
from datetime import datetime

# Prioritätsfaktoren für die Budgetverteilung
PRIORITÄTSFAKTOR = {1: 0.50, 2: 0.35, 3: 0.15}

def sparplan_rechner():
    # Benutzereingaben mit Validierung
    try:
        netto_gehalt = float(input("Monatliches Netto-Gehalt (€): "))
        fixkosten = float(input("Monatliche Fixkosten (Miete, Versicherungen etc., €): "))
        lebenshaltung = float(input("Durchschnittliche Lebenshaltungskosten (€): "))
    except ValueError:
        print("Ungültige Eingabe! Bitte nur Zahlen verwenden.")
        return

    # Grundberechnungen
    verfügbar = netto_gehalt - fixkosten - lebenshaltung
    if verfügbar <= 0:
        print("\n⚠️ Warnung: Deine Ausgaben übersteigen dein Einkommen! Bitte passe deine Eingaben an.")
        return

    # Sparzieleingabe
    sparziele = []
    print("\n===== SPARZIELE DEFINIEREN =====")
    
    while True:
        try:
            name = input("\nBezeichnung des Sparziels (z.B. 'Notgroschen'): ")
            if not name:
                break
                
            zielbetrag = float(input("Zielbetrag (€): "))
            priorität = int(input("Priorität (1=hoch, 2=mittel, 3=niedrig): "))
            
            if priorität not in [1, 2, 3]:
                print("Ungültige Priorität! Nur 1, 2 oder 3 erlaubt.")
                continue
                
        except ValueError:
            print("Ungültige Eingabe! Bitte korrekte Werte eingeben.")
            continue

        sparziele.append({
            'name': name,
            'zielbetrag': zielbetrag,
            'priorität': priorität,
            'aktuell': 0.0
        })

        if input("Weiteres Sparziel hinzufügen? (j/n): ").lower() != 'j':
            break

    # Budgetverteilung
    if sparziele:
        # Zähle Ziele pro Priorität
        prior_counts = {1: 0, 2: 0, 3: 0}
        for ziel in sparziele:
            prior_counts[ziel['priorität']] += 1

        # Verteile Budget
        for ziel in sparziele:
            faktor = PRIORITÄTSFAKTOR[ziel['priorität']] / prior_counts[ziel['priorität']]
            ziel['monatlich'] = verfügbar * faktor
    else:
        print("Keine Sparziele definiert. Programm beendet.")
        return

    # Monatliche Simulation
    monat = 0
    ziele_erreicht = 0
    gespart_insgesamt = 0
    
    print("\n" + "="*50)
    print(f"SPARPLAN START ({datetime.now().strftime('%d.%m.%Y')})")
    print("="*50)
    
    while ziele_erreicht < len(sparziele):
        monat += 1
        print(f"\n📅 Monat {monat}:")

        for ziel in sparziele:
            # Übersprungene Ziele
            if ziel['aktuell'] >= ziel['zielbetrag']:
                continue
                
            # Sparfortschritt
            ziel['aktuell'] += ziel['monatlich']
            gespart_insgesamt += ziel['monatlich']
            
            # Fortschrittsbalken
            prozent = min(100, (ziel['aktuell'] / ziel['zielbetrag']) * 100)
            bar_length = int(prozent // 5)
            progress_bar = '▓' * bar_length + '░' * (20 - bar_length)
            
            status = f"{ziel['name']}: {ziel['aktuell']:.2f}€/{ziel['zielbetrag']}€ ({prozent:.1f}%)"
            
            # Ziel erreicht
            if ziel['aktuell'] >= ziel['zielbetrag']:
                ziele_erreicht += 1
                überschuss = ziel['aktuell'] - ziel['zielbetrag']
                status += f" 🎉 (Überschuss: {überschuss:.2f}€)"
            
            print(f"  [{progress_bar}] {status}")

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

# Hauptprogramm
if __name__ == "__main__":
    print("""
    █▀ ▄▀█ █▀▄▀█ █▀█ █▀▀ █▀▀
    ▄█ █▀█ █░▀░█ █▄█ █▄▄ ██▄
    
    Sparplan Rechner 2.0 - Finanzziele erreicht!
    """)
    sparplan_rechner()
