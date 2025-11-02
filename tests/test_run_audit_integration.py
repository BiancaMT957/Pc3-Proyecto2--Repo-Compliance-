import json
from auditor import core

def test_run_audit_ok_end_to_end(repo_factory):
    repo = repo_factory(
        gitignore=True, env_in_gitignore=True,
        license_text="MIT",
        make_targets=("lint","test","coverage"),
        dot_env=False, dot_env_example=True,
    )
    rep = core.run_audit(repo)
    assert rep["summary"]["failed"] == 0
    json.dumps(rep)  # serializable

def test_run_audit_fail_detecta_faltantes(repo_factory):
    repo = repo_factory(
        gitignore=True, env_in_gitignore=False,  # falta .env en .gitignore
        license_text="",                         # LICENSE vacío
        make_targets=("lint",),                  # faltan test/coverage
        dot_env=True,                            # .env versionado
    )
    rep = core.run_audit(repo)
    assert rep["summary"]["failed"] >= 3
    # al menos debe aparecer MAKEFILE_TARGETS FAIL
    assert any(f["rule"] == "MAKEFILE_TARGETS" and f["status"] == "FAIL" for f in rep["findings"])