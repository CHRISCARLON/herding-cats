---
sidebar_position: 3
---

# French Government Explorer

The `FrenchGouvCatExplorer` class provides methods for exploring the French Government data catalogue.

## Creating a French Government Explorer

```python
import HerdingCats as hc

with hc.CatSession(hc.FrenchGouvCatalogue.GOUV_FR) as session:
    explorer = hc.FrenchGouvCatExplorer(session)
```

## Available Methods

### Basic Catalogue Information

```python
# Check the health of the French Government data portal
health = explorer.check_health_check()

# Get all organizations in the catalogue
orgs = explorer.get_all_orgs()
```

### Dataset Discovery

```python
# Get all datasets
datasets = explorer.get_all_datasets()
```

### Dataset Details

```python
# Get metadata for a specific dataset
metadata = explorer.get_dataset_meta("dataset_id")

# Get metadata as a dataframe
df_meta = explorer.get_dataset_meta_dataframe("dataset_id", df_type="pandas")

# Fetch metadata for multiple datasets
multi_meta = explorer.get_multiple_datasets_meta(["dataset_id1", "dataset_id2"])
```

### Resource Information

```python
# Get metadata for dataset resources
resource_meta = explorer.get_dataset_resource_meta(metadata)

# Get resource metadata as a dataframe
df_resource = explorer.get_dataset_resource_meta_dataframe(metadata, df_type="polars")
```

## Example Workflow

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.FrenchGouvCatalogue.GOUV_FR) as session:
        explorer = hc.FrenchGouvCatExplorer(session)

        # Get all datasets (limit results for example)
        all_datasets = list(explorer.get_all_datasets().items())[:5]

        # Print dataset IDs and titles
        for dataset_id, dataset_info in all_datasets:
            print(f"ID: {dataset_id}, Title: {dataset_info.get('title', 'N/A')}")

        # Choose a dataset ID
        if all_datasets:
            dataset_id = all_datasets[0][0]

            # Get dataset metadata
            metadata = explorer.get_dataset_meta(dataset_id)

            # Get resource metadata
            resource_meta = explorer.get_dataset_resource_meta(metadata)

            # Print available resources
            print("\nAvailable resources:")
            for resource in resource_meta:
                format_type = resource.get('format', 'N/A')
                url = resource.get('url', 'N/A')
                print(f"- Format: {format_type}, URL: {url}")

            # Create a loader and load a resource
            loader = hc.FrenchGouvLoader()

            # Choose a resource (e.g., the first one with a recognized format)
            for resource in resource_meta:
                format_type = resource.get('format', '').lower()
                if format_type in ["csv", "xlsx", "json"]:
                    df = loader.polars_data_loader(resource, format_type)
                    print(f"\nLoaded {len(df)} rows of data in {format_type} format")
                    break

if __name__ == "__main__":
    main()
```
