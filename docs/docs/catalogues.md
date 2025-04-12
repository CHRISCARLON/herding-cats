---
sidebar_position: 3
---

# Supported Catalogues

HerdingCATs supports the following data sources by default:

<div className="catalogueSection" style={{backgroundColor: '#282828', padding: '16px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 8px rgba(0,0,0,0.3)', borderLeft: '4px solid #5e9dd5'}}>

## CKAN-based Catalogues

### London Datastore

- **Website:** [data.london.gov.uk](https://data.london.gov.uk)
- **Description:** London city open data

### Subak Data Catalogue

- **Website:** [data.subak.org](https://data.subak.org)
- **Description:** Climate/environmental data

### UK Gov Open Data

- **Website:** [data.gov.uk](https://data.gov.uk)
- **Description:** UK government open data

### Humanitarian Data Exchange

- **Website:** [data.humdata.org](https://data.humdata.org)
- **Description:** Humanitarian/crisis data
</div>

<div className="catalogueSection" style={{backgroundColor: '#282828', padding: '16px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 8px rgba(0,0,0,0.3)', borderLeft: '4px solid #6abf69'}}>

## OpenDataSoft-based Catalogues

### UK Power Networks

- **Website:** [ukpowernetworks.opendatasoft.com](https://ukpowernetworks.opendatasoft.com)
- **Description:** UK energy network data

### Infrabel

- **Website:** [opendata.infrabel.be](https://opendata.infrabel.be)
- **Description:** Belgian railway data

### Paris

- **Website:** [opendata.paris.fr](https://opendata.paris.fr)
- **Description:** Paris city data

### Toulouse

- **Website:** [data.toulouse-metropole.fr](https://data.toulouse-metropole.fr)
- **Description:** Toulouse metropolitan data

### Elia Belgian Energy

- **Website:** [opendata.elia.be](https://opendata.elia.be)
- **Description:** Belgian energy grid data

### EDF Energy

- **Website:** [opendata.edf.fr](https://opendata.edf.fr)
- **Description:** French energy provider data

### Cadent Gas

- **Website:** [cadentgas.opendatasoft.com](https://cadentgas.opendatasoft.com)
- **Description:** UK gas distribution data

### Gestionnaire de Réseaux de Distribution

- **Website:** [opendata.agenceore.fr](https://opendata.agenceore.fr)
- **Description:** French grid distribution
</div>

<div className="catalogueSection" style={{backgroundColor: '#282828', padding: '16px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 8px rgba(0,0,0,0.3)', borderLeft: '4px solid #d4a05e'}}>

## Bespoke API Catalogues

### French Gov Open Data

- **Website:** [data.gouv.fr](https://data.gouv.fr)
- **Description:** French government open data

### ONS Nomis

- **Website:** [nomis.co.uk](https://nomis.co.uk)
- **Description:** UK official labor statistics
</div>

<div className="catalogueSection" style={{backgroundColor: '#282828', padding: '16px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 8px rgba(0,0,0,0.3)', borderLeft: '4px solid #d4838f'}}>

## Adding Custom Catalogues

HerdingCATs is designed to be extensible. If you have a custom data catalogue you would like to connect to, you can:

1. Raise an issue on the [GitHub repository](https://github.com/chriscarlon/herding-cats/issues)
2. Submit a pull request with your changes (you'll have to extend the `CatSession` class enum)

The reason for this is sometimes I like to check that a catalogue is working well with the library before committing to using it in the project.

However, the plan is to allow users to add their own catalogues with just a URL and a few other details in the future.

</div>
