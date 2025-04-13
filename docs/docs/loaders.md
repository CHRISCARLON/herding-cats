---
sidebar_position: 5
---

# Data Loaders

HerdingCATs provides specialised loader classes to transform data from various catalogue explorers into usable formats or storage solutions.

Each loader is designed to handle the specific data structure returned by its corresponding explorer class.

## Data Flow Architecture

The loaders follow a consistent pattern:

1. **Data Discovery**: Explorer classes locate and fetch metadata about datasets
2. **Data Structure Extraction**: Explorers provide structured data references to loaders
3. **Data Loading**: Loaders fetch the actual data from source URLs
4. **Data Transformation**: Loaders convert data into desired formats (DataFrame, Parquet, etc.)
5. **Data Storage/Usage**: Data is used for analysis or stored in a persistent location

## From Explorer to Loader

A key feature of the loader system is how data flows from explorer methods through validation decorators to loader methods. Each explorer produces a specific data structure that gets transformed by validation decorators into formats that loaders can efficiently process.

:::info Data Structure Transformation Flow
| Explorer Type | Explorer Method | Original Structure | Validation Decorator | Final Structure for Loader |
| ----------------- | -------------------------------------- | ----------------------------------------------------- | ------------------------------- | -------------------------- |
| CKAN | `extract_resource_url()` | `[name, date, format, url]` | `validate_ckan_resource` | `[format, url]` |
| OpenDataSoft | `show_dataset_export_options()` | `[{"format": "csv", "download_url": "..."}]` | `validate_opendata_resource` | Same structure |
| French Government | `get_dataset_resource_meta()` | `[{"resource_format": "csv", "resource_url": "..."}]` | `validate_french_gouv_resource` | Same structure |
| ONS Nomis | `generate_full_dataset_download_url()` | `"https://example.com/data.xlsx"` | `validate_ons_nomis_resource` | Same structure |
:::

### Explorer Methods

Each explorer type includes specialised methods that create the data structures required by their corresponding loader:

#### CKAN Explorer

```python
# Input: Package information from show_package_info()
# Output: List of resources with [name, date, format, url]
resources = explorer.extract_resource_url(package_info)
```

#### OpenDataSoft Explorer

```python
# Input: Dataset ID
# Output: List of dictionaries with format and download_url
export_options = explorer.show_dataset_export_options("dataset_id")
```

#### French Government Explorer

```python
# Input: Dataset metadata from get_dataset_meta()
# Output: List of dictionaries with resource_format, resource_url, etc.
resources = explorer.get_dataset_resource_meta(metadata)
```

#### ONS Nomis Explorer

```python
# Input: Dataset ID and optional geography codes
# Output: Direct URL string to the Excel file
url = explorer.generate_full_dataset_download_url("NM_2_1")
```

### Validation Decorator Transformations

The validation decorators serve multiple purposes:

1. **Verify** that the input data matches expected patterns
2. **Transform** the data into a standardized format (especially for CKAN resources)
3. **Extract** only the necessary fields for loading operations

For example, the CKAN validator transforms a complex structure into a simple [format, url] list:

```python
@staticmethod
def validate_ckan_resource(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator that transforms CKAN explorer data into loader-compatible format

    Input formats expected:
    - Single list: [name, date, format, url] indexed by ResourceIndex
    - List of lists: [[name, date, format, url], [...], ...]

    Output:
    - Simplified list: [format, url] that's passed to the decorated function
    """
```

These decorators standardize the input data format before processing, making the loader methods more robust and safer to use, while providing a consistent interface for all loaders.

## Type System and DataFrame Loading Traits

HerdingCATs uses the Protocol pattern from Python's typing module to define consistent interfaces for different operations:

### DataFrameLoaderTrait

The `DataFrameLoaderTrait` protocol ensures type-safe handling of both Pandas and Polars DataFrames:

```python
class DataFrameLoaderTrait(Protocol):
    """Protocol defining the interface for DataFrame loaders."""

    @overload
    def create_dataframe(
        self,
        data: BytesIO,
        format_type: str,
        loader_type: Literal["pandas"],
        sheet_name: Optional[str] = None,
        skip_rows: Optional[int] = None,
    ) -> PandasDataFrame: ...

    @overload
    def create_dataframe(
        self,
        data: BytesIO,
        format_type: str,
        loader_type: Literal["polars"],
        sheet_name: Optional[str] = None,
        skip_rows: Optional[int] = None,
    ) -> PolarsDataFrame: ...
```

### StorageTrait

The `StorageTrait` protocol defines a consistent interface for storage operations:

```python
class StorageTrait(Protocol):
    """Protocol defining the interface for remote storage uploaders."""

    def upload(
        self,
        data: BytesIO,
        bucket: str,
        key: str,
        mode: Literal["raw", "parquet"] = "parquet",
        file_format: Optional[str] = None,
    ) -> str: ...
```

These traits allow for consistent usage patterns regardless of the underlying implementation.

## Common Loading Capabilities

All loader classes implement these core functions:

### DataFrame Creation

```python
# Load into Polars DataFrame (faster for large datasets)
df_polars = loader.polars_data_loader(resources)

# Load into Pandas DataFrame (more familiar API)
df_pandas = loader.pandas_data_loader(resources)
```

### Storage Options

```python
# Upload to S3 storage
loader.upload_data(
    resources,
    bucket_name="your-bucket",
    custom_name="dataset-name",
    mode="raw",  # or "parquet" for automatic conversion
    storage_type="s3"
)

# Store locally (where supported)
loader.upload_data(
    resources,
    bucket_name="local-directory",
    custom_name="dataset-name",
    mode="parquet",
    storage_type="local"
)
```

