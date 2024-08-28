import requests

from typing import Any, Dict
from loguru import logger
from pprint import pprint

from .cats_errors import CATExploreError, CKANFetchError, DCATFetchError



class CATExplore:

    CKAN_API_PATH = "/api/3/action/{}"
    DCAT_API_PATH = "/api/feed/dcat-ap/2.1.1.json"
    REQUEST_TIMEOUT = 15

    def __init__(self, domain: str) -> None:
        """Initialise CATExplore with a domain."""
        self.domain = domain

    # DATA SAMPLES
    def fetch_sample(self) -> Dict[str, Any]:
        """Fetch a sample from either CKAN or DCAT API."""
        try:
            return self.fetch_ckan_sample()
        except CKANFetchError as ckan_error:
            logger.error(f"CKAN fetch failed: {ckan_error} - Attempting DCAT")
            try:
                return self.fetch_dcat_sample()
            except DCATFetchError as dcat_error:
                logger.error(f"DCAT fetch failed: {dcat_error}")
                raise CATExploreError("Both CKAN and DCAT fetches failed") from dcat_error

    def fetch_ckan_sample(self, endpoint: str = "package_search") -> Dict[str, Any]:
        """Fetch a sample from CKAN API."""
        url = f"https://{self.domain}{self.CKAN_API_PATH.format(endpoint)}"
        data = self._make_request(url)
        return self._extract_ckan_result_sample(data)

    def fetch_dcat_sample(self) -> Dict[str, Any]:
        """Fetch a sample from DCAT API."""
        url = f"https://{self.domain}{self.DCAT_API_PATH}"
        data = self._make_request(url)
        return self._extract_dcat_result_sample(data)

    # SEARCH DATA
    def basic_search_ckan_data(self, user_input: str, endpoint: str = "package_search") -> Dict[str, Any]:
            try:
                url = f"https://{self.domain}{self.CKAN_API_PATH.format(endpoint)}"
                params = {
                    "q": user_input
                }
                return self._make_request(url, params)
            except requests.exceptions.RequestException as error:
                logger.error(f"An error occurred during the request: {error}")
                raise

    # UTILITY FUNCTIONS
    def _make_request(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a GET request to the specified URL with optional parameters."""
        try:
            response = requests.get(url, params=params, timeout=self.REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            logger.error(f"An error occurred during the request: {error}")
            raise

    @staticmethod
    def _extract_ckan_result_sample(data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the first result from CKAN API response."""
        if 'result' in data:
            if 'results' in data['result'] and data['result']['results']:
                return data['result']['results'][0]
            elif 'result' in data['result'] and data['result']['result']:
                return data['result']['result'][0]
        raise CKANFetchError("Expected data structure not found in CKAN response")

    @staticmethod
    def _extract_dcat_result_sample(data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the first result from DCAT API response."""
        if 'dcat:dataset' in data and isinstance(data['dcat:dataset'], list):
            return data['dcat:dataset'][0]
        raise DCATFetchError("Expected data structure not found in DCAT response")

    @staticmethod
    def print_structure(data: Any, indent: int = 0, key: str = "root") -> None:
        """Print the structure of any data type."""
        if isinstance(data, dict):
            print(f"{' ' * indent}{key}:")
            for k, v in data.items():
                CATExplore.print_structure(v, indent + 1, k)
        elif isinstance(data, list):
            print(f"{' ' * indent}{key}: (list of {len(data)} items)")
            if data:
                CATExplore.print_structure(data[0], indent + 1, f"{key}[0]")
        else:
            value_type = type(data).__name__
            value_preview = str(data)[:50] + "..." if len(str(data)) > 50 else str(data)
            print(f"{' ' * indent}{key}: ({value_type}) {value_preview}")

    @staticmethod
    def pretty_print_helper(data: Any) -> None:
        return pprint(data)

# Example usage
if __name__ == "__main__":
    explorer = CATExplore("data.london.gov.uk")
    result = explorer.basic_search_ckan_data("climate")
    explorer.pretty_print_helper(result)
