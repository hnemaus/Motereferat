# Møtereferat-hjelper

A CLI tool that turns messy meeting notes into structured summaries with decisions and action points — using Claude AI. Output is formatted and optionally saved to file.

**Author:** Hanne Emaus — informatics student (robotics & AI) at UiO.

---

## Why I built this

One of the most common AI use cases in commercial organisations is turning unstructured notes into structured output. This is a practical implementation of that pattern — relevant for sales teams, project managers, and anyone who sits in a lot of meetings.

## What it produces

From raw notes, the tool extracts:

- **Summary** — 2–3 sentences describing what the meeting was about
- **Decisions** — explicit decisions made during the meeting
- **Action points** — task, responsible person, and deadline
- **Next meeting** — date/time if mentioned

## Setup

```bash
pip install anthropic python-dotenv
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=your-key-here
```

## Usage

```bash
python motereferat.py
```

Paste your notes, press Enter on an empty line, and get a formatted summary.

## Example output

```
========================================================
  MØTEREFERAT: KVARTALSMØTE Q2 SALG
  Generert: 19.04.2026
========================================================

OPPSUMMERING
Møtet handlet om Q2-resultater og plan for Q3...

BESLUTNINGER
  1. Ny prismodell innføres fra 1. juni
  2. Sara overtar kundeansvaret for region nord

ACTION POINTS
  Oppgave                             Ansvarlig            Frist
  -----------------------------------------------------------------
  Oppdatere prisliste                 Sara                 01.06
  Sende ut kundebrev                  Ikke spesifisert     Uke 20

NESTE MØTE: Tirsdag 28. april kl. 10:00
```

## Skills demonstrated

- Anthropic Python SDK
- Structured output with JSON schema prompting
- JSON parsing and error handling
- Formatted CLI output (tabular)
- Real-world workflow automation
