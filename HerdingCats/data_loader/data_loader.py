import requests
import pandas as pd
import polars as pl
import duckdb
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
import uuid

from ..errors.cats_errors import OpenDataSoftExplorerError
from io import BytesIO
from typing import Optional, Literal, List, Dict
from loguru import logger
from botocore.exceptions import ClientError


# START TO WRANGLE / ANALYSE
# LOAD DATA RESOURCES INTO STORAGE
class CkanCatResourceLoader:
    """
    Need to do:

        File Formats:
            Excel ✅
            Csv ✅
            Parquet
            JSON
            Geopackage
            Shapefile
            GeoJSON


        Tools and Libs:
            polars ✅
            pandas ✅
            duckdb ✅
            motherduck ✅

            S3 (duckdb)
            S3 (direct) ✅ - as both raw file or parquet
            S3 (DeltaLake)
            S3 (Iceberg)
            Redshift

            Databricks
            Snowflake

            Google Cloud Storage
            Google Big Query
    """

    def __init__(self):
        pass

    # ----------------------------
    # Load data into a variety of formats for aggregation and analysis
    # ----------------------------
    def polars_data_loader(
        self, resource_data: Optional[List]
    ) -> Optional[pl.DataFrame]:
        """
        Isolate a specific resource using the Explorer Class.

        Load a resource into a dataframe for further exploration.

        # Example usage...
        import HerdingCats as hc

        def main():
            with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
                explore = hc.CkanCatExplorer(session)
                all_packages = explore.package_list_dictionary()
                data = all_packages.get("number-bicycle-hires")
                info = explore.package_show_info_json(data)
                resource_list = explore.extract_resource_url(info, "tfl-daily-cycle-hires.xls")
                resource_loader = hc.CkanCatResourceLoader()
                polars_df = resource_loader.polars_data_loader(resource_list)
                print(polars_df)

        if __name__ =="__main__":
            main()

        """
        if resource_data:
            url = resource_data[1]
            response = requests.get(url)
            response.raise_for_status()
            binary_data = BytesIO(response.content)

            file_format = resource_data[0]

            if file_format and (
                file_format.lower() == "spreadsheet" or file_format.lower() == "xlsx"
            ):
                df = pl.read_excel(binary_data)
                return df
            elif file_format and file_format.lower() == "csv":
                df = pl.read_csv(binary_data)
                return df
            else:
                logger.error("Error")
        else:
            logger.error("Error")

    def pandas_data_loader(
        self, resource_data: Optional[List]
    ) -> Optional[pd.DataFrame]:
        """
        Isolate a specific resource using the Explorer Class.

        Load a resource into a dataframe for further exploration.

        # Example usage...
        import HerdingCats as hc

        def main():
            with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
                explore = hc.CkanCatExplorer(session)
                all_packages = explore.package_list_dictionary()
                data = all_packages.get("number-bicycle-hires")
                info = explore.package_show_info_json(data)
                resource_list = explore.extract_resource_url(info, "tfl-daily-cycle-hires.xls")
                resource_loader = hc.CkanCatResourceLoader()
                pandas_df = resource_loader.pandas_data_loader(resource_list)
                print(pandas_df)

        if __name__ =="__main__":
            main()
        """
        if resource_data:
            url = resource_data[1]
            response = requests.get(url)
            response.raise_for_status()
            binary_data = BytesIO(response.content)

            file_format = resource_data[0]

            if file_format and (
                file_format.lower() == "spreadsheet" or file_format.lower() == "xlsx"
            ):
                df = pd.read_excel(binary_data)
                return df
            elif file_format and file_format.lower() == "csv":
                df = pd.read_csv(binary_data)
                return df
            else:
                logger.error("Error")
        else:
            logger.error("Error")

    def duckdb_data_loader(
        self, resource_data: Optional[List], duckdb_name: str, table_name: str
    ):
        """
        Load resource data into a local duckdb database.

        Args:
            - resource_data: List containing file format and URL.
            - token: MotherDuck authentication token.
            - duckdb_name: Name of the DuckDB database.
            - table_name: Name of the table to create in DuckDB.
        """
        # Enforce that resource_data is not None or empty
        if not resource_data or len(resource_data) < 2:
            logger.error("Invalid or insufficient resource data provided")
            return

        # Ensure valid database and table names
        if (
            not isinstance(duckdb_name, str)
            or not duckdb_name.strip()
            or not isinstance(table_name, str)
            or not table_name.strip()
        ):
            logger.error("Database name or table name is invalid")
            return

        url = resource_data[1]
        file_format = resource_data[0].lower()

        try:
            response = requests.get(url)
            response.raise_for_status()
            binary_data = BytesIO(response.content)

            if file_format and (
                file_format.lower() == "spreadsheet" or file_format.lower() == "xlsx"
            ):
                df = pd.read_excel(binary_data)
            elif file_format and file_format.lower() == "csv":
                df = pd.read_csv(binary_data)
            else:
                logger.error(f"Unsupported file format: {file_format}")

            with duckdb.connect(f"{duckdb_name}.duckdb") as conn:
                conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")

            logger.info(f"Data successfully loaded into table '{table_name}'")

        except requests.RequestException as e:
            logger.error(f"Error fetching data from URL: {e}")
        except pd.errors.EmptyDataError:
            logger.error("The file contains no data")
        except duckdb.Error as e:
            logger.error(f"DuckDB error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def motherduck_data_loader(
        self,
        resource_data: Optional[List[str]],
        token: str,
        duckdb_name: str,
        table_name: str,
    ):
        """
        Load resource data into a MotherDuck database.

        The database should already exist in MotherDuck for this to work.

        Args:
            - resource_data: List containing file format and URL.
            - token: MotherDuck authentication token.
            - duckdb_name: Name of the DuckDB database.
            - table_name: Name of the table to create in DuckDB.
        """
        # Enforce that resource_data is not None or empty
        if not resource_data or len(resource_data) < 2:
            logger.error("Invalid or insufficient resource data provided")
            return

        # Enforce that a token is provided
        if len(token) < 10:
            logger.error("Token not long enough")
            return

        # Ensure valid database and table names
        if (
            not isinstance(duckdb_name, str)
            or not duckdb_name.strip()
            or not isinstance(table_name, str)
            or not table_name.strip()
        ):
            logger.error("Database name or table name is invalid")
            return

        # Establish connection to DuckDB using a context manager
        connection_string = f"md:{duckdb_name}?motherduck_token={token}"
        try:
            with duckdb.connect(connection_string) as conn:
                logger.info("MotherDuck Connection Made")

                # Extract file format and URL from resource_data
                file_format = resource_data[0].lower()
                url = resource_data[1]

                # Fetch data from the URL
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    binary_data = BytesIO(response.content)
                except requests.RequestException as e:
                    logger.error(f"Error fetching data from URL: {e}")
                    return

                # Load data into DataFrame based on file format
                try:
                    if file_format in ["spreadsheet", "xlsx"]:
                        df = pd.read_excel(binary_data)
                    elif file_format in ["csv"]:
                        df = pd.read_csv(binary_data)
                    elif file_format in ["json"]:
                        df = pd.read_json(binary_data)
                    else:
                        logger.error(f"Unsupported file format: {file_format}")
                        return
                except pd.errors.EmptyDataError:
                    logger.error("The file contains no data")
                    return
                except ValueError as e:
                    logger.error(f"Error loading data into DataFrame: {e}")
                    return

                # Load DataFrame into DuckDB
                try:
                    conn.execute(
                        f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df"
                    )
                    logger.info(f"Data successfully loaded into table '{table_name}'")
                except duckdb.Error as e:
                    logger.error(f"DuckDB error: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error while executing query: {e}")
        except duckdb.Error as e:
            logger.warning(f"An error occurred while connecting to MotherDuck: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while connecting to MotherDuck: {e}")

    def aws_s3_data_loader(
        self,
        resource_data: Optional[List[str]],
        bucket_name: str,
        custom_name: str,
        mode: Literal["raw", "parquet"],
    ):
        """
        Load resource data into remote S3 storage as current file type or as a parquet file.

        Args:
            - resource_data: List containing file format and URL.
            - bucket_name: S3 bucket
            - mode: Chose whether data is uploaded in current format or as parquet
        """
        # Enforce that resource_data is not None or empty
        if not resource_data or len(resource_data) < 2:
            logger.error("Invalid or insufficient resource data provided")
            return

        # Ensure bucket name is present before processing begins
        if not bucket_name:
            logger.error("No bucket name provided")
            return

        # Create an S3 client
        s3_client = boto3.client("s3")
        logger.success("S3 Client Created")

        # Check if the bucket exists before processing the data
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

        url = resource_data[1]
        file_format = resource_data[0].lower()
        try:
            response = requests.get(url)
            response.raise_for_status()
            binary_data = BytesIO(response.content)

            # Generate a unique filename
            filename = f"{custom_name}-{uuid.uuid4()}.{file_format}"

            if mode == "raw":
                # Upload the file in its original format
                try:
                    s3_client.upload_fileobj(binary_data, bucket_name, filename)
                    logger.success("File uploaded successfully to S3")
                except ClientError as e:
                    logger.error(f"Error uploading file to S3: {e}")
                    return

            elif mode == "parquet":
                # Convert to Parquet and upload
                try:
                    # Read the data based on the file format
                    if file_format and (
                        file_format.lower() == "spreadsheet"
                        or file_format.lower() == "xlsx"
                    ):
                        df = pd.read_excel(binary_data)
                    elif file_format == "csv":
                        df = pd.read_csv(binary_data)
                    elif file_format == "json":
                        df = pd.read_json(binary_data)
                    else:
                        logger.error(
                            f"Unsupported file format for Parquet conversion: {file_format}"
                        )
                        return

                    # Convert to Parquet
                    table = pa.Table.from_pandas(df)
                    parquet_buffer = BytesIO()
                    pq.write_table(table, parquet_buffer)
                    parquet_buffer.seek(0)

                    # Upload the Parquet file
                    parquet_filename = f"{custom_name}-{uuid.uuid4()}.parquet"
                    s3_client.upload_fileobj(
                        parquet_buffer, bucket_name, parquet_filename
                    )
                    logger.success(
                        "File converted to Parquet and uploaded successfully to S3"
                    )
                except Exception as e:
                    logger.error(f"Error converting to Parquet or uploading to S3: {e}")
                    return

            else:
                logger.error(f"Invalid mode specified: {mode}")
                return

        except requests.RequestException as e:
            logger.error(f"Error fetching data from URL: {e}")
            return

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
            self, resource_data: Optional[List[Dict]], format_type: Literal["parquet"], api_key: Optional[str] = None
        ) -> duckdb.DuckDBPyConnection:
        """
        Load data from a resource URL into a DuckDB in-memory DB via pandas.
        Args:
            resource_data: List of dictionaries containing resource information
            format_type: Expected format type (currently only supports 'parquet')
            api_key: Optional API key for authentication with OpenDataSoft
        Returns:
            DuckDB connection with loaded data
        Raises:
            OpenDataSoftExplorerError: If resource data is missing or download fails

        # Example usage:
            import HerdingCats as hc

            def main():
                with hc.CatSession(hc.OpenDataSoftDataCatalogues.ELIA_BELGIAN_ENERGY) as session:
                    explore = hc.OpenDataSoftCatExplorer(session)
                    loader = hc.OpenDataSoftResourceLoader()

                    data = explore.show_dataset_export_options_dict("ods036")
                    duckdb = loader.duckdb_data_loader(data, "parquet")
                    df = duckdb.execute("SELECT * FROM data LIMIT 10").fetchdf()
                    print(df)
        """
        if not resource_data:
            raise OpenDataSoftExplorerError("No resource data provided")

        headers = {'Accept': 'application/parquet'}
        if api_key:
            headers['Authorization'] = f'apikey {api_key}'

        # Create in-memory DuckDB connection
        con = duckdb.connect(':memory:')

        for resource in resource_data:
            if resource.get('format', '').lower() == 'parquet':
                url = resource.get('download_url')
                if not url:
                    continue
                try:
                    # Download parquet file to memory
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    binary_data = BytesIO(response.content)

                    # First read into pandas DataFrame
                    df = pd.read_parquet(binary_data)

                    # Check if DataFrame is empty
                    if df.empty and not api_key:
                        raise OpenDataSoftExplorerError(
                            "Received empty DataFrame. This likely means an API key is required for this dataset. "
                            "Please provide an API key and try again. You can usually do this by creating an account with the datastore you are trying to access"
                        )

                    # Load DataFrame into DuckDB
                    con.execute("CREATE TABLE data AS SELECT * FROM df")
                    return con

                except (requests.RequestException, pd.errors.EmptyDataError, duckdb.Error) as e:
                    raise OpenDataSoftExplorerError("Failed to download or load resource", e)

        raise OpenDataSoftExplorerError("No parquet format resource found")

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
