# Notes for thinking through problems

## Breadcrumbs for next time...

Reduce code duplication in each of the catalogues data loaders...

So...

Implement a shared DataUploader trait/protocol for motherduck and aws s3 for all catalogues

Implement a shared DataFrameLoader trait/protocol for all catalogues

## Notes for implementing shared loaders behaviours

Need to understand the structure of we pass to the data loaders of eacgh catalogues first

## SSEN (Scottish and Southern Electricity Networks) Data
**Return Type:** `List[List]`

| Field | Data Structure |
|-------|---------------|
| Index 0 (Resource Name) | String |
| Index 1 (Timestamp) | ISO 8601 DateTime String |
| Index 2 (Format) | String |
| Index 3 (URL) | String URL |

## UK Power Networks Data
**Return Type:** `List[Dict]`

| Field | Data Structure |
|-------|---------------|
| download_url | String URL |
| format | String |

## Data.gouv.fr (French Government Data)
**Return Type:** `List[Dict]`

| Field | Data Structure |
|-------|---------------|
| dataset_id | String |
| resource_created_at | ISO 8601 DateTime String with Timezone |
| resource_extras | Dictionary/Object |
| resource_format | String |
| resource_frequency | Nullable |
| resource_id | String |
| resource_last_modified | ISO 8601 DateTime String with Timezone |
| resource_latest | String URL |
| resource_title | String |
| resource_url | String URL |
| slug | String |

### Summary:
- SSEN: Each list element contains 4 fields
- UK Power Networks: Each dictionary contains 2 key-value pairs
- Data.gouv.fr: Each dictionary contains 11 key-value pairs
