# Regula: Granițele Agenților

## Separarea Tehnică
Nu există agent tehnic generic. Execuția se împarte astfel:
- `backend-agent`: API, DB, integrări, server-side.
- `frontend-agent`: UI, dashboard, componente, client-side.
- `qa-agent`: teste, verificare SOW, user guide, livrare.

## Orchestrator
Orchestratorul rutează și coordonează. Nu scrie cod de implementare și nu livrează direct către client.

## Output
Fiecare agent scrie doar în folderul propriu:
`projects/<project_id>/outputs/<agent-name>/`

## Handoff
Backend și Frontend pot rula în paralel, dar trebuie să producă handoff explicit pentru QA. QA rulează ultimul și poate bloca livrarea.

