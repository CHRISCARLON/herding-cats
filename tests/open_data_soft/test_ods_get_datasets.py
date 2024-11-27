import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.explorer.cat_explore import OpenDataSoftCatExplorer
import requests
from loguru import logger

CATALOGUES = ["https://ukpowernetworks.opendatasoft.com"]

@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_package_list_dictionary(catalogue_url):
    """
    Test the package list functionality for predefined data catalogues...
    """
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
