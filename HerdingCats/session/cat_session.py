import requests

from typing import Union
from loguru import logger
from urllib.parse import urlparse
from enum import Enum
from ..endpoints.api_endpoints import CkanDataCatalogues, OpenDataSoftDataCatalogues, FrenchGouvCatalogue
from ..errors.cats_errors import CatSessionError

# Current Supported Catalogue Types
class CatalogueType(Enum):
    CKAN = "ckan"
    OPENDATA_SOFT = "opendatasoft"
    GOUV_FR = "french_gov"

# START A SESSION WITH A DATA CATALOGUE
class CatSession:
    def __init__(
        self, domain: Union[str, CkanDataCatalogues, OpenDataSoftDataCatalogues, FrenchGouvCatalogue]
    ) -> None:
        """
        Initialise a session with a valid domain or a predefined catalog.

        Args:
            domain (url or catalogue item): str or catalog enum
        """
        self.domain, self.catalogue_type = self._process_domain(domain)
        self.session = requests.Session()
        self.base_url = (
            f"https://{self.domain}"
            if not self.domain.startswith("http")
            else self.domain
        )
        self._validate_url()

    @staticmethod
    def _process_domain(
        domain: Union[str, CkanDataCatalogues, OpenDataSoftDataCatalogues, FrenchGouvCatalogue]
    ) -> tuple[str, CatalogueType]:
        """
        Process the domain to ensure that it's in the correct format.

        This iterates through the CkanDataCatalogues, OpenDataSoftDataCatalogues, and FrenchGouvCatalogue
        Enums and checks for a match.

        Otherwise it processes the url as normal.

        Args:
            domain (url or catalogue item): str or catalog enum
        Returns:
            a tuple of (url in the correct format, catalog type)
        """
        # Check predefined catalogs first
        if isinstance(domain, (CkanDataCatalogues, OpenDataSoftDataCatalogues, FrenchGouvCatalogue)):
            if isinstance(domain, FrenchGouvCatalogue):
                catalog_type = CatalogueType.GOUV_FR
            else:
                catalog_type = (
                    CatalogueType.CKAN
                    if isinstance(domain, CkanDataCatalogues)
                    else CatalogueType.OPENDATA_SOFT
                )
            parsed_url = urlparse(domain.value)
            return parsed_url.netloc if parsed_url.netloc else parsed_url.path, catalog_type

        # Process as normal site url
        # Check if site url is in the catalogue already
        elif isinstance(domain, str):
            for catalog_enum in (CkanDataCatalogues, OpenDataSoftDataCatalogues, FrenchGouvCatalogue):
                for catalog in catalog_enum:
                    if domain.lower() == catalog.name.lower().replace("_", " "):
                        parsed_url = urlparse(catalog.value)
                        url = parsed_url.netloc if parsed_url.netloc else parsed_url.path
                        if catalog_enum == FrenchGouvCatalogue:
                            catalog_type = CatalogueType.GOUV_FR
                        else:
                            catalog_type = (
                                CatalogueType.CKAN
                                if catalog_enum == CkanDataCatalogues
                                else CatalogueType.OPENDATA_SOFT
                            )
                        return url, catalog_type

            # If not a predefined catalogue item, process as a regular domain or URL
            parsed = urlparse(domain)
            domain_str = parsed.netloc if parsed.netloc else parsed.path

            # Check if it's a French government domain
            # Otherwise default to CKAN
            if domain_str.endswith('.gouv.fr'):
                return domain_str, CatalogueType.GOUV_FR
            else:
                return domain_str, CatalogueType.CKAN
        else:
            raise ValueError(
                "Domain must be a string, CkanDataCatalogues enum, OpenDataSoftDataCatalogues enum, or FrenchGouvCatalogue enum"
            )

    def _validate_url(self) -> None:
        """
        Validate the URL to catch any errors.

        Will raise status code error if there is a problem with url.
        """
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to connect to {self.base_url}: {str(e)}")
            raise CatSessionError(
                f"Invalid or unreachable URL: {self.base_url}. Error: {str(e)}"
            )

    def start_session(self) -> None:
        """Start a session with the specified domain."""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            logger.success(f"Session started successfully with {self.domain}")
        except requests.RequestException as e:
            logger.error(f"Failed to start session: {e}")
            raise CatSessionError(f"Failed to start session: {str(e)}")

    def close_session(self) -> None:
        """Close the session."""
        self.session.close()
        logger.success("Session closed")

    def __enter__(self):
        """Allow use with the context manager with"""
        self.start_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Allows use with the context manager with"""
        self.close_session()

    def get_catalogue_type(self) -> CatalogueType:
        """Return the catalog type (CKAN, OpenDataSoft, or French Government)"""
        return self.catalogue_type
