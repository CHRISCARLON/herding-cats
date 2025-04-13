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
TBC
```
