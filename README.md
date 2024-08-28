# Herding-CATs

![Herding-CATs-Small](https://github.com/CHRISCARLON/Herding-CATs/assets/138154138/c8fa93e2-ac8b-4718-810d-c92c7254780f)

>[!IMPORTANT]
> THIS IS A WORK IN PROGRESS

# Purpose

**The aim of this project is simple, create a basic python library to explore and interact with the UK's open data catalogues**.

## Examples of UK Open Data Catalogues

1. [Bristol Open Data](https://opendata.bristol.gov.uk)
2. [London Datastore](https://data.london.gov.uk)
3. [Data Mill North](https://datamillnorth.org)
4. [Gov Open Data](https://www.data.gov.uk)

## Basic usage examples:

```python
# Example usage
if __name__ == "__main__":
    with CatSession("data.london.gov.uk") as session:
        explore = CatExplorer(session)
        v =  explore.package_search_json(search_query="census")
        pprint(v)
```
