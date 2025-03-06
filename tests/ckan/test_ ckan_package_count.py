import pytest
from HerdingCats.session.session import CatSession
from HerdingCats.explorer.explore import CkanCatExplorer
from HerdingCats.config.sources import CkanDataCatalogues
import requests
from loguru import logger


def test_get_package_count():
    """
    Test that the get_package_count method returns a valid count of datasets
    for predefined data catalogues...
    """
    with CatSession(CkanDataCatalogues.LONDON_DATA_STORE) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            # Get the package count
            package_count = explorer.get_package_count()

            # Assert that we got a valid integer
            assert isinstance(package_count, int), f"Expected integer package count, got {type(package_count)}"

            # Assert that the count is positive
            assert package_count > 0, f"Expected positive package count, got {package_count}"

            logger.info(f"Successfully retrieved package count for {cat_session.base_url}: {package_count} packages")

        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to CKAN endpoint for {cat_session.base_url}: {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))
