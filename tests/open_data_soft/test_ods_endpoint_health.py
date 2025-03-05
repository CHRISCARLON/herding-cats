import pytest
import requests

from HerdingCats.session.session import CatSession
from HerdingCats.config.source_endpoints import OpenDataSoftApiPaths
from HerdingCats.config.sources import OpenDataSoftDataCatalogues
from loguru import logger

def test_ckan_health_check():
    """
    Check that predefined data catalogues are healthy and available
    """
    with CatSession(OpenDataSoftDataCatalogues.UK_POWER_NETWORKS_DNO) as cat_session:
        url = cat_session.base_url + OpenDataSoftApiPaths.SHOW_DATASETS
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
                assert data['success'], f"OpenDataSoft returned success=False for {cat_session.base_url}"

            logger.info(f"Health check passed for {cat_session.base_url}")

        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to OpenDataSoft endpoint for {cat_session.base_url}: {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))
