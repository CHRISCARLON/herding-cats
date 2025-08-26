---
sidebar_position: 5
---

# ONS Geo Portal Explorer

The ONS Geo Portal Explorer provides access to the Office for National Statistics Open Geography Portal via the DCAT-AP API.

## Overview

The ONS Geo Portal contains geographic datasets from the UK's Office for National Statistics, including boundary files, UPRN directories, and other statistical geography products.

## Basic Usage

```python
import HerdingCats as hc

# Create a session
with hc.CatSession(hc.ONSGeoPortal.ONS_GEO) as session:
    # Create an explorer
    explorer = hc.ONSGeoExplorer(session)

    # Check site health - will return True if healthy
    explorer.check_site_health()
```

## Searching Datasets

### Basic Search

```python
# Search for ONSUD datasets
results = explorer.search_datasets("ONSUD")
print(results)
```

### Search with Sorting

```python
# Search with sorting by date created (descending)
results = explorer.search_datasets(
    q="ONSUD",
    sort="Date Created|created|desc"
)
```

### Get Dataset Summary

The `get_datasets_summary()` method returns a clean list of just IDs, titles, and descriptions:

```python
# Get summary without descriptions (lightweight)
summary = explorer.get_datasets_summary("ONSUD", description=False)

for dataset in summary:
    print(f"ID: {dataset['id']}")
    print(f"Title: {dataset['title']}")
    print("-" * 50)
```

```python
# Get summary with descriptions (default)
summary = explorer.get_datasets_summary("ONSUD")

for dataset in summary:
    print(f"ID: {dataset['id']}")
    print(f"Title: {dataset['title']}")
    print(f"Description: {dataset['description'][:200]}...")
    print("-" * 50)
```

## Getting Download Information

Once you have a dataset ID, you can get detailed resource metadata and download links:

```python
# Get the dataset ID from search results
summary = explorer.get_datasets_summary("ONSUD")
dataset_id = summary[0]['id']  # e.g., "b28cd21f0f274c77a2d556f0ee9ba594"

# Get detailed download information
download_info = explorer.get_download_info(dataset_id)

print(f"Title: {download_info['title']}")
print(f"Size: {download_info['size']} bytes")
print(f"Type: {download_info['type']}")
print(f"Created: {download_info['created']}")
print(f"Modified: {download_info['modified']}")
print(f"Download URL: {download_info['download_url']}")
```

## Complete Example

```python
import HerdingCats as hc

def explore_ons_geo_portal():
    """Example of exploring the ONS Geo Portal."""

    with hc.CatSession(hc.ONSGeoPortal.ONS_GEO) as session:
        explorer = hc.ONSGeoExplorer(session)

        print("Searching for ONSUD datasets...")
        summary = explorer.get_datasets_summary(
            q="ONSUD",
            sort="Date Created|created|desc",
            description=True
        )

        for i, dataset in enumerate(summary, 1):
            print(f"\n{i}. {dataset['title']}")
            print(f"   ID: {dataset['id']}")
            print(f"   Description: {dataset['description'][:150]}...")

        if summary:
            first_id = summary[0]['id']
            print(f"\nGetting download info for: {first_id}")

            download_info = explorer.get_download_info(first_id)
            print(f"\nDownload Details:")
            print(f"  Title: {download_info['title']}")
            print(f"  Size: {download_info['size']:,} bytes")
            print(f"  Download URL: {download_info['download_url']}")

if __name__ == "__main__":
    explore_ons_geo_portal()
```

## Available Methods

- `check_site_health()` - Check if the portal is accessible
- `get_datasets_summary()` - Get clean list of ID, title, description
- `get_download_info()` - Get download URLs and file information

## Common Datasets

Some commonly searched datasets in the ONS Geo Portal:

- **ONSUD** - ONS UPRN Directory
- **Boundaries** - Statistical boundary files
- **Lookups** - Geographic lookups

## Notes

- The ONS Geo Portal uses DCAT-AP 3.0.0 format
- Download URLs point to ArcGIS REST API endpoints
- Some large datasets may require authentication for download
- File sizes can be substantial (100+ MB for some datasets)
