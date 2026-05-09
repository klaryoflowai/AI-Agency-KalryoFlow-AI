# Proposal Template — BD Agent

Folosit de BD Agent pentru drafturi de propuneri comerciale.
REGULĂ: Propunerea nu se trimite fără aprobarea CEO.
Prețul vine ÎNTOTDEAUNA din Eval Agent output — nu se inventează.

---

# [Nume Client] — Automatizare [Proces Principal]

**Data:** [DD.MM.YYYY]
**Pregătit de:** KlaryoFlow AI Agency
**Valabil până:** [DD.MM.YYYY — 14 zile de la data propunerii]

---

## 1. Rezumat Executiv

[2-3 propoziții care descriu: ce problemă rezolvăm, ce facem concret, ce câștigă clientul.
Exemplu: "Comenzile voastre online sunt procesate manual, ceea ce ocupă ~X ore/săptămână și generează Y erori/lună. Vom automatiza fluxul complet de la primire comandă până la confirmare și actualizare stoc. Rezultatul: 0 procesări manuale, Z ore economisite lunar."]

---

## 2. Situația Actuală — Ce Costă Status Quo-ul

**Procesul actual:**
[Descriere în 3-5 rânduri a ce face clientul manual azi — fără judecată, doar observație]

**Costul estimat al procesului manual:**
- Timp investit lunar: [X ore × N persoane]
- Cost în timp (la [EUR/h] cost mediu): ~[EUR/lună]
- Erori estimate: [% sau număr] → impact: [descriere impact]

**Riscuri ale continuării fără automatizare:**
- [Risc 1: ex. scalabilitate — dacă volumul crește cu 50%, echipa nu mai face față]
- [Risc 2: ex. erori manuale care ajung la clienți finali]
- [Risc 3: ex. dependența de o singură persoană care cunoaște procesul]

---

## 3. Soluția Propusă

**Ce automatizăm:**
1. [Livrabil 1 — descriere clară, fără jargon]
2. [Livrabil 2]
3. [Livrabil 3]

**Cum funcționează (pentru non-tehnici):**
[2-3 propoziții care descriu fluxul din perspectiva clientului, nu a tehnologiei.
Ex: "Când un client plasează o comandă pe site, sistemul o preia automat, verifică stocul, trimite confirmarea și actualizează registrul — fără să atingeți nimic."]

**Ce tehnologii folosim:**
[Listă simplă, fără acronime — ex: "conectăm platforma voastră de comenzi cu un sistem de gestionare automată și o bază de date sincronizată în timp real"]

**Ce rămâne în responsabilitatea voastră:**
- Furnizarea acceselor la sistemele existente (primele 5 zile)
- Testarea soluției în etapa de UAT (User Acceptance Testing)
- [Altele dacă există]

---

## 4. Rezultate Așteptate

| Metric | Situația actuală | Post-implementare |
|--------|-----------------|-------------------|
| Ore procesare manuală/lună | [X ore] | 0 ore |
| Erori de procesare | [Y/lună] | [<1 sau 0] |
| Timp de răspuns la client | [ore/zile] | [minute] |
| Scalabilitate maximă | [volum actual] | [volum posibil] |

**ROI estimat:**
- Investiție totală: [EUR] (see Secțiunea 6)
- Economii lunare: ~[EUR/lună] (timp economisit × cost orar)
- Break-even: [N luni]

---

## 5. Scope — Ce Este Inclus / Exclus

**INCLUS:**
- [Item 1]
- [Item 2]
- [Item 3]
- Testing și validare (QA)
- Documentație utilizator (ghid de utilizare simplu)
- Bug-fix-uri timp de 14 zile post-livrare

**NEINCLUS:**
- [Item exclus 1 — ex: migrarea datelor istorice]
- [Item exclus 2 — ex: design grafic sau branding]
- [Item exclus 3 — ex: training utilizatori extins]
- Modificări de scope după semnarea SOW (cotate separat)
- Costurile de hosting / abonamente platforme terțe (dacă există)

---

## 6. Timeline

| Săptămâna | Activitate | Milestone |
|-----------|------------|-----------|
| 1 | Setup mediu, accese, configurare inițială | Mediu de lucru gata |
| 2 | Implementare [componenta principală] | Demo intern |
| 3 | Testare, ajustări, UAT cu clientul | Aprobare client |
| [X] | Livrare finală, documentație, handover | Proiect livrat |

**Condiție de start:** de la data primirii avansului și a acceselor necesare.

---

## 7. Investiție

### Setup (plată unică)
**[EUR] + TVA**

Detaliu calcul (transparent):
- [Tip task 1]: [ore estimate] × [EUR/h] = [subtotal]
- [Tip task 2]: [ore estimate] × [EUR/h] = [subtotal]
- Buffer risc [dacă complexitate ≥ 4]: +[%]

### Mentenanță Opțională (lunar)
**[EUR]/lună + TVA**
Include: monitorizare, bug-fix-uri minore, actualizări de compatibilitate.
Fără contract de mentenanță: intervențiile post-garanție se cotează la [EUR/h].

### Runtime LLM Client-Side (dacă este necesar)
**Estimat separat — aprobat înainte de activare.**
[Dacă `runtime_llm_needed: true` în evaluare: "Estimat ~[EUR]/lună la volum de [X runs]. Activat doar cu aprobare scrisă."]
[Dacă `runtime_llm_needed: false`: "Nu este necesară nicio cheltuială LLM runtime pentru această implementare."]

### Structura Plăților
- 50% avans la semnarea contractului: **[EUR]**
- 50% la livrarea finală aprobată de client: **[EUR]**

---

## 8. Termeni

- **Garanție bug-fix:** 14 zile de la livrare — orice bug din implementarea noastră se rezolvă gratuit
- **Modificări de scope:** evaluate și cotate separat, cu aprobare scrisă înainte de execuție
- **Proprietatea codului:** transferată la plata integrală
- **Confidențialitate:** datele clientului nu sunt shared sau folosite în alte proiecte
- **Anulare:** dacă clientul anulează după semnare, avansul nu se returnează (acoperă munca de configurare)

---

## 9. Pași Următori

Dacă propunerea e în regulă:

1. **Răspundeți cu "DA"** la acest email sau semnați SOW-ul atașat
2. **Avansul** se poate plăti prin transfer bancar (detalii la confirmare)
3. **Kickoff call** — programăm 30 minute pentru a alinia accesele și expectanțele
4. **Startul lucrărilor** — în [X zile lucrătoare] de la primirea avansului

**CTA:** Răspundeți la acest email sau sunați la [telefon CEO] — rezolvăm în 5 minute.

---

## Întrebări Frecvente (opțional — adaugă dacă e relevant)

**Q: Ce se întâmplă dacă nu funcționează cum am discutat?**
A: Aveți 14 zile de garanție — orice deviere față de ce e în SOW o rezolvăm gratuit.

**Q: Avem nevoie de un IT intern?**
A: Nu. Ne ocupăm noi de toată implementarea, aveți nevoie doar să ne dați accesele.

**Q: Cât timp durează până vedem primele rezultate?**
A: Primele rezultate le vedeți în săptămâna [X] — în faza de testare, înainte de livrarea finală.

---

*Propunere pregătită de BD Agent pe baza Eval Agent output (project_id: [ID]).*
*Prețurile sunt orientative și se confirmă în SOW final semnat.*
