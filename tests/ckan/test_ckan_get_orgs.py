import pytest
from HerdingCats.session.cat_session import CatSession
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
    with CatSession(catalogue_url) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            results = explorer.get_organisation_list()

            print(results)

            # Assert that we got a result
            assert results is not None, f"No results returned for {catalogue_url}"

            logger.info(f"Org list search test passed for {catalogue_url}")
        except requests.RequestException as e:
            pytest.fail(
                f"Failed to perform Org list search for {catalogue_url}: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))
