# HerdingCATs 🐈‍⬛

> [!NOTE]  
> Version 0.1.0 PyPi coming soon.

[![codecov](https://codecov.io/gh/CHRISCARLON/Herding-CATs/graph/badge.svg?token=Y9Z0QA39S3)](https://codecov.io/gh/CHRISCARLON/Herding-CATs)

## Purpose

**The aim of this project is simple: create a basic Python library to explore and interact with open data sources**.

This will improve and speed up how users:

- Navigate open data catalogues
- Find the data that they need
- Get that data into a format and/or location for further analysis

**PyPi package coming soon.**

```bash
pip install HerdingCats
```

or

```bash
poetry add HerdingCats
```

---

> [!NOTE]
> Herding-CATs is currently under active development. Features may change as the project evolves.
>
> Due to slight variations in how organisations set up and deploy their opendata catalogues, methods may not work 100% of the time for all catalogues.
>
> We will do our best to ensure that most methods work across all catalogues and that a good variety of data catalogues is present.

---

> [!NOTE]
> If the data seems worth it we will maintain methods for bespoke implementations that go beyond typical data catlogue implementations such as CKAN and OpenDataSoft.

---

## Current Default Open Data Catalogues

Herding-CATs supports the following data sources by default:

### Supported Catalogues

| Catalogue Name                          | Website                          | Catalogue Backend |
| --------------------------------------- | -------------------------------- | ----------------- |
| London Datastore                        | data.london.gov.uk               | CKAN              |
| Subak Data Catalogue                    | data.subak.org                   | CKAN              |
| UK Gov Open Data                        | data.gov.uk                      | CKAN              |
| Humanitarian Data Exchange              | data.humdata.org                 | CKAN              |
| UK Power Networks                       | ukpowernetworks.opendatasoft.com | Open Datasoft     |
| Infrabel                                | opendata.infrabel.be             | Open Datasoft     |
| Paris                                   | opendata.paris.fr                | Open Datasoft     |
| Toulouse                                | data.toulouse-metropole.fr       | Open Datasoft     |
| Elia Belgian Energy                     | opendata.elia.be                 | Open Datasoft     |
| EDF Energy                              | opendata.edf.fr                  | Open Datasoft     |
| Cadent Gas                              | cadentgas.opendatasoft.com       | Open Datasoft     |
| French Gov Open Data                    | data.gouv.fr                     | Bespoke API       |
| Gestionnaire de Réseaux de Distribution | opendata.agenceore.fr            | Open Datasoft     |
| ONS Nomis                               | opendata.agenceore.fr            | Bespoke API       |

## Overview

This Python library provides a way to explore and interact with CKAN, OpenDataSoft, and French Government data catalogues - as well as other bespoke sources.

HerdingCATs follows a Session -> Explorer -> Loader pattern.

It is structured around the folllwing main classes:

1. `CkanCatExplorer`: For exploring CKAN-based data catalogues
2. `OpenDataSoftCatExplorer`: For exploring OpenDataSoft-based data catalogues
3. `FrenchGouvCatExplorer`: For exploring the French Government data catalogue
4. `NomisCatExplorer`: For exploring ONS data

5. `CkanLoader`: For loading CKAN catalogue data
6. `OpenDataSoftLoader`: For loading OpenDataSoft catalogue data
7. `FrenchGouvLoader`: For loading French Government catalogue data
8. `NomisLoader`: For loading ONS Nomis data

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

##### Methods Ckan

1. `check_site_health()`: Checks the health of the CKAN site
2. `get_package_count()`: Returns the total number of packages in a catalogue
3. `get_package_list()`: Returns a dictionary of all available packages
4. `get_package_list_dataframe(df_type: Literal["pandas", "polars"])`: Returns a dataframe of all available packages
5. `get_package_list_extra()`: Returns a list with extra package information
6. `get_package_list_dataframe_extra(df_type: Literal["pandas", "polars"])`: Returns a dataframe with extra package information
7. `get_organisation_list()`: Returns total number of organizations and their details
8. `show_package_info(package_name: Union[str, dict, Any])`: Returns package metadata including resource information
9. `show_package_info_dataframe(package_name: Union[str, dict, Any], df_type: Literal["pandas", "polars"])`: Returns package metadata as a dataframe
10. `package_search(search_query: str, num_rows: int)`: Searches for packages and returns results
11. `package_search_condense(search_query: str, num_rows: int)`: Returns a condensed view of package information
12. `package_search_condense_dataframe(search_query: str, num_rows: int, df_type: Literal["pandas", "polars"])`: Returns a condensed view with packed resources as a dataframe
13. `package_search_condense_dataframe_unpack(search_query: str, num_rows: int, df_type: Literal["pandas", "polars"])`: Returns a condensed view with unpacked resources as a dataframe
14. `extract_resource_url(package_info: List[Dict])`: Extracts resource URLs and metadata from package info. This is used to get the resource URL and format for the CKAN data loader class.

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

##### Methods OpenDataSoft

1. `check_site_health()`: Checks the health of the OpenDataSoft site
2. `fetch_all_datasets()`: Retrieves all datasets from an OpenDataSoft catalogue
3. `show_dataset_info(dataset_id)`: Returns detailed metadata about a specific dataset
4. `show_dataset_export_options(dataset_id)`: Returns available export formats and download URLs

### French Government Components

#### FrenchGouvCatExplorer

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.FrenchGouvCatalogue.GOUV_FR) as session:
        explore = hc.FrenchGouvCatExplorer(session)

if __name__ == "__main__":
    main()
```

##### Methods FrenchGouv

1. `check_health_check()`: Checks the health of the French Government data portal
2. `get_all_datasets()`: Returns a dictionary of all available datasets
3. `get_dataset_meta(identifier: str)`: Returns metadata for a specific dataset
4. `get_dataset_meta_dataframe(identifier: str, df_type: Literal["pandas", "polars"])`: Returns dataset metadata as a dataframe
5. `get_multiple_datasets_meta(identifiers: list)`: Fetches metadata for multiple datasets
6. `get_dataset_resource_meta(data: dict)`: Returns metadata for dataset resources
7. `get_dataset_resource_meta_dataframe(data: dict, df_type: Literal["pandas", "polars"])`: Returns resource metadata as a dataframe
8. `get_all_orgs()`: Returns all organizations in the catalogue

### ONS Nomis Components

#### NomisCatExplorer

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.NomisDataCatalogues.ONS_NOMIS) as session:
        explore = hc.NomisCatExplorer(session)

if __name__ == "__main__":
    main()
```

##### Methods Nomis

1. `get_all_datasets()`: Returns a list of all available datasets
2. `get_dataset_info(dataset_id: str)`: Returns metadata for a specific dataset
3. `get_dataset_codelist(dataset_id: str)`: Returns a list of codelists for a specific dataset
4. `get_codelist_meta_info(codelist_id: str)`: Returns metadata for a specific codelist
5. `get_codelist_values(data: Dict[str, Any])`: Returns a dictionary of codelist values for a specific codelist
6. `generate_full_dataset_download_url(dataset_id: str, geography_codes: List[int] | None = None)`: Generates a full dataset download URL with an optional list of geography codes to filter the data via query parameters

### Resource Loaders

All resource loader classes (`CkanLoader`, `OpenDataSoftLoader`, `FrenchGouvLoader`, `NomisLoader`) support the following methods:

#### DataFrame Loaders

- `polars_data_loader()`: Loads data into a Polars DataFrame
- `pandas_data_loader()`: Loads data into a Pandas DataFrame

#### Cloud Storage Loaders

- `aws_s3_data_loader()`: Loads data into AWS S3 as either raw data (depending on the format) or parquet file (if you choose to load as parquet)

---

> [!NOTE]
> We will be supporting DuckDB and MotherDuck soon.

---

## Examples

### CKAN Example

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.CkanDataCatalogues.HUMANITARIAN_DATA_STORE) as session:
        explore = hc.CkanCatExplorer(session)
        loader = hc.CkanCatResourceLoader()

        # Get list of all packages
        packages = explore.get_package_list()

        # Get info for a specific package
        data = explore.show_package_info("package_name")

        # Extract resource URLs
        resources = explore.extract_resource_url(data)

        # Load into different formats
        df_polars = loader.polars_data_loader(resources)

        # Specify the desired format if you want to otherwise it will defaul to the first dataset in the list
        df_pandas = loader.pandas_data_loader(resources, desired_format="parquet")

