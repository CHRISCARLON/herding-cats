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

A key feature of the loader system is how data flows from explorer methods through validation decorators to loader methods.

Each explorer produces a specific data structure that gets transformed by validation decorators into formats that loaders can efficiently process.

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

#### Data Structure Transformation Flow

:::info Data Structure Transformation Flow

**CKAN Explorer**

- Explorer Method: `extract_resource_url()`
- Original Structure: `[name, date, format, url]`
- Validation Decorator: `validate_ckan_resource`
- Final Structure for Loader: `[format, url]`

**OpenDataSoft Explorer**

- Explorer Method: `show_dataset_export_options()`
- Original Structure: `[{"format": "csv", "download_url": "..."}]`
- Validation Decorator: `validate_opendata_resource`
- Final Structure for Loader: Same as original

**French Government Explorer**

- Explorer Method: `get_dataset_resource_meta()`
- Original Structure: `[{"resource_format": "csv", "resource_url": "..."}]`
- Validation Decorator: `validate_french_gouv_resource`
- Final Structure for Loader: Same as original

**ONS Nomis Explorer**

- Explorer Method: `generate_full_dataset_download_url()`
- Original Structure: `"https://example.com/data.xlsx"`
- Validation Decorator: `validate_ons_nomis_resource`
- Final Structure for Loader: Same as original
  :::

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

### DuckDB Integration

Most loaders now support direct loading and querying with DuckDB, providing powerful SQL-based analysis capabilities.

The plan is to extend this to all loaders in the future.

:::info Available DuckDB Methods

All loader classes implement these DuckDB-related methods:

- `duckdb_data_loader()`: Load data directly into a DuckDB table
- `execute_query()`: Run a SQL query on loaded data
- `query_to_pandas()`: Load data and return pandas DataFrame from a query
- `query_to_polars()`: Load data and return polars DataFrame from a query
  :::

**Example:**

```python
import HerdingCats as hc

with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS_DNO) as session:
    explorer = hc.OpenDataSoftCatExplorer(session)
    loader = hc.OpenDataSoftLoader()

    # Get dataset export options
    export_options = explorer.show_dataset_export_options("ukpn-flood-warning-areas")
    print(export_options)

    # Get results as pandas DataFrame
    df_pandas = loader.query_to_pandas(
        resource_data=export_options,
        table_name="flood_areas",
        format_type="parquet",
        query="SELECT * FROM flood_warnings LIMIT 15",
        api_key="your_api_key_if_needed"
    )

    print(df_pandas)
```

**Example Output:**

```bash
# Session initialisation
2025-04-13 12:29:49.364 | SUCCESS | Session started successfully with ukpowernetworks.opendatasoft.com

# Available export formats (truncated for readability)
[
  {'format': 'csv', 'download_url': 'https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/ukpn-flood-warning-areas/exports/csv'},
  {'format': 'json', 'download_url': 'https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/ukpn-flood-warning-areas/exports/json'},
  {'format': 'parquet', 'download_url': 'https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/ukpn-flood-warning-areas/exports/parquet'},
  # Additional formats available...
]

# DuckDB initialisation and data loading
2025-04-13 12:29:49.686 | INFO | Connected to DuckDB in-memory database
2025-04-13 12:29:49.742 | INFO | DuckDB extensions loaded: httpfs, spatial
2025-04-13 12:29:49.743 | INFO | Loading parquet data from URL into table 'flood_areas'

# Query results (SELECT * FROM flood_areas LIMIT 15)
| index | river_sea                    |
|-------|------------------------------|
| 0     | River Ray                    |
| 1     | River Thames                 |
| 2     | Cuckmere River, Bull River   |
| 3     | West Brook                   |
| 4     | Sussex River Ouse            |
| 5     | North Stream, South Streams  |
| 6     | River Leam                   |
| 7     | River Darent                 |
| 8     | River Leen                   |
| 9     | Beck                         |
| 10    | River Test                   |
| 11    | River Deben, North Sea       |
| 12    | River Thames                 |
| 13    | River Arun                   |
| 14    | River Sence                  |

Some of the columns have been truncated for readability.

# Session completion
2025-04-13 12:30:53.086 | SUCCESS | Session Closed: https://ukpowernetworks.opendatasoft.com
```

