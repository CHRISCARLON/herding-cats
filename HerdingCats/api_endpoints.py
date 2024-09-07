from enum import Enum

class CkanApiPaths:
    BASE_PATH = "/api/3/action/{}"
    SITE_READ = BASE_PATH.format("site_read")
    PACKAGE_LIST = BASE_PATH.format("package_list")
    PACKAGE_SEARCH = BASE_PATH.format("package_search")
    PACKAGE_INFO = BASE_PATH.format("package_show")
    # Add more paths as needed...


class DcatApiPaths:
    BASE_PATH = "/api/feed/dcat-ap/2.1.1.json"
    # Add more paths as needed...


class CkanDataCatalogues(Enum):
    LONDON_DATA_STORE = "https://data.london.gov.uk"
    UK_GOV = "https://data.gov.uk"
    SUBAK = "https://data.subak.org"
    HUMANITARIAN = "https://data.humdata.org"
    # Add more catalogues as needed...
