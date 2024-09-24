import pytest
from HerdingCats.session.cat_session import CkanCatSession
from HerdingCats.explorer.cat_explore import CkanCatExplorer
import requests
from loguru import logger

CATALOGUES = [
    "https://data.london.gov.uk",
    "https://data.humdata.org"
]

@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_package_list_dictionary(catalogue_url):
    """
    Test the package list functionality for predefined data catalogues
    """
    with CkanCatSession(catalogue_url) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:

            results = explorer.package_list_dictionary()

            # Assert that we got a result
            assert results is not None, f"No results returned for {catalogue_url}"

            # Check if we got the expected number of rows
            assert len(results) > 100, "There could be problem - check manually"

            logger.info(f"Package search test passed for {catalogue_url}")
        except requests.RequestException as e:
            pytest.fail(f"Failed to perform package search for {catalogue_url}: {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))

# COULD ADD IN TESTS FOR DATAFRAME PACKAGE LIST BUT DON'T WANT TO CALL THE ENDPOINTS TOO MUCH
# THIS WOULD CALL THEM ALL 12 TIMES - TEST ABOVE SHOULD DO FOR NOW
# @pytest.mark.parametrize("catalogue_url", CATALOGUES)
# def test_package_list_dataframe_polars(catalogue_url):
#     """
#     Test the package list functionality for predefined data catalogues
#     """
#     with CkanCatSession(catalogue_url) as cat_session:
#         explorer = CkanCatExplorer(cat_session)
#         try:

#             results = explorer.package_list_dataframe("polars")

#             # Assert that we got a result
#             assert results is not None, f"No results returned for {catalogue_url}"

#             # Check if we got the expected number of rows
#             assert len(results) > 100, f"There could be problem - check manually"

#             logger.info(f"Package search test passed for {catalogue_url}")
#         except requests.RequestException as e:
#             pytest.fail(f"Failed to perform package search for {catalogue_url}: {str(e)}")
#         except AssertionError as e:
#             pytest.fail(str(e))

# @pytest.mark.parametrize("catalogue_url", CATALOGUES)
# def test_package_list_dataframe_pandas(catalogue_url):
#     """
#     Test the package list functionality for predefined data catalogues
#     """
#     with CkanCatSession(catalogue_url) as cat_session:
#         explorer = CkanCatExplorer(cat_session)
#         try:

#             results = explorer.package_list_dataframe("pandas")

#             # Assert that we got a result
#             assert results is not None, f"No results returned for {catalogue_url}"

#             # Check if we got the expected number of rows
#             assert len(results) > 100, f"There could be problem - check manually"

#             logger.info(f"Package search test passed for {catalogue_url}")
#         except requests.RequestException as e:
#             pytest.fail(f"Failed to perform package search for {catalogue_url}: {str(e)}")
#         except AssertionError as e:
#             pytest.fail(str(e))
