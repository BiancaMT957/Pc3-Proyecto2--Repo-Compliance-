from auditor import core


def test_run_audit_maneja_excepcion(monkeypatch, repo_factory):

    # Espía: inyectamos una "regla" que explota para cubrir rama de excepción
    calls = {"count": 0}

    def boom(_repo):
        calls["count"] += 1
        raise RuntimeError("boom")

    # Parchea la lista de reglas usada en run_audit, conservando el resto
    monkeypatch.setattr(core, "check_env_in_gitignore", boom)

    repo = repo_factory()
    rep = core.run_audit(repo)

    # Verifica que el primer finding es por la excepción convertida en FAIL/HIGH
    first = rep["findings"][0]
    assert first["rule"] in {"boom", "check_env_in_gitignore"}
    assert first["status"] == "FAIL" and first["severity"] == "HIGH"
    assert "RuntimeError" in first["details"]["reason"]
    assert calls["count"] == 1


def test_exists_insensitive_llamado(monkeypatch, tmp_path):
    # Espía de argumentos: reemplazamos _exists_insensitive por un wrapper
    seen = {"args": []}
    real = core._exists_insensitive

    def spy(root, names):
        seen["args"].append((root, tuple(names)))
        return real(root, names)

    monkeypatch.setattr(core, "_exists_insensitive", spy)

    repo = tmp_path / "r"
    repo.mkdir()
    (repo / "LICENSE").write_text("MIT")
    _ = core.check_license_file(repo)

    # Validamos que fue llamado con la lista esperada
    assert len(seen["args"]) >= 1
    root, names = seen["args"][0]
    assert root == repo
    assert set(n.lower() for n in names) == {"license", "license.md"}
