from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

from auditor.core import run_audit

Finding = Dict


def _count_by_severity(findings: List[Finding]) -> Dict[str, int]:
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in findings:
        sev = f.get("severity")
        if sev in counts:
            counts[sev] += 1
    return counts


def write_json(findings: List[Finding], out_json: Path) -> Path:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "summary": {**_count_by_severity(findings), "total": len(findings)},
        "findings": findings,
    }
    out_json.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return out_json


def write_markdown(findings: List[Finding], out_md: Path) -> Path:
    out_md.parent.mkdir(parents=True, exist_ok=True)
    counts = _count_by_severity(findings)
    lines = []
    lines += [
        "# Repo-Compliance Report",
        "",
        "## Resumen por severidad",
        "| Severidad | Conteo |",
        "|---|---:|",
        f"| HIGH | {counts['HIGH']} |",
        f"| MEDIUM | {counts['MEDIUM']} |",
        f"| LOW | {counts['LOW']} |",
        "",
        f"**Total findings:** {sum(counts.values())}",
        "",
    ]
    icon = {"FAIL": "❌", "PASS": "✅"}
    for sev in ("HIGH", "MEDIUM", "LOW"):
        lines.append(f"## {sev}")
        group = [f for f in findings if f.get("severity") == sev]
        if not group:
            lines.append("_Sin findings_")
            lines.append("")
            continue
        for f in group:
            status = f.get("status", "UNKNOWN")
            rule = f.get("rule", "UNKNOWN_RULE")
            details = f.get("details")
            lines.append(f"- {icon.get(status, '•')} **{rule}** — *{status}*")
            if details:
                if isinstance(details, dict):
                    pretty = ", ".join(f"{k}={v}" for k, v in details.items())
                    lines.append(f"  - `{pretty}`")
                else:
                    lines.append(f"  - `{details}`")
        lines.append("")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_md


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Genera reportes del auditor")
    parser.add_argument("--repo", default=".", help="Ruta del repo a auditar")
    parser.add_argument(
        "--json", default="out/report.json", help="Ruta del JSON a generar"
    )
    parser.add_argument(
        "--md", default="out/report.md", help="Ruta del Markdown a generar"
    )
    parser.add_argument("--no-json", action="store_true", help="No generar JSON")
    parser.add_argument("--no-md", action="store_true", help="No generar Markdown")
    parser.add_argument(
        "--fail-on-high", action="store_true", help="Exit 1 si hay HIGH"
    )
    args = parser.parse_args(argv)

    repo = Path(args.repo)
    result = run_audit(repo)
    findings = result.get("findings", [])

    if not args.no_json:
        write_json(findings, Path(args.json))
    if not args.no_md:
        write_markdown(findings, Path(args.md))

    if args.fail_on_high and any(f.get("severity") == "HIGH" for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
