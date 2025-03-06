import requests
import pandas as pd
import polars as pl
import duckdb
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
import uuid

from ..errors.errors import OpenDataSoftExplorerError, FrenchCatDataLoaderError
from .loader_stores import S3Uploader, DataFrameLoader

from typing import Union, overload, Optional, Literal, List, Dict
from pandas.core.frame import DataFrame as PandasDataFrame
from polars.dataframe.frame import DataFrame as PolarsDataFrame
from botocore.exceptions import ClientError
from functools import wraps
from io import BytesIO
from loguru import logger

#TODO: Start building proper data loader stores for different formats and locations

# START TO WRANGLE / ANALYSE
# LOAD CKAN DATA RESOURCES INTO STORAGE
class CkanCatResourceLoader:
    """A class to load data resources into various formats and storage systems."""

    STORAGE_TYPES = {
        "s3": S3Uploader
    }

    def __init__(self):
        self._validate_dependencies()
        self.df_loader = DataFrameLoader()

    def _validate_dependencies(self):
        """Validate that all required dependencies are available."""
        required_modules = {
            'pandas': pd,
            'polars': pl,
            'duckdb': duckdb,
            'boto3': boto3,
            'pyarrow': pa
        }
        missing = [name for name, module in required_modules.items() if module is None]
        if missing:
            raise ImportError(f"Missing required dependencies: {', '.join(missing)}")

    def _fetch_data(self, url: str) -> BytesIO:
        """Fetch data from URL and return as BytesIO object."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            logger.error(f"Error fetching data from URL: {e}")
            raise

    @DataFrameLoader.validate_ckan_resource
    def polars_data_loader(
        self,
        resource_data: List,
        sheet_name: Optional[str] = None
    ) -> PolarsDataFrame:
        """
        Load a resource into a Polars DataFrame.

        Args:
            resource_data: List of resources or single resource
            sheet_name: Optional sheet name for Excel files
        """
        binary_data = self._fetch_data(resource_data[1])
        return self.df_loader.create_dataframe(
            binary_data,
            resource_data[0].lower(),
            sheet_name=sheet_name,
            loader_type="polars"
        )

    @DataFrameLoader.validate_ckan_resource
    def pandas_data_loader(
        self,
        resource_data: List,
        desired_format: Optional[str] = None,
        sheet_name: Optional[str] = None
        ) -> PandasDataFrame:
        """Load a resource into a Pandas DataFrame."""
        binary_data = self._fetch_data(resource_data[1])
        return self.df_loader.create_dataframe(
            binary_data,
            resource_data[0].lower(),
            sheet_name=sheet_name,
            loader_type="pandas"
        )

    @DataFrameLoader.validate_ckan_resource
    def upload_data(
        self,
        resource_data: List,
        bucket_name: str,
        custom_name: str,
        mode: Literal["raw", "parquet"],
        storage_type: Literal["s3"]
    ) -> str:
        """Upload data using specified uploader"""
        if not all(isinstance(x, str) and x.strip() for x in [bucket_name, custom_name]):
            raise ValueError("Bucket name and custom name must be non-empty strings")

        UploaderClass = self.STORAGE_TYPES[storage_type]
        uploader = UploaderClass()

        file_format = resource_data[0].lower()
        binary_data = self._fetch_data(resource_data[1])

        key = f"{custom_name}-{uuid.uuid4()}"
        return uploader.upload(
            data=binary_data,
            bucket=bucket_name,
            key=key,
            mode=mode,
            file_format=file_format
        )

# START TO WRANGLE / ANALYSE
# LOAD OPEN DATA SOFT DATA RESOURCES INTO STORAGE
class OpenDataSoftResourceLoader:
    """A class to load OpenDataSoft resources into various formats and storage systems."""

    SUPPORTED_FORMATS = {
        "spreadsheet": ["xls", "xlsx"],
        "csv": ["csv"],
        "parquet": ["parquet"],
        "geopackage": ["gpkg", "geopackage"]
    }

    def __init__(self) -> None:
        self._validate_dependencies()
        self.df_loader = DataFrameLoader()

    def _validate_dependencies(self):
        """Validate that all required dependencies are available."""
        required_modules = {
            'pandas': pd,
            'polars': pl,
            'duckdb': duckdb,
            'boto3': boto3,
            'pyarrow': pa
        }
        missing = [name for name, module in required_modules.items() if module is None]
        if missing:
            raise ImportError(f"Missing required dependencies: {', '.join(missing)}")

    def _extract_resource_data(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: str
    ) -> str:
        """Validate resource data and extract download URL."""
        if not resource_data:
            raise OpenDataSoftExplorerError("No resource data provided")

        # Get all supported formats
        all_formats = [fmt for formats in self.SUPPORTED_FORMATS.values() for fmt in formats]

        # If the provided format_type is a category, get its format
        valid_formats = (self.SUPPORTED_FORMATS.get(format_type, [])
                        if format_type in self.SUPPORTED_FORMATS
                        else [format_type])

        # Validate format type
        if format_type not in self.SUPPORTED_FORMATS and format_type not in all_formats:
            raise OpenDataSoftExplorerError(
                f"Unsupported format: {format_type}. "
                f"Supported formats: csv, parquet, xls, xlsx, geopackage"
            )

        # Find matching resource
        url = next(
            (r.get('download_url') for r in resource_data
            if r.get('format', '').lower() in valid_formats),
            None
        )

        # If format provided does not have a url provide the formats that do
        if not url:
            available_formats = [r['format'] for r in resource_data]
            raise OpenDataSoftExplorerError(
                f"No resource found with format: {format_type}. "
                f"Available formats: {', '.join(available_formats)}"
            )

        return url

    def _fetch_data(self, url: str, api_key: Optional[str] = None) -> BytesIO:
        """Fetch data from URL and return as BytesIO object."""
        try:
            # Add API key to URL if provided
            if api_key:
                url = f"{url}?apikey={api_key}"

            response = requests.get(url)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            raise OpenDataSoftExplorerError(f"Failed to download resource: {str(e)}", e)

    def _verify_data(self, df: Union[pd.DataFrame, pl.DataFrame], api_key: Optional[str]) -> None:
        """Verify that the DataFrame is not empty when no API key is provided."""
        is_empty = df.empty if isinstance(df, pd.DataFrame) else df.height == 0
        if is_empty and not api_key:
            raise OpenDataSoftExplorerError(
                "Received empty DataFrame. This likely means an API key is required. "
                "Please provide an API key and try again."
            )

    @DataFrameLoader.validate_opendata_resource
    def polars_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "spreadsheet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> pl.DataFrame:
        """Load data from a resource URL into a Polars DataFrame."""
        url = self._extract_resource_data(resource_data, format_type)
        binary_data = self._fetch_data(url, api_key)
        df = self.df_loader.create_dataframe(
            binary_data,
            format_type,
            "polars",
            sheet_name
        )
        self._verify_data(df, api_key)
        return df
    
    @DataFrameLoader.validate_opendata_resource
    def pandas_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "spreadsheet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> pd.DataFrame:
        """Load data from a resource URL into a Pandas DataFrame."""
        url = self._extract_resource_data(resource_data, format_type)
        binary_data = self._fetch_data(url, api_key)
        df = self.df_loader.create_dataframe(
            binary_data,
            format_type,
            "pandas",
            sheet_name
        )
        self._verify_data(df, api_key)
        return df


# START TO WRANGLE / ANALYSE
# LOAD FRENCH GOUV DATA RESOURCES INTO STORAGE
class FrenchGouvResourceLoader:
    """A class to load French Gouv data resources into various formats and storage systems."""

    SUPPORTED_FORMATS = {
        "xls": ["xls"],
        "xlsx": ["xlsx"],
        "csv": ["csv"],
        "parquet": ["parquet"],
        "geopackage": ["gpkg", "geopackage"]
    }

    def __init__(self) -> None:
        self._validate_dependencies()
        self.df_loader = DataFrameLoader()

    def _validate_dependencies(self):
        """Validate that all required dependencies are available."""
        required_modules = {
            'pandas': pd,
            'polars': pl,
            'duckdb': duckdb,
            'boto3': boto3,
            'pyarrow': pa
        }
        missing = [name for name, module in required_modules.items() if module is None]
        if missing:
            raise ImportError(f"Missing required dependencies: {', '.join(missing)}")

    def _extract_resource_data(
    self,
    resource_data: Optional[List[Dict[str, str]]],
    format_type: str
    ) -> tuple[str, str]:
        """Validate resource data and extract download URL."""
        if not resource_data:
            raise FrenchCatDataLoaderError("No resource data provided")

        # Get all supported formats
        all_formats = [fmt for formats in self.SUPPORTED_FORMATS.values() for fmt in formats]

        # If the provided format_type is a category, get its format
        valid_formats = (self.SUPPORTED_FORMATS.get(format_type, [])
                        if format_type in self.SUPPORTED_FORMATS
                        else [format_type])

        # Validate format type
        if format_type not in self.SUPPORTED_FORMATS and format_type not in all_formats:
            raise FrenchCatDataLoaderError(
                f"Unsupported format: {format_type}. "
                f"Supported formats: csv, parquet, xls, xlsx, geopackage"
            )

        # Find matching resource and its title
        matching_resource = next(
            (r for r in resource_data if r.get('resource_format', '').lower() in valid_formats),
            None
        )

        if not matching_resource:
            available_formats = [r['resource_format'] for r in resource_data]
            raise FrenchCatDataLoaderError(
                f"No resource found with format: {format_type}. "
                f"Available formats: {', '.join(available_formats)}"
            )

        url = matching_resource.get('resource_url')
        title = matching_resource.get('resource_title', 'Unnamed Resource')

        if not url:
            raise FrenchCatDataLoaderError("Resource URL not found in data")

        return url, title

    def _fetch_data(self, url: str, api_key: Optional[str] = None) -> BytesIO:
        """Fetch data from URL and return as BytesIO object."""
        try:
            # Add API key to URL if provided
            if api_key:
                url = f"{url}?apikey={api_key}"

            response = requests.get(url)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            raise OpenDataSoftExplorerError(f"Failed to download resource: {str(e)}", e)

    def _verify_data(self, df: Union[pd.DataFrame, pl.DataFrame], api_key: Optional[str]) -> None:
        """Verify that the DataFrame is not empty when no API key is provided."""
        is_empty = df.empty if isinstance(df, pd.DataFrame) else df.height == 0
        if is_empty and not api_key:
            raise FrenchCatDataLoaderError(
                "Received empty DataFrame. This likely means an API key is required. "
                "Please provide an API key and try again."
            )
  
    @DataFrameLoader.validate_french_gouv_resource
    def polars_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> pl.DataFrame:
        """Load data from a resource URL into a Polars DataFrame."""
        url, title = self._extract_resource_data(resource_data, format_type)
        binary_data = self._fetch_data(url, api_key)
        df = self.df_loader.create_dataframe(
            binary_data,
            format_type,
            "polars",
            sheet_name
        )
        self._verify_data(df, api_key)
        return df

    @DataFrameLoader.validate_french_gouv_resource
    def pandas_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "spreadsheet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> pd.DataFrame:
        """Load data from a resource URL into a Pandas DataFrame.""""""Load data from a resource URL into a Polars DataFrame."""
        url, title = self._extract_resource_data(resource_data, format_type)
        binary_data = self._fetch_data(url, api_key)
        df = self.df_loader.create_dataframe(
            binary_data,
            format_type,
            "pandas",
            sheet_name
        )
        self._verify_data(df, api_key)
        return df

# LOAD ONS NOMIS DATA RESOURCES INTO STORAGE
# TODO: Add support for other formats
class ONSNomisResourceLoader:
    """A class to load ONS Nomis data resources into various formats and storage systems."""

    SUPPORTED_FORMATS = {
        "xlsx": ["xlsx"],
    }

    def __init__(self) -> None:
        self._validate_dependencies()
        self.df_loader = DataFrameLoader()

    def _validate_dependencies(self):
        """Validate that all required dependencies are available."""
        required_modules = {
            'pandas': pd,
            'polars': pl,
            'duckdb': duckdb,
            'boto3': boto3,
            'pyarrow': pa
        }
        missing = [name for name, module in required_modules.items() if module is None]
        if missing:
            raise ImportError(f"Missing required dependencies: {', '.join(missing)}")
        
    def _fetch_data(self, url: str) -> BytesIO:
        """Fetch data from URL and return as BytesIO object."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            logger.error(f"Error fetching data from URL: {e}")
            raise
    
    @DataFrameLoader.validate_ons_nomis_resource
    def polars_data_loader(self, url: str) -> pl.DataFrame:
        """Load data from a resource URL into a Polars DataFrame."""
        binary_data = self._fetch_data(url)
        return self.df_loader.create_dataframe(
            binary_data,
            "xlsx",
            "polars"
        )
    
    @DataFrameLoader.validate_ons_nomis_resource
    def pandas_data_loader(self, url: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """Load data from a resource URL into a Pandas DataFrame."""
        binary_data = self._fetch_data(url)
        return self.df_loader.create_dataframe(
            binary_data,
            "xlsx",
            "pandas",
            sheet_name = sheet_name
        )