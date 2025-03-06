import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from typing import Protocol, Literal, Optional, overload, Union, Callable, List, Dict, Any, TypeVar
from functools import wraps
from io import BytesIO
from botocore.client import BaseClient as Boto3Client
from loguru import logger
from botocore.exceptions import ClientError

import polars as pl

from typing import Union
from pandas.core.frame import DataFrame as PandasDataFrame
from polars.dataframe.frame import DataFrame as PolarsDataFrame

# We can use protocols to define the methods that implementers must implement
# This is useful for having a more reusable pattern for defining shared behaviours

# This is a protocol for the remote storage uploader trait
class RemoteStorageTrait(Protocol):
    """Protocol defining the interface for remote storage uploaders."""
    def upload(
        self,
        data: BytesIO,
        bucket: str,
        key: str,
        mode: Literal["raw", "parquet"] = "parquet",
        file_format: Optional[str] = None
    ) -> str: ...

class S3Uploader(RemoteStorageTrait):
    """S3 uploader implementation."""
    def __init__(self, client: Optional[Boto3Client] = None):
        self.client = client or boto3.client("s3")

    def _verify_s3_bucket(self, bucket_name: str) -> None:
        """Verify S3 bucket exists."""
        try:
            self.client.head_bucket(Bucket=bucket_name)
            logger.info("Bucket Found")
        except ClientError as error:
            error_code = int(error.response["Error"]["Code"])
            if error_code == 404:
                raise ValueError(f"Bucket '{bucket_name}' does not exist")
            raise

    def _convert_to_parquet(self, binary_data: BytesIO, file_format: str) -> BytesIO:
        """Convert input data to parquet format."""
        match file_format:
            case "spreadsheet" | "xlsx":
                df = pd.read_excel(binary_data)
            case "csv":
                df = pd.read_csv(binary_data)
            case "json":
                df = pd.read_json(binary_data)
            case _:
                raise ValueError(f"Unsupported format for Parquet: {file_format}")

        if df.empty:
            raise ValueError("No data was loaded from the source file")

        table = pa.Table.from_pandas(df)
        parquet_buffer = BytesIO()
        pq.write_table(table, parquet_buffer)
        parquet_buffer.seek(0)
        return parquet_buffer

    def upload(
        self,
        data: BytesIO,
        bucket: str,
        key: str,
        mode: Literal["raw", "parquet"] = "parquet",
        file_format: Optional[str] = None
    ) -> str:
        """Upload data to S3 with support for raw and parquet modes."""
        if not all(isinstance(x, str) and x.strip() for x in [bucket, key]):
            raise ValueError("Bucket and key must be non-empty strings")

        self._verify_s3_bucket(bucket)

        try:
            match mode:
                case "raw":
                    filename = f"{key}.{file_format}" if file_format else key
                    self.client.upload_fileobj(data, bucket, filename)
                case "parquet":
                    if not file_format:
                        raise ValueError("file_format is required for parquet mode")
                    parquet_buffer = self._convert_to_parquet(data, file_format)
                    filename = f"{key}.parquet"
                    self.client.upload_fileobj(parquet_buffer, bucket, filename)

            logger.info(f"File uploaded successfully to S3 as {filename}")
            return filename

        except Exception as e:
            logger.error(f"AWS S3 upload error: {e}")
            raise

# This is a protocol for the DataFrame loader trait
T = TypeVar('T') 

class DataFrameLoaderTrait(Protocol):
    """Protocol defining the interface for DataFrame loaders."""
    @overload
    def create_dataframe(
        self,
        data: BytesIO,
        format_type: str,
        loader_type: Literal["pandas"],
        sheet_name: Optional[str] = None
    ) -> PandasDataFrame: ...
    
    @overload
    def create_dataframe(
        self,
        data: BytesIO,
        format_type: str,
        loader_type: Literal["polars"],
        sheet_name: Optional[str] = None
    ) -> PolarsDataFrame: ...
    
    def create_dataframe(
        self,
        data: BytesIO,
        format_type: str,
        loader_type: Literal["pandas", "polars"],
        sheet_name: Optional[str] = None
    ) -> Union[PandasDataFrame, PolarsDataFrame]: ...

