import requests

from typing import Union
from loguru import logger
from urllib.parse import urlparse

from endpoints.api_endpoints import CkanDataCatalogues
from errors.cats_errors import CatSessionError


# START A SESSION
class CkanCatSession:
    def __init__(self, domain: Union[str, CkanDataCatalogues]) -> None:
        """
        Initialise a session with a valid domain or predefined catalog.

        Args:
            domain (url or catalogue item): str
        """
        self.domain = self._process_domain(domain)
        self.session = requests.Session()
        self.base_url = (
            f"https://{self.domain}"
            if not self.domain.startswith("http")
            else self.domain
        )
        self._validate_url()

    # ----------------------------
    # Initiate a Session
    # ----------------------------
    @staticmethod
    def _process_domain(domain: Union[str, CkanDataCatalogues]) -> str:
        """
        Process the domain to ensure it's in the correct format

        This iterates through the CkanDataCatalogues Enum and checks for a match

        Otherwise it processes the url as normal

        Args:
            domain (url or ckan data catalogue item): str

        Returns:
            a url in the correct format
        """
        if isinstance(domain, CkanDataCatalogues):
            logger.info(f"You are using: {urlparse(domain.value).netloc}")
            return urlparse(domain.value).netloc
        elif isinstance(domain, str):
            for catalog in CkanDataCatalogues:
                if domain.lower() == catalog.name.lower().replace("_", " "):
                    url = urlparse(catalog.value).netloc
                    logger.info(f"You are using: {url}")
                    return url
            else:
                # If not a predefined catalog, process as a regular domain or URL
                parsed = urlparse(domain)
                logger.info(f"You are using: {parsed}")
                return parsed.netloc if parsed.netloc else parsed.path
        else:
            raise ValueError("Domain must be a string or CkanDataCatalogues enum")

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
