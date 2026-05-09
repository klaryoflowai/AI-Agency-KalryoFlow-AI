# PROJECT: [NumeClient] — [Descriere scurtă 1 rând]

## Metadata
- **project_id:** YYYY-MM_NumeClient
- **client_id:** [uuid din Supabase — completat după creare]
- **status:** draft
- **created:** [data azi]
- **deadline:** [data deadline]

---

## Brief Client
> Copiază EXACT ce a spus clientul. Nu parafaza.

```
[textul clientului aici]
```

### Clarificări obținute
- [ ] [întrebare 1]: [răspuns]
- [ ] [întrebare 2]: [răspuns]

---

## Parametri Specifici Proiect
```yaml
industrie: ""
sisteme_existente: []     # ex: WooCommerce, Gmail, HubSpot
buget_client_eur: 0
contact_tehnic: ""
contact_business: ""
limba_livrare: română     # limba în care livrăm documentele
complexitate: 0           # 1-5, completat de eval-agent
```

---

## Agenți Activați
> Bifează doar ce e necesar pentru acest proiect.
> Ordinea de execuție e întotdeauna top-down.

- [x] eval-agent           → `outputs/eval-agent/`
- [ ] bd-agent             → `outputs/bd-agent/`
- [ ] backend-agent      → `outputs/backend-agent/` (paralel cu frontend)
- [ ] frontend-agent     → `outputs/frontend-agent/` (paralel cu backend)
- [ ] ops-agent            → `outputs/ops-agent/`
- [ ] qa-agent             → `outputs/qa-agent/`
- [ ] marketing-agent      → `outputs/marketing-agent/`
- [ ] client-success-agent → `outputs/client-success-agent/`

---

## Output-uri Așteptate
> Completat automat de eval-agent după prima rulare.

| Agent | Fișier Output | Status |
|-------|--------------|--------|
| eval-agent | evaluation.json, sow.md | ⏳ pending |
| bd-agent | proposal.md | ⏳ pending |
| backend-agent | implementation-report.json, README.md | ⏳ pending |
| frontend-agent | implementation-report.json, README.md | ⏳ pending |
| ops-agent | sop.md, workflow-design.json | ⏳ pending |
| qa-agent | qa-report.json, user-guide.md | ⏳ pending |

---

## Log Execuții

| Data | Agent | Status | Note |
|------|-------|--------|------|
| | | | |

---

## Delivery Checklist
- [ ] Propunere comercială aprobată de client
- [ ] Avans încasat
- [ ] Toate output-urile din `outputs/` validate de QA Agent
- [ ] Documentație client copiată în `delivery/`
- [ ] Prezentare finală făcută
- [ ] Sold încasat
- [ ] Client Success Agent activat (follow-up 7/30/90 zile)
