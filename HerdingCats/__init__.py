"""
The aim of this project is simple: create a basic Python library to explore and interact with open data sources.

This will improve and speed up how users:

- Navigate open data catalogues
- Find the data that they need
- Get that data into a format and/or location for further analysis
"""

from importlib.metadata import version

try:
    __version__ = version("HerdingCats")
except Exception:
    __version__ = "0.1.2"

# Core components
from .session.session import CatSession

# Explorer components
from .explorer.explore import (
    CkanCatExplorer,
    OpenDataSoftCatExplorer,
    FrenchGouvCatExplorer,
    ONSNomisCatExplorer,
)

# Resource loader components
from .loader.loader import (
    CkanLoader,
    OpenDataSoftLoader,
    FrenchGouvLoader,
    ONSNomisLoader,
)

# Configuration components
from .config.sources import (
    CkanDataCatalogues,
    OpenDataSoftDataCatalogues,
    FrenchGouvCatalogue,
    ONSNomisAPI,
)

# Error handling components
from .errors.errors import (
    CatSessionError,
    CatExplorerError,
    OpenDataSoftExplorerError,
)

# Public API definition
__all__ = [
    # Core
    "CatSession",
    # Explorers
    "CkanCatExplorer",
    "OpenDataSoftCatExplorer",
    "FrenchGouvCatExplorer",
    "ONSNomisCatExplorer",
    # Resource Loaders
    "CkanLoader",
    "OpenDataSoftLoader",
    "FrenchGouvLoader",
    "ONSNomisLoader",
    # Configuration
    "CkanDataCatalogues",
    "OpenDataSoftDataCatalogues",
    "FrenchGouvCatalogue",
    "ONSNomisAPI",
    # Errors
    "CatSessionError",
    "CatExplorerError",
    "OpenDataSoftExplorerError",
]
