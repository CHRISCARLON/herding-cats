---
sidebar_position: 2
---

# Quick Start Guide

Get up and running with HerdingCATs in seconds.

## Basic Usage Pattern

All interactions with HerdingCATs follow this pattern:

1. Create a `CatSession` with your chosen data catalogue.
2. Use an explorer to find and inspect data.
3. Use a loader to retrieve and transform data.

## Example: Exploring Data with CKAN Catalogues

```python
import HerdingCats as hc

def main():

    # Create a session with a predefined catalogue
    with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
    # Create an explorer for the catalogue
    explorer = hc.CkanCatExplorer(session)

    # Check the catalogue health (optional)
    explorer.check_site_health()

    # Search for packages containing "climate"
    results = explorer.package_search_condense("climate", 5)
    print(results)

    # Unpack the results into a DataFrame for easier inspection
    results_df = explorer.package_search_condense_dataframe_unpack("climate", 5)
    print(results_df)

if __name__ == "__main__":
    main()
```

Example output of `results_df`:

```text
resource_name  ...                                     notes_markdown
0        Climate Just-Flood disadvantage_2011_Dec2014  ...  The 'Climate Just' Map Tool shows the geograph...
1   Climate Just-LA_summaries_vulnerability_disadv...  ...  The 'Climate Just' Map Tool shows the geograph...
2                               Climate Just web tool  ...  The 'Climate Just' Map Tool shows the geograph...
3           Climate Just-SSVI_indicators_2011_Dec2014  ...  The 'Climate Just' Map Tool shows the geograph...
4     Climate Just-Flood_hazard_exposure_2011_Dec2014  ...  The 'Climate Just' Map Tool shows the geograph...
```

## Example: Loading CKAN Data into a DataFrame

```python
import HerdingCats as hc

def main():
    # Create a session with a predefined catalogue
    with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
        # Create an explorer for the catalogue
        explorer = hc.CkanCatExplorer(session)

        # Create a data loader
        data_loader = hc.CkanLoader()

        # show the package info
        package = explorer.show_package_info("use-of-force")

        # Extract the resource URLs
        extracted_data = explorer.extract_resource_url(package)

        # Take the 8th resource from the list (as it's usually the most recent data)
        data_to_load = extracted_data[7]

        # Get the sheet names if a check is needed
        sheet_names = data_loader.get_sheet_names(data_to_load)
        print(sheet_names)

        # Load the data into a Polars DataFrame with a specific sheet name
        df = data_loader.polars_data_loader(data_to_load, "UoF")
        print(df.head(10))

if __name__ == "__main__":
    main()
```

Example output:

