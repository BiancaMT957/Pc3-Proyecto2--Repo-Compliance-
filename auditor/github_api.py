from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional

Finding = Dict[str, Any]


@dataclass
class GitHubAPI:
    token: Optional[str] = None

    @classmethod
    def from_env(
        cls,
        env: Optional[Mapping[str, str]] = None,
        var_name: str = "GITHUB_TOKEN",
    ) -> "GitHubAPI":
        source = env or os.environ
        return cls(token=source.get(var_name))

    # Mover tarjeta en GitHub Projects
    def move_card(self, card_id: str, column_id: str) -> Dict[str, Any]:
        return {
            "status": "ok",
            "action": "move_card",
            "card_id": card_id,
            "column_id": column_id,
            "used_token": bool(self.token),
        }

    # Comentar en un Issue / PR
    def comment_issue(
        self,
        repo: str,
        issue_number: int,
        body: str,
    ) -> Dict[str, Any]:
        return {
            "status": "ok",
            "action": "comment_issue",
            "repo": repo,
            "issue_number": issue_number,
            "body": body,
            "used_token": bool(self.token),
        }

    # Construir resumen de findings para comentar en un PR
    def build_audit_summary_body(
        self,
        findings: List[Finding],
        trend: str,
        blocked_time: str,
    ) -> str:
        total = len(findings)
        high = sum(1 for f in findings if f.get("severity") == "HIGH")
        medium = sum(1 for f in findings if f.get("severity") == "MEDIUM")
        low = sum(1 for f in findings if f.get("severity") == "LOW")

        lines = [
            "## Auditor Report Summary",
            "",
            f"- Total findings: **{total}**",
            f"- HIGH: **{high}**  |  MEDIUM: **{medium}**  |  LOW: **{low}**",
            f"- Trend: **{trend}**",
            f"- Blocked time: **{blocked_time}**",
            "",
        ]
        return "\n".join(lines)

    def comment_audit_summary(
        self,
        repo: str,
        pr_number: int,
        findings: List[Finding],
        trend: str,
        blocked_time: str,
    ) -> Dict[str, Any]:
        body = self.build_audit_summary_body(
            findings=findings,
            trend=trend,
            blocked_time=blocked_time,
        )
        return self.comment_issue(repo, pr_number, body)
