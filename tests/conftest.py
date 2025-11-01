import pytest

@pytest.fixture
def sample_repo(tmp_path):
    """Fixture de ejemplo para crear un repo temporal simulado."""
    repo = tmp_path / "fake_repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Proyecto temporal")
    return repo
