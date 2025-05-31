# ATS Testing

Quick reference for ATS compatibility testing.

## Commands

```bash
make test-ats                    # Run all ATS tests
make build-and-test              # Build + test
pytest tests/ -v -s              # Detailed test output  
pytest tests/ -k test_name -v -s # Specific test
```

## Current Status: ✅ 8/8 PASS

```
✅ Name: Mathéo Guilloux  
✅ Email: matheo.guilloux@gmail.com
✅ Position: DevOps Engineer
✅ Skills: 36 detected (100% coverage)
✅ Companies: Continental, Neverhack, Airbus
```

## Troubleshooting

**Test fails**: `pytest tests/ -v -s` for details  
**Dependencies**: `./setup_ats_deps.sh`  
**PDF missing**: `make pdf` first

The system validates your CV against `resume.yml` data automatically. 