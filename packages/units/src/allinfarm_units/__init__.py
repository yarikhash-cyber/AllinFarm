"""AllinFarm units: values are stored in base units and shown in a chosen unit set.

This is the lowest layer of the project: it must not import anything from other
AllinFarm packages (checked by import-linter in CI).
"""

from importlib.metadata import version

__all__ = ["__version__"]

__version__ = version("allinfarm-units")
