class CkanApiPaths:
    BASE_PATH = "/api/3/action/{}"
    PACKAGE_LIST = BASE_PATH.format("package_list")
    PACKAGE_SEARCH = BASE_PATH.format("package_search")
    # Add more paths as needed...


class DcatApiPaths:
    BASE_PATH = "/api/feed/dcat-ap/2.1.1.json"
