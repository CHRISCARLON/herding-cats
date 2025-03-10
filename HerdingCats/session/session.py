import requests
from typing import Union
from loguru import logger
from urllib.parse import urlparse
from enum import Enum
from ..config.sources import (
    CkanDataCatalogues,
    OpenDataSoftDataCatalogues,
    FrenchGouvCatalogue,
    ONSNomisAPI,
)
from ..errors.errors import CatSessionError


# TODO: We need to find a better pattern than just chaining match statements
# We could add a dictionary mapping for the catalogue types instead
# Current Supported Catalogue Types
class CatalogueType(Enum):
    CKAN = "ckan"
    OPENDATA_SOFT = "opendatasoft"
    GOUV_FR = "french_gov"
    ONS_NOMIS = "ons_nomis"


# START A SESSION WITH A DATA CATALOGUE
class CatSession:
    def __init__(
        self,
        catalogue: Union[
            CkanDataCatalogues,
            OpenDataSoftDataCatalogues,
            FrenchGouvCatalogue,
            ONSNomisAPI,
        ],
    ) -> None:
        """
        Initialise a session with a predefined catalog.

        Args:
            catalogue: A predefined catalogue from one of the supported enum types
            (CkanDataCatalogues, OpenDataSoftDataCatalogues, or FrenchGouvCatalogue)

        Returns:
            A CatSession Object
        """
        self.domain, self._catalogue_type = self._process_catalogue(catalogue)
        self.session = requests.Session()
        self.base_url = (
            f"https://{self.domain}"
            if not self.domain.startswith("http")
            else self.domain
        )
        self._validate_url()

    @staticmethod
    def _process_catalogue(
        catalogue: Union[
            CkanDataCatalogues,
            OpenDataSoftDataCatalogues,
            FrenchGouvCatalogue,
            ONSNomisAPI,
        ],
    ) -> tuple[str, CatalogueType]:
        """
        Process the predefined catalogue to extract domain and type.

        Args:
            catalogue: A predefined catalogue enum

        Returns:
            tuple[str, CatalogueType]: A tuple of (domain, catalogue_type)
        """
        match catalogue:
            case FrenchGouvCatalogue():
                catalog_type = CatalogueType.GOUV_FR
            case CkanDataCatalogues():
                catalog_type = CatalogueType.CKAN
            case OpenDataSoftDataCatalogues():
                catalog_type = CatalogueType.OPENDATA_SOFT
            case ONSNomisAPI():
                catalog_type = CatalogueType.ONS_NOMIS
            case _:
                raise ValueError(
                    "Catalogue must be one of: CkanDataCatalogues, OpenDataSoftDataCatalogues, or FrenchGouvCatalogue"
                )

        parsed_url = urlparse(catalogue.value)
        return parsed_url.netloc if parsed_url.netloc else parsed_url.path, catalog_type

    def _validate_url(self) -> None:
        """
        Validate the URL to catch any errors.
        Will raise status code error if there is a problem with the url.
        """
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to connect to {self.base_url}: {str(e)}")
            raise CatSessionError(
                message="Invalid or unreachable URL",
                url=self.base_url,
                original_error=e,
            )

    def start_session(self) -> None:
        """Start a session with the specified domain."""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            logger.success(f"Session started successfully with {self.domain}")
        except requests.RequestException as e:
            logger.error(f"Failed to start session: {e}")
            raise CatSessionError(
                message="Failed to start session", url=self.base_url, original_error=e
            )

    def close_session(self) -> None:
        """Close the session."""
        self.session.close()
        logger.success(f"Session Closed: {self.base_url}")

    def __enter__(self):
        """Allow use with the context manager with"""
        self.start_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Allows use with the context manager with"""
        self.close_session()

    @property
    def catalogue_type(self) -> CatalogueType:
        """Return the catalog type (CKAN, OpenDataSoft, or French Government)"""
        return self._catalogue_type
