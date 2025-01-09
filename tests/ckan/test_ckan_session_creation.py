import pytest
from HerdingCats.session.cat_session import CatSession
from HerdingCats.endpoints.api_endpoints import CkanDataCatalogues


def test_cat_session_creation():
    """
    Check that a valid Ckan session can be created
    """
    try:
        session = CatSession(CkanDataCatalogues.LONDON_DATA_STORE)
        assert isinstance(
            session, CatSession
        ), "CkanCatSession object should be created"

        
        assert (
            session.base_url == "https://data.london.gov.uk"
        ), "CkanCatSession should have the correct base URL"

    except Exception as e:
        pytest.fail(f"Failed to create CkanCatSession: {str(e)}")


def test_cat_session_start():
    try:
        with CatSession(CkanDataCatalogues.LONDON_DATA_STORE) as session:
            assert session.session is not None, "Session object should be created"
    except Exception as e:
        pytest.fail(f"Failed to start CkanCatSession: {str(e)}")
