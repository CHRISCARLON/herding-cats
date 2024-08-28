from pandas.io.clipboards import option_context
import requests
import pandas as pd
import polars as pl

from typing import Any, Dict, Optional, Union, Literal
from loguru import logger
from pprint import pprint
from enum import Enum
from urllib.parse import urlencode

from api_endpoints import CkanApiPaths
from cats_errors import CatExplorerError, CatSessionError

class CatSession:
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


class CatExplorer:
    def __init__(self, cat_session: CatSession):
        self.cat_session = cat_session

    def package_list_json(self, search_query: Optional[str]=None):
        url = self.cat_session.base_url + CkanApiPaths.PACKAGE_LIST
        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data['result']
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
                    import polars as pl
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
        base_url = self.cat_session.base_url + CkanApiPaths.PACKAGE_SEARCH

        params = {}
        if search_query:
            params["q"] = search_query

        url = f"{base_url}?{urlencode(params)}" if params else base_url
        print(url)

        try:
            response = self.cat_session.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data['result']
        except requests.RequestException as e:
            logger.error(f"Failed to search datasets: {e}")
            raise CatExplorerError(f"Failed to search datasets: {str(e)}")

    def get_package_count(self) -> int:
            url = self.cat_session.base_url + CkanApiPaths.PACKAGE_LIST
            try:
                response = self.cat_session.session.get(url)
                response.raise_for_status()
                data = response.json()
                return len(data['result'])
            except requests.RequestException as e:
                logger.error(f"Failed to get package count: {e}")
                raise CatExplorerError(f"Failed to get package count: {str(e)}")

# Example usage
if __name__ == "__main__":
    with CatSession("data.london.gov.uk") as session:
        explore = CatExplorer(session)
        v =  explore.package_search_json(search_query="census")
        pprint(v)