### Excel File Helpers

For spreadsheets, additional options are available:

```python
# Get sheet names from Excel files
sheet_names = loader.get_sheet_names(resources)

# Load specific sheets and skip header rows
df = loader.polars_data_loader(
    resources,
    sheet_name="Sheet1",
    skip_rows=5
)
```

## Detailed Usage Examples

### CKAN Loader Example

```python
import HerdingCats as hc

with hc.CatSession(hc.CkanDataCatalogues.HUMANITARIAN_DATA_STORE) as session:
    explorer = hc.CkanCatExplorer(session)
    loader = hc.CkanLoader()

    # Find data about refugees
    results = explorer.package_search_condense("refugees", num_rows=1)

    if results:
        # Get package information
        package_info = explorer.show_package_info(results[0])

        # Extract resource URLs - transforms into the format loader expects
        resources = explorer.extract_resource_url(package_info)

        print(f"Resource format: {resources[0][0]}")
        print(f"Resource URL: {resources[0][1]}")

        # Load into a Polars DataFrame (fast for large data)
        df = loader.polars_data_loader(resources)

        # Or load a specific format if multiple are available
        csv_df = loader.pandas_data_loader(resources, desired_format="csv")

        # Upload to S3 in raw format (preserves original)
        s3_path = loader.upload_data(
            resources,
            bucket_name="your-bucket",
            custom_name="refugee-data",
            mode="raw",
            storage_type="s3"
        )
```

### OpenDataSoft Loader Example

```python
import HerdingCats as hc

with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
    explorer = hc.OpenDataSoftCatExplorer(session)
    loader = hc.OpenDataSoftLoader()

    # Get export options for a dataset
    data = explorer.show_dataset_export_options("your_dataset_id")

    # The data format will be a list of dicts with format and download_url keys
    for resource in data:
        print(f"Format: {resource['format']}, URL: {resource['download_url']}")

    # Load into a Polars DataFrame (some catalogues require an API key)
    df = loader.polars_data_loader(
        data,
        format_type="csv",  # Specify which format to use
        api_key="your_api_key",  # Some datasets require authentication
        skip_rows=2  # Skip header rows if needed
    )

    # Convert to parquet and upload to S3
    loader.upload_data(
        data,
        bucket_name="your-bucket",
        custom_name="power-networks",
        format_type="csv",  # Specify which format to use as source
        mode="parquet",  # Convert to parquet during upload
        storage_type="s3",
        api_key="your_api_key"
    )
```

### French Government Loader Example

```python
import HerdingCats as hc

with hc.CatSession(hc.FrenchGouvCatalogue.GOUV_FR) as session:
    explorer = hc.FrenchGouvCatExplorer(session)
    loader = hc.FrenchGouvLoader()

    # Get metadata for a dataset
    metadata = explorer.get_dataset_meta("your-dataset-id")

    # Get resource metadata
    resources = explorer.get_dataset_resource_meta(metadata)

    # Resources will be a list of dicts with resource_format and resource_url keys
    if resources:
        print(f"Format: {resources[0]['resource_format']}")
        print(f"URL: {resources[0]['resource_url']}")
        print(f"Title: {resources[0]['resource_title']}")

        # Load CSV resource into DataFrame
        df = loader.polars_data_loader(resources, "csv")

        # For Excel files, you can work with specific sheets
        if resources[0]['resource_format'].lower() in ['xlsx', 'xls']:
            df = loader.pandas_data_loader(
                resources,
                "xlsx",
                sheet_name="Data Sheet",
                skip_rows=3  # Skip header information
            )
```

### ONS Nomis Loader Example

```python
import HerdingCats as hc

with hc.CatSession(hc.NomisDataCatalogues.ONS_NOMIS) as session:
    explorer = hc.NomisCatExplorer(session)
    loader = hc.ONSNomisLoader()  # Note the name is ONSNomisLoader

    # Generate a download URL - this is directly passed to the loader
    download_url = explorer.generate_full_dataset_download_url("NM_2_1")

    print(f"Download URL: {download_url}")

    # The ONS Nomis files are often complex Excel files
    # Check available sheets
    sheets = loader.get_sheet_names(download_url)
    print(f"Available sheets: {sheets}")

    # Load data from a specific sheet, skipping header rows
    # ONS Nomis data often requires skipping metadata rows
    df = loader.polars_data_loader(
        download_url,
        sheet_name=sheets[0] if sheets else None,
        skip_rows=9
    )

    # Save directly to S3
    loader.upload_data(
        download_url,
        bucket_name="your-bucket",
        custom_name="nomis-employment-data",
        mode="parquet",  # Convert to parquet during upload
        storage_type="s3"
    )
```

## Implementation Details

### Storage Mechanisms

Under the hood, loaders use two main storage implementations:

1. `S3Uploader`: For storing data in AWS S3 buckets
2. `LocalUploader`: For storing data in local directories

Both implement the `StorageTrait` protocol, allowing for consistent usage patterns regardless of storage location.

## Future Extensions

Upcoming loader capabilities include:

- **DuckDB Integration**: Direct loading into DuckDB for fast local analytics
- **MotherDuck Cloud Database**: Integration with the cloud version of DuckDB
- **More Format Support**: Adding support for additional data formats like GeoJSON, Shapefile, etc.
- **Incremental Loading**: Support for larger datasets by loading data in chunks
