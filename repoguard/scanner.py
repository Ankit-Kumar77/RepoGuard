
from pathlib import Path
import re


def scan_repository(repo_path):
    repo = Path(repo_path)

    if not repo.exists():
        print("Repository path does not exist")
        return None

    if not repo.is_dir():
        print("The provided path is not a directory")
        return None

    print(f"Scanning repository: {repo.resolve()}")

    checks = {}

    # Basic repository checks
    checks["README.md"] = (repo / "README.md").exists()
    checks[".gitignore"] = (repo / ".gitignore").exists()
    checks["LICENSE"] = (repo / "LICENSE").exists()
    checks["requirements.txt"] = (repo / "requirements.txt").exists()

    # Test directory check
    checks["tests directory"] = (repo / "tests").is_dir()

    # Python package check
    checks["repoguard package"] = (repo / "repoguard").is_dir()

    # Repository statistics
    items = list(repo.iterdir())
    file_count = sum(1 for item in items if item.is_file())
    directory_count = sum(1 for item in items if item.is_dir())

    # Basic secret-pattern scan (limited heuristic)
    secret_patterns = {
        "Possible API key": r"(?i)(api_key|apikey)\s*=\s*['\"][^'\"]+['\"]",
        "Possible password": r"(?i)(password|passwd)\s*=\s*['\"][^'\"]+['\"]",
        "Possible token": r"(?i)(access_token|secret_token)\s*=\s*['\"][^'\"]+['\"]",
    }

    findings = []

    ignored_dirs = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
    }

    for current_file in repo.rglob("*"):
        if not current_file.is_file():
            continue

        if any(part in ignored_dirs for part in current_file.parts):
            continue

        try:
            content = current_file.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except Exception:
            continue

        for finding_name, pattern in secret_patterns.items():
            if re.search(pattern, content):
                findings.append(
                    f"{finding_name} found in {current_file.relative_to(repo)}"
                )

    # Scoring
    passed_checks = sum(checks.values())
    total_checks = len(checks)

    score = int((passed_checks / total_checks) * 100)

    if findings:
        score = max(0, score - (10 * len(findings)))

    # Report
    print("\n" + "=" * 45)
    print("             RepoGuard Report")
    print("=" * 45)

    print(f"Repository: {repo.resolve()}")
    print(f"Files found: {file_count}")
    print(f"Directories found: {directory_count}")

    print("\nQuality Checks:")

    for check_name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {check_name:<22} : {status}")

    print("\nSecret Pattern Scan:")

    if findings:
        for finding in findings:
            print(f"  WARNING: {finding}")
    else:
        print("  No suspicious patterns detected")

    print("\nQuality Score:")
    print(f"  {score}/100")

    if score >= 80 and not findings:
        print("  Overall Status: GOOD")
    elif score >= 50:
        print("  Overall Status: NEEDS IMPROVEMENT")
    else:
        print("  Overall Status: POOR")

    print("=" * 45)

    return {
        "repository": str(repo.resolve()),
        "checks": checks,
        "findings": findings,
        "score": score,
    }
