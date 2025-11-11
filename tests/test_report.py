from __future__ import annotations

import json

import pytest

from auditor.report import write_json, write_markdown


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
