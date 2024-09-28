from enum import Enum


# CKAN
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


class CkanDataCatalogues(Enum):
    LONDON_DATA_STORE = "https://data.london.gov.uk"
    UK_GOV = "https://data.gov.uk"
    SUBAK = "https://data.subak.org"
    HUMANITARIAN = "https://data.humdata.org"
    AFRICA = "https://open.africa"
    CANADA_GOV = "https://search.open.canada.ca/opendata"
    # Add more catalogues as needed...


class OpenDataSoftDataCatalogues(Enum):
    UK_POWER_NETWORKS = "https://ukpowernetworks.opendatasoft.com"
    INFRABEL = "https://opendata.infrabel.be"
    PARIS = "https://opendata.paris.fr"
    TOULOUSE = "https://data.toulouse-metropole.fr"
    # Add more catalogues as needed...


# OPEN DATASOFT
class OpenDataSoftApiPaths:
    # Normal base paths...
    BASE_PATH = "/api/v2/catalog/{}"
    SHOW_DATASETS = BASE_PATH.format("datasets")

    # Alternativre base paths...
    BASE_PATH_2 = "/api/explore/v2.0/catalog/{}"
    SHOW_DATASETS_2 = BASE_PATH_2.format("datasets")

    # Add more paths as needed...


# DCAT TBC
class DcatApiPaths:
    BASE_PATH = "/api/feed/dcat-ap/2.1.1.json"
    # Add more paths as needed...
