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
import HerdingCats as hc
from loguru import logger

def main():
    with hc.CatSession(hc.NomisDataCatalogues.ONS_NOMIS) as session:
        explorer = hc.NomisCatExplorer(session)
        loader = hc.NomisLoader()

        # Get all datasets
        datasets = explorer.get_all_datasets()

        # Print dataset IDs
        for dataset in datasets[:5]:  # Show first 5 for brevity
            print(f"Dataset ID: {dataset}")

        # Choose a dataset (e.g., "NM_2_1" - Census 2021 population estimates)
        dataset_id = "NM_2_1"

        # Get codelists for the dataset
        codelists = explorer.get_dataset_codelist(dataset_id)

        # Get metadata for the first codelist
        if codelists:
            codelist_meta = explorer.get_codelist_meta_info(codelists[0])

            # Get codelist values
            geo_types_with_codes = explorer.get_codelist_values(codelist_meta)

            # Print available geography types
            print("\nAvailable geography types:")
            for geo_type in geo_types_with_codes.keys():
                print(f"- {geo_type}")

            # Check if "unitary authority areas" is available
            if "unitary authority areas" in geo_types_with_codes:
                unitary_codes = geo_types_with_codes["unitary authority areas"]

                # Generate download URL for unitary authorities
                download_url = explorer.generate_full_dataset_download_url(
                    dataset_id,
                    geography_codes=unitary_codes[:5]  # First 5 for example
                )

                # Print the download URL
                print(f"\nGenerated download URL: {download_url}")

                # Get available sheet names
                sheets = loader.get_sheet_names(download_url)
                print(f"\nAvailable sheets: {sheets}")

                # Load data from a specific sheet
                if sheets:
                    df = loader.polars_data_loader(
                        download_url,
                        sheet_name=sheets[0],
                        skip_rows=9  # ONS data often has headers
                    )
                    print(f"\nLoaded {len(df)} rows of data")

if __name__ == "__main__":
    main()
```
