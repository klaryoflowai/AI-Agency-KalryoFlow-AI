# QA Evidence Checklist

Fiecare livrabil client trebuie sa aiba dovezi verificabile, nu doar opinie.

## Metadata

- project_id:
- agent verificat:
- QA operator:
- data:

## Dovezi Obligatorii

- [ ] Brief/SOW comparat cu output-ul final.
- [ ] Output JSON validat cu `python3 execution/agency.py validate`.
- [ ] Sursele/inputurile folosite sunt listate.
- [ ] Datele clientului sunt anonimizate cand output-ul e public.
- [ ] Nu exista runtime LLM platit neaprobat.
- [ ] Nu exista secrete in repo sau output.
- [ ] Exista handover sau user guide daca livrabilul merge la client.

## Pentru UI / Browser Automation

- [ ] Screenshot desktop.
- [ ] Screenshot mobile, daca e relevant.
- [ ] Flow critic testat end-to-end.
- [ ] Stari de eroare verificate.
- [ ] Date introduse in formulare validate.

## Pentru Backend / Integrari

- [ ] Migrare sau schema verificata.
- [ ] Webhook/API testat cu input valid.
- [ ] Input invalid testat.
- [ ] Loguri si erori verificate.
- [ ] Fallback uman documentat.

## Scor QA

| Criteriu | Scor 1-10 | Note |
|----------|-----------|------|
| Functionalitate | | |
| Acoperire SOW | | |
| Securitate | | |
| UX / claritate | | |
| Handover | | |

## Decizie

- QA score:
- Status: APPROVED / APPROVED_WITH_NOTES / NEEDS_FIXES
- Bugs:
- Riscuri ramase:
- Conditii inainte de livrare:
