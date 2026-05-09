# Client Context Pack — Restaurant Demo

## Identitate Client

- Client: Restaurant Demo
- Industrie: restaurant / food delivery
- Marime companie: IMM local, 10-25 angajati
- Contact business: proprietar
- Contact tehnic: manager restaurant
- Limba livrare: romana

## Ce Vinde / Ce Livreaza Clientul

- Mancare gatita pentru servire in locatie si livrare proprie.
- Clienti finali: consumatori locali, comenzi recurente la pranz si seara.
- Procese critice: preluare comenzi, confirmare, verificare stoc, raport zilnic.

## Ton si Preferinte

- Ton preferat: clar, practic, fara jargon tehnic.
- Cuvinte de evitat: "platforma enterprise", "AI magic", promisiuni fara cifre.
- Exemple bune: instructiuni scurte pentru operatori, rapoarte tabelare.
- Exemple de evitat: documentatie tehnica lunga pentru personal non-tehnic.

## Tool-uri si Sisteme

| Sistem | Rol | Acces | Observatii |
|--------|-----|-------|------------|
| WordPress | formular comenzi site | Partial | acces de test necesar |
| Google Sheets | registru comenzi si stoc | Partial | sheet de test pentru MVP |
| Gmail | confirmari si raport zilnic | Nu | se cere doar dupa aprobarea SOW |
| WhatsApp Business | comenzi manuale | Nu | MVP poate incepe cu captura manuala in sheet |

## Reguli Business

- Comenzile trebuie confirmate rapid in orele de varf.
- Daca un produs nu este pe stoc, operatorul trebuie alertat inainte de confirmare.
- Raportul zilnic trebuie sa arate produse vandute, produse low-stock si erori.
- Platile sau comenzile catre furnizori nu se fac automat in MVP.
- Datele clientilor finali nu se folosesc in materiale publice.

## Exemple

### Input bun

```text
Comanda #1842: 2x Pizza Margherita, 1x Limonada, livrare 19:30, str. Exemplu 12.
```

### Output bun

```text
Comanda #1842 confirmata. Stoc actualizat. Limonada a trecut sub pragul minim: reaprovizionare recomandata.
```

## Definitia Succesului

- Reducere erori de comanda: minim 50%.
- Timp operator economisit: minim 10 ore/luna.
- Raport zilnic generat automat sau semi-automat.
- QA score minim: 7.

## Decizii Aprobate

| Data | Decizie | Aprobat de | Note |
|------|---------|------------|------|
| 2026-05-09 | MVP zero-API LLM, fara plati autonome | CEO | Automatizari deterministe si operator uman pentru exceptii |
