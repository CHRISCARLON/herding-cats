import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.explorer.cat_explore import CkanCatExplorer
from HerdingCats.endpoints.api_endpoints import CkanDataCatalogues
import requests
from loguru import logger


def test_package_list_dictionary():
    """
    Test the package list functionality for predefined data catalogues
    """
    with CatSession(CkanDataCatalogues.LONDON_DATA_STORE) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            results = explorer.get_package_list()

            print(results)

            # Assert that we got a result
            assert results is not None, f"No results returned for {cat_session.base_url}"

            logger.info(f"Package search test passed for {cat_session.base_url}")
        except requests.RequestException as e:
            pytest.fail(
                f"Failed to perform package search for {cat_session.base_url}: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))


def test_package_list_dataframe():
    """
    Test the package list dataframe functionality for predefined data catalogues
    """
    with CatSession(CkanDataCatalogues.LONDON_DATA_STORE) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            results_pandas = explorer.get_package_list_dataframe("pandas")

            print(results_pandas)

            # Assert that we got a result
            assert results_pandas is not None, f"No results returned for {cat_session.base_url}"

            # Check if we got the expected number of rows
            assert len(results_pandas) > 100, "There could be a problem - check manually"

            logger.info(f"Package search test passed for {cat_session.base_url}")
        except requests.RequestException as e:
            pytest.fail(
                f"Failed to perform package search for {cat_session.base_url}: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))