# Herding-CATs

![Herding-CATs-Small](https://github.com/CHRISCARLON/Herding-CATs/assets/138154138/c8fa93e2-ac8b-4718-810d-c92c7254780f)

>[!IMPORTANT]
> THIS IS A WORK IN PROGRESS
>
> Currently using London's Datastore to test functionality

# Purpose

**The aim of this project is simple, create a basic python library to explore and interact with the UK's open data catalogues**.

## Examples of UK Open Data Catalogues

| Catalogue Name | Website | Catalogue API Endpoint |
|----------------|---------|-------------------|
| Bristol Open Data | https://opendata.bristol.gov.uk | TBC |
| London Datastore | https://data.london.gov.uk | CKAN: https://data.london.gov.uk/api/3/ |
| Data Mill North | https://datamillnorth.org | TBC |
| Gov Open Data | https://www.data.gov.uk | TBC |

## Basic usage examples:

```python
# Example usage 1
if __name__ == "__main__":
    with CatSession("data.london.gov.uk") as session:
        explore = CatExplorer(session)
        census_package =  explore.package_search_json(search_query="census")
        pprint(census_package)
```

```python
# Example usage 2
if __name__ == "__main__":
    with CatSession("data.london.gov.uk") as session:
        explore = CatExplorer(session)
        packlage_list = explore.package_list_json()
        boundary_info = explore.package_show_info_json('2011-boundary-files')
        pprint(show_info)
```