if __name__ == "__main__":
    main()
```

### OpenDataSoft Example

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:
        explore = hc.OpenDataSoftCatExplorer(session)
        loader = hc.OpenDataSoftResourceLoader()

        # Get export options for a dataset
        data = explore.show_dataset_export_options("package_name")

        # Load into Polars DataFrame (some catalogues require an API key)
        df = loader.polars_data_loader(data, format_type="parquet", api_key="your_api_key")

if __name__ == "__main__":
    main()
```

### French Government Example

```python
import HerdingCats as hc

def main():
    with hc.CatSession(hc.FrenchGouvCatalogue.GOUV_FR) as session:
        explore = hc.FrenchGouvCatExplorer(session)
        loader = hc.FrenchGouvResourceLoader()

        # Get all datasets
        datasets = explore.get_all_datasets()

        # Get metadata for a specific dataset
        meta_data = explore.get_dataset_meta("dataset-id")

        # Get resource metadata for a specific dataset
        resource_meta = explore.get_dataset_resource_meta(meta_data)

        # Load resource metadata into Polars DataFrame and specify the format of the data you want to load
        df = loader.polars_data_loader(resource_meta, "xlsx")

if __name__ == "__main__":
    main()
```

### ONS Nomis Example

```python
import HerdingCats as hc
from loguru import logger

def main():
    with hc.CatSession(hc.ONSNomisAPI.ONS_NOMI) as session:
        explore = hc.ONSNomisCatExplorer(session)
        loader = hc.ONSNomisLoader()

        # Get codelist for a dataset
        codelist = explore.get_dataset_codelist("NM_2_1")
        codelist = explore.get_codelist_meta_info(codelist[0])
        geo_types_with_codes = explore.get_codelist_values(codelist)

        # Generate download URL with these codes
        download_url = None

        # Check if "unitary authority areas" is in the geo_types_with_codes dictionary
        if "unitary authority areas" in geo_types_with_codes:
            unitary_authority_codes = geo_types_with_codes["unitary authority areas"]

            # Generate download URL with these codes
            download_url = explore.generate_full_dataset_download_url(
                "NM_2_1",
                geography_codes=unitary_authority_codes
            )
            logger.info(f"Download URL: {download_url}")

        # Download the data
        data = loader.get_sheet_names(download_url)
        logger.info(f"Data: {data}")

        # Load the data
        data = loader.polars_data_loader(download_url, sheet_name="Sheet 1", skip_rows=9)
        logger.info(f"Data: {data}")

if __name__ =="__main__":
    main()
```

## Contributing

Contributions are welcome! Please feel free to submit a PR.

For major changes, please open an issue first to discuss what you would like to change.
