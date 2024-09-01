import requests
import pandas as pd
import polars as pl

from typing import Any, Dict, Optional, Union, Literal, List
from loguru import logger
from urllib.parse import urlencode, urlparse

from .api_endpoints import CkanApiPaths, CKANDataCatalogues
from .cats_errors import CatExplorerError, CatSessionError


class CkanCatSession:
    def __init__(self, domain: Union[str, CKANDataCatalogues]) -> None:
        """Initialise CATExplore with a valid domain or predefined catalog."""
        self.domain = self._process_domain(domain)
        self.session = requests.Session()
        self.base_url = f"https://{self.domain}" if not self.domain.startswith('http') else self.domain

    @staticmethod
    def _process_domain(domain: Union[str, CKANDataCatalogues]) -> str:
        """Process the domain to ensure it's in the correct format."""
        if isinstance(domain, CKANDataCatalogues):
            return urlparse(domain.value).netloc

        # Check if the domain matches any predefined catalog
        for catalog in CKANDataCatalogues:
            if domain.lower() == catalog.name.lower().replace('_', ' '):
                url = urlparse(catalog.value).netloc
                logger.info(f"You are using: {url}")
                return url

        # If not a predefined catalog, process as a regular domain or URL
        parsed = urlparse(domain)
        return parsed.netloc if parsed.netloc else parsed.path


    def start_session(self) -> None:
        """Start a session with the specified domain."""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            logger.success(f"Session started successfully with {self.domain}")
        except requests.RequestException as e:
            logger.error(f"Failed to start session: {e}")
            raise CatSessionError(f"Failed to start session: {str(e)}")

    def close_session(self) -> None:
        """Close the session."""
        self.session.close()
        logger.info(f"Session closed for {self.domain}")

    def __enter__(self):
        """Allow use with context manager with"""
        self.start_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Allows use with context manager with"""
        self.close_session()

class CkanCatExplorer:
    def __init__(self, cat_session: CkanCatSession):
        self.cat_session = cat_session

    def package_list_dictionary(self) -> dict:
        """
        Returns dictionary of potential packages to use for further exploration:
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
            dictionary_prep = data['result']
            dictionary_data = {item: item for item in dictionary_prep}
            return dictionary_data
        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_list_dataframe(self, df_type: Literal["pandas", "polars"]) -> Union[pd.DataFrame, 'pl.DataFrame']:
        """Return all package information as a dataframe for further exploration.

        Must specify as df type:
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
            raise ValueError(f"Invalid df_type: '{df_type}'. Must be either 'pandas' or 'polars'.")

        url = self.cat_session.base_url + CkanApiPaths.PACKAGE_LIST
        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            result = data['result']

            if df_type.lower() == "polars":
                try:
                    return pl.DataFrame(result)
                except ImportError:
                    logger.warning("Polars is not installed. Please run 'pip install polars' to use this option.")
                    raise ImportError("Polars is not installed. Please run 'pip install polars' to use this option.")
            else:  # df_type.lower() == "pandas"
                return pd.DataFrame(result)

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to create DataFrame: {e}")
            raise CatExplorerError(f"Failed to create DataFrame: {str(e)}")

    def package_search_json(self, search_query: str, num_rows: int):
        """
        Returns all available data for a particular search query.

        Specify the number of rows if the 'count' is large as the ouput is capped.

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
            return data['result']
        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_search_condense_json(self, search_query: str, num_rows: int):
        """
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

        # Example usage...
        if __name__ == "__main__":
            with CatSession("data.london.gov.uk") as session:
                explorer = CatExplorer(session)
                condensed_results = explorer.package_search_condense("police")
                pprint(condensed_results)

        """
        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_SEARCH

        params = {}
        if search_query:
            params["q"] = search_query
            params['rows'] = num_rows

        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            data_prep = data['result']

            # Check for both 'result' and 'results' keys
            if 'result' in data_prep:
                result_data = data_prep['result']
            elif 'results' in data_prep:
                result_data = data_prep['results']
            else:
                raise KeyError("Neither 'result' nor 'results' key found in the API response")

            return self._extract_condensed_package_data(result_data,
                                    ['name', 'notes_markdown', 'num_resources'],
                                    ['name', 'created', 'format', 'url'])

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_search_condense_dataframe_packed(self, search_query: str, num_rows: int ,df_type: Literal["pandas", "polars"] = "pandas") -> Union[pd.DataFrame, 'pl.DataFrame']:
        """
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
            raise ValueError(f"Invalid df_type: '{df_type}'. Must be either 'pandas' or 'polars'.")

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
            data_prep = data['result']

            # Check for both 'result' and 'results' keys
            if 'result' in data_prep:
                result_data = data_prep['result']
            elif 'results' in data_prep:
                result_data = data_prep['results']
            else:
                raise KeyError("Neither 'result' nor 'results' key found in the API response")

            extracted_data = self._extract_condensed_package_data(
                result_data,
                ['name', 'notes_markdown', 'num_resources'],
                ['name', 'created', 'format', 'url']
            )

            if df_type.lower() == "polars":
                return pl.DataFrame(extracted_data)
            else:  # pandas
                return pd.DataFrame(extracted_data)

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_search_condense_dataframe_unpacked(self, search_query: str, num_rows: int, df_type: Literal["pandas", "polars"] = "pandas") -> Union[pd.DataFrame, 'pl.DataFrame']:
        """
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

        The resources column is now unested so you can use specific datasets more easily.

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
            raise ValueError(f"Invalid df_type: '{df_type}'. Must be either 'pandas' or 'polars'.")

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
            data_prep = data['result']

            # Check for both 'result' and 'results' keys
            if 'result' in data_prep:
                result_data = data_prep['result']
            elif 'results' in data_prep:
                result_data = data_prep['results']
            else:
                raise KeyError("Neither 'result' nor 'results' key found in the API response")

            extracted_data = self._extract_condensed_package_data(
                result_data,
                ['name', 'notes_markdown', 'num_resources'],
                ['name', 'created', 'format', 'url']
            )

            if df_type.lower() == "polars":
                return self._create_polars_dataframe(extracted_data)
            else:  # pandas
                return self._create_pandas_dataframe(extracted_data)

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    @staticmethod
    def _extract_condensed_package_data(data: List[Dict[str, Any]], fields: List[str], resource_fields: List[str]) -> List[Dict[str, Any]]:
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
                'resources': [
                    {resource_field: resource.get(resource_field) for resource_field in resource_fields}
                    for resource in entry.get('resources', [])
                ]
            }
            for entry in data
        ]

    @staticmethod
    def _create_pandas_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
        """TBC"""
        df = pd.json_normalize(
            data,
            record_path='resources',
            meta=['name', 'notes_markdown'],
            record_prefix='resource_'
        )
        return df

    @staticmethod
    def _create_polars_dataframe(data: List[Dict[str, Any]]) -> pl.DataFrame:
        """TBC"""
        df = pl.DataFrame(data)
        return df.explode('resources').with_columns([
            pl.col('resources').struct.field(f).alias(f"resource_{f}")
            for f in ['name', 'created', 'format', 'url']
        ]).drop('resources', 'num_resources')

    def package_show_info_json(self, package_name: Union[str, dict, Any]):
        """
        Pass in a package name as a string or as a value from a dictionary.

        # Example usage...
        if __name__ == "__main__":
            with CatSession("data.london.gov.uk") as session:
                explore = CatExplorer(session)
                all_packages = explore.package_list_json()
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
            return data['result']
        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def get_package_count(self) -> int:
        """TBC"""
        url = self.cat_session.base_url + CkanApiPaths.PACKAGE_LIST
        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            return len(data['result'])
        except requests.RequestException as e:
            logger.error(f"Failed to get package count: {e}")
            raise CatExplorerError(f"Failed to get package count: {str(e)}")

# Example usage...
if __name__ == "__main__":
    with CkanCatSession("subak") as session:
        explorer = CkanCatExplorer(session)
        results = explorer.package_search_condense_dataframe_unpacked('police', 500, "polars")
        print(results)