```text
shape: (10, 275)
┌──────────────┬──────────────┬──────────────┬───────────────────┬───┬──────────┬──────────────────┬──────────────────┬──────────────┐
│ IncidentDate ┆ IncidentTime ┆ Incident     ┆ Incident          ┆ … ┆ Outcome: ┆ Outcome: Other   ┆ Outcome: No      ┆ Refresh Date │
│ ---          ┆ ---          ┆ Location:    ┆ Location: Public  ┆   ┆ Fatality ┆ ---              ┆ Further Action   ┆ ---          │
│ str          ┆ str          ┆ Street/High… ┆ Tran…             ┆   ┆ ---      ┆ str              ┆ ---              ┆ date         │
│              ┆              ┆ ---          ┆ ---               ┆   ┆ str      ┆                  ┆ str              ┆              │
│              ┆              ┆ str          ┆ str               ┆   ┆          ┆                  ┆                  ┆              │
╞══════════════╪══════════════╪══════════════╪═══════════════════╪═══╪══════════╪══════════════════╪══════════════════╪══════════════╡
│ 2024-04-01   ┆ 00:20:00     ┆ Yes          ┆ No                ┆ … ┆ No       ┆ No               ┆ Yes              ┆ 2025-04-11   │
│ 2024-04-01   ┆ 00:25:00     ┆ No           ┆ No                ┆ … ┆ No       ┆ No               ┆ No               ┆ 2025-04-11   │
│ 2024-04-01   ┆ 00:35:00     ┆ Yes          ┆ No                ┆ … ┆ No       ┆ No               ┆ No               ┆ 2025-04-11   │
│ 2024-04-01   ┆ 01:30:00     ┆ No           ┆ No                ┆ … ┆ No       ┆ No               ┆ No               ┆ 2025-04-11   │
│ 2024-04-01   ┆ 00:50:00     ┆ Yes          ┆ No                ┆ … ┆ No       ┆ No               ┆ Yes              ┆ 2025-04-11   │
│ 2024-04-01   ┆ 01:30:00     ┆ Yes          ┆ No                ┆ … ┆ No       ┆ No               ┆ No               ┆ 2025-04-11   │
│ 2024-04-01   ┆ 00:50:00     ┆ Yes          ┆ No                ┆ … ┆ No       ┆ No               ┆ Yes              ┆ 2025-04-11   │
│ 2024-04-01   ┆ 01:15:00     ┆ Yes          ┆ No                ┆ … ┆ No       ┆ No               ┆ No               ┆ 2025-04-11   │
│ 2024-04-01   ┆ 01:10:00     ┆ Yes          ┆ No                ┆ … ┆ No       ┆ No               ┆ No               ┆ 2025-04-11   │
│ 2024-04-01   ┆ 02:00:00     ┆ Yes          ┆ No                ┆ … ┆ No       ┆ No               ┆ No               ┆ 2025-04-11   │
└──────────────┴──────────────┴──────────────┴───────────────────┴───┴──────────┴──────────────────┴──────────────────┴──────────────┘
```

## Example: Loading CKAN Data to Cloud Storage

```python
import HerdingCats as hc

def main():
    # Create a session with a predefined catalogue
    with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
        # Create an explorer for the catalogue
        explorer = hc.CkanCatExplorer(session)

        # Create a data loader
        data_loader = hc.CkanLoader()

        # Check the catalogue health
        package = explorer.show_package_info("use-of-force")

        # Extract the resource URLs
        extracted_data = explorer.extract_resource_url(package)

        # Take the 8th resource from the list
        data_to_load = extracted_data[7]

        # Upload the data to AWS S3
        # This uploads as "raw" data
        # But you can specify upload as "parquet" as well
        data_loader.upload_data(
            data_to_load,
            "your-bucket-name",
            "your-custom-name",
            "raw"
            "s3"
        )

if __name__ == "__main__":
    main()
```

# Example: Loading OpenDataSoft Data into DuckDB

```python
import HerdingCats as hc

def main():

    with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS_DNO) as session:
        explorer = hc.OpenDataSoftCatExplorer(session)
        loader = hc.OpenDataSoftLoader()
        api_key = ""

        # Get dataset export options
        export_options = explorer.show_dataset_export_options("ukpn-flood-warning-areas")
        print(export_options)

        # Use DuckDB for query
        # But get results as pandas DataFrame
        df_pandas = loader.query_to_pandas(
            resource_data=export_options,
            table_name="flood_areas",
            format_type="parquet",
            query="SELECT * FROM flood_areas LIMIT 15",
            api_key=api_key
        )
        print(df_pandas)


if __name__ == "__main__":
    main()
```

## More Detailed Guides

Check out the following sections to learn more:

- [Supported Catalogues](./catalogues) - See all available data sources
- [CKAN Explorer Guide](./explorers/ckan) - Learn about CKAN data exploration
- [OpenDataSoft Explorer Guide](./explorers/opendatasoft) - Learn about OpenDataSoft data exploration
- [French Gouv Explorer Guide](./explorers/frenchgouv) - Learn about French Gouv data exploration
- [ONS Nomis Explorer Guide](./explorers/nomis) - Learn about ONS Nomis data exploration
- [Data Loaders](./loaders) - Learn about all data loading options
