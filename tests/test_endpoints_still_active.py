import pytest
from src.herding_cats import CatSession

@pytest.fixture
def domain():
    return "data.london.gov.uk"

def test_cat_session_creation(domain):
    try:
        session = CatSession(domain)
        assert isinstance(session, CatSession), "CatSession object should be created"
        assert session.domain == domain, "CatSession should have the correct domain"
        assert session.base_url == f"https://{domain}", "CatSession should have the correct base URL"
    except Exception as e:
        pytest.fail(f"Failed to create CatSession: {str(e)}")

def test_cat_session_start(domain):
    try:
        with CatSession(domain) as session:
            assert session.session is not None, "Session object should be created"
    except Exception as e:
        pytest.fail(f"Failed to start CatSession: {str(e)}")
