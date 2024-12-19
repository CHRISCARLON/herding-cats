import requests
import pandas as pd
import polars as pl
import duckdb
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
import uuid

from ..errors.cats_errors import OpenDataSoftExplorerError

from typing import Union, overload, Optional, Literal, List, Dict
from pandas.core.frame import DataFrame as PandasDataFrame
from polars.dataframe.frame import DataFrame as PolarsDataFrame
from botocore.client import BaseClient as Boto3Client
from botocore.exceptions import ClientError
from functools import wraps
from io import BytesIO
from loguru import logger


# START TO WRANGLE / ANALYSE
# LOAD DATA RESOURCES INTO STORAGE
class CkanCatResourceLoader:
    """A class to load data resources into various formats and storage systems."""
    
    SUPPORTED_FORMATS = {
        "spreadsheet": ["xlsx", "xls"],
        "csv": ["csv"],
        "json": ["json"]
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
        """Decorator to validate common input parameters."""
        @wraps(func)
        def wrapper(self, resource_data: Optional[List], *args, **kwargs):
            if not resource_data or len(resource_data) < 2:
                logger.error("Invalid or insufficient resource data provided")
                raise ValueError("Resource data must be a list with at least 2 elements")
            
            url = resource_data[1]
            
            # Validate URL format
            if not url.startswith(('http://', 'https://')):
                raise ValueError("Invalid URL format")
                
            return func(self, resource_data, *args, **kwargs)
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
        Common method to load data into either pandas or polars DataFrame.
        
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
                
                case _:
                    logger.error(f"Unsupported format: {file_format}")
                    raise ValueError(f"Unsupported file format: {file_format}")
                    
        except Exception as e:
            logger.error(f"Failed to load {loader_type} DataFrame: {str(e)}")
            raise


    @validate_inputs
    def polars_data_loader(self, resource_data: List, sheet_name: Optional[str] = None) -> PolarsDataFrame:
        """Load a resource into a Polars DataFrame."""
        binary_data = self._fetch_data(resource_data[1])
        return self._load_dataframe(
            binary_data, 
            resource_data[0].lower(), 
            sheet_name=sheet_name, 
            loader_type="polars"
        )

    @validate_inputs
    def pandas_data_loader(self, resource_data: List, sheet_name: Optional[str] = None) -> PandasDataFrame:
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
    def duckdb_data_loader(self, resource_data: List, sheet_name: str,  table_name: str) -> duckdb.DuckDBPyConnection:
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


class OpenDataSoftResourceLoader:
    def __init__(self) -> None:
        pass

    def polars_data_loader(
            self, resource_data: Optional[List[Dict]], format_type: Literal["parquet"], api_key: Optional[str] = None
        ) -> pl.DataFrame:
            """
            Load data from a resource URL into a Polars DataFrame.
            Args:
                resource_data: List of dictionaries containing resource information
                format_type: Expected format type (currently only supports 'parquet')
                api_key: Optional API key for authentication with OpenDataSoft
            Returns:
                Polars DataFrame
            Raises:
                OpenDataSoftExplorerError: If resource data is missing or download fails

            # Example usage
            import HerdingCats as hc

            def main():
                with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
                    explore = hc.OpenDataSoftCatExplorer(session)
                    data_loader = hc.OpenDataSoftResourceLoader()

                    data = explore.show_dataset_export_options_dict("ukpn-smart-meter-installation-volumes")
                    pl_df = data_loader.polars_data_loader(data, "parquet", "api_key")
                    print(pl_df.head(10))

            if __name__ == "__main__":
                main()

            """
            if not resource_data:
                raise OpenDataSoftExplorerError("No resource data provided")

            headers = {'Accept': 'application/parquet'}
            if api_key:
                headers['Authorization'] = f'apikey {api_key}'

            for resource in resource_data:
                if resource.get('format', '').lower() == 'parquet':
                    url = resource.get('download_url')
                    if not url:
                        continue
                    try:
                        response = requests.get(url, headers=headers)
                        response.raise_for_status()
                        binary_data = BytesIO(response.content)
                        df = pl.read_parquet(binary_data)

                        if df.height == 0 and not api_key:
                            raise OpenDataSoftExplorerError(
                                "Received empty DataFrame. This likely means an API key is required for this dataset. "
                                "Please provide an API key and try again. You can usually do this by creating an account with the datastore you are tyring to access"
                            )
                        return df

                    except (requests.RequestException, Exception) as e:
                        raise OpenDataSoftExplorerError("Failed to download resource", e)

            raise OpenDataSoftExplorerError("No parquet format resource found")

    def pandas_data_loader(
            self, resource_data: Optional[List[Dict]], format_type: Literal["parquet"], api_key: Optional[str] = None
        ) -> pd.DataFrame:
            """
            Load data from a resource URL into a Polars DataFrame.
            Args:
                resource_data: List of dictionaries containing resource information
                format_type: Expected format type (currently only supports 'parquet')
                api_key: Optional API key for authentication with OpenDataSoft
            Returns:
                Polars DataFrame
            Raises:
                OpenDataSoftExplorerError: If resource data is missing or download fails

            # Example usage
            import HerdingCats as hc

            def main():
                with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
                    explore = hc.OpenDataSoftCatExplorer(session)
                    data_loader = hc.OpenDataSoftResourceLoader()

                    data = explore.show_dataset_export_options_dict("ukpn-smart-meter-installation-volumes")
                    pd_df = data_loader.pandas_data_loader(data, "parquet", "api_key")
                    print(pd_df.head(10))

            if __name__ == "__main__":
                main()

            """
            if not resource_data:
                raise OpenDataSoftExplorerError("No resource data provided")

            headers = {'Accept': 'application/parquet'}
            if api_key:
                headers['Authorization'] = f'apikey {api_key}'

            for resource in resource_data:
                if resource.get('format', '').lower() == 'parquet':
                    url = resource.get('download_url')
                    if not url:
                        continue
                    try:
                        response = requests.get(url, headers=headers)
                        response.raise_for_status()
                        binary_data = BytesIO(response.content)
                        df = pd.read_parquet(binary_data)

                        if df.size == 0 and not api_key:
                            raise OpenDataSoftExplorerError(
                                "Received empty DataFrame. This likely means an API key is required for this dataset. "
                                "Please provide an API key and try again. You can usually do this by creating an account with the datastore you are tyring to access"
                            )
                        return df

                    except (requests.RequestException, Exception) as e:
                        raise OpenDataSoftExplorerError("Failed to download resource", e)

            raise OpenDataSoftExplorerError("No parquet format resource found")

    def duckdb_data_loader(
        self, 
        resource_data: Optional[List[Dict]], 
        format_type: Literal["parquet", "xlsx", "csv"],
        api_key: Optional[str] = None
    ) -> duckdb.DuckDBPyConnection:
        """
        Load data from a resource URL directly into DuckDB.
        
        Args:
            resource_data: List of dictionaries containing resource information
            format_type: Expected format type ('parquet', 'xlsx', or 'csv')
            api_key: Optional API key for authentication with OpenDataSoft
            
        Returns:
            DuckDB connection with loaded data
            
        Raises:
            OpenDataSoftExplorerError: If resource data is missing or download fails
        """
        if not resource_data:
            raise OpenDataSoftExplorerError("No resource data provided")

        # Create in-memory DuckDB connection
        con = duckdb.connect(':memory:')
        con.execute("SET force_download=true")
        
        for resource in resource_data:
            match resource.get('format', '').lower():
                case fmt if fmt == format_type:
                    url = resource.get('download_url')
                    if not url:
                        continue
                        
                    try:
                        # Append API key to URL if provided
                        if api_key:
                            url = f"{url}?apikey={api_key}"
                        
                        # Load data based on format type
                        match format_type:
                            case "parquet":
                                con.execute(
                                    "CREATE TABLE data AS SELECT * FROM read_parquet(?)",
                                    [url]
                                )
                            case "xlsx":
                                con.execute(
                                    "CREATE TABLE data AS SELECT * FROM read_xlsx(?)",
                                    [url]
                                )
                            case "csv":
                                con.execute(
                                    "CREATE TABLE data AS SELECT * FROM read_csv_auto(?)",
                                    [url]
                                )
                        
                        # Verify data was loaded
                        sample_data = con.execute("SELECT * FROM data LIMIT 10").fetchall()
                        if not sample_data and not api_key:
                            raise OpenDataSoftExplorerError(
                                "Received empty dataset. This likely means an API key is required. "
                                "Please provide an API key and try again. You can usually do this by "
                                "creating an account with the datastore you are trying to access"
                                )
                        
                        return con
                        
                    except duckdb.Error as e:
                        raise OpenDataSoftExplorerError(f"Failed to load {format_type} resource into DuckDB", e)
                
                case _:
                    continue
        
        raise OpenDataSoftExplorerError(f"No {format_type} format resource found")

    def aws_s3_data_loader(
        self,
        resource_data: Optional[List[Dict]],
        bucket_name: str,
        custom_name: str,
        api_key: Optional[str] = None,
    ) -> None:
        """
        Load resource data into remote S3 storage as a parquet file.

        Args:
            resource_data: List of dictionaries containing resource information
            bucket_name: S3 bucket name
            custom_name: Custom prefix for the filename
            api_key: Optional API key for authentication
        """
        if not resource_data:
            raise OpenDataSoftExplorerError("No resource data provided")

        if not bucket_name:
            raise ValueError("No bucket name provided")

        # Create an S3 client
        s3_client = boto3.client("s3")
        logger.success("S3 Client Created")

        # Check if the bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            logger.success("Bucket Found")
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                logger.error(f"Bucket '{bucket_name}' does not exist.")
            else:
                logger.error(f"Error checking bucket '{bucket_name}': {e}")
            return

        headers = {'Accept': 'application/parquet'}
        if api_key:
            headers['Authorization'] = f'apikey {api_key}'

        for resource in resource_data:
            if resource.get('format', '').lower() == 'parquet':
                url = resource.get('download_url')
                if not url:
                    continue

                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    binary_data = BytesIO(response.content)

                    # Generate a unique filename
                    filename = f"{custom_name}-{uuid.uuid4()}.parquet"

                    # Upload the parquet file directly
                    s3_client.upload_fileobj(binary_data, bucket_name, filename)
                    logger.success("Parquet file uploaded successfully to S3")
                    return

                except requests.RequestException as e:
                    raise OpenDataSoftExplorerError("Failed to download resource", e)
                except ClientError as e:
                    logger.error(f"Error: {e}")
                    return

        raise OpenDataSoftExplorerError("No parquet format resource found")
