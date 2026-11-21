# RepoGuard

RepoGuard is a lightweight repository health and quality checker built with Python.

It evaluates a repository's basic structure, checks the presence of essential project files,
runs basic secret-pattern checks, and calculates a repository quality score.

## Features

- Repository structure inspection
- Essential file validation
- README and Git configuration checks
- Test directory validation
- Basic suspicious secret-pattern detection
- Repository quality scoring
- Jenkins CI pipeline integration

## Project Structure

RepoGuard/
├── repoguard/
│   └── scanner.py
├── tests/
│   └── test_scanner.py
├── reports/
├── sample_repositories/
├── Jenkinsfile
└── requirements.txt

## Requirements

- Python 3.10+
- Git
- Jenkins (for CI integration)

## Run RepoGuard

```bash
python -c "from repoguard.scanner import scan_repository; scan_repository('.')"