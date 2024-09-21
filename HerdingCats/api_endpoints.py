from enum import Enum


class CkanApiPathsDocs:
    PACKAGE_LIST = "https://docs.ckan.org/en/2.11/api/index.html#ckan.logic.action.get.package_list"
    PACKAGE_SEARCH = "https://docs.ckan.org/en/2.11/api/index.html#ckan.logic.action.get.package_search"
    # Need to add the rest !!


class CkanApiPaths:
    BASE_PATH = "/api/3/action/{}"
    SITE_READ = BASE_PATH.format("site_read")
    PACKAGE_LIST = BASE_PATH.format("package_list")
    PACKAGE_SEARCH = BASE_PATH.format("package_search")
    PACKAGE_INFO = BASE_PATH.format("package_show")
    CURRENT_PACKAGE_LIST_WITH_RESOURCES = BASE_PATH.format(
        "current_package_list_with_resources"
    )
    # Add more paths as needed...


class DcatApiPaths:
    BASE_PATH = "/api/feed/dcat-ap/2.1.1.json"
    # Add more paths as needed...


class CkanDataCatalogues(Enum):
    LONDON_DATA_STORE = "https://data.london.gov.uk"
    UK_GOV = "https://data.gov.uk"
    SUBAK = "https://data.subak.org"
    HUMANITARIAN = "https://data.humdata.org"
    AFRICA = "https://open.africa"
    CANADA_GOV = "https://search.open.canada.ca/opendata"
    # Add more default catalogues as needed...
