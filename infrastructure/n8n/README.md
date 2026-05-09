# n8n Orchestrator MVP

Acest folder contine workflow-uri n8n pentru orchestrarea MVP zero-API.

## Principiu Important

n8n Cloud nu ruleaza comenzi shell locale. Din motive de securitate si compatibilitate Cloud, workflow-urile noastre NU folosesc `Execute Command`.

Rolul n8n in MVP:

- primeste evenimente prin Webhook;
- valideaza payload-ul;
- standardizeaza statusul proiectului/agentului;
- raspunde cu urmatoarea actiune recomandata;
- ulterior poate scrie in Supabase prin HTTP Request credentials.

Rolul `execution/agency.py` ramane local/operator-side:

- genereaza prompt packets;
- valideaza output JSON;
- face dry-run sau apply pentru Supabase sync.

## Workflow-uri

| Fisier | Rol |
|--------|-----|
| `workflows/agency-orchestrator-webhook.json` | webhook Cloud-safe pentru evenimente de proiect/agent |

## Evenimente Acceptate

- `project.created`
- `agent.prepared`
- `agent.output_submitted`
- `agent.validated`
- `qa.approved`
- `delivery.ready`

## Exemplu Request

```json
{
  "event_type": "agent.validated",
  "project_id": "2026-05_Restaurant_Demo",
  "agent": "eval-agent",
  "status": "PASS"
}
```

## Validare Locala

```bash
python3 execution/validate_n8n_workflows.py
```

Validatorul verifica:

- JSON valid;
- existenta Webhook + Respond to Webhook;
- lipsa `Execute Command`;
- lipsa credentialelor/secrets in workflow JSON;
- existenta evenimentelor suportate.

## Import in n8n

1. Deschide n8n.
2. Import from File.
3. Alege `infrastructure/n8n/workflows/agency-orchestrator-webhook.json`.
4. Testeaza cu Test URL.
5. Publica workflow-ul numai dupa ce webhook-ul returneaza raspunsul asteptat.

## Guardrails

- Nu include chei Supabase sau token-uri in JSON.
- Nu trimite emailuri sau mesaje client fara aprobare CEO.
- Nu declanseaza runtime LLM API.
- Nu face plati.
- Nu ruleaza shell commands in n8n Cloud.
