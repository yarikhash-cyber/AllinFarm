"""Check that every Python and JavaScript dependency has a license compatible with AGPL-3.0.

ADR 0001. Run from the repository root:

    uv run python scripts/check_licenses.py

A license expression passes when every alternative of an "OR" has at least one allowed
license, and every part of an "AND" is allowed. Unknown licenses fail: add the package to
EXCEPTIONS only after reading its license, with the reason.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass

ALLOWED = {
    "0BSD",
    "AGPL-3.0",
    "AGPL-3.0-only",
    "AGPL-3.0-or-later",
    "Apache-2.0",
    "BlueOak-1.0.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "CC-BY-4.0",
    "CC0-1.0",
    "GPL-3.0",
    "GPL-3.0-only",
    "GPL-3.0-or-later",
    "ISC",
    "LGPL-2.1",
    "LGPL-2.1-only",
    "LGPL-2.1-or-later",
    "LGPL-3.0",
    "LGPL-3.0-only",
    "LGPL-3.0-or-later",
    "MIT",
    "MIT-0",
    "MPL-2.0",
    "PSF-2.0",
    "Python-2.0",
    "Unlicense",
    "Zlib",
}

# Old-style Python classifiers and free-text names mapped to SPDX identifiers.
ALIASES = {
    "MIT License": "MIT",
    "BSD License": "BSD-3-Clause",
    "Apache Software License": "Apache-2.0",
    "Apache License 2.0": "Apache-2.0",
    "Mozilla Public License 2.0 (MPL 2.0)": "MPL-2.0",
    "ISC License (ISCL)": "ISC",
    "Python Software Foundation License": "PSF-2.0",
    "The Unlicense (Unlicense)": "Unlicense",
    "GNU Lesser General Public License v3 (LGPLv3)": "LGPL-3.0-only",
    "GNU Affero General Public License v3 or later (AGPLv3+)": "AGPL-3.0-or-later",
}

# Packages whose license metadata is missing or unusual, checked by hand.
EXCEPTIONS: dict[str, str] = {}


@dataclass(frozen=True)
class Dependency:
    ecosystem: str
    name: str
    version: str
    license: str


def normalize(token: str) -> str:
    token = token.strip()
    if token in ALIASES:
        return ALIASES[token]
    token = token.strip("()").strip()
    return ALIASES.get(token, token)


def is_allowed(expression: str) -> bool:
    expression = expression.strip()
    if not expression or expression.upper() in {"UNKNOWN", "UNLICENSED"}:
        return False
    # pip-licenses joins several classifiers with "; " meaning the package offers all of them.
    if ";" in expression:
        return any(is_allowed(part) for part in expression.split(";"))
    if normalize(expression) in ALLOWED:
        return True
    alternatives = re.split(r"\s+OR\s+", expression.strip("()"))
    for alternative in alternatives:
        parts = re.split(r"\s+AND\s+", alternative)
        if all(normalize(part) in ALLOWED for part in parts):
            return True
    return False


def python_dependencies() -> list[Dependency]:
    output = subprocess.run(
        [sys.executable, "-m", "piplicenses", "--format=json", "--from=mixed"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [
        Dependency("python", item["Name"], item["Version"], item["License"])
        for item in json.loads(output)
    ]


def javascript_dependencies() -> list[Dependency]:
    pnpm = shutil.which("pnpm")
    if pnpm is None:
        raise SystemExit("pnpm is not installed")
    output = subprocess.run(
        [pnpm, "licenses", "list", "--json"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    dependencies = []
    for license_name, packages in json.loads(output).items():
        for package in packages:
            for version in package.get("versions", [""]):
                dependencies.append(Dependency("js", package["name"], version, license_name))
    return dependencies


def main() -> int:
    dependencies = python_dependencies() + javascript_dependencies()
    bad = [
        dep for dep in dependencies if dep.name not in EXCEPTIONS and not is_allowed(dep.license)
    ]
    print(f"Checked {len(dependencies)} dependencies.")
    if bad:
        print("Licenses not on the allow list (ADR 0001):")
        for dep in sorted(bad, key=lambda d: (d.ecosystem, d.name)):
            print(f"  {dep.ecosystem:6} {dep.name} {dep.version}: {dep.license}")
        return 1
    print("All licenses are compatible with AGPL-3.0-or-later.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
