# Herding-CATs

![Herding-CATs-Small](https://github.com/CHRISCARLON/Herding-CATs/assets/138154138/c8fa93e2-ac8b-4718-810d-c92c7254780f)

# Purpose

**The aim of this project is simple, create a basic python library to explore and interact with the UK's open data catalogues**.

## Examples of UK Open Data Catalogues

**CKAN**
| Catalogue Name | Website | Catalogue API Endpoint Definition |
|----------------|---------|-------------------|
| London Datastore | https://data.london.gov.uk | CKAN |
| Subak Data Catalogue | https://data.subak.org | CKAN |

**TBC**
| Catalogue Name | Website | Catalogue API Endpoint Definition |
|----------------|---------|-------------------|
| Bristol Open Data | https://opendata.bristol.gov.uk | TBC |
| Data Mill North | https://datamillnorth.org | TBC |
| Gov Open Data | https://www.data.gov.uk | TBC |

## Basic usage examples:

```python
# Example usage 1: Basic Search
if __name__ == "__main__":
    with CatSession("data.london.gov.uk") as session:
        explore = CatExplorer(session)
        census_package =  explore.package_search_json(search_query="census")
        pprint(census_package)
```

```python
# Example usage 2: List packages and show package info
if __name__ == "__main__":
    with CatSession("data.london.gov.uk") as session:
        explore = CatExplorer(session)
        packlage_list = explore.package_list_json()
        boundary_info = explore.package_show_info_json('2011-boundary-files')
        pprint(show_info)
```

```python
# Example usage 3: Condensed package info view with resource access
if __name__ == "__main__":
    with CatSession("data.london.gov.uk") as session:
        explorer = CatExplorer(session)
        condensed_results = explorer.package_search_condense_dataframe_packed("police", 'polars')
        print(condensed_results)

        condensed_results = explorer.package_search_condense_dataframe_unpacked("police", 'polars')
        print(condensed_results)
```
