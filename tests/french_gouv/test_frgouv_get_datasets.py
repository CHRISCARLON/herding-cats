import pytest
import requests

from HerdingCats.session.cat_session import CatSession
from HerdingCats.endpoints.api_endpoints import FrenchGouvApiPaths
from HerdingCats.explorer.cat_explore import FrenchGouvCatExplorer
from loguru import logger

CATALOGUES = [
    "https://www.data.gouv.fr"
]

@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_ckan_health_check(catalogue_url):
    """
    Check that predefined data catalogue fetches all data catalogs available.
    The French government catalog should have >1000 datasets.
    """
    with CatSession(catalogue_url) as cat_session:
        explore = FrenchGouvCatExplorer(cat_session)
        try:
            data = explore.get_all_datasets()
            data_length = len(data)
            print(data_length)
            assert data_length > 10000, (
                f"Insufficient datasets from {catalogue_url}. "
                f"Found {data_length} datasets, expected >10000. "
                "This might indicate an API issue or data availability problem."
            )
            logger.info(
                f"Health check passed for {catalogue_url}: "
                f"retrieved {data_length} datasets"
            )
        except requests.RequestException as e:
            pytest.fail(
                f"Connection failed to French Gov endpoint {catalogue_url}: "
                f"Error: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))
        except Exception as e:
            pytest.fail(
                f"Unexpected error while fetching data from {catalogue_url}: "
            )
