import pytest
from auditor import core

# .env en .gitignore
@pytest.mark.parametrize("gitignore, env_in_gitignore, expected_status, expected_sev", [
    (False, False, "FAIL", "HIGH"),
    (True,  False, "FAIL", "HIGH"),
    (True,  True,  "PASS", "LOW"),
])
def test_check_env_in_gitignore(repo_factory, gitignore, env_in_gitignore, expected_status, expected_sev):
    repo = repo_factory(gitignore=gitignore, env_in_gitignore=env_in_gitignore)
    res = core.check_env_in_gitignore(repo)
    assert res["status"] == expected_status
    assert res["severity"] == expected_sev


# LICENSE presente y no vacío
@pytest.mark.parametrize("license_text, expected_status", [
    (None,  "FAIL"),
    ("",    "FAIL"),
    ("MIT", "PASS"),
])
def test_check_license_file(repo_factory, license_text, expected_status):
    repo = repo_factory(license_text=license_text)
    res = core.check_license_file(repo)
    assert res["status"] == expected_status


# Makefile con targets obligatorios
@pytest.mark.parametrize("targets, expected_status, missing_subset", [
    (None,                 "FAIL", {"lint","test","coverage"}), # sin Makefile
    (("lint",),            "FAIL", {"test","coverage"}),
    (("lint","test"),      "FAIL", {"coverage"}),
    (("lint","test","coverage"), "PASS", set()),
])
def test_check_makefile_targets(repo_factory, targets, expected_status, missing_subset):
    repo = repo_factory(make_targets=targets)
    res = core.check_makefile_targets(repo)
    assert res["status"] == expected_status
    if expected_status == "FAIL" and targets is not None:
        assert set(res["details"]["missing"]).issuperset(missing_subset)


# Config vía env (sin .env versionado ni secretos)
@pytest.mark.parametrize("dot_env, settings_secret, config_secret, expected_status, expected_sev", [
    (True,  False, False, "FAIL", "HIGH"),   # .env versionado
    (False, True,  False, "FAIL", "HIGH"),   # secreto en settings.py
    (False, False, True,  "FAIL", "HIGH"),   # secreto en config.py
    (False, False, False, "PASS", "MEDIUM"), # OK sin .env.example
])
def test_check_config_via_env(repo_factory, dot_env, settings_secret, config_secret, expected_status, expected_sev):
    repo = repo_factory(
        dot_env=dot_env,
        dot_env_example=False,
        settings_secret=settings_secret,
        config_secret=config_secret,
    )
    res = core.check_config_via_env(repo)
    assert res["status"] == expected_status
    assert res["severity"] == expected_sev


def test_check_config_via_env_ok_with_example(repo_factory):
    repo = repo_factory(dot_env=False, dot_env_example=True)
    res = core.check_config_via_env(repo)
    assert res["status"] == "PASS"
    assert res["severity"] in {"LOW", "MEDIUM"}  # implementacion permite bajar a LOW con .env.example