import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.endpoints.api_endpoints import OpenDataSoftApiPaths
import requests
from loguru import logger

CATALOGUES = [
    "https://ukpowernetworks.opendatasoft.com"
]

@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_ckan_health_check(catalogue_url):
    """
    Check that predefined data catalogues are healthy and available
    """
    with CatSession(catalogue_url) as cat_session:
        url = cat_session.base_url + OpenDataSoftApiPaths.SHOW_DATASETS
        try:
            response = cat_session.session.get(url)
            print(response)

            # Check status code
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

            # Check data is not empty
            data = response.json()
            assert data, f"Received empty data from {catalogue_url}"

            # Additional check for 'success' key if your API returns it
            if 'success' in data:
                assert data['success'], f"OpenDataSoft returned success=False for {catalogue_url}"

            logger.info(f"Health check passed for {catalogue_url}")

        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to OpenDataSoft endpoint for {catalogue_url}: {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))
