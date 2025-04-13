---
sidebar_position: 4
---

# ONS Nomis Explorer

The `NomisCatExplorer` class provides methods for exploring ONS Nomis data.

## Creating a Nomis Explorer

```python
import HerdingCats as hc

with hc.CatSession(hc.NomisDataCatalogues.ONS_NOMIS) as session:
    explorer = hc.NomisCatExplorer(session)
```

## Available Methods

### Dataset Discovery

```python
# Returns a list of all available datasets
datasets = explorer.get_all_datasets()
```

### Dataset Details

```python
# Returns metadata for a specific dataset
dataset_info = explorer.get_dataset_info("dataset_id")

# Returns a list of codelists for a specific dataset
codelists = explorer.get_dataset_codelist("dataset_id")

# Returns metadata for a specific codelist
codelist_info = explorer.get_codelist_meta_info("codelist_id")

# Returns a dictionary of codelist values for a specific codelist
codelist_values = explorer.get_codelist_values(codelist_info)
```

### Download URL Generation

```python
# Generates a full dataset download URL with optional geographic filtering
download_url = explorer.generate_full_dataset_download_url(
    "dataset_id",
    geography_codes=[1234, 5678]
)
```

## Example Workflow

```python
TBC
```
