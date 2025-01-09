import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.explorer.cat_explore import CkanCatExplorer
from HerdingCats.endpoints.api_endpoints import CkanDataCatalogues
import requests
from loguru import logger


def test_package_show_info_json():
    """
    Test the package_show_info_json functionality
    """
    with CatSession(CkanDataCatalogues.LONDON_DATA_STORE) as cat_session:
        explorer = CkanCatExplorer(cat_session)

        package_name = "2011-boundary-files"

        try:
            results = explorer.show_package_info(package_name)
            print(results)

            # Basic assertions
            assert results is not None, "No results returned"
            assert isinstance(results, list), "Results should be a list"

            # Check structure of returned data
            if results:
                first_result = results[0]
                assert isinstance(first_result, dict), "Result items should be dictionaries"

                # Check for some expected keys as a basic check
                expected_keys = [
                    'name',
                    'notes_markdown',
                    'resource_created',
                    'resource_format',
                    'resource_name',
                    'resource_url'
                ]
                for key in expected_keys:
                    assert key in first_result, f"Missing expected key: {key}"

                # Verify specific values we know should be there
                assert first_result['name'] == package_name
                assert first_result['resource_format'] == 'shp'

            logger.info(f"Package show info test passed for {package_name}")

        except requests.RequestException as e:
            pytest.fail(f"Failed to get package info for {package_name}: {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))
