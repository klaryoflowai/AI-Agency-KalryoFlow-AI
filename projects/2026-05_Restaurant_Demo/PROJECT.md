# PROJECT: Restaurant Demo — Automatizare comenzi si inventar

## Metadata
- **project_id:** 2026-05_Restaurant_Demo
- **client_id:** [uuid din Supabase — completat după creare]
- **status:** pilot-ready
- **created:** 2026-05-09
- **deadline:** 2026-06-05

---

## Brief Client
> Copiază EXACT ce a spus clientul. Nu parafaza.

```
Bună, avem un restaurant cu livrare proprie și comenzi care vin din trei locuri:
telefon, formular de pe site și mesaje WhatsApp. Azi o persoană verifică manual
comenzile, le copiază într-un Google Sheet, sună bucătăria dacă lipsește ceva,
actualizează stocurile la finalul zilei și trimite confirmări manual.

Problema e că pierdem mult timp la orele de vârf, mai apar greșeli la comenzi,
iar uneori vindem produse care nu mai sunt pe stoc. Vrem o soluție simplă care
să centralizeze comenzile, să verifice stocul, să trimită confirmări și să ne
dea un raport zilnic cu ce s-a vândut și ce trebuie reaprovizionat.

Nu vrem ceva foarte complicat. Folosim Google Sheets, Gmail, WhatsApp Business
și site WordPress. Bugetul orientativ este 2.500-4.000 EUR dacă putem vedea
rezultate în maximum o lună.
```

### Clarificări obținute
- [x] Volum comenzi: 40-80/zi în timpul săptămânii, 120+/zi în weekend.
- [x] Persoane implicate: manager restaurant, operator comenzi, bucătărie.
- [x] Prioritate principală: reducerea erorilor și raport zilnic de stoc.
- [x] Acceptă MVP fără runtime LLM plătit: da, preferă automatizări deterministe.

---

## Parametri Specifici Proiect
```yaml
industrie: "restaurant / food delivery"
sisteme_existente: ["WordPress", "Google Sheets", "Gmail", "WhatsApp Business"]
buget_client_eur: 3500
contact_tehnic: "manager restaurant"
contact_business: "proprietar"
limba_livrare: română     # limba în care livrăm documentele
complexitate: 0           # 1-5, completat de eval-agent
```

---

## Agenți Activați
> Bifează doar ce e necesar pentru acest proiect.
> Ordinea de execuție e întotdeauna top-down.

- [x] eval-agent           → `outputs/eval-agent/`
- [x] bd-agent             → `outputs/bd-agent/`
- [x] backend-agent      → `outputs/backend-agent/` (paralel cu frontend)
- [x] frontend-agent     → `outputs/frontend-agent/` (paralel cu backend)
- [x] ops-agent            → `outputs/ops-agent/`
- [x] qa-agent             → `outputs/qa-agent/`
- [x] marketing-agent      → `outputs/marketing-agent/`
- [x] client-success-agent → `outputs/client-success-agent/`

---

## Output-uri Așteptate
> Completat automat de eval-agent după prima rulare.

| Agent | Fișier Output | Status |
|-------|--------------|--------|
| eval-agent | evaluation.json, sow.md | PASS |
| bd-agent | proposal.md | PASS |
| backend-agent | implementation-report.json, README.md | PASS |
| frontend-agent | implementation-report.json, README.md | PASS |
| ops-agent | sop.md, workflow-design.json | PASS |
| marketing-agent | content.json | PASS |
| client-success-agent | client-success.json | PASS |
| qa-agent | qa-report.json, user-guide.md | PASS |

---

## Log Execuții

| Data | Agent | Status | Note |
|------|-------|--------|------|
| 2026-05-09 | proiect | created | Pilot fictiv pentru validarea fluxului end-to-end zero-API |
| 2026-05-09 | eval-agent | PASS | Evaluare, cost si SOW validate |
| 2026-05-09 | bd-agent | PASS | Propunere comerciala draft validata |
| 2026-05-09 | backend-agent | PASS | Design backend zero-runtime validat |
| 2026-05-09 | frontend-agent | PASS | Design UI operator validat |
| 2026-05-09 | ops-agent | PASS | Workflow si SOP validate |
| 2026-05-09 | marketing-agent | PASS | Draft case study anonimizat validat |
| 2026-05-09 | client-success-agent | PASS | Check-in 7 zile validat |
| 2026-05-09 | qa-agent | PASS | QA score 8.4, status APPROVED_WITH_NOTES |

---

## Delivery Checklist
- [ ] Propunere comercială aprobată de client
- [ ] Avans încasat
- [x] Toate output-urile din `outputs/` validate de QA Agent
- [x] Documentație client copiată în `delivery/`
- [ ] Prezentare finală făcută
- [ ] Sold încasat
- [x] Client Success Agent activat (follow-up 7/30/90 zile)
