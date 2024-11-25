import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.explorer.cat_explore import CkanCatExplorer
import requests
from loguru import logger

CATALOGUES = ["https://data.london.gov.uk"]


@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_package_list_dictionary(catalogue_url):
    """
    Test the package list functionality for predefined data catalogues
    """
    with CatSession(catalogue_url) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            results = explorer.package_list_dictionary()

            print(results)

            # Assert that we got a result
            assert results is not None, f"No results returned for {catalogue_url}"

            # Check if we got the expected number of rows
            assert len(results) > 100, "There could be a problem - check manually"

            logger.info(f"Package search test passed for {catalogue_url}")
        except requests.RequestException as e:
            pytest.fail(
                f"Failed to perform package search for {catalogue_url}: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))

@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_package_list_dataframe(catalogue_url):
    """
    Test the package list dataframe functionality for predefined data catalogues
    """
    with CatSession(catalogue_url) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            results_pandas = explorer.package_list_dataframe("pandas")

            print(results_pandas)

            # Assert that we got a result
            assert results_pandas is not None, f"No results returned for {catalogue_url}"

            # Check if we got the expected number of rows
            assert len(results_pandas) > 100, "There could be a problem - check manually"

            logger.info(f"Package search test passed for {catalogue_url}")
        except requests.RequestException as e:
            pytest.fail(
                f"Failed to perform package search for {catalogue_url}: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))

@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_package_list_dataframe_extra(catalogue_url):
    """
    Test the package list dataframe extra functionality for predefined data catalogues
    """
    with CatSession(catalogue_url) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            results_pandas = explorer.package_list_dataframe_extra("polars")

            print(results_pandas)

            # Assert that we got a result
            assert results_pandas is not None, f"No results returned for {catalogue_url}"

            # Check if we got the expected number of rows
            assert len(results_pandas) > 100, "There could be a problem - check manually"

            logger.info(f"Package search test passed for {catalogue_url}")
        except requests.RequestException as e:
            pytest.fail(
                f"Failed to perform package search for {catalogue_url}: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))
