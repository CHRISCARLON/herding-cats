import pytest
import requests

from HerdingCats.session.session import CatSession
from HerdingCats.explorer.explore import OpenDataSoftCatExplorer
from HerdingCats.config.sources import OpenDataSoftDataCatalogues
from loguru import logger

def test_package_list_dictionary():
    """
    Test the package list functionality for predefined data catalogues...
    """
    catalogue_url = OpenDataSoftDataCatalogues.UK_POWER_NETWORKS_DNO
    with CatSession(catalogue_url) as cat_session:
        explorer = OpenDataSoftCatExplorer(cat_session)
        try:
            results = explorer.fetch_all_datasets()

            print(results)

            # Assert that we got a result
            assert results is not None, f"No results returned for {catalogue_url}"

            logger.info(f"Package search test passed for {catalogue_url}")
        except requests.RequestException as e:
            pytest.fail(
                f"Failed to perform package search for {catalogue_url}: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))
