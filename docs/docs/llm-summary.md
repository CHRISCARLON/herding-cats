---
sidebar_position: 7
---

# LLM Summary

Use AI to automatically summarise and understand dataset metadata from data catalogues.

## Overview

The LLM Summary feature uses OpenAI's GPT models to analyse and summarise dataset information.

## Prerequisites

You need an OpenAI API key to use this feature:

```bash
# Set your OpenAI API key as an environment variable
export OPENAI_API_KEY="sk-your-api-key-here"
```

## Basic Usage

```python
import HerdingCats as hc
from HerdingCats.llm.llm_summary import CatalogueSummariser

summariser = CatalogueSummariser(temperature=0.2)

# Get dataset metadata (from any explorer)
with hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:
    explorer = hc.CkanCatExplorer(session)
    package_info = explorer.show_package_info("london-borough-profiles")

    summary = summariser.summarise_catalogue(package_info)

    print(f"Title: {summary['title']}")
    print(f"\nDescription: {summary['description']}")
    print(f"\nKey Resources: {summary['key_resources']}")
    print(f"\nMetadata: {summary['metadata_summary']}")
```

## Output Structure

The summariser returns a structured dictionary with:

```python
{
    "title": "Dataset title",
    "description": "A concise description in ~100 words",
    "key_resources": [
        {
            "name": "Resource name",
            "format": "CSV",
            "description": "What this resource contains"
        }
    ],
    "metadata_summary": {
        "created": "2024-01-01",
        "update_frequency": "Monthly",
        "license": "Open Government License",
        "other_key_info": "..."
    }
}
```

## API Usage and Costs

- Uses OpenAI's `gpt-4o-mini` model by default
- Monitor your OpenAI API usage dashboard for costs

## Limitations

- API key must have sufficient credits
- Summary quality depends on metadata quality

## Future Enhancements

- Support for other providers (Anthropic, etc.)
- Custom prompt templates
