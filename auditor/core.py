from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, List


# Helpers
def _read_text(p: Path) -> str:
    # Dividido en un if/else normal para legibilidad y longitud
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="ignore")


def _exists_insensitive(root: Path, names: Iterable[str]) -> Path | None:
    lower = {p.name.lower(): p for p in root.glob("*")}
    for n in names:
        p = lower.get(n.lower())
        if p:
            return p
    return None


# Definición de función dividida en múltiples líneas
def _rule_result(
    rule: str,
    status: str,
    severity: str,
    details: Dict | str | None = None,
) -> Dict:
    # status: "PASS" | "FAIL"
    # severity: "LOW" | "MEDIUM" | "HIGH"
    payload: Dict = {"rule": rule, "status": status, "severity": severity}
    if details is not None:
        payload["details"] = details
    return payload


# 1) .env debe estar en .gitignore
#    (FAIL+HIGH si falta)
def check_env_in_gitignore(repo: Path) -> Dict:
    """Verifica que '.env' aparezca en el .gitignore."""
    gi = repo / ".gitignore"
    if not gi.exists():
        return _rule_result(
            "ENV_IN_GITIGNORE", "FAIL", "HIGH", {"reason": ".gitignore no existe"}
        )
    content = _read_text(gi)
    if ".env" not in content:
        return _rule_result(
            "ENV_IN_GITIGNORE",
            "FAIL",
            "HIGH",
            # Diccionario dividido en múltiples líneas
            {
                "path": str(gi),
                "reason": "Falta la entrada .env en .gitignore",
            },
        )
    return _rule_result("ENV_IN_GITIGNORE", "PASS", "LOW", {"path": str(gi)})


# 2) Debe existir LICENSE o LICENSE.md y NO estar vacío
def check_license_file(repo: Path) -> Dict:
    """Verifica LICENSE/License(.md) y que no esté vacío."""
    candidate = _exists_insensitive(repo, ["LICENSE", "LICENSE.md"])
    if not candidate:
        return _rule_result(
            "LICENSE_FILE",
            "FAIL",
            "MEDIUM",
            {"reason": "No se encontró LICENSE/License.md"},
        )
    text = _read_text(candidate).strip()
    if not text:
        return _rule_result(
            "LICENSE_FILE",
            "FAIL",
            "MEDIUM",
            # Diccionario dividido en múltiples líneas
            {
                "path": str(candidate),
                "reason": "Archivo LICENSE vacío",
            },
        )
    return _rule_result("LICENSE_FILE", "PASS", "LOW", {"path": str(candidate)})


# 3) Makefile con targets obligatorios (lint, test, coverage).
#    Devolver faltantes
REQUIRED_MAKE_TARGETS = ("lint", "test", "coverage")


def check_makefile_targets(repo: Path) -> Dict:
    """
    Valida Makefile y presencia de targets requeridos;
    lista los faltantes en details.
    """
    mk = _exists_insensitive(repo, ["Makefile"])
    if not mk:
        return _rule_result(
            "MAKEFILE_TARGETS",
            "FAIL",
            "HIGH",
            {"reason": "No existe Makefile en la raíz"},
        )
    content = _read_text(mk)

    missing: List[str] = []
    for t in REQUIRED_MAKE_TARGETS:
        # busca 'target:' al inicio de línea (permitiendo espacios previos)
        # Expresión regular guardada en variable para acortar línea
        pattern = rf"(?m)^\s*{re.escape(t)}\s*:"
        if not re.search(pattern, content):
            missing.append(t)

    if missing:
        return _rule_result(
            "MAKEFILE_TARGETS",
            "FAIL",
            "MEDIUM",
            {
                "path": str(mk),
                "missing": missing,
                "required": list(REQUIRED_MAKE_TARGETS),
            },
        )
    return _rule_result("MAKEFILE_TARGETS", "PASS", "LOW", {"path": str(mk)})


# 4) Config vía variables de entorno /
#    NO credenciales en archivos
# Reglas mínimas:
#  - Si existe un archivo .env versionado => FAIL HIGH
#  - Scan simple de secretos en archivos de config comunes (heurística mínima)

