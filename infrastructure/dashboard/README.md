# KlaryoFlow AI Dashboard

Next.js dashboard MVP pentru operarea agentiei zero-API.

## Ce include

- `/` - cockpit pentru proiecte, statusuri, QA score si operator queue.
- `/projects/new` - intake local-first si pachet de comenzi pentru Codex.
- `/projects/[id]` - detaliu proiect, agent runs, livrabile si urmatorul sync.

Datele sunt momentan demo/local in `src/lib/agency-data.ts`. Conectarea live la
Supabase ramane pasul urmator, dupa ce exista proiectul Supabase si service key-ul
local este configurat.

## Comenzi

```bash
cd infrastructure/dashboard
npm ci
npm run dev
npm run lint
npm run build
```

## Guardrails

- Nu introduce chei Supabase sau chei LLM in codul frontend.
- Nu adauga runtime LLM paid in dashboard pentru MVP.
- Orice mutatie live catre Supabase trebuie sa treaca prin backend/server action
  cu initializare lazy si aprobare explicita.
