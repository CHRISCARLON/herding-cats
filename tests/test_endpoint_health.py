import pytest
from HerdingCats.herding_cats import CkanCatSession
from HerdingCats.api_endpoints import CkanApiPaths, CkanDataCatalogues
import requests
from loguru import logger

CATALOGUES = [
    "https://data.london.gov.uk",
    "https://data.humdata.org"
]

@pytest.mark.parametrize("catalogue_url", CATALOGUES)
def test_site_read(catalogue_url):
    """
    Check that predefined data cataloues return True - means they can be used
    """
    with CkanCatSession(catalogue_url) as cat_session:
        url = cat_session.base_url + CkanApiPaths.SITE_READ
        try:
            response = cat_session.session.get(url)
            response.raise_for_status()
            assert response.status_code == 200
            data = response.json()
            assert data.get("success") == True, f"CKAN site_read endpoint returned False for {catalogue_url}"
            logger.info(f"CKAN site_read check passed for {catalogue_url}")
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to CKAN site_read endpoint for {catalogue_url}: {str(e)}")
        except AssertionError as e:
            pytest.fail(str(e))
