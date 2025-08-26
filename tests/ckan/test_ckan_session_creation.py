import pytest
from HerdingCats.session.session import CatSession
from HerdingCats.config.sources import CkanDataCatalogues


def test_cat_session_creation():
    """
    Check that a valid Ckan session can be created
    """
    try:
        session = CatSession(CkanDataCatalogues.UK_GOV)
        assert isinstance(session, CatSession), (
            "CkanCatSession object should be created"
        )

    except Exception as e:
        pytest.fail(f"Failed to create CkanCatSession: {str(e)}")


def test_cat_session_start():
    try:
        with CatSession(CkanDataCatalogues.UK_GOV) as session:
            assert session.session is not None, "Session object should be created"
    except Exception as e:
        pytest.fail(f"Failed to start CkanCatSession: {str(e)}")
