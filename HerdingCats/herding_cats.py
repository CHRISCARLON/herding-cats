import requests
import pandas as pd
import polars as pl

from typing import Any, Dict, Optional, Union, Literal, List
from loguru import logger
from urllib.parse import urlencode

from api_endpoints import CkanApiPaths
from cats_errors import CatExplorerError, CatSessionError

class CkanCatSession:
    def __init__(self, domain: str) -> None:
        """Initialise CATExplore with a domain."""
        self.domain = domain
        self.session = requests.Session()
        self.base_url = f"https://{self.domain}"

    def start_session(self) -> None:
        """Start a session with the specified domain."""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            logger.info(f"Session started successfully with {self.domain}")
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

    def package_search_json(self, search_query: Optional[str]=None):
        """TBC"""
        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_SEARCH

        params = {}
        if search_query:
            params["q"] = search_query

        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data['result']
        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_search_condense_json(self, search_query: Optional[str]=None):
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

        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            data_prep = data['result']

            return self._extract_condensed_package_data(data_prep['result'],
                                    ['name', 'notes_markdown', 'num_resources'],
                                    ['name', 'created', 'format', 'url'])

        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def package_search_condense_dataframe_packed(self, search_query: Optional[str] = None, df_type: Literal["pandas", "polars"] = "pandas") -> Union[pd.DataFrame, 'pl.DataFrame']:
        """TBC"""
        if df_type.lower() not in ["pandas", "polars"]:
            raise ValueError(f"Invalid df_type: '{df_type}'. Must be either 'pandas' or 'polars'.")

        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_SEARCH
        params = {}
        if search_query:
            params["q"] = search_query
        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            data_prep = data['result']

            extracted_data = self._extract_condensed_package_data(
                data_prep['result'],
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

    def package_search_condense_dataframe_unpacked(self, search_query: Optional[str] = None, df_type: Literal["pandas", "polars"] = "pandas") -> Union[pd.DataFrame, 'pl.DataFrame']:
        """TBC"""
        if df_type.lower() not in ["pandas", "polars"]:
            raise ValueError(f"Invalid df_type: '{df_type}'. Must be either 'pandas' or 'polars'.")

        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_SEARCH
        params = {}
        if search_query:
            params["q"] = search_query
        url = f"{base_url}?{urlencode(params)}" if params else base_url

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            data_prep = data['result']

            extracted_data = self._extract_condensed_package_data(
                data_prep['result'],
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
    def _create_polars_dataframe(data: List[Dict[str, Any]]) -> 'pl.DataFrame':
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
    with CkanCatSession("data.london.gov.uk") as session:
        explorer = CkanCatExplorer(session)
        condensed_results = explorer.package_search_condense_dataframe_packed("police", 'polars')
        print(condensed_results)

        condensed_results = explorer.package_search_condense_dataframe_unpacked("police", 'polars')
        print(condensed_results)
