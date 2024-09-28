import requests
import pandas as pd
import polars as pl
import duckdb
import json

from typing import Any, Dict, Optional, Union, Literal, List
from loguru import logger
from urllib.parse import urlencode

from ..endpoints.api_endpoints import CkanApiPaths, OpenDataSoftApiPaths
from ..errors.cats_errors import CatExplorerError
from ..session.cat_session import CatSession


# FIND THE DATA YOU WANT / NEED / ISOLATE PACKAGES AND RESOURCES
# For Ckan Catalogues Only
class CkanCatExplorer:
    def __init__(self, cat_session: CatSession):
        """
        Takes in a CatSession

        Allows user to start exploring data catalogue programatically

        Make sure you pass a valid CkanCatSession in

        Args:
            CkanCatSession

        # Example usage...
        if __name__ == "__main__":
            with CatSession("data.london.gov.uk") as session:
                explore = CatExplorer(session)
        """
        self.cat_session = cat_session

    # ----------------------------
    # Check CKAN backend health
    # ----------------------------
    def check_site_health(self) -> None:
        """
        Make sure the Ckan endpoints are healthy and reachable

        This calls the Ckan site_read endpoint

        Will return a dictionary with a "success" field if all is well

        # Example usage...
        if __name__ == "__main__":
            with CatSession("data.london.gov.uk") as session:
                explore = CatExplorer(session)
                health_check = explore.check_site_health()

        """
        url = self.cat_session.base_url + CkanApiPaths.SITE_READ

        response = self.cat_session.session.get(url)
        response.raise_for_status()
        data = response.json()
        health_status = data.get("success")

        if health_status:
            logger.success("Health Check Passed: CKAN is running and available")
        else:
            logger.error(
                "Health Check Failed: Something went wrong and CKAN is currently not available"
            )

    # ----------------------------
    # Basic Available package lists + metadata
    # ----------------------------
    def get_package_count(self) -> int:
        """
        Quick way to see how 'big' a data catalogue is

        E.g how many datasets (packages) there are

        Returns:
            package_count: int

        # Example usage...
        if __name__ == "__main__":
            with CatSession("data.london.gov.uk") as session:
                explore = CatExplorer(session)
                package_count = get_package_count()
                pprint(package_count)
        """

        url = self.cat_session.base_url + CkanApiPaths.PACKAGE_LIST

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            package_count = response.json()
            return len(package_count["result"])
        except requests.RequestException as e:
            logger.error(f"Failed to get package count: {e}")
            raise CatExplorerError(f"Failed to get package count: {str(e)}")

    def package_list_dictionary(self) -> dict:
        """
        Explore all packages that are available to query.

        Returns:
            Dictionary of all available packages to use for further exploration.

            It follows a {"package_name": "package_name"} structure so that you can use the package names for
            additional methods

            {'--lfb-financial-and-performance-reporting-2021-22': '--lfb-financial-and-performance-reporting-2021-22',
             '-ghg-emissions-per-capita-from-food-and-non-alcoholic-drinks-': '-ghg-emissions-per-capita-from-food-and-non-alcoholic-drinks-',
             '100-west-cromwell-road-consultation-documents': '100-west-cromwell-road-consultation-documents',
             '19-year-olds-qualified-to-nvq-level-3': '19-year-olds-qualified-to-nvq-level-3',
             '1a---1c-eynsham-drive-public-consultation': '1a---1c-eynsham-drive-public-consultation',
             '2010-2013-gla-budget-detail': '2010-2013-gla-budget-detail',
             '2011-boundary-files': '2011-boundary-files',
             '2011-census-assembly': '2011-census-assembly',
             '2011-census-demography': '2011-census-demography'}

        # Example usage...
        if __name__ == "__main__":
            with CatSession("data.london.gov.uk") as session:
                explore = CatExplorer(session)
                all_packages = explore.package_list_json()
                pprint(all_packages)
        """

        url = self.cat_session.base_url + CkanApiPaths.PACKAGE_LIST

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            dictionary_prep = data["result"]
            dictionary_data = {item: item for item in dictionary_prep}
            return dictionary_data
        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_list_dataframe(
        self, df_type: Literal["pandas", "polars"]
    ) -> Union[pd.DataFrame, "pl.DataFrame"]:
        """
        Explore all packages that are available to query as a dataframe

        Must specify a df type:
            pandas
            polars

        Example ouput:
            shape: (68_995, 1)
            ┌─────────────────────
            │ column_0                        │
            │ ---                             │
            │ str                             │
            ╞═════════════════════
            │ 0-1-annual-probability-extents… │
            │ 0-1-annual-probability-extents… │
            │ 0-1-annual-probability-outputs… │
            │ 0-1-annual-probability-outputs… │
            │ 02a8c314-e726-44fb-88da-2e535e… │
            │ …                               │
            │ zoo-licensing-database          │
            │ zooplankton-abundance-data-der… │
            │ zooplankton-data-from-ring-net… │
            │ zoos-expert-committee-data      │
            │ zostera-descriptions-north-nor… │
            └─────────────────────

        # Example usage...
        if __name__ == "__main__":
            with CkanCatSession("uk gov") as session:
                explorer = CkanCatExplorer(session)
                results = explorer.package_list_dataframe('polars')
                print(results)

        """
        if df_type.lower() not in ["pandas", "polars"]:
            raise ValueError(
                f"Invalid df_type: '{df_type}'. DataFrame type must be either 'pandas' or 'polars'."
            )

        url = self.cat_session.base_url + CkanApiPaths.PACKAGE_LIST

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            result = data["result"]

            match df_type.lower():
                case "polars":
                    try:
                        return pl.DataFrame(result)
                    except ImportError:
                        raise ImportError(
                            "Polars is not installed. Please run 'pip install polars' to use this option."
                        )
                case "pandas":
                    try:
                        return pd.DataFrame(result)
                    except ImportError:
                        raise ImportError(
                            "Pandas is not installed. Please run 'pip install pandas' to use this option."
                        )
                case _:
                    raise ValueError(f"Unsupported DataFrame type: {df_type}")

        except (requests.RequestException, Exception) as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_list_dictionary_extra(self):
        """
        Explore all packages that are available to query.

        With extra resource and meta information.

        Sorted by most recently updated dataset first.

        # Example usage...
        if __name__ == "__main__":
            with CatSession("data.london.gov.uk") as session:
                explore = CatExplorer(session)
                info_extra = package_list_dictionary_extra()
                pprint(info_extra)

        """
        url = (
            self.cat_session.base_url + CkanApiPaths.CURRENT_PACKAGE_LIST_WITH_RESOURCES
        )
        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            dictionary_prep = data["result"]
            dictionary_data = [
                {
                    "owner_org": entry.get("owner_org"),
                    "name": entry.get("name"),
                    "title": entry.get("title"),
                    "maintainer": entry.get("maintainer"),
                    "metadata_created": entry.get("metadata_created"),
                    "metadata_modified": entry.get("metadata_modified"),
                    "resources": entry.get("resources"),
                    "groups": entry.get("groups"),
                }
                for entry in dictionary_prep
            ]
            return dictionary_data
        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")
        return

    # ----------------------------
    # Show catalogue freshness
    # ----------------------------
    def catalogue_freshness(self):
        """
        Explore all packages that are available to query.
        Returns a view of how many resources have been updated in the last 6 months
        as a percentage of the total number of resources, based on unique package names.
        """
        logger.warning(
            "This method might not work for all catalogues, and will return 0s"
        )

        url = (
            self.cat_session.base_url + CkanApiPaths.CURRENT_PACKAGE_LIST_WITH_RESOURCES
        )
        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            dictionary_prep = data["result"]

            dictionary_data = [
                {
                    "owner_org": entry.get("owner_org"),
                    "name": entry.get("name"),
                    "title": entry.get("title"),
                    "maintainer": entry.get("maintainer"),
                    "metadata_created": entry.get("metadata_created"),
                    "metadata_modified": entry.get("metadata_modified"),
                    "resources": entry.get("resources"),
                    "groups": entry.get("groups"),
                }
                for entry in dictionary_prep
            ]

            df = self._duckdb_explore(
                dictionary_data,
                "freshness",
                """
                WITH package_stats AS (
                    SELECT
                        name,
                        COUNT(*) as resource_count,
                        MAX(TRY_CAST(metadata_modified AS TIMESTAMP)) as last_update
                    FROM freshness
                    GROUP BY name
                )
                SELECT
                    COUNT(DISTINCT name) as total_packages,
                    SUM(resource_count) as total_resources,
                    COUNT(DISTINCT CASE WHEN last_update >= CURRENT_TIMESTAMP - INTERVAL 6 MONTH THEN name END) as updated_packages_last_6_months,
                    COUNT(DISTINCT CASE WHEN last_update >= CURRENT_TIMESTAMP - INTERVAL 6 MONTH THEN name END) * 100.0 / COUNT(DISTINCT name) as percentage_updated_packages_last_6_months
                FROM package_stats
                """,
            )

            return df

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    # ----------------------------
    # Show metadata using a package name
    # ----------------------------
    def package_show_info_json(self, package_name: Union[str, dict, Any]) -> List[Dict]:
        """
        Pass in a package name as a string or as a value from a dictionary

        This will return package metadata including resource information and download links for the data

        # Example usage...
        if __name__ == "__main__":
            with CkanCatSession("data.london.gov.uk") as session:
                explore = CkanCatExplorer(session)
                all_packages = explore.package_list_dictionary()
                census = all_packages.get("2011-boundary-files")
                census_info = explore.package_show_info_json(census)
                pprint(census_info)
        """

        if package_name is None:
            raise ValueError("package name cannot be none")

        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_INFO

        params = {}
        if package_name:
            params["id"] = package_name

        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            result_data = data["result"]

            return self._extract_resource_data(result_data)

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    # ----------------------------
    # Search Packages and store in DataFrames / or keep as Dicts
    # Unpack data or keep it packed (e.g. don't split out resources into own columns')
    # ----------------------------
    def package_search_json(self, search_query: str, num_rows: int):
        """
        Returns all available data for a particular search query

        Specify the number of rows if the 'count' is large

        """

        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_SEARCH

        params = {}
        if search_query:
            params["q"] = search_query
            params["rows"] = num_rows

        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data["result"]
        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_search_condense_json_unpacked(
        self, search_query: str, num_rows: int
    ) -> Optional[List[Dict]]:
        """
        Args:
            Search query: str
            Number of rows: int

        Returns a more condensed view of package informaton focusing on:
            name
            number of resources
            notes
            resource:
                name
                created date
                format
                url to download

        # Example usage...
        if __name__ == "__main__":
            with CatSession("data.london.gov.uk") as session:
                explorer = CatExplorer(session)
                condensed_results = explorer.package_search_condense_json_unpacked("police")
                pprint(condensed_results)

        """
        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_SEARCH

        params = {}
        if search_query:
            params["q"] = search_query
            params["rows"] = num_rows

        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            data_prep = data["result"]

            # Check for both 'result' and 'results' keys
            if "result" in data_prep:
                result_data = data_prep["result"]
            elif "results" in data_prep:
                result_data = data_prep["results"]
            else:
                raise KeyError(
                    "Neither 'result' nor 'results' key found in the API response"
                )

            return self._extract_condensed_package_data(
                result_data,
                ["name", "notes_markdown"],
                ["name", "created", "format", "url"],
            )

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_search_condense_dataframe_packed(
        self,
        search_query: str,
        num_rows: int,
        df_type: Literal["pandas", "polars"] = "pandas",
    ) -> Union[pd.DataFrame, "pl.DataFrame"]:
        """
        Args:
            Search query: str
            Number of rows: int

        Returns a more condensed view of package informaton focusing on:
            name
            number of resources
            notes
            resource:
                name
                created date
                format
                url to download

        Specify the number of rows if the 'count' is large as the ouput is capped.

        The resources column is still nested.

        shape: (409, 4)
        ┌─────────────────────────────────┬────────────────┬───────────
        │ name                            ┆ notes_markdown ┆ num_resources ┆ resources                       │
        │ ---                             ┆ ---            ┆ ---           ┆ ---                             │
        │ str                             ┆ null           ┆ i64           ┆ list[struct[4]]                 │
        ╞═════════════════════════════════╪════════════════╪═══════════
        │ police-force1                   ┆ null           ┆ 3             ┆ [{"Police Force","2020-04-12T0… │
        │ police-stations-nsc             ┆ null           ┆ 5             ┆ [{null,"2015-05-29T16:11:17.58… │
        │ police-stations                 ┆ null           ┆ 2             ┆ [{"Police Stations","2016-01-1… │
        │ police-stations1                ┆ null           ┆ 8             ┆ [{"ArcGIS Hub Dataset","2019-0… │
        │ police-force-strength           ┆ null           ┆ 1             ┆ [{"Police force strength","202… │
        │ …                               ┆ …              ┆ …             ┆ …                               │
        │ crown_prosecution_service       ┆ null           ┆ 2             ┆ [{null,"2013-03-11T19:20:34.43… │
        │ register-of-geographic-codes-j… ┆ null           ┆ 1             ┆ [{"ArcGIS Hub Dataset","2024-0… │
        │ code-history-database-august-2… ┆ null           ┆ 1             ┆ [{"ArcGIS Hub Dataset","2024-0… │
        │ council-tax                     ┆ null           ┆ 3             ┆ [{"Council tax average per cha… │
        │ code-history-database-june-201… ┆ null           ┆ 1             ┆ [{"ArcGIS Hub Dataset","2024-0… │
        └─────────────────────────────────┴────────────────┴───────────

        # Example usage...
        if __name__ == "__main__":
            with CkanCatSession("uk gov") as session:
                explorer = CkanCatExplorer(session)
                results = explorer.package_search_condense_dataframe_packed('police', 500, "polars")
                print(results)

        """
        if df_type.lower() not in ["pandas", "polars"]:
            raise ValueError(
                f"Invalid df_type: '{df_type}'. Must be either 'pandas' or 'polars'."
            )

        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_SEARCH
        params = {}
        if search_query:
            params["q"] = search_query
            params["rows"] = num_rows

        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            data_prep = data["result"]

            # Check for both 'result' and 'results' keys
            if "result" in data_prep:
                result_data = data_prep["result"]
            elif "results" in data_prep:
                result_data = data_prep["results"]
            else:
                raise KeyError(
                    "Neither 'result' nor 'results' key found in the API response"
                )

            extracted_data = self._extract_condensed_package_data(
                result_data,
                ["name", "notes_markdown", "num_resources"],
                ["name", "created", "format", "url"],
            )

            if df_type.lower() == "polars":
                return pl.DataFrame(extracted_data)
            else:  # pandas
                return pd.DataFrame(extracted_data)

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_search_condense_dataframe_unpacked(
        self,
        search_query: str,
        num_rows: int,
        df_type: Literal["pandas", "polars"] = "pandas",
    ) -> Union[pd.DataFrame, "pl.DataFrame"]:
        """
        Args:
            Search query: str
            Number of rows: int

        Returns a more condensed view of package informaton focusing on:
            name
            number of resources
            notes
            resource:
                name
                created date
                format
                url to download

        Specify the number of rows if the 'count' is large as the ouput is capped.

        The resources column is now unested so you can use specific dataset resources more easily.

        This will be a much larger df as a result - check the shape.

        shape: (2_593, 6)
        ┌─────────────────────────────┬────────────────┬─────────────────────────────┬─────────────────
        │ name                        ┆ notes_markdown ┆ resource_name               ┆ resource_created           ┆ resource_format ┆ resource_url               │
        │ ---                         ┆ ---            ┆ ---                         ┆ ---                        ┆ ---             ┆ ---                        │
        │ str                         ┆ null           ┆ str                         ┆ str                        ┆ str             ┆ str                        │
        ╞═════════════════════════════╪════════════════╪═════════════════════════════╪═════════════════
        │ police-force1               ┆ null           ┆ Police Force                ┆ 2020-04-12T08:28:35.449556 ┆ JSON            ┆ http://<div class="field   │
        │                             ┆                ┆                             ┆                            ┆                 ┆ field…                     │
        │ police-force1               ┆ null           ┆ List of neighbourhoods for  ┆ 2020-04-12T08:28:35.449564 ┆ JSON            ┆ http://<div class="field   │
        │                             ┆                ┆ the…                        ┆                            ┆                 ┆ field…                     │
        │ police-force1               ┆ null           ┆ Senior officers for the     ┆ 2020-04-12T08:28:35.449566 ┆ JSON            ┆ http://<div class="field   │
        │                             ┆                ┆ Cambri…                     ┆                            ┆                 ┆ field…                     │
        │ police-stations-nsc         ┆ null           ┆ null                        ┆ 2015-05-29T16:11:17.586034 ┆ HTML            ┆ http://data.n-somerset.gov │
        │                             ┆                ┆                             ┆                            ┆                 ┆ .uk/…                      │
        │ police-stations-nsc         ┆ null           ┆ null                        ┆ 2020-08-11T13:35:47.462440 ┆ CSV             ┆ http://data.n-somerset.gov │
        │                             ┆                ┆                             ┆                            ┆                 ┆ .uk/…                      │
        │ …                           ┆ …              ┆ …                           ┆ …                          ┆ …               ┆ …                          │
        │ code-history-database-augus ┆ null           ┆ ArcGIS Hub Dataset          ┆ 2024-05-31T19:06:58.646735 ┆ HTML            ┆ https://open-geography-por │
        │ t-2…                        ┆                ┆                             ┆                            ┆                 ┆ talx…                      │
        │ council-tax                 ┆ null           ┆ Council tax average per     ┆ 2017-07-20T08:21:23.185880 ┆ CSV             ┆ https://plymouth.thedata.p │
        │                             ┆                ┆ charge…                     ┆                            ┆                 ┆ lace…                      │
        │ council-tax                 ┆ null           ┆ Council Tax Band D amounts  ┆ 2017-07-20T08:26:28.314556 ┆ CSV             ┆ https://plymouth.thedata.p │
        │                             ┆                ┆ pai…                        ┆                            ┆                 ┆ lace…                      │
        │ council-tax                 ┆ null           ┆ Council Tax Collected as    ┆ 2017-07-20T15:23:26.889271 ┆ CSV             ┆ https://plymouth.thedata.p │
        │                             ┆                ┆ Perce…                      ┆                            ┆                 ┆ lace…                      │
        │ code-history-database-june- ┆ null           ┆ ArcGIS Hub Dataset          ┆ 2024-05-31T19:06:20.071480 ┆ HTML            ┆ https://open-geography-por │
        │ 201…                        ┆                ┆                             ┆                            ┆                 ┆ talx…                      │
        └─────────────────────────────┴────────────────┴─────────────────────────────┴─────────────────

        # Example usage...
        if __name__ == "__main__":
            with CkanCatSession("uk gov") as session:
                explorer = CkanCatExplorer(session)
                results = explorer.package_search_condense_dataframe_unpacked('police', 500, "polars")
                print(results)

        """
        if df_type.lower() not in ["pandas", "polars"]:
            raise ValueError(
                f"Invalid df_type: '{df_type}'. Must be either 'pandas' or 'polars'."
            )

        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_SEARCH
        params = {}
        if search_query:
            params["q"] = search_query
            params["rows"] = num_rows
        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            data_prep = data["result"]

            # Check for both 'result' and 'results' keys
            if "result" in data_prep:
                result_data = data_prep["result"]
            elif "results" in data_prep:
                result_data = data_prep["results"]
            else:
                raise KeyError(
                    "Neither 'result' nor 'results' key found in the API response"
                )

            extracted_data = self._extract_condensed_package_data(
                result_data,
                ["name", "notes_markdown"],
                ["name", "created", "format", "url"],
            )

            if df_type.lower() == "polars":
                return self._create_polars_dataframe(extracted_data)
            else:  # pandas
                return self._create_pandas_dataframe(extracted_data)

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    # ----------------------------
    # Extract specific data from results
    # OR flatten nested data structures
    # ----------------------------
    def extract_resource_url(
        self, package_info: List[Dict], resource_name: str
    ) -> List[str] | None:
        """
        Extracts the URL and format of a specific resource from a package.

        Specify the name of the resource you want to use.

        Returns:
        List[format, url]: The format of the resource and the URL.

        Example:
            if __name__ == "__main__":
                with CkanCatSession("data.london.gov.uk") as session:
                    explore = CkanCatExplorer(session)
                    all_packages = explore.package_list_dictionary()
                    data = all_packages.get("violence-reduction-unit")
                    info = explore.package_show_info_json(data)
                    dl_link = explore.extract_resource_url(info, "VRU Q1 2023-24 Dataset")
                    print(dl_link)

        [
        'spreadsheet',
        'https://data.london.gov.uk/download/violence-reduction-unit/1ef840d0-2c02-499c-ae40-382005b2a0c7/VRU%2520Dataset%2520Q1%2520April-Nov%25202023.xlsx'
        ]

        """

        for item in package_info:
            if item.get("resource_name") == resource_name:
                url = item.get("resource_url")
                format = item.get("resource_format")
                if url and format:
                    logger.success(
                        f"Found URL for resource '{resource_name}'. Format is: {format}"
                    )
                    return [format, url]
                else:
                    logger.warning(
                        f"Resource '{resource_name}' found in package, but no URL available"
                    )
                    return None

    @staticmethod
    def _extract_condensed_package_data(
        data: List[Dict[str, Any]], fields: List[str], resource_fields: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Static method to extract specified fields from Package Search dataset entries and their resources.

        Args:
            data (List[Dict[str, Any]]): List of dataset entries.
            fields (List[str]): List of field names to extract from each entry.
            resource_fields (List[str]): List of field names to extract from each resource section.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing extracted data.

        Example output:
            [{'name': 'police-force-strength',
            'notes_markdown': 'Numbers of police officers, police civilian staff, and '
                                'Police Community Support Officers in the Metropolitan '
                                "Police Force. Figures are reported by MOPAC to the GLA's "
                                'Police and Crime Committee each month. The figures are '
                                'full-time equivalent figures (FTE) in order to take '
                                'account of part-time working, job sharing etc, and do not '
                                'represent a measure of headcount.
                                'For more information, click here and here.',
            'num_resources': 1,
            'resources': [{'created': '2024-08-28T16:15:59.080Z',
                            'format': 'csv',
                            'name': 'Police force strength',
                            'url': 'https://airdrive-secure.s3-eu-west-1.amazonaws.com/
                            london/dataset/police-force-strength/2024-08-28T16%3A15%3A56/
                            Police_Force_Strength.csv'}]}
        """
        return [
            {
                **{field: entry.get(field) for field in fields},
                "resources": [
                    {
                        resource_field: resource.get(resource_field)
                        for resource_field in resource_fields
                    }
                    for resource in entry.get("resources", [])
                ],
            }
            for entry in data
        ]

    @staticmethod
    def _create_pandas_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
        """TBC"""
        df = pd.json_normalize(
            data,
            record_path="resources",
            meta=["name", "notes_markdown"],
            record_prefix="resource_",
        )
        return df

    @staticmethod
    def _create_polars_dataframe(data: List[Dict[str, Any]]) -> pl.DataFrame:
        """TBC"""
        df = pl.DataFrame(data)
        return (
            df.explode("resources")
            .with_columns(
                [
                    pl.col("resources").struct.field(f).alias(f"resource_{f}")
                    for f in ["name", "created", "format", "url"]
                ]
            )
            .drop("resources", "num_resources")
        )

    @staticmethod
    def _extract_resource_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts specific fields for a specific package and creates a list of dictionaries,
        one for each resource, containing the specified fields.

        Args:
        data (Dict[str, Any]): The input package data dictionary.

        Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the specified fields for a resource.
        """
        base_fields = {
            "name": data.get("name"),
            "notes_markdown": data.get("notes_markdown"),
        }

        resource_fields = ["url", "name", "format", "created", "last_modified"]

        result = []
        for resource in data.get("resources", []):
            resource_data = base_fields.copy()
            for field in resource_fields:
                resource_data[f"resource_{field}"] = resource.get(field)
            result.append(resource_data)

        return result

    @staticmethod
    def _duckdb_explore(
        data: List[Dict[str, Any]],
        table_name: str,
        query: str = "",
    ) -> pd.DataFrame:
        """
        Create in memory duckdb to explore catalogue data and isolate resources for further analysis
        """
        try:
            flattened_data = []
            for entry in data:
                base_entry = {
                    k: v for k, v in entry.items() if k not in ["resources", "groups"]
                }
                # Handle groups - store as a list of group names
                base_entry["groups"] = [
                    group["name"] for group in entry.get("groups", [])
                ]
                # Handle resources
                if entry.get("resources"):
                    for resource in entry["resources"]:
                        resource_entry = base_entry.copy()
                        resource_entry.update(
                            {f"resource_{k}": v for k, v in resource.items()}
                        )
                        flattened_data.append(resource_entry)
                else:
                    flattened_data.append(base_entry)
            # Convert the flattened data to a pandas DataFrame
            df = pd.DataFrame(flattened_data)
            logger.success("DataFrame Successfully Created")
            # Use a context manager for the DuckDB connection
            with duckdb.connect(":memory:") as con:
                # Register the pandas DataFrame as a table in DuckDB
                con.register(f"{table_name}", df)
                # Execute the provided query
                result = con.execute(query).fetchdf()
            return result
        except Exception as e:
            print(f"Error when creating DuckDB DataFrame: {str(e)}")
            print("First few elements of input data:")
            print(json.dumps(data[:2], indent=2))
            return pd.DataFrame()


# FIND THE DATA YOU WANT / NEED / ISOLATE PACKAGES AND RESOURCES
# For Open Datasoft Catalogues Only
class OpenDataSoftCatExplorer:
    def __init__(self, cat_session: CatSession):
        """
        Takes in a CatSession

        Allows user to start exploring data catalogue programatically

        Make sure you pass a valid CkanCatSession in

        Args:
            CkanCatSession

        # Example usage...
        if __name__ == "__main__":
            with CatSession("ukpowernetworks.opendatasoft.com") as session:
                explore = CatExplorer(session)
        """
        self.cat_session = cat_session

    def fetch_all_datasets(self) -> dict | None:
        urls = [
            self.cat_session.base_url + OpenDataSoftApiPaths.SHOW_DATASETS,
            self.cat_session.base_url + OpenDataSoftApiPaths.SHOW_DATASETS_2,
        ]
        dataset_dict = {}
        total_count = 0

        for url in urls:
            offset = 0
            limit = 100

            try:
                while True:
                    params = {"offset": offset, "limit": limit}
                    response = self.cat_session.session.get(url, params=params)

                    if response.status_code == 400 and url == urls[0]:
                        logger.warning(
                            "SHOW_DATASETS endpoint returned 400 status. Trying SHOW_DATASETS_2."
                        )
                        break  # Break the inner loop to try the next URL

                    response.raise_for_status()
                    result = response.json()

                    for dataset_info in result.get("datasets", []):
                        if (
                            "dataset" in dataset_info
                            and "metas" in dataset_info["dataset"]
                            and "default" in dataset_info["dataset"]["metas"]
                            and "title" in dataset_info["dataset"]["metas"]["default"]
                            and "dataset_id" in dataset_info["dataset"]
                        ):
                            title = dataset_info["dataset"]["metas"]["default"]["title"]
                            dataset_id = dataset_info["dataset"]["dataset_id"]
                            dataset_dict[title] = dataset_id

                    # Update total_count if available
                    if "total_count" in result:
                        total_count = result["total_count"]

                    # Check if we've reached the end of the datasets
                    if len(result.get("datasets", [])) < limit:
                        break
                    offset += limit

                # If we've successfully retrieved datasets, no need to try the second URL
                if dataset_dict:
                    break

            except requests.RequestException as e:
                if url == urls[-1]:
                    logger.error(f"Failed to fetch datasets: {e}")
                    raise CatExplorerError(f"Failed to fetch datasets: {str(e)}")
                else:
                    logger.warning(
                        f"Failed to fetch datasets from {url}: {e}. Trying next URL."
                    )

        if dataset_dict:
            returned_count = len(dataset_dict)
            if returned_count == total_count:
                logger.success(
                    f"total_count = {total_count} AND returned_count = {returned_count}"
                )
            else:
                logger.warning(
                    f"Mismatch in counts: total_count = {total_count}, returned_count = {returned_count}"
                )
            return dataset_dict
        else:
            logger.warning("No datasets were retrieved.")
            return None