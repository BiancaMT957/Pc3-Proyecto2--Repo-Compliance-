from __future__ import annotations

from unittest.mock import patch

from auditor.github_api import GitHubAPI


def test_from_env_lee_token_de_entorno(monkeypatch):
    # Simulamos variable de entorno GITHUB_TOKEN
    monkeypatch.setenv("GITHUB_TOKEN", "dummy-token")
    api = GitHubAPI.from_env()
    assert api.token == "dummy-token"


def test_move_card_con_autospec():
    api = GitHubAPI(token="dummy-token")

    # Patch sobre el método de la CLASE, con autospec, para validar la firma
    with patch.object(
        GitHubAPI, "move_card", autospec=True, return_value={"status": "ok"}
    ) as mock_move:
        result = api.move_card("card-123", "col-999")

        # Primer argumento siempre es self (api)
        mock_move.assert_called_once_with(api, "card-123", "col-999")
        assert result == {"status": "ok"}


def test_comment_issue_con_autospec():
    api = GitHubAPI(token="dummy-token")

    with patch.object(
        GitHubAPI, "comment_issue", autospec=True, return_value={"status": "ok"}
    ) as mock_comment:
        result = api.comment_issue("owner/repo", 7, "Hola auditor")

        mock_comment.assert_called_once_with(api, "owner/repo", 7, "Hola auditor")
        assert result["status"] == "ok"


def test_build_audit_summary_body_conteos_correctos():
    api = GitHubAPI()
    findings = [
        {"severity": "HIGH"},
        {"severity": "LOW"},
        {"severity": "MEDIUM"},
        {"severity": "LOW"},
    ]

    body = api.build_audit_summary_body(
        findings=findings,
        trend="mejora",
        blocked_time="120s",
    )

    # Validamos que el texto contenga lo importante
    assert "Total findings: **4**" in body
    assert "HIGH: **1**" in body
    assert "MEDIUM: **1**" in body
    assert "LOW: **2**" in body
    assert "Trend: **mejora**" in body
    assert "Blocked time: **120s**" in body


def test_comment_audit_summary_usa_comment_issue(monkeypatch):
    api = GitHubAPI(token="dummy-token")
    findings = [{"severity": "HIGH"}, {"severity": "LOW"}]

    with patch.object(
        GitHubAPI, "comment_issue", autospec=True, return_value={"status": "ok"}
    ) as mock_comment:
        result = api.comment_audit_summary(
            repo="owner/repo",
            pr_number=10,
            findings=findings,
            trend="empeora",
            blocked_time="300s",
        )

        # Se llama internamente a comment_issue
        mock_comment.assert_called_once()
        args, _ = mock_comment.call_args

        # args[0] = self, args[1] = repo, args[2] = pr_number, args[3] = body
        assert args[0] is api
        assert args[1] == "owner/repo"
        assert args[2] == 10
        body = args[3]
        assert "Auditor Report Summary" in body
        assert "Trend: **empeora**" in body
        assert "Blocked time: **300s**" in body

        assert result["status"] == "ok"
