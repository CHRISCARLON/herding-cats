---
sidebar_position: 2
---

# OpenDataSoft Explorer

The `OpenDataSoftCatExplorer` class provides methods for exploring OpenDataSoft-based data catalogues.

## Creating an OpenDataSoft Explorer

```python
import HerdingCats as hc

with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
    explorer = hc.OpenDataSoftCatExplorer(session)
```

## Available Methods

### Basic Catalogue Information

```python
# Check the health of the OpenDataSoft site
health = explorer.check_site_health()
```

### Dataset Discovery

```python
# Retrieve all datasets from an OpenDataSoft catalogue
datasets = explorer.fetch_all_datasets()
```

### Dataset Details

```python
# Get detailed metadata about a specific dataset
dataset_info = explorer.show_dataset_info("dataset_id")

# Get available export formats and download URLs
export_options = explorer.show_dataset_export_options("dataset_id")
```

## Example Workflow

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
        explorer = hc.OpenDataSoftCatExplorer(session)

        # Get all datasets
        all_datasets = explorer.fetch_all_datasets()

        # Print dataset names and IDs
        for dataset in all_datasets:
            print(f"Name: {dataset.get('dataset_id', 'N/A')}")

        # Get export options for a specific dataset
        dataset_id = all_datasets[0].get('dataset_id') if all_datasets else None
        if dataset_id:
            export_options = explorer.show_dataset_export_options(dataset_id)

            # Print available export formats
            print("\nAvailable export formats:")
            for format_type, url in export_options.items():
                print(f"- {format_type}")

            # Create a loader and load data
            loader = hc.OpenDataSoftLoader()

            # Choose a format (e.g., "csv")
            chosen_format = "csv"

            # Load data into a Polars DataFrame
            if chosen_format in export_options:
                df = loader.polars_data_loader(export_options, format_type=chosen_format)
                print(f"\nLoaded {len(df)} rows of data")

if __name__ == "__main__":
    main()
```
