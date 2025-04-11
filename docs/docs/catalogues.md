---
sidebar_position: 3
---

# Supported Catalogues

HerdingCATs supports the following data sources by default:

## CKAN-based Catalogues

| Catalogue Name             | Website            | Description                |
| -------------------------- | ------------------ | -------------------------- |
| London Datastore           | data.london.gov.uk | London city open data      |
| Subak Data Catalogue       | data.subak.org     | Climate/environmental data |
| UK Gov Open Data           | data.gov.uk        | UK government open data    |
| Humanitarian Data Exchange | data.humdata.org   | Humanitarian/crisis data   |

## OpenDataSoft-based Catalogues

| Catalogue Name                          | Website                          | Description                 |
| --------------------------------------- | -------------------------------- | --------------------------- |
| UK Power Networks                       | ukpowernetworks.opendatasoft.com | UK energy network data      |
| Infrabel                                | opendata.infrabel.be             | Belgian railway data        |
| Paris                                   | opendata.paris.fr                | Paris city data             |
| Toulouse                                | data.toulouse-metropole.fr       | Toulouse metropolitan data  |
| Elia Belgian Energy                     | opendata.elia.be                 | Belgian energy grid data    |
| EDF Energy                              | opendata.edf.fr                  | French energy provider data |
| Cadent Gas                              | cadentgas.opendatasoft.com       | UK gas distribution data    |
| Gestionnaire de Réseaux de Distribution | opendata.agenceore.fr            | French grid distribution    |

## Bespoke API Catalogues

| Catalogue Name       | Website      | Description                  |
| -------------------- | ------------ | ---------------------------- |
| French Gov Open Data | data.gouv.fr | French government open data  |
| ONS Nomis            | nomis.co.uk  | UK official labor statistics |

## Adding Custom Catalogues

HerdingCATs is designed to be extensible. If you have a custom data catalogue you would like to connect to, you can:

1. Create a custom session using the base URL
2. Use the appropriate explorer for the catalogue type (CKAN, OpenDataSoft, etc.)
