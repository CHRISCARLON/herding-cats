import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.endpoints.api_endpoints import CkanApiPaths
from HerdingCats.endpoints.api_endpoints import CkanDataCatalogues
import requests
from loguru import logger


def test_ckan_health_check():
    """
    Check that predefined data catalogues are healthy and available
    """
    with CatSession(CkanDataCatalogues.LONDON_DATA_STORE) as cat_session:
        url = cat_session.base_url + CkanApiPaths.PACKAGE_LIST
        try:
            response = cat_session.session.get(url)
            print(response)

            # Check status code
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

            # Check data is not empty
            data = response.json()
            assert data, f"Received empty data from {cat_session.base_url}"

            # Additional check for 'success' key if your API returns it
            if 'success' in data:
                assert data['success'], f"CKAN returned success=False for {cat_session.base_url}"

            logger.info(f"Health check passed for {cat_session.base_url}")

        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to CKAN endpoint for {cat_session.base_url}: {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))
