import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from typing import Protocol, Literal, List, Optional
from io import BytesIO
from botocore.client import BaseClient as Boto3Client
from loguru import logger
from botocore.exceptions import ClientError

class DataUploaderTrait(Protocol):
    def upload(
        self,
        data: BytesIO,
        bucket: str,
        key: str,
        mode: Literal["raw", "parquet"] = "parquet",
        file_format: Optional[str] = None
    ) -> str: ...

class S3Uploader(DataUploaderTrait):
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
