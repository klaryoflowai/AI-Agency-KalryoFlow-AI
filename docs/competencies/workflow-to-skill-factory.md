# Workflow-to-Skill Factory

Aceasta este competenta centrala a agentiei: transformam un workflow manual real intr-un sistem operational repetabil, apoi intr-un skill reutilizabil numai dupa ce workflow-ul a fost rulat si validat.

Nu cream `SKILL.md` din teorie. Cream skill-uri dupa dovezi: input real, output acceptat, edge cases, QA si lectii invatate.

## Obiectiv

Pentru fiecare proces client important, agentia trebuie sa poata produce:

1. `Client Context Pack` complet.
2. `Workflow Capture` cu pasii reali ai procesului.
3. Primul run controlat cu Codex/Claude Code ca operatori.
4. QA Evidence Pack cu teste, surse, screenshots/loguri si scor.
5. Skill Candidate draft, daca procesul merita reutilizat.
6. Template de livrare client: SOP, handover si checklist.

## Cand Activam Fabrica

- Procesul se repeta lunar/saptamanal/zilnic.
- Clientul are multe exceptii sau reguli tacite.
- Output-ul are un standard clar de calitate.
- E probabil sa refolosim acelasi tip de workflow pentru alti clienti.
- Un run manual cu operator AI a produs deja rezultat acceptat de QA.

Nu activam fabrica pentru taskuri one-off, research generic sau livrabile fara sansa reala de reutilizare.

## Flux Standard

### 1. Capture

Colectam procesul manual asa cum se intampla azi:

- cine face procesul;
- ce inputuri primeste;
- ce tool-uri foloseste;
- ce decizii ia;
- ce exceptii apar;
- cum arata un output bun si unul prost;
- ce verificari face omul inainte de a livra.

Template: `resources/templates/workflow-capture-template.md`.

### 2. Context Pack

Centralizam memoria clientului:

- brief original;
- ton si preferinte;
- tool-uri si acces;
- exemple bune/rele;
- reguli speciale;
- decizii si tradeoff-uri aprobate;
- date care nu pot fi publicate;
- definitia succesului.

Template: `resources/templates/client-context-pack-template.md`.

### 3. Controlled Run

Runner-ul genereaza prompt packet-ul, operatorul executa, apoi output-ul este salvat in `projects/<id>/outputs/<agent>/`.

Reguli:

- un agent lucreaza doar in boundary-ul lui;
- output JSON valid;
- fara API LLM platit in MVP;
- orice output extern are aprobare CEO;
- orice deliverable client trece prin QA Agent.

### 4. QA Evidence

QA nu verifica doar textul final. QA verifica dovada:

- surse/inputuri folosite;
- teste rulate;
- screenshots cand exista UI/browser;
- comparatie cu brief/SOW;
- riscuri ramase;
- scor si decizie.

Template: `resources/templates/qa-evidence-checklist.md`.

### 5. Skill Candidate

Un workflow devine candidat de skill doar daca:

- s-a repetat de cel putin 2 ori sau are probabilitate mare de reutilizare;
- are output schema stabil;
- QA score a fost >= 7;
- edge cases sunt cunoscute;
- exista exemple de input/output;
- CEO aproba crearea sau modificarea unui `SKILL.md`.

Template: `resources/templates/skill-candidate-template.md`.

### 6. Package

La final, pachetul livrabil include:

- output client;
- SOP;
- QA evidence;
- handover;
- recomandari de automatizare viitoare;
- daca e cazul, skill candidate pentru biblioteca interna.

## Roluri Codex si Claude Code

| Etapa | Owner Preferat | Motiv |
|-------|----------------|-------|
| Capture tehnic / integrari | Codex | intelege backend, date, fluxuri si verificari |
| Copy, SOP, skill wording | Claude Code | structurare, claritate, business language |
| Browser automation | Codex sau Claude, cu ownership clar | depinde de proiect |
| QA evidence | operator independent | trebuie separat de implementator |
| Integrare finala | Codex | repo, teste, CI, validare |

## Browser Automation Competency

Pentru IMM-uri, multe procese nu au API. Agentia trebuie sa poata automatiza sau testa:

- formulare web;
- dashboard-uri SaaS;
- email/CRM flows;
- marketplace-uri;
- descarcari CSV/PDF;
- verificare vizuala cu screenshots.

Reguli:

- prefera API cand exista si e stabil;
- foloseste browser automation cand API-ul lipseste sau este inaccesibil;
- nu ocoli rate limits, paywalls sau termeni de utilizare;
- nu introduce credentiale in repo;
- salveaza screenshots/loguri in `artefacts/` sau output-ul proiectului;
- QA verifica vizual pasii critici.

## Agentic Payments Guardrails

Nu implementam plati autonome in MVP. Pentru design viitor, orice plata facuta sau pregatita de agent cere:

- aprobare umana explicita;
- limita pe tranzactie si pe luna;
- card virtual sau metoda cu limitare;
- audit log complet;
- alerta la esec sau abatere;
- posibilitate de anulare/rollback;
- reconciliere in raportul clientului.

Pana cand exista aprobare explicita, agentii pot doar sa pregateasca recomandari, facturi draft sau liste de achizitii, nu sa execute plati.

## Definition of Done

Un workflow este suficient de matur pentru skill daca:

- exista Context Pack complet;
- exista Capture complet;
- exista cel putin un run controlat;
- exista QA Evidence Pack;
- output schema este stabila;
- edge cases sunt documentate;
- costurile runtime sunt zero sau aprobate explicit;
- CEO a aprobat transformarea in `SKILL.md`.
