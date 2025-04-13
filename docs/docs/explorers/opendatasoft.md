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
TBC
```
