# Notes for thinking through problems

## Notes for implementing shared loaders behaviours

<img width="995" alt="Screenshot 2025-03-06 at 16 38 25" src="https://github.com/user-attachments/assets/5a25b2a8-2177-49a9-a581-0103f5d3f82b"/>

The data loaders all accept different data structures based on the corresponding explorer type.

The explorer passes over a data structures to the loader to parse and handle.

This might need to change in the future? Should there just be one data structure that is passed over??

## CKAN Data

**Return Type:** `List[List]`

| Field                   | Data Structure           |
| ----------------------- | ------------------------ |
| Index 0 (Resource Name) | String                   |
| Index 1 (Timestamp)     | ISO 8601 DateTime String |
| Index 2 (Format)        | String                   |
| Index 3 (URL)           | String URL               |

## OPEN DATASOFT Data

**Return Type:** `List[Dict]`

| Field        | Data Structure |
| ------------ | -------------- |
| download_url | String URL     |
| format       | String         |

## Data.gouv.fr (French Government Data)

**Return Type:** `List[Dict]`

| Field                  | Data Structure                         |
| ---------------------- | -------------------------------------- |
| dataset_id             | String                                 |
| resource_created_at    | ISO 8601 DateTime String with Timezone |
| resource_extras        | Dictionary/Object                      |
| resource_format        | String                                 |
| resource_frequency     | Nullable                               |
| resource_id            | String                                 |
| resource_last_modified | ISO 8601 DateTime String with Timezone |
| resource_latest        | String URL                             |
| resource_title         | String                                 |
| resource_url           | String URL                             |
| slug                   | String                                 |

## ONS Nomis Data

**Return Type:** `List[Dict]`