class DataFrameLoader(DataFrameLoaderTrait):
    """DataFrame loading functionality with input validation."""
    
    def get_sheet_names(self, data: bytes) -> list:
        """
        Get all sheet names from an Excel file.
        
        Args:
            data (bytes): Excel file as bytes
            
        Returns:
            list[str]: List of sheet names
            
        Raises:
            ValueError: If the file is not an Excel file
        """
        try:
            with BytesIO(data) as buffer:
                return pd.ExcelFile(buffer).sheet_names
        except Exception as e:
            logger.error(f"Failed to get sheet names: {str(e)}")
            raise ValueError("Could not read sheet names. Is this a valid Excel file?")
    
    @overload
    def create_dataframe(
        self,
        data: BytesIO,
        format_type: str,
        loader_type: Literal["pandas"],
        sheet_name: Optional[str] = None
    ) -> PandasDataFrame: ...
    
    @overload
    def create_dataframe(
        self,
        data: BytesIO,
        format_type: str,
        loader_type: Literal["polars"],
        sheet_name: Optional[str] = None
    ) -> PolarsDataFrame: ...
    
    def create_dataframe(
        self,
        data: BytesIO,
        format_type: str,
        loader_type: Literal["pandas", "polars"],
        sheet_name: Optional[str] = None
    ) -> Union[PandasDataFrame, PolarsDataFrame]:
        """Load data into specified DataFrame type."""
        try:
            match (format_type.lower(), loader_type):
                case ("parquet", "pandas"):
                    return pd.read_parquet(data)
                
                case ("parquet", "polars"):
                    return pl.read_parquet(data)
                                
                case (("xls" | "xlsx" | "spreadsheet"), "pandas"):
                    return (pd.read_excel(data, sheet_name=sheet_name) 
                           if sheet_name else pd.read_excel(data))
                
                case (("xls" | "xlsx" | "spreadsheet"), "polars"):
                    return (pl.read_excel(data, sheet_name=sheet_name) 
                           if sheet_name else pl.read_excel(data))
                
                case ("csv", "pandas"):
                    return pd.read_csv(data)
                
                case ("csv", "polars"):
                    return pl.read_csv(data)
                
                case ("json", "pandas"):
                    return pd.read_json(data)
                
                case ("json", "polars"):
                    return pl.read_json(data)
                
                case (("geopackage" | "gpkg"), _):
                    raise ValueError("Geopackage format requires using geopandas")
                
                case _:
                    raise ValueError(f"Unsupported format {format_type} or loader type {loader_type}")

        except Exception as e:
            logger.error(f"Failed to load {loader_type} DataFrame: {str(e)}")
            raise
    
    # ----- Input Validation Methods -----
    
    @staticmethod
    def validate_ckan_resource(func: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator to validate CKAN resource data.
        Handles both single resource lists and lists of resource lists.
        
        Format expected:
        - Single list: [name, date, format, url]
        - List of lists: [[name, date, format, url], [...], ...]
        """
        @wraps(func)
        def wrapper(self, resource_data: Optional[List], desired_format: Optional[str] = None, *args, **kwargs):
            # First validate we have a list
            if not isinstance(resource_data, list) or not resource_data:
                logger.error("Invalid resource data: must be a non-empty list")
                raise ValueError("Resource data must be a non-empty list")

            # If we have multiple resources (list of lists)
            if isinstance(resource_data[0], list):
                if desired_format:
                    # Find the resource with matching format
                    target_resource = next(
                        (res for res in resource_data if res[2].lower() == desired_format.lower()),
                        None
                    )
                    if not target_resource:
                        available_formats = [res[2] for res in resource_data]
                        logger.error(f"No resource found with format: {desired_format}")
                        raise ValueError(
                            f"No resource with format '{desired_format}' found. "
                            f"Available formats: {', '.join(available_formats)}"
                        )
                else:
                    # If no format specified, use first resource
                    target_resource = resource_data[0]
            else:
                # Single resource case
                target_resource = resource_data

            # Validate the resource has all required elements
            if len(target_resource) < 4:
                logger.error("Invalid resource format: resource must have at least 4 elements")
                raise ValueError("Resource must contain at least 4 elements")

            # Extract format and URL from their positions
            format_type = target_resource[2].lower()
            url = target_resource[3]

            # Validate URL format
            if not url.startswith(('http://', 'https://')):
                logger.error(f"Invalid URL format: {url}")
                raise ValueError("Invalid URL format")

            # Create the modified resource in the expected format
            modified_resource = [format_type, url]
            logger.info(f"You're currently working with this resource {modified_resource}")

            return func(self, modified_resource, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def validate_opendata_resource(func: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator to validate OpenDataSoft resource data.
        
        Expected format:
        - List of dictionaries with 'format' and 'download_url' keys
        """
        @wraps(func)
        def wrapper(self, resource_data: List[Dict[str, Any]], *args, **kwargs):
            # Check if resource data exists and is non-empty
            if not resource_data or not isinstance(resource_data, list):
                logger.error("Resource data must be a list")
                raise ValueError("Resource data must be a list of dictionaries")
                
            # Check if at least one item has the expected format and download_url keys
            has_valid_item = any(
                isinstance(item, dict) and 'format' in item and 'download_url' in item
                for item in resource_data
            )
            
            if not has_valid_item:
                logger.error("Resource data must contain dictionaries with 'format' and 'download_url' keys")
                raise ValueError("Invalid resource data format for OpenDataSoft")
                
            return func(self, resource_data, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def validate_french_gouv_resource(func: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator to validate French Government resource data.
        
        Expected format:
        - List of dictionaries with 'resource_format' and 'resource_url' keys
        """
        @wraps(func)
        def wrapper(self, resource_data: List[Dict[str, Any]], *args, **kwargs):
            # Check if resource data exists and is non-empty
            if not resource_data or not isinstance(resource_data, list):
                logger.error("Resource data must be a list")
                raise ValueError("Resource data must be a list of dictionaries")
                
            # Check if at least one item has the expected resource_format and resource_url keys
            has_valid_item = any(
                isinstance(item, dict) and 'resource_format' in item and 'resource_url' in item
                for item in resource_data
            )
            
            if not has_valid_item:
                logger.error("Resource data must contain dictionaries with 'resource_format' and 'resource_url' keys")
                raise ValueError("Invalid resource data format for French Government data")
                
            return func(self, resource_data, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def validate_ons_nomis_resource(func: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator to validate ONS Nomis resource data.
        
        Expected format: string of the url
        """
        @wraps(func)
        def wrapper(self, resource_data: str, *args, **kwargs):
            if not resource_data or not isinstance(resource_data, str):
                logger.error("Resource data must be a string")
                raise ValueError("Resource data must be a string")
            logger.info("Resource data validated")
            return func(self, resource_data, *args, **kwargs)
        return wrapper  