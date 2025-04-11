---
sidebar_position: 2
---

# Quick Start Guide

Get up and running with HerdingCATs in minutes.

## Basic Usage Pattern

All interactions with HerdingCATs follow this pattern:

1. Create a `CatSession` with your chosen data catalogue
2. Use an explorer to find and inspect data
3. Use a loader to retrieve and transform data

## Example: Finding Data in CKAN

```python
import HerdingCats as hc

# Create a session with a predefined catalogue
with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
    # Create an explorer for the catalogue
    explorer = hc.CkanCatExplorer(session)

    # Check the catalogue health
    health = explorer.check_site_health()
    print(f"Catalogue status: {health}")

    # Search for packages containing "climate"
    results = explorer.package_search_condense("climate", 5)

    # Get more detailed info about the first result
    if results:
        detailed_info = explorer.show_package_info(results[0])
        print(f"Found dataset: {detailed_info.get('title')}")
```

## Example: Loading Data into a DataFrame

```python
import HerdingCats as hc

# Create session and explorer
with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
    explorer = hc.CkanCatExplorer(session)

    # Find a dataset about air quality
    results = explorer.package_search_condense("air quality", 1)

    if results:
        # Get detailed info
        package_info = explorer.show_package_info(results[0])

        # Extract resource URLs
        resources = explorer.extract_resource_url(package_info)

        # Create a loader
        loader = hc.CkanLoader()

        # Load into a Polars DataFrame
        df = loader.polars_data_loader(resources)

        # Or load into a Pandas DataFrame
        # df = loader.pandas_data_loader(resources)

        print(f"Loaded {len(df)} rows of data")
```

## Example: Loading Data to Cloud Storage

```python
import HerdingCats as hc

# Create session, explorer, and find data (as above)
with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
    explorer = hc.OpenDataSoftCatExplorer(session)

    # Get export options for a dataset
    data = explorer.show_dataset_export_options("your_dataset_id")

    # Create loader
    loader = hc.OpenDataSoftLoader()

    # Load directly to S3
    loader.aws_s3_data_loader(
        data,
        bucket_name="your-bucket-name",
        s3_key="data/your-file.parquet",
        format_type="parquet"
    )
```

## Next Steps

Check out the following sections to learn more:

- [Supported Catalogues](./catalogues) - See all available data sources
- [CKAN Explorer Guide](./explorers/ckan) - Learn about CKAN data exploration
- [Data Loaders](./loaders) - Learn about all data loading options