SUSPECT_FILES = (".env", "settings.py", "config.py")
SECRET_PATTERNS = (
    # String largo (regex) dividido en dos
    r"(?i)AWS[_-]?SECRET[_-]?ACCESS[_-]?KEY\s*[:=]\s*['\"]"
    r"[A-Za-z0-9\/+=]{20,}['\"]?",
    r"(?i)SECRET[_-]?KEY\s*[:=]\s*['\"].{12,}['\"]",
    r"(?i)API[_-]?KEY\s*[:=]\s*['\"][A-Za-z0-9\-_]{12,}['\"]",
    r"(?i)DB[_-]?PASSWORD\s*[:=]\s*['\"].+['\"]",
    r"(?i)TOKEN\s*[:=]\s*['\"][A-Za-z0-9\._\-]{12,}['\"]",
)


def check_config_via_env(repo: Path) -> Dict:
    """
    .env no debe versionarse; detectar credenciales en
    archivos de config comunes.
    """
    # 4.a .env presente => FAIL HIGH
    if (repo / ".env").exists():
        return _rule_result(
            "CONFIG_VIA_ENV",
            "FAIL",
            "HIGH",
            {
                "path": str(repo / ".env"),
                # String dividido con paréntesis
                "reason": ("Se detectó .env versionado en el repositorio"),
            },
        )

    # 4.b Heurística de secretos en archivos comunes
    # List comprehension "desenrollada" en un bucle for
    suspects: List[Path] = []
    for name in SUSPECT_FILES:
        if (p := repo / name).exists():
            suspects.append(p)

    leaks: Dict[str, List[str]] = {}
    for p in suspects:
        text = _read_text(p)
        for pat in SECRET_PATTERNS:
            if re.search(pat, text):
                leaks.setdefault(str(p), []).append(pat)

    if leaks:
        return _rule_result(
            "CONFIG_VIA_ENV",
            "FAIL",
            "HIGH",
            {
                "reason": ("Posibles credenciales en archivos de configuración"),
                "matches": leaks,
            },
        )

    # OK (ideal si existe .env.example documentando variables)
    ok_detail = {}
    if (repo / ".env.example").exists():
        # String dividido con paréntesis
        ok_detail["hint"] = ".env.example presente (documenta variables sin valores)"

    # Llamada a función dividida en múltiples líneas
    return _rule_result(
        "CONFIG_VIA_ENV",
        "PASS",
        "LOW" if ok_detail else "MEDIUM",
        ok_detail or None,
    )


# 5) run_audit: ejecutar todas y agrupar findings
def run_audit(repo: Path) -> Dict:
    """Ejecuta todas las reglas y devuelve findings + resumen."""
    rules = [
        check_env_in_gitignore,
        check_license_file,
        check_makefile_targets,
        check_config_via_env,
    ]
    findings: List[Dict] = []

    for rule in rules:
        try:
            findings.append(rule(repo))
        except Exception as exc:  # protección de motor
            # Razón guardada en variable para acortar línea
            detail = {"reason": f"{type(exc).__name__}: {exc}"}
            findings.append(
                _rule_result(
                    rule.__name__,
                    "FAIL",
                    "HIGH",
                    detail,
                )
            )

    # Resumen útil (opcional, pero práctico para CI)
    total = len(findings)
    failed = sum(f["status"] == "FAIL" for f in findings)
    by_sev: Dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in findings:
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1

    return {
        "summary": {
            "total": total,
            "failed": failed,
            "passed": total - failed,
            "by_severity": by_sev,
        },
        "findings": findings,
    }


if __name__ == "__main__":
    import json
    import sys

    repo = Path(".")
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)

    # Ejecutar auditor
    result = run_audit(repo)

    # Guardar reporte
    report_path = out_dir / "report.json"
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f" Reporte generado en {report_path}")

    # Si hay findings HIGH → exit 1
    # List comprehension "desenrollada" para legibilidad
    high_findings = []
    for f in result["findings"]:
        if f.get("severity") == "HIGH":
            high_findings.append(f)

    if high_findings:
        print(" Se detectaron findings HIGH. Bloqueando pipeline.")
        sys.exit(1)

    print(" Auditoría sin findings HIGH.")
    sys.exit(0)
