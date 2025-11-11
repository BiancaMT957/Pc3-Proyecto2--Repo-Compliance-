from __future__ import annotations

import json

import pytest

from auditor.report import main  # CLI de report.py para probar flags
from auditor.report import (  # función interna para simular blocked_time
    _update_blocked_time,
    write_json,
    write_markdown,
)


@pytest.mark.parametrize(
    "findings,expected_counts",
    [
        ([], {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "total": 0}),
        (
            [
                {"rule": "A", "status": "FAIL", "severity": "HIGH"},
                {"rule": "B", "status": "PASS", "severity": "LOW"},
                {"rule": "C", "status": "FAIL", "severity": "MEDIUM"},
                {"rule": "D", "status": "PASS", "severity": "LOW"},
            ],
            {"HIGH": 1, "MEDIUM": 1, "LOW": 2, "total": 4},
        ),
    ],
)
def test_write_json(tmp_path, findings, expected_counts):
    out = tmp_path / "out" / "report.json"
    p = write_json(findings, out)
    assert p.exists()

    data = json.loads(p.read_text(encoding="utf-8"))
    assert "summary" in data and "findings" in data
    for k, v in expected_counts.items():
        assert data["summary"].get(k) == v
    assert isinstance(data["findings"], list)
    assert len(data["findings"]) == expected_counts["total"]


@pytest.mark.parametrize(
    "findings,expect_fragments",
    [
        (
            [],
            ["| HIGH | 0 |", "| MEDIUM | 0 |", "| LOW | 0 |", "**Total findings:** 0"],
        ),
        (
            [
                {
                    "rule": "ENV_IN_GITIGNORE",
                    "status": "FAIL",
                    "severity": "HIGH",
                    "details": {"reason": "missing .env"},
                },
                {"rule": "LICENSE_FILE", "status": "PASS", "severity": "LOW"},
            ],
            [
                "| HIGH | 1 |",
                "| LOW | 1 |",
                "ENV_IN_GITIGNORE",
                "LICENSE_FILE",
                "❌",
                "✅",
            ],
        ),
    ],
)
def test_write_markdown(tmp_path, findings, expect_fragments):
    out = tmp_path / "out" / "report.md"
    p = write_markdown(findings, out)
    assert p.exists()

    text = p.read_text(encoding="utf-8")
    for frag in expect_fragments:
        assert frag in text


def test_blocked_time_abre_y_cierra(tmp_path):
    out = tmp_path / "out" / "blocked_time.json"
    # Abre ventana (HIGH presente)
    _update_blocked_time([{"severity": "HIGH", "status": "FAIL"}], out)
    text = out.read_text(encoding="utf-8")
    assert (
        '"blocked": true' in text
        and '"started_at":' in text
        and '"ended_at": null' in text
    )

    # Cierra ventana (sin HIGH)
    _update_blocked_time([], out)
    text2 = out.read_text(encoding="utf-8")
    assert '"blocked": false' in text2 and '"ended_at":' in text2


def _repo_ok(tmp_path):
    repo = tmp_path / "repo_ok"
    repo.mkdir()
    (repo / ".gitignore").write_text(".env\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT", encoding="utf-8")
    (repo / "Makefile").write_text(
        "lint:\n\t@\n\ntest:\n\t@\n\ncoverage:\n\t@\n", encoding="utf-8"
    )
    return repo


def test_cli_generates_files_and_flags(tmp_path):
    repo = _repo_ok(tmp_path)
    out_json = tmp_path / "out" / "r.json"
    out_md = tmp_path / "out" / "r.md"
    # Caso normal: no hay HIGH → rc=0 y escribe archivos
    rc = main(
        [
            "--repo",
            str(repo),
            "--json",
            str(out_json),
            "--md",
            str(out_md),
            "--fail-on-high",
        ]
    )
    assert rc == 0 and out_json.exists() and out_md.exists()

    # Flags --no-json/--no-md: no debe generar archivos
    out_json2 = tmp_path / "out" / "r2.json"
    out_md2 = tmp_path / "out" / "r2.md"
    rc2 = main(
        [
            "--repo",
            str(repo),
            "--json",
            str(out_json2),
            "--md",
            str(out_md2),
            "--no-json",
            "--no-md",
        ]
    )
    assert rc2 == 0 and not out_json2.exists() and not out_md2.exists()


def test_cli_fail_on_high_devuelve_1(tmp_path):
    repo = tmp_path / "repo_bad"
    repo.mkdir()
    (repo / ".env").write_text("X=1", encoding="utf-8")  # HIGH por .env versionado
    (repo / "LICENSE").write_text("", encoding="utf-8")  # LICENSE vacío (MEDIUM)
    (repo / "Makefile").write_text(
        "lint:\n\t@\n", encoding="utf-8"
    )  # incompleto (MEDIUM)
    rc = main(["--repo", str(repo), "--fail-on-high"])
    assert rc == 1


def test_markdown_cubre_details_como_string(tmp_path):
    # Cubre rama where details es str (no dict)
    findings = [
        {"rule": "R", "status": "FAIL", "severity": "LOW", "details": "mensaje plano"}
    ]
    p = write_markdown(findings, tmp_path / "out" / "s.md")
    assert "mensaje plano" in p.read_text(encoding="utf-8")
