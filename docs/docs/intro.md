---
sidebar_position: 1
---

# Introduction to HerdingCATs

**HerdingCATs** is a Python library designed to speed up how data analysts explore and interact with open data sources.

## Purpose

The aim of this project is simple:

- **Navigate** the open data ecosystem
- **Find** the data that you need
- **Load** that data into a format and/or location for further analysis

## Installation

**PyPi package coming soon.**

Once available, you can install with:

```bash
pip install HerdingCats
```

```bash
poetry add HerdingCats
```

```bash
uv add HerdingCats
```

## Important Notes

Herding-CATs is currently under active development.

Features will change as the project evolves.

## Core Concepts

HerdingCATs follows a **Session → Explorer → Loader** pattern:

1. Create a session to connect to an open data source.
2. Use an explorer to browse and find the data you need.
3. Use a loader to load the data into your preferred format and/or location.

## Supported Data Sources

HerdingCATs supports multiple open data sources:

- **CKAN** - Widely used for open data catalogues
- **OpenDataSoft** - Popular in Europe, especially for energy related data catalogues
- **Bespoke APIs** - Including French Government open data and ONS Nomis

See the [Supported Catalogues](./catalogues) page for a complete list.

More sources are being added all the time.

If you need a data source that is not listed, please [raise an issue](https://github.com/chriscarlon/herding-cats/issues).