#### Benefits of DuckDB Integration

- **Efficient Memory Usage**: Process large datasets without loading everything into memory
- **SQL Power**: Leverage SQL for filtering, joining, and aggregating data
- **Performance**: DuckDB is optimized for analytical queries on columnar data
- **Seamless Integration**: Results can be easily converted to familiar pandas or polars DataFrames

#### Example: Filtering and Aggregating Large Datasets

When working with large datasets, you can use SQL to filter and aggregate data before loading it into memory:

```python
# Instead of loading entire dataset and filtering in Python:
df = loader.query_to_polars(
    resource_data=export_options,
    table_name="energy_consumption",
    format_type="csv",
    query="""
        SELECT
            region,
            AVG(consumption) as avg_consumption,
            SUM(consumption) as total_consumption,
            COUNT(*) as count
        FROM energy_consumption
        WHERE year >= 2020
        GROUP BY region
        ORDER BY total_consumption DESC
    """
)
```

This approach is particularly useful for OpenDataSoft datasets that can be quite large and may benefit from pre-filtering or aggregation before analysis.

## Detailed Usage Examples

### CKAN Loader Example

```python
import HerdingCats as hc

with hc.CatSession(hc.CkanDataCatalogues.HUMANITARIAN_DATA_STORE) as session:
    explorer = hc.CkanCatExplorer(session)
    loader = hc.CkanLoader()

    # Find data about refugees
    results = explorer.package_search_condense("refugees", num_rows=10)

    if results:
        # Find a specific dataset in the results list
        syria_dataset = next((item for item in results if "syria" in item.get("name", "").lower()), results[0])
        package_info = explorer.show_package_info(syria_dataset["name"])

        # Extract resource URLs - transforms into the format loader expects
        resources = explorer.extract_resource_url(package_info)
        print(resources)

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

### Querying CKAN Datastore with SQL

CKAN supports a "datastore" extension that allows you to run SQL queries directly against tabular resources. The `ckan_sql_to_polars` method is available **only on the CKAN loader** and lets you fetch filtered data as a Polars DataFrame using SQL syntax.

**Parameters:**

- `session`: Your active CatSession object - it automatically uses the base url of the session and the datastore_search_sql endpoint
- `resource_name`: The resource ID or name.
- `filters`: (Optional) A dictionary of column-value pairs to filter the results (translated to a SQL WHERE clause).
- `api_key`: (Optional) If the dataset is private, provide your CKAN API key.

**Returns:**  
A Polars DataFrame containing the query results.

**When to use:**  
Use this method when you want to filter or query large CKAN tabular datasets server-side before loading them into memory, leveraging the power of SQL and the efficiency of Polars.

> **Note:** This method is only available for CKAN loaders and only works with CKAN catalogues that support the "datastore" extension.

**Example:**

```python
import HerdingCats as hc

def main():

    with hc.CatSession(hc.CkanDataCatalogues.NHSBSA_OPEN_DATA) as session:
        loader = hc.CkanLoader()

        df = loader.ckan_sql_to_polars(
            session,
            resource_name="EPD_202001",
            filters={"pco_code": "13T00", "bnf_chemical_substance": "0407010H0"}
        )
        print(df.head(25))


if __name__ == "__main__":
    main()
```

**Output:**

```bash

