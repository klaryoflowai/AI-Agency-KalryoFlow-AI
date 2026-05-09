# Workflow Capture — Restaurant Demo

## Metadata

- project_id: 2026-05_Restaurant_Demo
- client: Restaurant Demo
- proces: order intake and stock validation
- owner client: manager restaurant
- owner agentie: Codex operator
- data capturii: 2026-05-09

## Procesul Manual Curent

1. Operatorul primeste comenzi din telefon, site si WhatsApp.
2. Comanda este copiata manual in Google Sheets.
3. Operatorul verifica informal daca produsul exista si daca stocul este suficient.
4. Daca lipseste ceva, operatorul suna bucataria sau managerul.
5. Confirmarea este trimisa manual.
6. La final de zi, stocul si vanzarile sunt reconciliate manual.

## Inputuri

| Input | Sursa | Format | Exemplu | Frecventa |
|-------|-------|--------|---------|-----------|
| Comanda | WordPress / telefon / WhatsApp | text / row | 2x Pizza Margherita | 40-120/zi |
| Catalog | Google Sheets | tabel | SKU, nume, alias | saptamanal |
| Stoc | Google Sheets | tabel | SKU, cantitate, prag minim | zilnic |

## Outputuri

| Output | Format | Cine il foloseste | Criterii de calitate |
|--------|--------|-------------------|----------------------|
| Confirmare draft | text | operator | produs, cantitate, ora, status |
| Exceptie | row | operator/manager | motiv clar si actiune recomandata |
| Raport zilnic | tabel | manager | vanzari, low-stock, exceptii |

## Decizii si Reguli

- Automatizabil: potrivire produs, verificare prag stoc, raport zilnic.
- Cere om: produs necunoscut, stoc incert, client fara contact, supplier reorder.
- Escaladare: out_of_stock in timpul orelor de varf.

## Edge Cases

| Caz | Cum apare | Ce face omul azi | Recomandare automatizare |
|-----|-----------|------------------|--------------------------|
| Produs scris diferit | WhatsApp/telefon | intreaba bucataria | alias catalog |
| Stoc incert | final de zi neactualizat | verifica fizic | needs_review |
| Client fara telefon | formular incomplet | cauta manual | hold confirmation |

## Run Controlat

- Operator: Codex
- Agent sequence: eval, bd, backend, frontend, ops, marketing, client-success, qa
- Validare: toate output-urile active au PASS.

## Lectii Pentru Skill

- QA trebuie sa ramana ultimul gate.
- Context Pack-ul reduce ambiguitatea pentru toate output-urile.
- Pentru restaurante, phase 1 trebuie sa ramana determinist si cu operator uman pe exceptii.
