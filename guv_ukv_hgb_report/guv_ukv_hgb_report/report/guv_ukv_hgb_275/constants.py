GUV_POSITIONS = [
    "1 - Umsatzerlöse",
    "2 - Herstellungskosten der zur Erzielung der Umsatzerlöse erbrachten Leistungen",
    "3 - Bruttoergebnis vom Umsatz",
    "4 - Vertriebskosten",
    "5 - allgemeine Verwaltungskosten",
    "6 - sonstige betriebliche Erträge",
    "7 - sonstige betriebliche Aufwendungen",
    "8 - Erträge aus Beteiligungen",
    "9 - Erträge aus anderen Wertpapieren und Ausleihungen des Finanzanlagevermögens",
    "10 - sonstige Zinsen und ähnliche Erträge",
    "11 - Abschreibungen auf Finanzanlagen und auf Wertpapiere des Umlaufvermögens",
    "12 - Zinsen und ähnliche Aufwendungen",
    "13 - Steuern vom Einkommen und vom Ertrag",
    "14 - Ergebnis nach Steuern",
    "15 - sonstige Steuern",
    "16 - Jahresüberschuß/Jahresfehlbetrag",
 ]

HERSTELLUNGSKOSTEN = GUV_POSITIONS[2-1]
VERTRIEBSKOSTEN = GUV_POSITIONS[4-1]
VERWALTUNGSKOSTEN = GUV_POSITIONS[5-1]
SONSTIGE_AUFWENDUNGEN = GUV_POSITIONS[7-1]

VERTRIEBSKOSTEN_PREFIX = "4 - "
VERWALTUNGSKOSTEN_PREFIX = "5 - "
SONSTIGE_AUFWENDUNGEN_PREFIX = "7 - "

# Cost center types
CC_HERSTELLUNG = "Herstellungskosten"
CC_VERTRIEB = "Vertriebskosten"
CC_VERWALTUNG = "Verwaltungskosten"
CC_SONSTIGE = "Sonstige betriebliche Aufwendungen"
