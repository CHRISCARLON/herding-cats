import pytest
from HerdingCats.session.session import CatSession
from HerdingCats.explorer.explore import CkanCatExplorer
from HerdingCats.config.sources import CkanDataCatalogues
import requests
from loguru import logger


def test_package_list_dictionary():
    """
    Test the package list functionality for predefined data catalogues
    """
    with CatSession(CkanDataCatalogues.UK_GOV) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            results = explorer.get_organisation_list()

            print(results)

            # Assert that we got a result
            assert (
                results is not None
            ), f"No results returned for {cat_session.base_url}"

            logger.info(f"Org list search test passed for {cat_session.base_url}")
        except requests.RequestException as e:
            pytest.fail(
                f"Failed to perform Org list search for {cat_session.base_url}: {str(e)}"
            )
        except AssertionError as e:
            pytest.fail(str(e))
