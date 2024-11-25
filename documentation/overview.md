# HerdingCats Overview

## Overview

This python library provides a way to explore CKAN and OpenDataSoft data catalogues.

It includes two main classes:

1. `CkanCatExplorer`: For exploring CKAN-based data catalogues
2. `OpenDataSoftCatExplorer`: For exploring OpenDataSoft-based data catalogues

Both classes are designed to work with a `CatSession` object, which handles the connection to the data catalogue.

## Usage

### CkanCatExplorer

#### Initialization

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
        explore = hc.CkanCatExplorer(session)

if __name__ =="__main__":
    main()

```

#### Methods

1. `check_site_health()`: Checks the health of the CKAN site.

2. `get_package_count()`: Returns the total number of packages in a catalogue.

3. `package_list_dictionary()`: Returns a dictionary of all available packages.

4. `package_list_dataframe(df_type: Literal["pandas", "polars"])`: Returns a dataframe of all available packages.

5. `package_list_dictionary_extra()`: Returns a dictionary with extra package information.

6. `catalogue_freshness()`: Provides a view of how many resources have been updated in the last 6 months.

7. `package_show_info_json(package_name: Union[str, dict, Any])`: Returns package metadata including resource information.

8. `package_search_json(search_query: str, num_rows: int)`: Searches for packages and returns results as JSON.

9. `package_search_condense_json_unpacked(search_query: str, num_rows: int)`: Returns a condensed view of package information.

10. `package_search_condense_dataframe_packed(search_query: str, num_rows: int, df_type: Literal["pandas", "polars"])`: Returns a condensed view of package information as a dataframe with packed resources.

11. `package_search_condense_dataframe_unpacked(search_query: str, num_rows: int, df_type: Literal["pandas", "polars"])`: Returns a condensed view of package information as a dataframe with unpacked resources.

12. `extract_resource_url(package_info: List[Dict], resource_name: str)`: Extracts the URL and format of a specific resource from a package.

### OpenDataSoftCatExplorer

#### Initialization

```python
from cat_session import CatSession
from cat_explorer import OpenDataSoftCatExplorer

with CatSession("ukpowernetworks.opendatasoft.com") as session:
    explorer = OpenDataSoftCatExplorer(session)
```

#### Methods

1. `fetch_all_datasets()`: Retrieves all datasets from the OpenDataSoft catalogue.
