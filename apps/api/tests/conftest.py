import os

import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Tests marked `db` need DATABASE_URL. In CI a missing database is an error, not a skip."""
    if os.environ.get("DATABASE_URL"):
        return
    if os.environ.get("CI"):
        raise pytest.UsageError("DATABASE_URL must be set in CI")
    skip = pytest.mark.skip(reason="DATABASE_URL is not set")
    for item in items:
        if "db" in item.keywords:
            item.add_marker(skip)
