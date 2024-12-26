from enum import Enum

# CKAN
class CkanApiPathsDocs:
    PACKAGE_LIST = "https://docs.ckan.org/en/2.11/api/index.html#ckan.logic.action.get.package_list"
    PACKAGE_SEARCH = "https://docs.ckan.org/en/2.11/api/index.html#ckan.logic.action.get.package_search"
    CURRENT_PACKAGE_LIST_WITH_RESOURCES = "https://docs.ckan.org/en/2.11/api/index.html#ckan.logic.action.get.current_package_list_with_resources"
    ORGANIZATION_LIST = "https://docs.ckan.org/en/2.10/api/index.html#ckan.logic.action.get.organization_list"
    # Need to add the rest....

class CkanApiPaths:
    BASE_PATH = "/api/3/action/{}"
    PACKAGE_LIST = BASE_PATH.format("package_list")
    PACKAGE_SEARCH = BASE_PATH.format("package_search")
    PACKAGE_INFO = BASE_PATH.format("package_show")
    CURRENT_PACKAGE_LIST_WITH_RESOURCES = BASE_PATH.format(
        "current_package_list_with_resources"
    )
    ORGANIZATION_LIST = BASE_PATH.format("organization_list")
    # Add more paths as needed...

class CkanDataCatalogues(Enum):
    LONDON_DATA_STORE = "https://data.london.gov.uk"
    UK_GOV = "https://data.gov.uk"
    SUBAK = "https://data.subak.org"
    HUMANITARIAN_DATA_STORE = "https://data.humdata.org"
    OPEN_AFRICA = "https://open.africa"
    # CANADA_GOV = "https://search.open.canada.ca/opendata" NEED TO LOOK INTO THIS ONE MORE
    # NORTHERN_DATA_MILL = "https://datamillnorth.org" NEED TO LOOK INTO THIS ONE MORE
    # Add more catalogues as needed...

# OPEN DATASOFT
class OpenDataSoftDataCatalogues(Enum):
    UK_POWER_NETWORKS = "https://ukpowernetworks.opendatasoft.com"
    INFRABEL = "https://opendata.infrabel.be"
    PARIS = "https://opendata.paris.fr"
    TOULOUSE = "https://data.toulouse-metropole.fr"
    ELIA_BELGIAN_ENERGY = "https://opendata.elia.be"
    EDF_ENERGY = "https://opendata.edf.fr"
    CADENT_GAS = "https://cadentgas.opendatasoft.com"
    GRD_FRANCE = "https://opendata.agenceore.fr"
    # Add more catalogues as needed...

class OpenDataSoftApiPaths:
    # Normal base paths...
    BASE_PATH = "/api/v2/catalog/{}"
    SHOW_DATASETS = BASE_PATH.format("datasets")
    SHOW_DATASET_INFO = BASE_PATH.format("datasets/{}")
    SHOW_DATASET_EXPORTS = BASE_PATH.format("datasets/{}/exports")

    # Alternative base paths...
    # TODO Sometimes these are needed - not sure why need to dig into this!
    BASE_PATH_2 = "/api/explore/v2.0/catalog/{}"
    SHOW_DATASETS_2 = BASE_PATH_2.format("datasets")
    SHOW_DATASET_INFO_2 = BASE_PATH_2.format("datasets/{}")
    SHOW_DATASET_EXPORTS_2 = BASE_PATH_2.format("datasets/{}/exports")
    # Add more paths as needed...

# DCAT TBC
class DcatApiPaths:
    BASE_PATH = "/api/feed/dcat-ap/2.1.1.json"
    # Add more paths as needed...

# BESPOKE DATA GOUV FR
class FrenchGouvApiDocs:
    DATASET_DOCS = "https://guides.data.gouv.fr/guide-data.gouv.fr/api-1/reference/datasets"

class FrenchGouvApiPaths:
    BASE_PATH = "/api/1/{}"
    SHOW_DATASETS = BASE_PATH.format("datasets")
    SHOW_DATASETS_BY_ID = BASE_PATH.format("datasets/{}")
    SHOW_DATASET_RESOURCE_BY_ID = BASE_PATH.format("datasets/{}/resources/")
    CATALOGUE = "https://object.files.data.gouv.fr/hydra-parquet/hydra-parquet/b06842f8ee27a0302ebbaaa344d35e4c.parquet"

class FrenchGouvCatalogue(Enum):
    GOUV_FR = "https://www.data.gouv.fr"
