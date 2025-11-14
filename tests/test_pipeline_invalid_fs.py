from pathlib import Path

from auditor.core import run_audit
from auditor.report import write_json, write_markdown


def test_pipeline_invalid_fs(tmp_path):
    # Apuntamos al repo inválido REAL (filesystem)
    repo = Path("tests/demo_repo_invalid").resolve()
    assert repo.exists(), "Falta tests/demo_repo_invalid/"

    # Ejecutar el auditor
    result = run_audit(repo)
    findings = result["findings"]

    # Debe haber varios FAIL
    assert result["summary"]["failed"] >= 3

    # Generar reportes reales en una carpeta temporal
    out_dir = tmp_path / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    p_json = write_json(findings, out_dir / "report.json")
    p_md = write_markdown(findings, out_dir / "report.md")

    assert p_json.exists()
    assert p_md.exists()

    # Comprobamos que aparezcan reglas clave
    text_md = p_md.read_text(encoding="utf-8")
    assert "ENV_IN_GITIGNORE" in text_md
    assert "LICENSE_FILE" in text_md
    assert "MAKEFILE_TARGETS" in text_md
    assert "CONFIG_VIA_ENV" in text_md
