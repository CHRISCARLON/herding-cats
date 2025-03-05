import pytest
import requests
from pprint import pprint
from HerdingCats.session.session import CatSession
from HerdingCats.explorer.explore import CkanCatExplorer
from HerdingCats.config.sources import CkanDataCatalogues
from loguru import logger

def test_package_search_json():
    """Test the package_search_json functionality"""
    with CatSession(CkanDataCatalogues.LONDON_DATA_STORE) as cat_session:
        explorer = CkanCatExplorer(cat_session)
        query = "police" 
        try:
            results = explorer.package_search(query, 50)
            pprint(results)
            
            # Basic assertions
            assert results is not None, "No results returned"
            assert isinstance(results, dict), "Results should be a dictionary"
            
            # Check for expected keys in response
            assert 'count' in results, "Missing count key"
            assert 'result' in results or 'results' in results, "Missing result/results key"
            
            # Get the results list
            results_list = results.get('results', results.get('result', []))
            assert isinstance(results_list, list), "Results should be a list"
            
            # Check content of results if any found
            if results_list:
                first_result = results_list[0]
                assert isinstance(first_result, dict), "Result list items should include dictionaries"
                
                # Check for common CKAN package fields
                package_keys = ['id', 'name', 'title']
                for key in package_keys:
                    assert key in first_result, f"Missing expected package key: {key}"
                    
                logger.info(f"Package search test passed for query '{query}' with {len(results_list)} results")
                
        except requests.RequestException as e:
            pytest.fail(f"Failed to search packages with query '{query}': {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))