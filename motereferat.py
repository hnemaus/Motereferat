"""
Møtereferat-hjelper
===================
Tar inn rånotater fra et møte og genererer et ryddig referat
med oppsummering, beslutninger og action points.

Krever: pip install anthropic python-dotenv
Forfatter: Hanne Emaus
"""

import os
import json
from datetime import date
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM = """Du er en presis møtereferent. Du får rånotater fra et møte og returnerer KUN et JSON-objekt – ingen annen tekst.

JSON-strukturen skal være nøyaktig slik:
{
  "tittel": "Kort tittel som beskriver møtet",
  "oppsummering": "2-3 setninger som oppsummerer hva møtet handlet om",
  "beslutninger": ["beslutning 1", "beslutning 2"],
  "action_points": [
    {"oppgave": "hva som skal gjøres", "ansvarlig": "hvem (eller 'Ikke spesifisert')", "frist": "når (eller 'Ikke spesifisert')"}
  ],
  "neste_møte": "dato/tidspunkt eller 'Ikke nevnt'"
}"""


def analyser_notat(notat: str) -> dict:
    klient = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    respons = klient.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Rånotater:\n\n{notat}"}]
    )
    tekst = respons.content[0].text.strip()
    if tekst.startswith("```"):
        tekst = tekst.split("```")[1]
        if tekst.startswith("json"):
            tekst = tekst[4:]
    return json.loads(tekst)


def skriv_referat(data: dict, notat: str) -> str:
    linjer = []
    linjer.append("=" * 56)
    linjer.append(f"  MØTEREFERAT: {data['tittel'].upper()}")
    linjer.append(f"  Generert: {date.today().strftime('%d.%m.%Y')}")
    linjer.append("=" * 56)
    linjer.append(f"\nOPPSUMMERING\n{data['oppsummering']}")

    if data.get("beslutninger"):
        linjer.append("\nBESLUTNINGER")
        for i, b in enumerate(data["beslutninger"], 1):
            linjer.append(f"  {i}. {b}")

    if data.get("action_points"):
        linjer.append("\nACTION POINTS")
        linjer.append(f"  {'Oppgave':<35} {'Ansvarlig':<20} {'Frist'}")
        linjer.append("  " + "-" * 65)
        for ap in data["action_points"]:
            linjer.append(f"  {ap['oppgave']:<35} {ap['ansvarlig']:<20} {ap['frist']}")

    linjer.append(f"\nNESTe MØTE: {data['neste_møte']}")
    linjer.append("=" * 56)
    return "\n".join(linjer)


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("FEIL: Sett ANTHROPIC_API_KEY i .env-filen.")
        return

    print("=" * 56)
    print("  Møtereferat-hjelper  |  Skrevet av Hanne Emaus")
    print("=" * 56)
    print("\nLim inn møtenotatene dine (avslutt med tom linje):\n")

    linjer = []
    while True:
        linje = input()
        if linje == "":
            break
        linjer.append(linje)

    if not linjer:
        print("Ingen notater oppgitt.")
        return

    notat = "\n".join(linjer)
    print("\nAnalyserer notater...\n")

    try:
        data = analyser_notat(notat)
        referat = skriv_referat(data, notat)
        print(referat)

        lagre = input("\nLagre referat til fil? (j/n): ").strip().lower()
        if lagre == "j":
            filnavn = f"referat_{date.today().isoformat()}.txt"
            with open(filnavn, "w", encoding="utf-8") as f:
                f.write(referat)
            print(f"Lagret til {filnavn}")
    except json.JSONDecodeError:
        print("Kunne ikke tolke svaret fra AI. Prøv igjen.")
    except Exception as e:
        print(f"Feil: {e}")


if __name__ == "__main__":
    main()
