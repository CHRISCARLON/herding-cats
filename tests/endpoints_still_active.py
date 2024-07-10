import pytest
import requests
from herding_cats_explorer.herding_cats import CATExplore

@pytest.fixture
def cat_explore():
    return CATExplore("data.london.gov.uk")

@pytest.mark.parametrize("endpoint", [
    "package_search"
])
def test_fetch_ckan_sample_endpoint_active(cat_explore, endpoint):
    try:
        # Attempt to fetch data from the endpoint
        result = cat_explore.fetch_ckan_sample(endpoint)
        
        # If we get here, the request was successful
        assert True, f"Endpoint {endpoint} is active"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Endpoint {endpoint} is not active: {str(e)}")