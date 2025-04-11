---
sidebar_position: 1
---

# CKAN Explorer

The `CkanCatExplorer` class provides methods for exploring CKAN-based data catalogues.

## Creating a CKAN Explorer

```python
import HerdingCats as hc

with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
    explorer = hc.CkanCatExplorer(session)
```

## Available Methods

### Basic Catalogue Information

```python
# Check the health of the CKAN site
health = explorer.check_site_health()

# Get the total number of packages
count = explorer.get_package_count()

# Get a list of all organizations
orgs = explorer.get_organisation_list()
```

### Listing Packages

```python
# Get a dictionary of all available packages
packages = explorer.get_package_list()

# Get a dataframe of all available packages
df = explorer.get_package_list_dataframe(df_type="pandas")  # or "polars"

# Get a list with extra package information
packages_extra = explorer.get_package_list_extra()

# Get a dataframe with extra package information
df_extra = explorer.get_package_list_dataframe_extra(df_type="polars")
```

### Package Details and Search

```python
# Get detailed information about a specific package
package_info = explorer.show_package_info("package_name")

# Get package information as a dataframe
df_info = explorer.show_package_info_dataframe("package_name", df_type="pandas")

# Search for packages
results = explorer.package_search("climate change", num_rows=10)

# Get a condensed view of search results
condensed = explorer.package_search_condense("air quality", num_rows=5)

# Get search results as a dataframe with packed resources
df_search = explorer.package_search_condense_dataframe("population", num_rows=5, df_type="polars")

# Get search results as a dataframe with unpacked resources
df_search_unpacked = explorer.package_search_condense_dataframe_unpack("transport", num_rows=5, df_type="pandas")
```

### Working with Resources

```python
# Extract resource URLs from package info for use with loaders
resources = explorer.extract_resource_url(package_info)
```

## Example Workflow

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.CkanDataCatalogues.UK_GOV_DATA) as session:
        explorer = hc.CkanCatExplorer(session)

        # Search for datasets about "covid"
        results = explorer.package_search_condense("covid", num_rows=5)

        for i, result in enumerate(results):
            print(f"{i+1}. {result.get('title', 'N/A')}")

        # Let user select a dataset
        selection = int(input("Select a dataset (number): ")) - 1
        if 0 <= selection < len(results):
            # Get detailed information
            package_info = explorer.show_package_info(results[selection])

            # Extract resources
            resources = explorer.extract_resource_url(package_info)

            # Print available resources
            for i, resource in enumerate(resources):
                print(f"{i+1}. {resource.get('name', 'N/A')} ({resource.get('format', 'N/A')})")

if __name__ == "__main__":
    main()
```
