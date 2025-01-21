import requests
import pandas as pd
import polars as pl
import duckdb
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
import uuid

from ..errors.cats_errors import OpenDataSoftExplorerError, FrenchCatDataLoaderError

from typing import Union, overload, Optional, Literal, List, Dict
from pandas.core.frame import DataFrame as PandasDataFrame
from polars.dataframe.frame import DataFrame as PolarsDataFrame
from botocore.client import BaseClient as Boto3Client
from botocore.exceptions import ClientError
from functools import wraps
from io import BytesIO
from loguru import logger


# START TO WRANGLE / ANALYSE
# LOAD CKAN DATA RESOURCES INTO STORAGE
class CkanCatResourceLoader:
    """A class to load data resources into various formats and storage systems."""

    SUPPORTED_FORMATS = {
        "spreadsheet": ["xlsx", "xls"],
        "csv": ["csv"],
        "json": ["json"],
        "parquet": ["parquet"]
    }

    def __init__(self):
        self._validate_dependencies()

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

    @staticmethod
    def validate_inputs(func):
        """
        Decorator to validate common input parameters.
        Handles both single resource lists and lists of resource lists.

        This is because what we input will look like this:

        Format 1: Single List
        ┌─────────── Single Resource List ───────────┐
        │ [0]: "Homicide Accused.csv"                │
        │ [1]: "2024-09-20T13:21:02.610Z"            │
        │ [2]: "csv"         ◄─── Format             │
        │ [3]: "https://..." ◄─── URL                │
        └────────────────────────────────────────────┘

        Format 2: List of Lists
        ┌─────────────────────── Outer List ────────────────────────┐
        │ ┌─────────── Inner List 1 ───────────┐  ┌─── List 2 ───┐  │
        │ │ [0]: "Homicide Accused.csv"        │  │    same      │  │
        │ │ [1]: "2024-09-20T13:21:02.610Z"    │  │    same      │  │
        │ │ [2]: "csv"         ◄─── Format     │  │    same      │  │
        │ │ [3]: "https://..." ◄─── URL        │  │    same      │  │
        │ └────────────────────────────────────┘  └───────────── ┘  │
        └────────────────────────────────────────────────────────── ┘

        But we only want to focus on the first list and only need format and url.
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

    def _fetch_data(self, url: str) -> BytesIO:
        """Fetch data from URL and return as BytesIO object."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            logger.error(f"Error fetching data from URL: {e}")
            raise

    @overload
    def _load_dataframe(
        self,
        binary_data: BytesIO,
        file_format: str,
        *,
        sheet_name: Optional[str] = None,
        loader_type: Literal["pandas"]
    ) -> PandasDataFrame: ...

    @overload
    def _load_dataframe(
        self,
        binary_data: BytesIO,
        file_format: str,
        *,
        sheet_name: Optional[str] = None,
        loader_type: Literal["polars"]
    ) -> PolarsDataFrame: ...

    def _load_dataframe(
        self,
        binary_data: BytesIO,
        file_format: str,
        *,
        sheet_name: Optional[str] = None,
        loader_type: Literal["pandas"] | Literal["polars"]
    ) -> Union[PandasDataFrame, PolarsDataFrame]:
        """
        Common method to load data into either Pandas or Polars DataFrame.

        Args:
            binary_data: BytesIO object containing the file data
            file_format: Format of the file (e.g., 'csv', 'xlsx')
            sheet_name: Name of the sheet for Excel files
            loader_type: Which DataFrame implementation to use ('pandas' or 'polars')

        Returns:
            Either a pandas or polars DataFrame depending on loader_type

        Raises:
            ValueError: If file format is unsupported
            Exception: If loading fails for any other reason
        """
        try:
            match (file_format, loader_type):
                case ("spreadsheet" | "xlsx", "pandas"):
                    return (pd.read_excel(binary_data, sheet_name=sheet_name)
                        if sheet_name else pd.read_excel(binary_data))

                case ("spreadsheet" | "xlsx", "polars"):
                    return (pl.read_excel(binary_data, sheet_name=sheet_name)
                        if sheet_name else pl.read_excel(binary_data))

                case ("csv", "pandas"):
                    return pd.read_csv(binary_data)

                case ("csv", "polars"):
                    return pl.read_csv(binary_data)

                case ("parquet", "pandas"):
                    return pd.read_parquet(binary_data)

                case ("parquet", "polars"):
                    return pl.read_parquet(binary_data)

                case _:
                    logger.error(f"Unsupported format: {file_format}")
                    raise ValueError(f"Unsupported file format: {file_format}")

        except Exception as e:
            logger.error(f"Failed to load {loader_type} DataFrame: {str(e)}")
            raise

    @validate_inputs
    def polars_data_loader(
        self, 
        resource_data: List, 
        desired_format: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> PolarsDataFrame:
        """
        Load a resource into a Polars DataFrame.
        
        Args:
            resource_data: List of resources or single resource
            desired_format: Optional format to load (e.g., 'csv', 'xlsx')
            sheet_name: Optional sheet name for Excel files
        """
        binary_data = self._fetch_data(resource_data[1])
        return self._load_dataframe(
            binary_data,
            resource_data[0].lower(),
            sheet_name=sheet_name,
            loader_type="polars"
        )

    @validate_inputs
    def pandas_data_loader(
        self, 
        resource_data: List, 
        desired_format: Optional[str] = None, 
        sheet_name: Optional[str] = None
        ) -> PandasDataFrame:
        """Load a resource into a Pandas DataFrame."""
        binary_data = self._fetch_data(resource_data[1])
        return self._load_dataframe(
            binary_data,
            resource_data[0].lower(),
            sheet_name=sheet_name,
            loader_type="pandas"
        )

    def _create_duckdb_table(self, conn: duckdb.DuckDBPyConnection, df: pd.DataFrame, table_name: str) -> None:
        """Create a table in DuckDB from a pandas DataFrame."""
        try:
            # Convert pandas DataFrame directly to DuckDB table
            conn.register(f'temp_{table_name}', df)

            # Create permanent table from temporary registration
            sql_command = f"""
                CREATE TABLE {table_name} AS
                SELECT * FROM temp_{table_name}
            """
            conn.execute(sql_command)

            # Verify the table
            result = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetch_df()
            print(result)
            if len(result) == 0:
                raise duckdb.Error("No data was loaded into the table")

            logger.info(f"Successfully created table '{table_name}'")

        except Exception as e:
            logger.error(f"Failed to create DuckDB table: {str(e)}")
            raise

    @validate_inputs
    def duckdb_data_loader(self, resource_data: List, table_name: str, sheet_name: Optional[str] = None) -> duckdb.DuckDBPyConnection:
        """Load resource data into an in-memory DuckDB database via pandas."""
        if not isinstance(table_name, str) or not table_name.strip():
            raise ValueError("Table name must be a non-empty string")

        try:
            # First load data into pandas DataFrame
            df = self.pandas_data_loader(resource_data, sheet_name=sheet_name)

            # Then create DuckDB connection and load the DataFrame
            conn = duckdb.connect(":memory:")
            self._create_duckdb_table(conn, df, table_name)

            logger.info(f"Data successfully loaded into in-memory table '{table_name}'")
            return conn
        except Exception as e:
            logger.error(f"DuckDB error: {e}")
            raise

    @validate_inputs
    def motherduck_data_loader(self, resource_data: List, token: str,
                            duckdb_name: str, table_name: str) -> None:
        """Load resource data into a MotherDuck database via pandas."""
        if not token or len(token) < 10:
            raise ValueError("Token must be at least 10 characters long")
        if not all(isinstance(x, str) and x.strip() for x in [duckdb_name, table_name]):
            raise ValueError("Database and table names must be non-empty strings")

        connection_string = f"md:{duckdb_name}?motherduck_token={token}"

        try:
            # First load data into pandas DataFrame
            df = self.pandas_data_loader(resource_data)

            # Then connect to MotherDuck and load the DataFrame
            with duckdb.connect(connection_string) as conn:
                logger.info("MotherDuck Connection Established")
                self._create_duckdb_table(conn, df, table_name)
                logger.info(f"Data successfully loaded into table '{table_name}'")
        except Exception as e:
            logger.error(f"MotherDuck error: {e}")
            raise

    def _verify_s3_bucket(self, s3_client: Boto3Client, bucket_name: str) -> None:
        """Verify S3 bucket exists."""
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            logger.info("Bucket Found")
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
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
                raise ValueError(f"Unsupported file format for Parquet conversion: {file_format}")

        if df.empty:
            raise ValueError("No data was loaded from the source file")

        table = pa.Table.from_pandas(df)
        parquet_buffer = BytesIO()
        pq.write_table(table, parquet_buffer)
        parquet_buffer.seek(0)
        return parquet_buffer

    @validate_inputs
    def aws_s3_data_loader(self, resource_data: List, bucket_name: str,
                        custom_name: str, mode: Literal["raw", "parquet"]) -> str:
        """Load resource data into remote S3 storage."""
        if not all(isinstance(x, str) and x.strip() for x in [bucket_name, custom_name]):
            raise ValueError("Bucket name and custom name must be non-empty strings")

        file_format = resource_data[0].lower()
        binary_data = self._fetch_data(resource_data[1])
        s3_client = boto3.client("s3")
        self._verify_s3_bucket(s3_client, bucket_name)

        try:
            match mode:
                case "raw":
                    filename = f"{custom_name}-{uuid.uuid4()}.{file_format}"
                    s3_client.upload_fileobj(binary_data, bucket_name, filename)

                case "parquet":
                    parquet_buffer = self._convert_to_parquet(binary_data, file_format)
                    filename = f"{custom_name}-{uuid.uuid4()}.parquet"
                    s3_client.upload_fileobj(parquet_buffer, bucket_name, filename)

            logger.info(f"File uploaded successfully to S3 as {filename}")
            return filename

        except Exception as e:
            logger.error(f"AWS S3 upload error: {e}")
            raise

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

    @staticmethod
    def validate_inputs(func):
        """Decorator to validate resource data containing download URLs and formats."""
        @wraps(func)
        def wrapper(self, resource_data: Optional[List[Dict]], *args, **kwargs):
            # Check if resource data exists and is non-empty
            if not resource_data or not isinstance(resource_data, list):
                logger.error("Resource data must be a list")
                raise ValueError("Resource data must be a list of dictionaries")
            return func(self, resource_data, *args, **kwargs)
        return wrapper

    def _validate_resource_data(
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

    def _load_dataframe(
        self,
        binary_data: BytesIO,
        format_type: str,
        loader_type: Literal["pandas", "polars"],
        sheet_name: Optional[str] = None
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """Load binary data into specified DataFrame type."""
        try:
            match (format_type, loader_type):
                case ("parquet", "pandas"):
                    return pd.read_parquet(binary_data)
                case ("parquet", "polars"):
                    return pl.read_parquet(binary_data)
                case ("csv", "pandas"):
                    return pd.read_csv(binary_data)
                case ("csv", "polars"):
                    return pl.read_csv(binary_data)
                case (("xls" | "xlsx" | "spreadsheet"), "pandas"):
                    return pd.read_excel(binary_data, sheet_name=sheet_name) if sheet_name else pd.read_excel(binary_data)
                case (("xls" | "xlsx" | "spreadsheet"), "polars"):
                    return pl.read_excel(binary_data, sheet_name=sheet_name) if sheet_name else pl.read_excel(binary_data)
                case (("geopackage" | "gpkg"), _):
                    raise ValueError("Geopackage format requires using geopandas or a specialized GIS library")
                case _:
                    raise ValueError(f"Unsupported format {format_type} or loader type {loader_type}")
        except Exception as e:
            raise OpenDataSoftExplorerError(f"Failed to load {loader_type} DataFrame: {str(e)}", e)

    @overload
    def _load_to_frame(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: str,
        loader_type: Literal["pandas"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> PandasDataFrame: ...

    @overload
    def _load_to_frame(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: str,
        loader_type: Literal["polars"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> PolarsDataFrame: ...

    def _load_to_frame(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: str,
        loader_type: Literal["pandas", "polars"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """Common method for loading data into pandas or polars DataFrame."""
        url = self._validate_resource_data(resource_data, format_type)
        binary_data = self._fetch_data(url, api_key)
        df = self._load_dataframe(binary_data, format_type, loader_type, sheet_name)
        self._verify_data(df, api_key)
        return df

    @validate_inputs
    def polars_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "spreadsheet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> pl.DataFrame:
        """Load data from a resource URL into a Polars DataFrame."""
        return self._load_to_frame(resource_data, format_type, "polars", api_key, sheet_name)

    @validate_inputs
    def pandas_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "spreadsheet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> pd.DataFrame:
        """Load data from a resource URL into a Pandas DataFrame."""
        return self._load_to_frame(resource_data, format_type, "pandas", api_key, sheet_name)

    @validate_inputs
    def duckdb_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> duckdb.DuckDBPyConnection:
        """Load data from a resource URL directly into DuckDB."""
        url = self._validate_resource_data(resource_data, format_type)

        if api_key:
            url = f"{url}?apikey={api_key}"

        con = duckdb.connect(':memory:')
        con.execute("SET force_download=true")
        con.execute("INSTALL spatial")
        con.execute("LOAD spatial")

        try:
            match format_type:
                case "parquet":
                    con.execute("CREATE TABLE data AS SELECT * FROM read_parquet(?)", [url])
                case "csv":
                    con.execute("CREATE TABLE data AS SELECT * FROM read_csv(?)", [url])
                case "xls" | "xlsx" | "spreadsheet":
                    if sheet_name:
                        con.execute("CREATE TABLE data AS SELECT * FROM st_read(?, sheet_name=?)", [url, sheet_name])
                    else:
                        con.execute("CREATE TABLE data AS SELECT * FROM st_read(?)", [url])
                case _:
                    raise ValueError(f"Unsupported format type: {format_type}")

            # Verify data was loaded
            sample_data = con.execute("SELECT * FROM data LIMIT 10").fetchall()
            if not sample_data and not api_key:
                raise OpenDataSoftExplorerError(
                    "Received empty dataset. This likely means an API key is required."
                )

            return con

        except duckdb.Error as e:
            raise OpenDataSoftExplorerError(f"Failed to load {format_type} resource into DuckDB", e)


    def _verify_s3_bucket(self, s3_client, bucket_name: str) -> None:
        """Verify S3 bucket exists."""
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            logger.success("Bucket Found")
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                raise ValueError(f"Bucket '{bucket_name}' does not exist")
            raise

    def _convert_to_parquet(self, binary_data: BytesIO, format_type: str) -> BytesIO:
        """Convert input data to parquet format."""
        try:
            match format_type:
                case "csv":
                    df = pd.read_csv(binary_data)
                case "xls" | "xlsx":
                    df = pd.read_excel(binary_data)
                case _:
                    raise ValueError(f"Unsupported format type for Parquet conversion: {format_type}")

            if df.empty:
                raise ValueError("No data was loaded from the source file")

            # Convert to parquet
            parquet_buffer = BytesIO()
            table = pa.Table.from_pandas(df)
            pq.write_table(table, parquet_buffer)
            parquet_buffer.seek(0)
            return parquet_buffer
        except Exception as e:
            raise OpenDataSoftExplorerError(f"Failed to convert to parquet: {str(e)}", e)

    @validate_inputs
    def aws_s3_data_loader(
        self,
        resource_data: List[Dict[str, str]],
        bucket_name: str,
        custom_name: str,
        mode: Literal["raw", "parquet"],
        format_type: Literal["csv", "parquet", "xls", "xlsx"],
        api_key: Optional[str] = None
    ) -> str:
        """
        Load resource data into remote S3 storage.

        Args:
            resource_data: List of dictionaries containing format and download_url
            bucket_name: S3 bucket name
            custom_name: Custom prefix for the filename
            mode: 'raw' to keep original format, 'parquet' to convert to parquet
            format_type: Format to download ('csv', 'parquet', 'xls', 'xlsx')
            api_key: Optional API key for authentication

        Returns:
            str: Name of the uploaded file
        """

        # Validate inputs
        if not all(isinstance(x, str) and x.strip() for x in [bucket_name, custom_name]):
            raise ValueError("Bucket name and custom name must be non-empty strings")

        # Get URL for specified format
        url = self._validate_resource_data(resource_data, format_type)

        # Fetch data
        binary_data = self._fetch_data(url, api_key)

        # Setup S3
        s3_client = boto3.client("s3")
        self._verify_s3_bucket(s3_client, bucket_name)

        try:
            match mode:
                case "raw":
                    filename = f"{custom_name}-{uuid.uuid4()}.{format_type}"
                    s3_client.upload_fileobj(binary_data, bucket_name, filename)
                case "parquet":
                    parquet_buffer = self._convert_to_parquet(binary_data, format_type)
                    filename = f"{custom_name}-{uuid.uuid4()}.parquet"
                    s3_client.upload_fileobj(parquet_buffer, bucket_name, filename)

            logger.success(f"File uploaded successfully to S3 as {filename}")
            return filename
        except Exception as e:
            logger.error(f"AWS S3 upload error: {e}")
            raise

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

    @staticmethod
    def validate_inputs(func):
        """Decorator to validate resource data containing download URLs and formats."""
        @wraps(func)
        def wrapper(self, resource_data: Optional[List[Dict]], *args, **kwargs):
            # Check if resource data exists and is non-empty
            if not resource_data or not isinstance(resource_data, list):
                logger.error("Resource data must be a list")
                raise ValueError("Resource data must be a list of dictionaries")
            return func(self, resource_data, *args, **kwargs)
        return wrapper

    def _validate_resource_data(
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

    @validate_inputs
    def duckdb_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> duckdb.DuckDBPyConnection:
        """Load data from a resource URL directly into DuckDB."""
        url = self._validate_resource_data(resource_data, format_type)

        if api_key:
            url = f"{url}?apikey={api_key}"

        con = duckdb.connect(':memory:')
        con.execute("SET force_download=true")
        con.execute("INSTALL spatial")
        con.execute("LOAD spatial")

        try:
            match format_type:
                case "parquet":
                    con.execute("CREATE TABLE data AS SELECT * FROM read_parquet(?)", [url])
                case "csv":
                    con.execute("CREATE TABLE data AS SELECT * FROM read_csv(?)", [url])
                case "xls" | "xlsx" | "spreadsheet":
                    if sheet_name:
                        con.execute("CREATE TABLE data AS SELECT * FROM st_read(?, sheet_name=?)", [url, sheet_name])
                    else:
                        con.execute("CREATE TABLE data AS SELECT * FROM st_read(?)", [url])
                case _:
                    raise ValueError(f"Unsupported format type: {format_type}")

            # Verify data was loaded
            sample_data = con.execute("SELECT * FROM data LIMIT 10").fetchall()
            if not sample_data and not api_key:
                raise FrenchCatDataLoaderError(
                    "Received empty dataset. This likely means an API key is required."
                )

            return con

        except duckdb.Error as e:
            raise FrenchCatDataLoaderError(f"Failed to load {format_type} resource into DuckDB", e)

    def _fetch_data(self, url: str, api_key: Optional[str] = None) -> BytesIO:
        """Fetch data from URL and return as BytesIO object."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            logger.error(f"Error fetching data from URL: {e}")
            raise

    def _verify_data(self, df: Union[pd.DataFrame, pl.DataFrame], api_key: Optional[str]) -> None:
        """Verify that the DataFrame is not empty when no API key is provided."""
        is_empty = df.empty if isinstance(df, pd.DataFrame) else df.height == 0
        if is_empty and not api_key:
            raise FrenchCatDataLoaderError(
                "Received empty DataFrame. This likely means an API key is required. "
                "Please provide an API key and try again."
            )

    @overload
    def _load_to_frame(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: str,
        loader_type: Literal["pandas"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> PandasDataFrame: ...

    @overload
    def _load_to_frame(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: str,
        loader_type: Literal["polars"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> PolarsDataFrame: ...

    def _load_to_frame(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: str,
        loader_type: Literal["pandas", "polars"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None,
        **csv_options
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """Common method for loading data into pandas or polars DataFrame."""
        url, title = self._validate_resource_data(resource_data, format_type)
        logger.info(f"Loading data from {title} into {loader_type} DataFrame")
        binary_data = self._fetch_data(url, api_key)
        df = self._load_dataframe(binary_data, format_type, loader_type, sheet_name, **csv_options)
        self._verify_data(df, api_key)
        return df

    def _load_dataframe(
        self,
        binary_data: BytesIO,
        format_type: str,
        loader_type: Literal["pandas", "polars"],
        sheet_name: Optional[str] = None,
        **csv_options
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """Load binary data into specified DataFrame type."""
        try:
            match (format_type, loader_type):
                case ("parquet", "pandas"):
                    return pd.read_parquet(binary_data)
                case ("parquet", "polars"):
                    return pl.read_parquet(binary_data)
                case ("csv", "pandas"):
                    # If no separator specified, try to detect it
                    if 'sep' not in csv_options:
                        # Read first chunk of data to detect separator
                        sample = binary_data.read(1024).decode('utf-8')
                        binary_data.seek(0)

                        # Count potential separators
                        separators = {
                            ',': sample.count(','),
                            '\t': sample.count('\t'),
                            ';': sample.count(';'),
                            '|': sample.count('|')
                        }
                        most_common_sep = max(separators.items(), key=lambda x: x[1])[0]
                        csv_options['sep'] = most_common_sep

                    # Set default options if not provided
                    csv_options.setdefault('encoding', 'utf-8')
                    csv_options.setdefault('on_bad_lines', 'warn')

                    return pd.read_csv(binary_data, **csv_options)
                case ("csv", "polars"):
                    # If no separator specified, try to detect it
                    if 'separator' not in csv_options:
                        # Read first chunk of data to detect separator
                        sample = binary_data.read(1024).decode('utf-8')
                        binary_data.seek(0)  #

                        # Count potential separators
                        separators = {
                            ',': sample.count(','),
                            '\t': sample.count('\t'),
                            ';': sample.count(';'),
                            '|': sample.count('|')
                        }
                        most_common_sep = max(separators.items(), key=lambda x: x[1])[0]
                        csv_options['separator'] = most_common_sep

                    # Set default options for polars
                    csv_options.setdefault('encoding', 'utf-8')
                    csv_options.setdefault('truncate_ragged_lines', True)

                    return pl.read_csv(binary_data, infer_schema_length=10000, **csv_options)
                case (("xls" | "xlsx"), "pandas"):
                    return pd.read_excel(binary_data, sheet_name=sheet_name) if sheet_name else pd.read_excel(binary_data)
                case (("xls" | "xlsx"), "polars"):
                    return pl.read_excel(binary_data, sheet_name=sheet_name) if sheet_name else pl.read_excel(binary_data)
                case (("geopackage" | "gpkg"), _):
                    raise ValueError("Geopackage format requires using geopandas or a specialized GIS library")
                case _:
                    raise ValueError(f"Unsupported format {format_type} or loader type {loader_type}")
        except Exception as e:
            raise FrenchCatDataLoaderError(f"Failed to load {loader_type} DataFrame: {str(e)}", e)

    @validate_inputs
    def polars_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> pl.DataFrame:
        """Load data from a resource URL into a Polars DataFrame."""
        return self._load_to_frame(resource_data, format_type, "polars", api_key, sheet_name)

    @validate_inputs
    def pandas_data_loader(
        self,
        resource_data: Optional[List[Dict[str, str]]],
        format_type: Literal["csv", "parquet", "spreadsheet", "xls", "xlsx"],
        api_key: Optional[str] = None,
        sheet_name: Optional[str] = None
    ) -> pd.DataFrame:
        """Load data from a resource URL into a Pandas DataFrame."""
        return self._load_to_frame(resource_data, format_type, "pandas", api_key, sheet_name)
