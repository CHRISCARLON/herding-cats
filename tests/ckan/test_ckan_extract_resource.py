import pytest
from HerdingCats.session.session import CatSession
from HerdingCats.explorer.explore import CkanCatExplorer
from HerdingCats.config.sources import CkanDataCatalogues
from loguru import logger


def test_extract_resource_url():
    """Test successful resource URL extraction"""
    with CatSession(CkanDataCatalogues.LONDON_DATA_STORE) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        try:
            # First get package info
            package_info = explorer.show_package_info("violence-reduction-unit")
            # Extract resource URL
            result = explorer.extract_resource_url(package_info)
            logger.success(result)

            # Assertions
            assert result is not None, "Should return result for known resource"
            assert isinstance(result, list), "Should return a list"

            assert all(
                map(
                    lambda x: len(x) == 4 and all(isinstance(i, str) for i in x), result
                )
            ), "All sublists should have 4 string elements"

        except Exception as e:
            pytest.fail(f"Failed to extract resource URL: {str(e)}")
