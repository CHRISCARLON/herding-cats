import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.endpoints.api_endpoints import CkanApiPaths
import requests
from loguru import logger

CATALOGUES = [
    "https://data.london.gov.uk",
    "https://data.humdata.org",
    "https://data.gov.uk",
    "https://open.africa"
]

@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_ckan_health_check(catalogue_url):
    """
    Check that predefined data catalogues are healthy and available
    """
    with CatSession(catalogue_url) as cat_session:
        url = cat_session.base_url + CkanApiPaths.PACKAGE_LIST
        try:
            response = cat_session.session.get(url)

            # Check status code
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

            # Check data is not empty
            data = response.json()
            assert data, f"Received empty data from {catalogue_url}"

            # Additional check for 'success' key if your API returns it
            if 'success' in data:
                assert data['success'], f"CKAN returned success=False for {catalogue_url}"

            logger.info(f"Health check passed for {catalogue_url}")

        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to CKAN endpoint for {catalogue_url}: {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))
