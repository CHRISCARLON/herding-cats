import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.explorer.cat_explore import CkanCatExplorer
from HerdingCats.errors.cats_errors import CatExplorerError
from loguru import logger

CATALOGUES = ["https://data.london.gov.uk"]
TEST_PACKAGE = "violence-reduction-unit"
TEST_RESOURCE = "VRU Q1 2023-24 Dataset"

def test_extract_resource_url():
   """Test successful resource URL extraction"""
   with CatSession(CATALOGUES[0]) as cat_session:
       explorer = CkanCatExplorer(cat_session)
       try:
           # First get package info
           package_info = explorer.package_show_info_json(TEST_PACKAGE)

           # Extract resource URL
           result = explorer.extract_resource_url(package_info, TEST_RESOURCE)

           logger.success(result)

           # Assertions
           assert result is not None, "Should return result for known resource"
           assert isinstance(result, list), "Should return a list"
           assert len(result) == 2, "Should return format and URL"
           assert isinstance(result[0], str), "Format should be string"
           assert isinstance(result[1], str), "URL should be string"

       except Exception as e:
           pytest.fail(f"Failed to extract resource URL: {str(e)}")
