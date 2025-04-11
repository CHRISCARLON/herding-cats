---
sidebar_position: 5
---

# Data Loaders

HerdingCATs provides various loader classes to retrieve data from catalogues and transform it into useful formats.

## Loader Types

There are different loader classes for each catalogue type:

- `CkanLoader` - For CKAN catalogue data
- `OpenDataSoftLoader` - For OpenDataSoft catalogue data
- `FrenchGouvLoader` - For French Government catalogue data
- `NomisLoader` - For ONS Nomis data

## Common Loading Methods

All loader classes support these standard methods:

### DataFrame Loaders

```python
# Load data into a Polars DataFrame
df_polars = loader.polars_data_loader(resources)

# Load data into a Pandas DataFrame
df_pandas = loader.pandas_data_loader(resources)
```

### Cloud Storage Loaders

```python
# Load data into AWS S3
loader.aws_s3_data_loader(
    resources,
    bucket_name="your-bucket",
    s3_key="path/to/file.parquet",
    save_as_parquet=True
)
```

## CKAN Loader Example

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

        # Extract resource URLs
        resources = explorer.extract_resource_url(package_info)

        # Load into a Polars DataFrame
        df = loader.polars_data_loader(resources)

        # Specify a particular format if the resource has multiple options
        df = loader.pandas_data_loader(resources, desired_format="csv")
```

## OpenDataSoft Loader Example

```python
import HerdingCats as hc

with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
    explorer = hc.OpenDataSoftCatExplorer(session)
    loader = hc.OpenDataSoftLoader()

    # Get export options for a dataset
    data = explorer.show_dataset_export_options("your_dataset_id")

    # Load into a Polars DataFrame (some catalogues require an API key)
    df = loader.polars_data_loader(data, format_type="csv", api_key="your_api_key")
```

## French Government Loader Example

```python
import HerdingCats as hc

with hc.CatSession(hc.FrenchGouvCatalogue.GOUV_FR) as session:
    explorer = hc.FrenchGouvCatExplorer(session)
    loader = hc.FrenchGouvLoader()

    # Get metadata for a dataset
    metadata = explorer.get_dataset_meta("your-dataset-id")

    # Get resource metadata
    resources = explorer.get_dataset_resource_meta(metadata)

    # Load the first resource into a DataFrame
    if resources:
        df = loader.polars_data_loader(resources[0], "csv")
```

## ONS Nomis Loader Example

```python
import HerdingCats as hc

with hc.CatSession(hc.NomisDataCatalogues.ONS_NOMIS) as session:
    explorer = hc.NomisCatExplorer(session)
    loader = hc.NomisLoader()

    # Generate a download URL
    download_url = explorer.generate_full_dataset_download_url("NM_2_1")

    # Check available sheets (for Excel files)
    sheets = loader.get_sheet_names(download_url)

    # Load data from a specific sheet, skipping header rows
    df = loader.polars_data_loader(
        download_url,
        sheet_name=sheets[0] if sheets else None,
        skip_rows=9
    )
```

## Coming Soon

Additional loader functionality:

- DuckDB integration
- MotherDuck cloud database integration
