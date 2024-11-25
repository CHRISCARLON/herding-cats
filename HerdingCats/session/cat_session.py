import requests

from typing import Union
from loguru import logger
from urllib.parse import urlparse
from enum import Enum
from ..endpoints.api_endpoints import CkanDataCatalogues, OpenDataSoftDataCatalogues
from ..errors.cats_errors import CatSessionError

class CatalogType(Enum):
    CKAN = "ckan"
    OPENDATA_SOFT = "opendatasoft"

class CatSession:
    def __init__(
        self, domain: Union[str, CkanDataCatalogues, OpenDataSoftDataCatalogues]
    ) -> None:
        """
        Initialise a session with a valid domain or predefined catalog.
        Args:
            domain (url or catalogue item): str
        """
        self.domain, self.catalog_type = self._process_domain(domain)
        self.session = requests.Session()
        self.base_url = (
            f"https://{self.domain}"
            if not self.domain.startswith("http")
            else self.domain
        )
        self._validate_url()

    @staticmethod
    def _process_domain(
        domain: Union[str, CkanDataCatalogues, OpenDataSoftDataCatalogues],
    ) -> tuple[str, CatalogType]:
        """
        Process the domain to ensure it's in the correct format.

        This iterates through the CkanDataCatalogues and OpenDataSoftDataCatalogues Enums and checks for a match
        Otherwise it processes the url as normal.

        Args:
            domain (url or data catalogue item): str
        Returns:
            a tuple of (url in the correct format, catalog type)
        """
        if isinstance(domain, (CkanDataCatalogues, OpenDataSoftDataCatalogues)):
            catalog_type = (
                CatalogType.CKAN
                if isinstance(domain, CkanDataCatalogues)
                else CatalogType.OPENDATA_SOFT
            )
            return urlparse(domain.value).netloc, catalog_type
        elif isinstance(domain, str):
            for catalog_enum in (CkanDataCatalogues, OpenDataSoftDataCatalogues):
                for catalog in catalog_enum:
                    if domain.lower() == catalog.name.lower().replace("_", " "):
                        url = urlparse(catalog.value).netloc
                        catalog_type = (
                            CatalogType.CKAN
                            if catalog_enum == CkanDataCatalogues
                            else CatalogType.OPENDATA_SOFT
                        )
                        return url, catalog_type
            else:
                # If not a predefined catalog, process as a regular domain or URL
                parsed = urlparse(domain)
                return (
                    parsed.netloc if parsed.netloc else parsed.path,
                    CatalogType.CKAN,
                )  # Default to CKAN for custom URLs
        else:
            raise ValueError(
                "Domain must be a string, CkanDataCatalogues enum, or OpenDataSoftDataCatalogues enum"
            )

    def _validate_url(self) -> None:
        """
        Validate the URL to catch any errors
        Will raise status code error if there is a problem
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

    def get_catalog_type(self) -> CatalogType:
        """Return the catalog type (CKAN or OpenDataSoft)"""
        return self.catalog_type
