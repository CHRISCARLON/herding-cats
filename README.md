# Herding-CATs 🐈‍⬛

[![codecov](https://codecov.io/gh/CHRISCARLON/Herding-CATs/graph/badge.svg?token=Y9Z0QA39S3)](https://codecov.io/gh/CHRISCARLON/Herding-CATs)

## Purpose

**The aim of this project is simple: create a basic Python library to explore and interact with open data catalogues**.

This will improve and speed up how people:
  - Navigate open data catalogues
  - Find the data that they need
  - Get that data into a format and/or location for further analysis

> [!NOTE]
> Herding-CATs is currently under active development. Features may change as the project evolves.
>
> Due to slight variations in how organisations set up and deploy their opendata catalogues, methods may not work 100% of the time for all catalogues.
>
> We will do our best to ensure that most methods work across all catalogues and that a good variety of data catalogues is present.

## Current Default Open Data Catalogues

Herding-CATs supports the following catalogues by default:

### Default Catalogues

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
| Elia Belgian Energy | https://opendata.elia.be | Open Datasoft |
| EDF Energy | https://opendata.edf.fr | Open Datasoft |

### TBC Catalogues

| Catalogue Name | Website | Catalogue API Endpoint Definition | Comments |
|----------------|---------|-----------------------------------|----------|
| Bristol Open Data | https://opendata.bristol.gov.uk | TBC | Need to figure out how to call the catalogue backend |
| Icebreaker One | https://ib1.org | CKAN | Needs further investigation as authentication with an API key may be required |
| Data Mill North | https://datamillnorth.org | CKAN | Seems to have a slightly different implementation - may not work with all methods |
| Canada Open Data | https://open.canada.ca | CKAN | Needs further investigation due to different implementation |

# Herding-Cats Quick Start!🏃‍♂️‍➡️

## Overview
This Python library provides a way to explore and interact with CKAN and OpenDataSoft data catalogues. It includes four main classes:

1. `CkanCatExplorer`: For exploring CKAN-based data catalogues
2. `OpenDataSoftCatExplorer`: For exploring OpenDataSoft-based data catalogues
3. `CkanCatResourceLoader`: For loading and transforming CKAN catalogue data
4. `OpenDataSoftResourceLoader`: For loading and transforming OpenDataSoft catalogue data

All explorer classes work with a `CatSession` object that handles the connection to the chosen data catalogue.

## Usage

### CKAN Components

#### CkanCatExplorer

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
        explore = hc.CkanCatExplorer(session)

if __name__ == "__main__":
    main()
```

##### Methods
1. `check_site_health()`: Checks the health of the CKAN site
2. `get_package_count()`: Returns the total number of packages in a catalogue
3. `package_list_dictionary()`: Returns a dictionary of all available packages
4. `package_list_dataframe(df_type: Literal["pandas", "polars"])`: Returns a dataframe of all available packages
5. `package_list_dictionary_extra()`: Returns a dictionary with extra package information
6. `catalogue_freshness()`: Provides a view of how many resources have been updated in the last 6 months (London Datastore only)
7. `package_show_info_json(package_name: Union[str, dict, Any])`: Returns package metadata including resource information
8. `package_search_json(search_query: str, num_rows: int)`: Searches for packages and returns results as JSON
9. `package_search_condense_json_unpacked(search_query: str, num_rows: int)`: Returns a condensed view of package information
10. `package_search_condense_dataframe_packed(search_query: str, num_rows: int, df_type: Literal["pandas", "polars"])`: Returns a condensed view with packed resources
11. `package_search_condense_dataframe_unpacked(search_query: str, num_rows: int, df_type: Literal["pandas", "polars"])`: Returns a condensed view with unpacked resources
12. `extract_resource_url(package_info: List[Dict], resource_name: str)`: Extracts the URL and format of a specific resource

#### CkanCatResourceLoader

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
        explore = hc.CkanCatExplorer(session)
        loader = hc.CkanCatResourceLoader()

if __name__ == "__main__":
    main()
```

##### Methods

###### Data Frame Loaders
- `polars_data_loader(resource_data: Optional[List]) -> Optional[pl.DataFrame]`
  - Loads data into a Polars DataFrame
  - Supports Excel (.xlsx) and CSV formats

- `pandas_data_loader(resource_data: Optional[List]) -> Optional[pd.DataFrame]`
  - Loads data into a Pandas DataFrame
  - Supports Excel (.xlsx) and CSV formats

###### Database Loaders
- `duckdb_data_loader(resource_data: Optional[List], duckdb_name: str, table_name: str)`
  - Loads data into a local DuckDB database
  - Supports Excel (.xlsx) and CSV formats

- `motherduck_data_loader(resource_data: Optional[List[str]], token: str, duckdb_name: str, table_name: str)`
  - Loads data into MotherDuck
  - Supports Excel (.xlsx), CSV, and JSON formats

###### Cloud Storage Loaders
- `aws_s3_data_loader(resource_data: Optional[List[str]], bucket_name: str, custom_name: str, mode: Literal["raw", "parquet"])`
  - Loads data into an AWS S3 bucket
  - Supports raw file upload or Parquet conversion
  - Supports Excel (.xlsx), CSV, and JSON formats

### OpenDataSoft Components

#### OpenDataSoftCatExplorer

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
        explore = hc.OpenDataSoftCatExplorer(session)

if __name__ == "__main__":
    main()
```

##### Methods
1. `fetch_all_datasets()`: Retrieves all datasets from an OpenDataSoft catalogue
2. `show_dataset_info_dict(dataset_id)`: Returns detailed metadata about a specific dataset
3. `show_dataset_export_options_dict(dataset_id)`: Returns available export formats and download URLs

#### OpenDataSoftResourceLoader

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
        explore = hc.OpenDataSoftCatExplorer(session)
        loader = hc.OpenDataSoftResourceLoader()

if __name__ == "__main__":
    main()
```

##### Methods

###### Data Frame Loaders
- `polars_data_loader(resource_data: Optional[List[Dict]], format_type: Literal["parquet"], api_key: Optional[str] = None) -> pl.DataFrame`
  - Loads Parquet data into a Polars DataFrame
  - Optional API key for authenticated access

- `pandas_data_loader(resource_data: Optional[List[Dict]], format_type: Literal["parquet"], api_key: Optional[str] = None) -> pd.DataFrame`
  - Loads Parquet data into a Pandas DataFrame
  - Optional API key for authenticated access

###### Database Loaders
- `duckdb_data_loader(resource_data: Optional[List[Dict]], format_type: Literal["parquet"], api_key: Optional[str] = None) -> duckdb.DuckDBPyConnection`
  - Loads Parquet data into an in-memory DuckDB database
  - Optional API key for authenticated access

###### Cloud Storage Loaders
- `aws_s3_data_loader(resource_data: Optional[List[Dict]], bucket_name: str, custom_name: str, api_key: Optional[str] = None)`
  - Loads Parquet data into an AWS S3 bucket
  - Optional API key for authenticated access
  - Requires configured AWS credentials

## Examples

### CKAN Example

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.CkanDataCatalogues.HUMANITARIAN_DATA_STORE) as session:
        explore = hc.CkanCatExplorer(session)
        loader = hc.CkanCatResourceLoader()

        list = explore.package_list_dictionary()

        data = explore.package_show_info_json("burkina-faso-violence-against-civilians-and-vital-civilian-facilities")
        data_prep = explore.extract_resource_url(data, "2020-2024-BFA Aid Worker KIKA Incident Data.xlsx")

        df = loader.polars_data_loader(data_prep)
        df_2 = loader.pandas_data_loader(data_prep)

        print(df.head(15))
        print(df_2.head(15))

if __name__ == "__main__":
    main()

```

### OpenDataSoft Example

For some data catalogues a free api key is required.

Simply sign up to the datastore to generate an api key.

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
        explore = hc.OpenDataSoftCatExplorer(session)
        loader = hc.OpenDataSoftResourceLoader()

        data = explore.show_dataset_export_options_dict("ukpn-smart-meter-installation-volumes")
        pl_df = loader.polars_data_loader(data, "parquet", "your_api_key")
        print(pl_df.head(15))

if __name__ == "__main__":
    main()
```
