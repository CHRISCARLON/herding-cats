import pytest
import requests

from HerdingCats.session.cat_session import CatSession
from HerdingCats.explorer.cat_explore import FrenchGouvCatExplorer
from HerdingCats.endpoints.api_endpoints import FrenchGouvCatalogue
from loguru import logger

def test_ckan_health_check():
    """
    Check that predefined data catalogue fetches all data catalogs available.
    The French government catalog should have >1000 datasets.
    """
    with CatSession(FrenchGouvCatalogue.GOUV_FR) as cat_session:
        explore = FrenchGouvCatExplorer(cat_session)
        try:
            data = explore.get_all_datasets()
            data_length = len(data)
            print(data_length)
            assert data_length > 10000, (
                f"Insufficient datasets from {cat_session.base_url}. "
                f"Found {data_length} datasets, expected >10000. "
                "This might indicate an API issue or data availability problem."
            )
            logger.info(
                f"Health check passed for {cat_session.base_url}: "
                f"retrieved {data_length} datasets"
            )
        except requests.RequestException as e:
            pytest.fail(
                f"Connection failed to French Gov endpoint {cat_session.base_url}: "
                f"Error: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))
        except Exception:
            pytest.fail(
                f"Unexpected error while fetching data from {cat_session.base_url}: "
            )
