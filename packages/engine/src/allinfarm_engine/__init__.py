"""AllinFarm calculation engine.

A pure library: everything comes in as input, results come out with a manifest.
It must not import the API, a database driver, a web framework or an HTTP client
(checked by import-linter in CI).
"""

from importlib.metadata import version

import allinfarm_units

__all__ = ["__version__", "engine_info"]

__version__ = version("allinfarm-engine")


def engine_info() -> dict[str, str]:
    """Versions of the engine and the packages it depends on."""
    return {"engine": __version__, "units": allinfarm_units.__version__}
