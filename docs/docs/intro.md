---
sidebar_position: 1
---

# Introduction to HerdingCATs

**HerdingCATs** is a Python library designed to speed up how data analysts explore and interact with open data sources.

## Purpose

The aim of this project is simple:

- **Navigate** the open data ecosystem
- **Find** the data that you need
- **Get** that data into a format and/or location for further analysis

## Installation

**PyPi package coming soon.** Once available, you can install with:

```bash
pip install HerdingCats
```

or if you're using Poetry:

```bash
poetry add HerdingCats
```

## Important Notes

Herding-CATs is currently under active development.

Features will change as the project evolves.

## Core Concepts

HerdingCATs follows a **Session → Explorer → Loader** pattern:

1. Create a session to connect to a data catalogue
2. Use an explorer to browse and find datasets
3. Use a loader to convert data to your preferred format

## Supported Data Catalogues

HerdingCATs supports multiple data catalogue types:

- **CKAN** - The most widely used open data platform
- **OpenDataSoft** - Popular in Europe, especially for energy data
- **Bespoke APIs** - Including French Government Data and ONS Nomis

See the [Supported Catalogues](./catalogues) page for a complete list.
