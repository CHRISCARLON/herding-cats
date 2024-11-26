import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.explorer.cat_explore import CkanCatExplorer
import requests
from loguru import logger

CATALOGUES = [
    "https://data.london.gov.uk"
]

@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_get_package_count(catalogue_url):
    """
    Test that the get_package_count method returns a valid count of datasets
    for predefined data catalogues
    """
    with CatSession(catalogue_url) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            # Get the package count
            package_count = explorer.get_package_count()

            # Assert that we got a valid integer
            assert isinstance(package_count, int), f"Expected integer package count, got {type(package_count)}"

            # Assert that the count is positive
            assert package_count > 0, f"Expected positive package count, got {package_count}"

            logger.info(f"Successfully retrieved package count for {catalogue_url}: {package_count} packages")

        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to CKAN endpoint for {catalogue_url}: {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))
