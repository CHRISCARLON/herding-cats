class CATExploreError(Exception):
    """Base exception for CATExplore"""

class CKANFetchError(CATExploreError):
    """Raised when CKAN fetch fails"""

class DCATFetchError(CATExploreError):
    """Raised when DCAT fetch fails"""