shape: (25, 26)
┌─────────────────┬────────────────┬──────────┬────────────┬───┬─────────────────┬─────────────────┬────────────────┬────────────────┐
│ BNF_CODE        ┆ TOTAL_QUANTITY ┆ POSTCODE ┆ YEAR_MONTH ┆ … ┆ PCO_NAME        ┆ AREA_TEAM_NAME  ┆ BNF_DESCRIPTIO ┆ ADDRESS_1      │
│ ---             ┆ ---            ┆ ---      ┆ ---        ┆   ┆ ---             ┆ ---             ┆ N              ┆ ---            │
│ str             ┆ f64            ┆ str      ┆ i64        ┆   ┆ str             ┆ str             ┆ ---            ┆ str            │
│                 ┆                ┆          ┆            ┆   ┆                 ┆                 ┆ str            ┆                │
╞═════════════════╪════════════════╪══════════╪════════════╪═══╪═════════════════╪═════════════════╪════════════════╪════════════════╡
│ 0407010H0AAAMAM ┆ 3136.0         ┆ NE8 4QR  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ 108 RAWLING    │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 500mg tablets  ┆ ROAD           │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆                ┆                │
│ 0407010H0AABGBG ┆ 280.0          ┆ NE9 6SX  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ QUEEN          │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 250mg/5ml oral ┆ ELIZABETH      │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆ sus…           ┆ HOSPITAL       │
│ 0407010H0AAAWAW ┆ 400.0          ┆ NE9 6SX  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ EMERGENCY CARE │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 120mg/5ml oral ┆ CENTRE         │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆ sus…           ┆                │
│ 0407010H0AAA7A7 ┆ 100.0          ┆ NE6 1SG  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ MOLINEUX       │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 120mg/5ml oral ┆ WALK-IN CENTRE │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆ sol…           ┆                │
│ 0407010H0AAACAC ┆ 200.0          ┆ NE5 3AE  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ PONTELAND RD   │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 250mg/5ml oral ┆ WIC            │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆ sus…           ┆                │
│ …               ┆ …              ┆ …        ┆ …          ┆ … ┆ …               ┆ …               ┆ …              ┆ …              │
│ 0407010H0AAACAC ┆ 200.0          ┆ NE6 1SG  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ MOLINEUX       │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 250mg/5ml oral ┆ WALK-IN CENTRE │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆ sus…           ┆                │
│ 0407010H0AAAMAM ┆ 56.0           ┆ NE6 1SG  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ MOLINEUX       │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 500mg tablets  ┆ WALK-IN CENTRE │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆                ┆                │
│ 0407010H0AAAQAQ ┆ 100.0          ┆ NE4 6SS  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ MARIE CURIE    │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 500mg soluble  ┆ HOSPICE        │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆ tabl…          ┆                │
│ 0407010H0AAAMAM ┆ 32.0           ┆ NE1 4LP  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ ACCIDENT &     │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 500mg tablets  ┆ EMERGENCY DPT  │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆                ┆                │
│ 0407010H0AAAWAW ┆ 100.0          ┆ NE9 6SX  ┆ 202001     ┆ … ┆ NEWCASTLE       ┆ CUMBRIA,NORTHUM ┆ Paracetamol    ┆ EMERGENCY CARE │
│                 ┆                ┆          ┆            ┆   ┆ GATESHEAD CCG   ┆ B,TYNE & WEAR   ┆ 120mg/5ml oral ┆ CENTRE         │
│                 ┆                ┆          ┆            ┆   ┆                 ┆ A…              ┆ sus…           ┆                │
└─────────────────┴────────────────┴──────────┴────────────┴───┴─────────────────┴─────────────────┴────────────────┴────────────────┘
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
    loader = hc.ONSNomisLoader()

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

- **DuckDB Integration**: Direct loading into DuckDB for fast local analytics for all loader types. Currently only supported for OpenDataSoft.
- **MotherDuck Cloud Database**: Integration with the cloud version of DuckDB. Not yet implemented.
- **More Format Support**: Adding support for additional data formats like GeoJSON, Shapefile, etc. Not yet implemented.
- **Incremental Loading**: Support for larger datasets by loading data in chunks. Not yet implemented.
