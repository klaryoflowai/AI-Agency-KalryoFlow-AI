# QA Evidence — Restaurant Demo Pilot

## Commands

```bash
python3 execution/agency.py status 2026-05_Restaurant_Demo
python3 execution/agency.py next 2026-05_Restaurant_Demo
python3 execution/validate_supabase_migrations.py
python3 execution/hooks/scan_forbidden_runtime.py
PYTHONPATH=.tmp/test-deps python3 -m pytest
```

## Evidence Summary

- All active agent outputs validated with runner.
- QA is final in pipeline order.
- Supabase migration static validation passes.
- No paid LLM runtime drift detected.
- Contract tests pass.

## Known Notes

- Pilot found one process bug: QA was ordered before Marketing and Client Success.
- Fix applied in `execution/agency.py`; tests updated.
- Production implementation still requires real backend/frontend code and live infrastructure.
