import pytest
from pathlib import Path

@pytest.fixture
def repo_factory(tmp_path):
    """
    Crea un repositorio temporal con archivos opcionales.
    Uso:
      repo = repo_factory(
        gitignore=True, env_in_gitignore=True,
        license_text="MIT",
        make_targets=("lint","test","coverage"),
        dot_env=False,
        dot_env_example=True,
        settings_secret=False,
        config_secret=False,
      )
    """
    def _make(
        gitignore: bool = True,
        env_in_gitignore: bool = True,
        license_text: str | None = None,   # None = no LICENSE, "" = vacío
        make_targets: tuple[str, ...] | None = ("lint", "test", "coverage"),
        dot_env: bool = False,
        dot_env_example: bool = False,
        settings_secret: bool = False,
        config_secret: bool = False,
    ) -> Path:
        repo = tmp_path / "repo"
        repo.mkdir()

        # .gitignore
        if gitignore:
            lines = []
            if env_in_gitignore:
                lines.append(".env")
            (repo / ".gitignore").write_text("\n".join(lines) + ("\n" if lines else ""))

        # LICENSE / LICENSE.md
        if license_text is not None:
            (repo / "LICENSE").write_text(license_text)

        # Makefile
        if make_targets is not None:
            content = []
            for t in make_targets:
                content.append(f"{t}:\n\t@echo {t}")
            (repo / "Makefile").write_text("\n\n".join(content))

        # .env y .env.example
        if dot_env:
            (repo / ".env").write_text("SECRET=ultra\n")
        if dot_env_example:
            (repo / ".env.example").write_text("API_KEY=\n")

        # settings.py/config.py con o sin secretos
        if settings_secret:
            (repo / "settings.py").write_text('SECRET_KEY = "supersecret-super-largo"\n')
        if config_secret:
            (repo / "config.py").write_text('TOKEN="tok_123456789_abcd"\n')

        return repo
    return _make