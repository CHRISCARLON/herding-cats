# Herding-CATs 🐈‍⬛

Version: 0.1.3

## Purpose

**The aim of this project is simple: create a basic Python library to explore and interact with open data catalogues**.

This will improve and speed up how people:
  - Navigate open data catalogues
  - Find the data they need
  - Get data into a format / location for further analysis

> [!NOTE]
> Herding-CATs is currently under active development. Features may change as the project evolves.
>
> Due to slight variations in how Organisations set up and deploy their opendata catalogues, methods may not work 100% of the time for all catalogues.
>
> We will do our best to ensure that most methods work and a good variety of data catalogues is present.

## To-Do List

### File Formats

| Format     | Status |
|------------|--------|
| Excel       | ✅    |
| Csv        | ✅     |
| Parquet    | 🚧     |
| JSON       | 🚧     |
| Geopackage | 🚧     |
| Shapefile  | 🚧     |
| GeoJSON    | 🚧     |

### Tools and Libraries

#### Implemented
- polars ✅
- pandas ✅
- duckdb ✅
- motherduck ✅

#### Planned
- S3 Integration
  - duckdb
  - direct ✅ - Upload as default file format or as a parquet file
  - DeltaLake
  - Iceberg
- Redshift
- Databricks
- Snowflake
- Google Cloud Platform
  - Google Cloud Storage 🚧
  - Google BigQuery


## Current Default Open Data Catalogues

**Herding-CATs supports the following catalogues by default**

**Default**
| Catalogue Name | Website | Catalogue Endpoint | Comments |
|----------------|---------|-------------------|----------|
| London Datastore | https://data.london.gov.uk | CKAN | Works with all methods |
| Subak Data Catalogue | https://data.subak.org | CKAN | TBC |
| Gov Open Data | https://www.data.gov.uk | CKAN | TBC |
| Humanitarian Data Exchange | https://data.humdata.org | CKAN | Works with most methods |
| Data Mill North | https://datamillnorth.org | CKAN | Seems to have a slightly different implementation - may not work with all methods |
| UK Power Networks | https://ukpowernetworks.opendatasoft.com | Open Datasoft | Works with all methods |
| Infrabel | https://opendata.infrabel.be | Open Datasoft | Works with all methods |
| Paris | https://opendata.paris.fr | Open Datasoft | Works with all methods |
| Toulouse | https://data.toulouse-metropole.fr | Open Datasoft | Works with all methods but Endpoint deviates from standard implementation |

**TBC**
| Catalogue Name | Website | Catalogue API Endpoint Definition |
|----------------|---------|-------------------|
| Bristol Open Data | https://opendata.bristol.gov.uk | TBC |
| Icebreaker One | https://ib1.org | TBC |

## Basic usage examples:

```python
# Example usage 0: List all available data packages in the catalogue
if __name__ == "__main__":
    with CkanCatSession("data.london.gov.uk") as session:
        explore = CkanCatExplorer(session)
        package_list =  explore.package_list()
        pprint(package_list)
```

```python
# Example usage 1: Basic Search: Look for packages with a basic search term
if __name__ == "__main__":
    with CkanCatSession("data.london.gov.uk") as session:
        explore = CkanCatExplorer(session)
        census_package =  explore.package_search_json(search_query="census")
        pprint(census_package)
```

```python
# Example usage 2: List packages and show package info
if __name__ == "__main__":
    with CkanCatSession("data.london.gov.uk") as session:
        explore = ckanCatExplorer(session)
        packlage_list = explore.package_list_json()
        boundary_info = explore.package_show_info_json('2011-boundary-files')
        pprint(show_info)
```

```python
# Example usage 3: Condensed package info view with resource info - either packed or unpacked
if __name__ == "__main__":
    with CatSession("data.london.gov.uk") as session:
        explorer = CatExplorer(session)

        condensed_results = explorer.package_search_condense_dataframe_packed("police", 'polars')
        print(condensed_results)

        condensed_results = explorer.package_search_condense_dataframe_unpacked("police", 'polars')
        print(condensed_results)
```

```python
# Example usage 4: Find the data you want, and then load it into a polars df for further processing
if __name__ == "__main__":
    with CkanCatSession("data.london.gov.uk") as session:
        explore = CkanCatExplorer(session)
        all_packages = explore.package_list_dictionary()
        data = all_packages.get("violence-reduction-unit")
        info = explore.package_show_info_json(data)
        dl_link = explore.extract_resource_url(info, "VRU Q1 2023-24 Dataset")

    analyser = CkanCatAnalyser()
    df = analyser.polars_data_loader(dl_link)
    print(df)
    # Use it like a normal Polars DF from here

# This works for different data catalogues as well
if __name__ == "__main__":
    with CkanCatSession("HUMANITARIAN") as session:
        explore = CkanCatExplorer(session)
        all_packages = explore.package_list_dictionary()
        data = all_packages.get("cameroon-humanitarian-needs")
        info = explore.package_show_info_json(data)
        dl_link = explore.extract_resource_url(info, "cmr_hpc_needs_2024")

    analyser = CkanCatAnalyser()
    df = analyser.polars_data_loader(dl_link)
    print(df)
```

```python
# Example usage 5: Find the data you want, and then load it into a local duckdb for further processing
if __name__ == "__main__":
    with CkanCatSession("humanitarian") as session:
        explore = CkanCatExplorer(session)
        all_packages = explore.package_list_dictionary()
        data = all_packages.get("cameroon-humanitarian-needs")
        info = explore.package_show_info_json(data)
        dl_link = explore.extract_resource_url(info, "cmr_hpc_needs_2024")

    analyser = CkanCatAnalyser()
    df = analyser.duckdb_data_loader_persist(dl_link, "test", "test_table")
    print(df)
```
