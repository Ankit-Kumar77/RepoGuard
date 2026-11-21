from repoguard.scanner import scan_repository


def test_scanner_detects_readme(tmp_path):
    (tmp_path / "README.md").write_text("Test README")

    result = scan_repository(tmp_path)

    assert result is not None
    assert result["checks"]["README.md"] is True


def test_scanner_detects_gitignore(tmp_path):
    (tmp_path / ".gitignore").write_text("*.pyc")

    result = scan_repository(tmp_path)

    assert result["checks"][".gitignore"] is True


def test_scanner_calculates_score(tmp_path):
    (tmp_path / "README.md").write_text("Test README")
    (tmp_path / ".gitignore").write_text("*.pyc")
    (tmp_path / "LICENSE").write_text("MIT")
    (tmp_path / "requirements.txt").write_text("pytest")
    (tmp_path / "tests").mkdir()
    (tmp_path / "repoguard").mkdir()

    result = scan_repository(tmp_path)

    assert result["score"] == 100


def test_scanner_rejects_invalid_path():
    result = scan_repository("invalid_repository_path")

    assert result is None