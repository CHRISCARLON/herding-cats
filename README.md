# Herding-CATs 🐈‍⬛

Version: 0.1.4

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

## Current Default Open Data Catalogues

Herding-CATs supports the following catalogues by default:

### Default

| Catalogue Name | Website | Catalogue Endpoint | Comments |
|----------------|---------|-------------------|----------|
| London Datastore | https://data.london.gov.uk | CKAN | Works with all methods |
| Subak Data Catalogue | https://data.subak.org | CKAN | Works with all methods |
| Gov Open Data | https://www.data.gov.uk | CKAN | Works with all methods |
| Humanitarian Data Exchange | https://data.humdata.org | CKAN | Works with most methods |
| UK Power Networks | https://ukpowernetworks.opendatasoft.com | Open Datasoft | Works with all methods |
| Infrabel | https://opendata.infrabel.be | Open Datasoft | Works with all methods |
| Paris | https://opendata.paris.fr | Open Datasoft | Works with all methods |
| Toulouse | https://data.toulouse-metropole.fr | Open Datasoft | Works with all methods |

### TBC

| Catalogue Name | Website | Catalogue API Endpoint Definition | Comments |
|----------------|---------|-----------------------------------|----------|
| Bristol Open Data | https://opendata.bristol.gov.uk | TBC | Need to figure out how to call the catalogue backend |
| Icebreaker One | https://ib1.org | CKAN | Needs further investigation as authentication with an API key may be required |
| Data Mill North | https://datamillnorth.org | CKAN | Seems to have a slightly different implementation - may not work with all methods |
| Canada Open Data | https://open.canada.ca | CKAN | Needs further investigation due to different implementation |
