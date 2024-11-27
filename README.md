# Herding-CATs 🐈‍⬛

Current Version: 0.1.4

[![codecov](https://codecov.io/gh/CHRISCARLON/Herding-CATs/graph/badge.svg?token=Y9Z0QA39S3)](https://codecov.io/gh/CHRISCARLON/Herding-CATs)

## Purpose

**The aim of this project is simple: create a basic Python library to explore and interact with open data catalogues**.

This will improve and speed up how people:
  - Navigate open data catalogues
  - Find the data they need
  - Get data into a format / location for further analysis

> [!NOTE]
> Herding-CATs is currently under active development. Features may change as the project evolves.
>
> Due to slight variations in how organisations set up and deploy their opendata catalogues, methods may not work 100% of the time for all catalogues.
>
> We will do our best to ensure that most methods work across all catalogues and that a good variety of data catalogues is present.

## Current Default Open Data Catalogues

Herding-CATs supports the following catalogues by default:

### Default

| Catalogue Name | Website | Catalogue Endpoint
|----------------|---------|-------------------|
| London Datastore | https://data.london.gov.uk | CKAN |
| Subak Data Catalogue | https://data.subak.org | CKAN |
| Gov Open Data | https://www.data.gov.uk | CKAN |
| Humanitarian Data Exchange | https://data.humdata.org | CKAN |
| UK Power Networks | https://ukpowernetworks.opendatasoft.com | Open Datasoft |
| Infrabel | https://opendata.infrabel.be | Open Datasoft |
| Paris | https://opendata.paris.fr | Open Datasoft |
| Toulouse | https://data.toulouse-metropole.fr | Open Datasoft |

### TBC

| Catalogue Name | Website | Catalogue API Endpoint Definition | Comments |
|----------------|---------|-----------------------------------|----------|
| Bristol Open Data | https://opendata.bristol.gov.uk | TBC | Need to figure out how to call the catalogue backend |
| Icebreaker One | https://ib1.org | CKAN | Needs further investigation as authentication with an API key may be required |
| Data Mill North | https://datamillnorth.org | CKAN | Seems to have a slightly different implementation - may not work with all methods |
| Canada Open Data | https://open.canada.ca | CKAN | Needs further investigation due to different implementation |

# Herding-Cats Quick Start!🏃‍♂️‍➡️

## Overview
This Python library currently provides a way to explore CKAN and OpenDataSoft data catalogues.

It currently includes three main classes:
1. `CkanCatExplorer`: For exploring CKAN-based data catalogues
2. `OpenDataSoftCatExplorer`: For exploring OpenDataSoft-based data catalogues
3. `CkanCatResourceLoader`: For loading and transforming catalogue data

Both explorer classes are designed to work with a `CatSession` object, which handles the connection to the chosen data catalogue.

## Usage

### CkanCatExplorer

#### Initialisation
```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
        explore = hc.CkanCatExplorer(session)

if __name__ == "__main__":
    main()
```

#### Methods
1. `check_site_health()`: Checks the health of the CKAN site.
2. `get_package_count()`: Returns the total number of packages in a catalogue.
3. `package_list_dictionary()`: Returns a dictionary of all available packages.
4. `package_list_dataframe(df_type: Literal["pandas", "polars"])`: Returns a dataframe of all available packages.
5. `package_list_dictionary_extra()`: Returns a dictionary with extra package information.
6. `catalogue_freshness()`: Provides a view of how many resources have been updated in the last 6 months. THIS ONLY WORKS WITH THE LONDON DATASTORE AND IS CURRENTLY BEING IMPROVED.
7. `package_show_info_json(package_name: Union[str, dict, Any])`: Returns package metadata including resource information.
8. `package_search_json(search_query: str, num_rows: int)`: Searches for packages and returns results as JSON.
9. `package_search_condense_json_unpacked(search_query: str, num_rows: int)`: Returns a condensed view of package information.
10. `package_search_condense_dataframe_packed(search_query: str, num_rows: int, df_type: Literal["pandas", "polars"])`: Returns a condensed view of package information as a dataframe with packed resources.
11. `package_search_condense_dataframe_unpacked(search_query: str, num_rows: int, df_type: Literal["pandas", "polars"])`: Returns a condensed view of package information as a dataframe with unpacked resources.
12. `extract_resource_url(package_info: List[Dict], resource_name: str)`: Extracts the URL and format of a specific resource from a package.

### OpenDataSoftCatExplorer

#### Initialisation
```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
        explore = hc.OpenDataSoftCatExplorer(session)

if __name__ == "__main__":
    main()
```

#### Methods
1. `fetch_all_datasets()`: Retrieves all datasets from an OpenDataSoft catalogue.

### CkanCatResourceLoader

The `CkanCatResourceLoader` class provides functionality to load and transform data from CKAN resources into various formats and storage solutions.

#### Initialisation
```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
        explore = hc.CkanCatExplorer(session)
        loader = hc.CkanCatResourceLoader()

if __name__ == "__main__":
    main()
```

#### Methods

##### Data Frame Loaders

1. `polars_data_loader(resource_data: Optional[List]) -> Optional[pl.DataFrame]`
   - Loads data into a Polars DataFrame
   - Supports Excel (.xlsx) and CSV formats
   - Returns None if loading fails

2. `pandas_data_loader(resource_data: Optional[List]) -> Optional[pd.DataFrame]`
   - Loads data into a Pandas DataFrame
   - Supports Excel (.xlsx) and CSV formats
   - Returns None if loading fails

##### Database Loaders

3. `duckdb_data_loader(resource_data: Optional[List], duckdb_name: str, table_name: str)`
   - Loads data into a local DuckDB database
   - Creates a new table with the specified name
   - Supports Excel (.xlsx) and CSV formats

4. `motherduck_data_loader(resource_data: Optional[List[str]], token: str, duckdb_name: str, table_name: str)`
   - Loads data into a MotherDuck cloud database
   - Requires a valid MotherDuck authentication token
   - Supports Excel (.xlsx), CSV, and JSON formats
   - Creates a new table if it doesn't exist

##### Cloud Storage Loaders

5. `aws_s3_data_loader(resource_data: Optional[List[str]], bucket_name: str, custom_name: str, mode: Literal["raw", "parquet"])`
   - Loads data into an AWS S3 bucket
   - Two modes available:
     - `raw`: Uploads the file in its original format
     - `parquet`: Converts the file to Parquet format before uploading
   - Supports Excel (.xlsx), CSV, and JSON formats
   - Generates unique filenames using UUID
   - Requires appropriate AWS credentials configured

#### Example Usage

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
        # Set up explorer and loader
        explore = hc.CkanCatExplorer(session)
        loader = hc.CkanCatResourceLoader()

        # Get package information
        all_packages = explore.package_list_dictionary()
        cycle_hire_data = all_packages.get("number-bicycle-hires")
        info = explore.package_show_info_json(cycle_hire_data)

        # Extract specific resource
        resource_list = explore.extract_resource_url(info, "tfl-daily-cycle-hires.xls")

        # Load into different formats
        polars_df = loader.polars_data_loader(resource_list)
        pandas_df = loader.pandas_data_loader(resource_list)

        # Load into in-memory DuckDB and specify db name and table name
        loader.duckdb_data_loader(resource_list, "cycle_hire_db", "daily_hires")

        # Load into S3 as Parquet - AWS creds need to be configured with something like AWS vault for this
        loader.aws_s3_data_loader(
            resource_list,
            "my-data-bucket",
            "cycle-hire-data",
            mode="parquet"
        )

if __name__ == "__main__":
    main()
```

## Supported File Types for Resource Loader

The Resource Loader currently supports the following resource file types:
- Excel (.xlsx) ✅
- CSV ✅
- JSON (partial support) ✅
- Parquet (for S3 storage) ✅

Future format support planned for:
- GeoPackage
- Shapefile
- GeoJSON

## Data Formats and Storage Solutions

Current data formats and storage solutions supported:
- Polars DataFrame ✅
- Pandas DataFrame ✅
- DuckDB (local) ✅
- MotherDuck (cloud) ✅
- AWS S3 ✅

Planned future support for:
- S3 (DeltaLake)
- S3 (Iceberg)
- Amazon Redshift
- Databricks
- Snowflake
- Google Cloud Storage
- Google BigQuery
