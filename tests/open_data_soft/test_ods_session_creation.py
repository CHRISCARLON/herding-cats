import pytest
from HerdingCats.session.cat_session import CatSession

@pytest.fixture
def domain():
    return "ukpowernetworks.opendatasoft.com"

def test_cat_session_creation(domain):
    """
    Check that a valid Ckan session can be created
    """
    try:
        session = CatSession(domain)
        assert isinstance(
            session, CatSession
        ), "OpenDataSoftCatSession object should be created"
        assert session.domain == domain, "OpenDataSoftCatSession should have the correct domain"
        assert (
            session.base_url == f"https://{domain}"
        ), "OpenDataSoftCatSession should have the correct base URL"
    except Exception as e:
        pytest.fail(f"Failed to create OpenDataSoftCatSession: {str(e)}")


def test_cat_session_start(domain):
    try:
        with CatSession(domain) as session:
            assert session.session is not None, "Session object should be created"
    except Exception as e:
        pytest.fail(f"Failed to start CkanCatSession: {str(e)}")
