---
sidebar_position: 1
---

# CKAN Explorer

The `CkanCatExplorer` class provides methods for exploring CKAN-based data catalogues. CKAN (Comprehensive Knowledge Archive Network) is an open-source data management system used by many government and research organisations to publish and share data.

## Creating a CKAN Explorer

```python
import HerdingCats as hc

# Use a predefined catalogue from the library
with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
    explorer = hc.CkanCatExplorer(session)
```

## Available Methods

### Health Check

```python
# Check the health of the CKAN site
explorer.check_site_health()
```

The health check will log success, warning, or error messages depending on the status of the CKAN site.

### Basic Catalogue Information

```python
# Get the total number of packages (datasets)
count = explorer.get_package_count()

# Get a list of all organizations
org_count, orgs = explorer.get_organisation_list()
print(f"Found {org_count} organizations")
```

### Listing Packages

```python
# Get a dictionary of all available packages
packages = explorer.get_package_list()

# Get a dataframe of all available packages
df = explorer.get_package_list_dataframe(df_type="pandas")  # or "polars"
```

### Package Details and Search

```python
# Get detailed information about a specific package
package_info = explorer.show_package_info("package_name")

# Get package information as a dataframe
df_info = explorer.show_package_info_dataframe("package_name", df_type="pandas")

# Search for packages with a keyword (limited to 10 results)
results = explorer.package_search("climate change", num_rows=10)

# Get a condensed view of search results
condensed = explorer.package_search_condense("air quality", num_rows=5)
```

### Working with DataFrames

```python
# Get search results as a dataframe with nested resources
df_search = explorer.package_search_condense_dataframe(
    "population", num_rows=5, df_type="polars"
)

# Get search results as a dataframe with unpacked resources
# This creates a flatter structure with one row per resource
df_search_unpacked = explorer.package_search_condense_dataframe_unpack(
    "transport", num_rows=5, df_type="pandas"
)
```

The unpacked dataframe has the following structure:

- Each dataset resource becomes a separate row
- Column prefixes like `resource_name`, `resource_created`, etc. are added
- This results in a larger dataframe but with easier access to individual resources

### Extracting Resource URLs

```python
# Extract resource URLs from package info for use with loaders
resources = explorer.extract_resource_url(package_info)

# Each resource contains [name, created_date, format, download_url]
for resource in enumerate(resources):
    print(resource)
```

## Complete Example Workflow

```python
TBC
```

## Data Structure Considerations

When working with CKAN data, you'll encounter several important data structures:

1. **Packages** - These are datasets containing one or more resources (data files)
2. **Resources** - The actual data files within packages (CSV, JSON, Excel, etc.)
3. **Organizations** - Groups that publish and maintain datasets

The explorer offers different methods to access these structures in formats that are convenient for further processing, including:

- Raw dictionaries for direct access to all properties
- Condensed views focusing on the most important metadata
- Pandas or Polars dataframes for data analysis workflows
- Nested or flattened (unpacked) resource structures

Choose the appropriate method based on your specific needs and analysis workflow.
