"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[533],{2021:(e,a,r)=>{r.r(a),r.d(a,{assets:()=>l,contentTitle:()=>i,default:()=>p,frontMatter:()=>s,metadata:()=>n,toc:()=>d});const n=JSON.parse('{"id":"loaders","title":"Data Loaders","description":"HerdingCATs provides specialised loader classes to transform data from various catalogue explorers into usable formats or storage solutions.","source":"@site/docs/loaders.md","sourceDirName":".","slug":"/loaders","permalink":"/docs/loaders","draft":false,"unlisted":false,"tags":[],"version":"current","sidebarPosition":5,"frontMatter":{"sidebar_position":5},"sidebar":"tutorialSidebar","previous":{"title":"ONS Nomis Explorer","permalink":"/docs/explorers/nomis"}}');var t=r(4848),o=r(8453);const s={sidebar_position:5},i="Data Loaders",l={},d=[{value:"Data Flow Architecture",id:"data-flow-architecture",level:2},{value:"From Explorer to Loader",id:"from-explorer-to-loader",level:2},{value:"CKAN Explorer",id:"ckan-explorer",level:4},{value:"OpenDataSoft Explorer",id:"opendatasoft-explorer",level:4},{value:"French Government Explorer",id:"french-government-explorer",level:4},{value:"ONS Nomis Explorer",id:"ons-nomis-explorer",level:4},{value:"Data Structure Transformation Flow",id:"data-structure-transformation-flow",level:4},{value:"Validation Decorator Transformations",id:"validation-decorator-transformations",level:3},{value:"Type System and DataFrame Loading Traits",id:"type-system-and-dataframe-loading-traits",level:2},{value:"DataFrameLoaderTrait",id:"dataframeloadertrait",level:3},{value:"StorageTrait",id:"storagetrait",level:3},{value:"Common Loading Capabilities",id:"common-loading-capabilities",level:2},{value:"DataFrame Creation",id:"dataframe-creation",level:3},{value:"Storage Options",id:"storage-options",level:3},{value:"Excel File Helpers",id:"excel-file-helpers",level:3},{value:"DuckDB Integration",id:"duckdb-integration",level:3},{value:"Benefits of DuckDB Integration",id:"benefits-of-duckdb-integration",level:4},{value:"Available DuckDB Methods",id:"available-duckdb-methods",level:4},{value:"Example: Filtering and Aggregating Large Datasets",id:"example-filtering-and-aggregating-large-datasets",level:4},{value:"Detailed Usage Examples",id:"detailed-usage-examples",level:2},{value:"CKAN Loader Example",id:"ckan-loader-example",level:3},{value:"OpenDataSoft Loader Example",id:"opendatasoft-loader-example",level:3},{value:"French Government Loader Example",id:"french-government-loader-example",level:3},{value:"ONS Nomis Loader Example",id:"ons-nomis-loader-example",level:3},{value:"Implementation Details",id:"implementation-details",level:2},{value:"Storage Mechanisms",id:"storage-mechanisms",level:3},{value:"Future Extensions",id:"future-extensions",level:2}];function c(e){const a={admonition:"admonition",code:"code",h1:"h1",h2:"h2",h3:"h3",h4:"h4",header:"header",li:"li",ol:"ol",p:"p",pre:"pre",strong:"strong",table:"table",tbody:"tbody",td:"td",th:"th",thead:"thead",tr:"tr",ul:"ul",...(0,o.R)(),...e.components};return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(a.header,{children:(0,t.jsx)(a.h1,{id:"data-loaders",children:"Data Loaders"})}),"\n",(0,t.jsx)(a.p,{children:"HerdingCATs provides specialised loader classes to transform data from various catalogue explorers into usable formats or storage solutions."}),"\n",(0,t.jsx)(a.p,{children:"Each loader is designed to handle the specific data structure returned by its corresponding explorer class."}),"\n",(0,t.jsx)(a.h2,{id:"data-flow-architecture",children:"Data Flow Architecture"}),"\n",(0,t.jsx)(a.p,{children:"The loaders follow a consistent pattern:"}),"\n",(0,t.jsxs)(a.ol,{children:["\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Data Discovery"}),": Explorer classes locate and fetch metadata about datasets"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Data Structure Extraction"}),": Explorers provide structured data references to loaders"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Data Loading"}),": Loaders fetch the actual data from source URLs"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Data Transformation"}),": Loaders convert data into desired formats (DataFrame, Parquet, etc.)"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Data Storage/Usage"}),": Data is used for analysis or stored in a persistent location"]}),"\n"]}),"\n",(0,t.jsx)(a.h2,{id:"from-explorer-to-loader",children:"From Explorer to Loader"}),"\n",(0,t.jsx)(a.p,{children:"A key feature of the loader system is how data flows from explorer methods through validation decorators to loader methods."}),"\n",(0,t.jsx)(a.p,{children:"Each explorer produces a specific data structure that gets transformed by validation decorators into formats that loaders can efficiently process."}),"\n",(0,t.jsx)(a.p,{children:"Each explorer type includes specialised methods that create the data structures required by their corresponding loader:"}),"\n",(0,t.jsx)(a.h4,{id:"ckan-explorer",children:"CKAN Explorer"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:"# Input: Package information from show_package_info()\n# Output: List of resources with [name, date, format, url]\nresources = explorer.extract_resource_url(package_info)\n"})}),"\n",(0,t.jsx)(a.h4,{id:"opendatasoft-explorer",children:"OpenDataSoft Explorer"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'# Input: Dataset ID\n# Output: List of dictionaries with format and download_url\nexport_options = explorer.show_dataset_export_options("dataset_id")\n'})}),"\n",(0,t.jsx)(a.h4,{id:"french-government-explorer",children:"French Government Explorer"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:"# Input: Dataset metadata from get_dataset_meta()\n# Output: List of dictionaries with resource_format, resource_url, etc.\nresources = explorer.get_dataset_resource_meta(metadata)\n"})}),"\n",(0,t.jsx)(a.h4,{id:"ons-nomis-explorer",children:"ONS Nomis Explorer"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'# Input: Dataset ID and optional geography codes\n# Output: Direct URL string to the Excel file\nurl = explorer.generate_full_dataset_download_url("NM_2_1")\n'})}),"\n",(0,t.jsx)(a.h4,{id:"data-structure-transformation-flow",children:"Data Structure Transformation Flow"}),"\n",(0,t.jsxs)(a.admonition,{title:"Data Structure Transformation Flow",type:"info",children:[(0,t.jsx)(a.p,{children:(0,t.jsx)(a.strong,{children:"CKAN Explorer"})}),(0,t.jsxs)(a.ul,{children:["\n",(0,t.jsxs)(a.li,{children:["Explorer Method: ",(0,t.jsx)(a.code,{children:"extract_resource_url()"})]}),"\n",(0,t.jsxs)(a.li,{children:["Original Structure: ",(0,t.jsx)(a.code,{children:"[name, date, format, url]"})]}),"\n",(0,t.jsxs)(a.li,{children:["Validation Decorator: ",(0,t.jsx)(a.code,{children:"validate_ckan_resource"})]}),"\n",(0,t.jsxs)(a.li,{children:["Final Structure for Loader: ",(0,t.jsx)(a.code,{children:"[format, url]"})]}),"\n"]}),(0,t.jsx)(a.p,{children:(0,t.jsx)(a.strong,{children:"OpenDataSoft Explorer"})}),(0,t.jsxs)(a.ul,{children:["\n",(0,t.jsxs)(a.li,{children:["Explorer Method: ",(0,t.jsx)(a.code,{children:"show_dataset_export_options()"})]}),"\n",(0,t.jsxs)(a.li,{children:["Original Structure: ",(0,t.jsx)(a.code,{children:'[{"format": "csv", "download_url": "..."}]'})]}),"\n",(0,t.jsxs)(a.li,{children:["Validation Decorator: ",(0,t.jsx)(a.code,{children:"validate_opendata_resource"})]}),"\n",(0,t.jsx)(a.li,{children:"Final Structure for Loader: Same as original"}),"\n"]}),(0,t.jsx)(a.p,{children:(0,t.jsx)(a.strong,{children:"French Government Explorer"})}),(0,t.jsxs)(a.ul,{children:["\n",(0,t.jsxs)(a.li,{children:["Explorer Method: ",(0,t.jsx)(a.code,{children:"get_dataset_resource_meta()"})]}),"\n",(0,t.jsxs)(a.li,{children:["Original Structure: ",(0,t.jsx)(a.code,{children:'[{"resource_format": "csv", "resource_url": "..."}]'})]}),"\n",(0,t.jsxs)(a.li,{children:["Validation Decorator: ",(0,t.jsx)(a.code,{children:"validate_french_gouv_resource"})]}),"\n",(0,t.jsx)(a.li,{children:"Final Structure for Loader: Same as original"}),"\n"]}),(0,t.jsx)(a.p,{children:(0,t.jsx)(a.strong,{children:"ONS Nomis Explorer"})}),(0,t.jsxs)(a.ul,{children:["\n",(0,t.jsxs)(a.li,{children:["Explorer Method: ",(0,t.jsx)(a.code,{children:"generate_full_dataset_download_url()"})]}),"\n",(0,t.jsxs)(a.li,{children:["Original Structure: ",(0,t.jsx)(a.code,{children:'"https://example.com/data.xlsx"'})]}),"\n",(0,t.jsxs)(a.li,{children:["Validation Decorator: ",(0,t.jsx)(a.code,{children:"validate_ons_nomis_resource"})]}),"\n",(0,t.jsx)(a.li,{children:"Final Structure for Loader: Same as original"}),"\n"]})]}),"\n",(0,t.jsx)(a.h3,{id:"validation-decorator-transformations",children:"Validation Decorator Transformations"}),"\n",(0,t.jsx)(a.p,{children:"The validation decorators serve multiple purposes:"}),"\n",(0,t.jsxs)(a.ol,{children:["\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Verify"})," that the input data matches expected patterns"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Transform"})," the data into a standardized format (especially for CKAN resources)"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Extract"})," only the necessary fields for loading operations"]}),"\n"]}),"\n",(0,t.jsx)(a.p,{children:"For example, the CKAN validator transforms a complex structure into a simple [format, url] list:"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'@staticmethod\ndef validate_ckan_resource(func: Callable[..., T]) -> Callable[..., T]:\n    """\n    Decorator that transforms CKAN explorer data into loader-compatible format\n\n    Input formats expected:\n    - Single list: [name, date, format, url] indexed by ResourceIndex\n    - List of lists: [[name, date, format, url], [...], ...]\n\n    Output:\n    - Simplified list: [format, url] that\'s passed to the decorated function\n    """\n'})}),"\n",(0,t.jsx)(a.p,{children:"These decorators standardize the input data format before processing, making the loader methods more robust and safer to use, while providing a consistent interface for all loaders."}),"\n",(0,t.jsx)(a.h2,{id:"type-system-and-dataframe-loading-traits",children:"Type System and DataFrame Loading Traits"}),"\n",(0,t.jsx)(a.p,{children:"HerdingCATs uses the Protocol pattern from Python's typing module to define consistent interfaces for different operations:"}),"\n",(0,t.jsx)(a.h3,{id:"dataframeloadertrait",children:"DataFrameLoaderTrait"}),"\n",(0,t.jsxs)(a.p,{children:["The ",(0,t.jsx)(a.code,{children:"DataFrameLoaderTrait"})," protocol ensures type-safe handling of both Pandas and Polars DataFrames:"]}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'class DataFrameLoaderTrait(Protocol):\n    """Protocol defining the interface for DataFrame loaders."""\n\n    @overload\n    def create_dataframe(\n        self,\n        data: BytesIO,\n        format_type: str,\n        loader_type: Literal["pandas"],\n        sheet_name: Optional[str] = None,\n        skip_rows: Optional[int] = None,\n    ) -> PandasDataFrame: ...\n\n    @overload\n    def create_dataframe(\n        self,\n        data: BytesIO,\n        format_type: str,\n        loader_type: Literal["polars"],\n        sheet_name: Optional[str] = None,\n        skip_rows: Optional[int] = None,\n    ) -> PolarsDataFrame: ...\n'})}),"\n",(0,t.jsx)(a.h3,{id:"storagetrait",children:"StorageTrait"}),"\n",(0,t.jsxs)(a.p,{children:["The ",(0,t.jsx)(a.code,{children:"StorageTrait"})," protocol defines a consistent interface for storage operations:"]}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'class StorageTrait(Protocol):\n    """Protocol defining the interface for remote storage uploaders."""\n\n    def upload(\n        self,\n        data: BytesIO,\n        bucket: str,\n        key: str,\n        mode: Literal["raw", "parquet"] = "parquet",\n        file_format: Optional[str] = None,\n    ) -> str: ...\n'})}),"\n",(0,t.jsx)(a.p,{children:"These traits allow for consistent usage patterns regardless of the underlying implementation."}),"\n",(0,t.jsx)(a.h2,{id:"common-loading-capabilities",children:"Common Loading Capabilities"}),"\n",(0,t.jsx)(a.p,{children:"All loader classes implement these core functions:"}),"\n",(0,t.jsx)(a.h3,{id:"dataframe-creation",children:"DataFrame Creation"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:"# Load into Polars DataFrame (faster for large datasets)\ndf_polars = loader.polars_data_loader(resources)\n\n# Load into Pandas DataFrame (more familiar API)\ndf_pandas = loader.pandas_data_loader(resources)\n"})}),"\n",(0,t.jsx)(a.h3,{id:"storage-options",children:"Storage Options"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'# Upload to S3 storage\nloader.upload_data(\n    resources,\n    bucket_name="your-bucket",\n    custom_name="dataset-name",\n    mode="raw",  # or "parquet" for automatic conversion\n    storage_type="s3"\n)\n\n# Store locally (where supported)\nloader.upload_data(\n    resources,\n    bucket_name="local-directory",\n    custom_name="dataset-name",\n    mode="parquet",\n    storage_type="local"\n)\n'})}),"\n",(0,t.jsx)(a.h3,{id:"excel-file-helpers",children:"Excel File Helpers"}),"\n",(0,t.jsx)(a.p,{children:"For spreadsheets, additional options are available:"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'# Get sheet names from Excel files\nsheet_names = loader.get_sheet_names(resources)\n\n# Load specific sheets and skip header rows\ndf = loader.polars_data_loader(\n    resources,\n    sheet_name="Sheet1",\n    skip_rows=5\n)\n'})}),"\n",(0,t.jsx)(a.h3,{id:"duckdb-integration",children:"DuckDB Integration"}),"\n",(0,t.jsx)(a.p,{children:"OpenDataSoft now supports direct loading and querying with DuckDB, providing powerful SQL-based analysis capabilities."}),"\n",(0,t.jsx)(a.p,{children:"The plan is to extend this to all loaders in the future."}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\nwith hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS_DNO) as session:\n    explorer = hc.OpenDataSoftCatExplorer(session)\n    loader = hc.OpenDataSoftLoader()\n\n    # Get dataset export options\n    export_options = explorer.show_dataset_export_options("ukpn-flood-warning-areas")\n    print(export_options)\n\n    # Get results as pandas DataFrame\n    df_pandas = loader.query_to_pandas(\n        resource_data=export_options,\n        table_name="flood_areas",\n        format_type="parquet",\n        query="SELECT * FROM flood_warnings LIMIT 15",\n        api_key="your_api_key_if_needed"\n    )\n\n    print(df_pandas)\n'})}),"\n",(0,t.jsx)(a.p,{children:"Example Output..."}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-bash",children:"# Session initialisation\n2025-04-13 12:29:49.364 | SUCCESS | Session started successfully with ukpowernetworks.opendatasoft.com\n\n# Available export formats (truncated for readability)\n[\n  {'format': 'csv', 'download_url': 'https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/ukpn-flood-warning-areas/exports/csv'},\n  {'format': 'json', 'download_url': 'https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/ukpn-flood-warning-areas/exports/json'},\n  {'format': 'parquet', 'download_url': 'https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/ukpn-flood-warning-areas/exports/parquet'},\n  # Additional formats available...\n]\n\n# DuckDB initialisation and data loading\n2025-04-13 12:29:49.686 | INFO | Connected to DuckDB in-memory database\n2025-04-13 12:29:49.742 | INFO | DuckDB extensions loaded: httpfs, spatial\n2025-04-13 12:29:49.743 | INFO | Loading parquet data from URL into table 'flood_areas'\n\n# Query results (SELECT * FROM flood_areas LIMIT 15)\n| index | river_sea                    |\n|-------|------------------------------|\n| 0     | River Ray                    |\n| 1     | River Thames                 |\n| 2     | Cuckmere River, Bull River   |\n| 3     | West Brook                   |\n| 4     | Sussex River Ouse            |\n| 5     | North Stream, South Streams  |\n| 6     | River Leam                   |\n| 7     | River Darent                 |\n| 8     | River Leen                   |\n| 9     | Beck                         |\n| 10    | River Test                   |\n| 11    | River Deben, North Sea       |\n| 12    | River Thames                 |\n| 13    | River Arun                   |\n| 14    | River Sence                  |\n\nSome of the columns have been truncated for readability.\n\n# Session completion\n2025-04-13 12:30:53.086 | SUCCESS | Session Closed: https://ukpowernetworks.opendatasoft.com\n"})}),"\n",(0,t.jsx)(a.h4,{id:"benefits-of-duckdb-integration",children:"Benefits of DuckDB Integration"}),"\n",(0,t.jsxs)(a.ul,{children:["\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Efficient Memory Usage"}),": Process large datasets without loading everything into memory"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"SQL Power"}),": Leverage SQL for filtering, joining, and aggregating data"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Performance"}),": DuckDB is optimized for analytical queries on columnar data"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Seamless Integration"}),": Results can be easily converted to familiar pandas or polars DataFrames"]}),"\n"]}),"\n",(0,t.jsx)(a.h4,{id:"available-duckdb-methods",children:"Available DuckDB Methods"}),"\n",(0,t.jsx)(a.p,{children:"All loader classes implement these DuckDB-related methods:"}),"\n",(0,t.jsxs)(a.table,{children:[(0,t.jsx)(a.thead,{children:(0,t.jsxs)(a.tr,{children:[(0,t.jsx)(a.th,{children:"Method"}),(0,t.jsx)(a.th,{children:"Description"})]})}),(0,t.jsxs)(a.tbody,{children:[(0,t.jsxs)(a.tr,{children:[(0,t.jsx)(a.td,{children:(0,t.jsx)(a.code,{children:"duckdb_data_loader()"})}),(0,t.jsx)(a.td,{children:"Load data directly into a DuckDB table"})]}),(0,t.jsxs)(a.tr,{children:[(0,t.jsx)(a.td,{children:(0,t.jsx)(a.code,{children:"execute_query()"})}),(0,t.jsx)(a.td,{children:"Run a SQL query on loaded data"})]}),(0,t.jsxs)(a.tr,{children:[(0,t.jsx)(a.td,{children:(0,t.jsx)(a.code,{children:"query_to_pandas()"})}),(0,t.jsx)(a.td,{children:"Load data and return pandas DataFrame from a query"})]}),(0,t.jsxs)(a.tr,{children:[(0,t.jsx)(a.td,{children:(0,t.jsx)(a.code,{children:"query_to_polars()"})}),(0,t.jsx)(a.td,{children:"Load data and return polars DataFrame from a query"})]})]})]}),"\n",(0,t.jsx)(a.h4,{id:"example-filtering-and-aggregating-large-datasets",children:"Example: Filtering and Aggregating Large Datasets"}),"\n",(0,t.jsx)(a.p,{children:"When working with large datasets, you can use SQL to filter and aggregate data before loading it into memory:"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'# Instead of loading entire dataset and filtering in Python:\ndf = loader.query_to_polars(\n    resource_data=export_options,\n    table_name="energy_consumption",\n    format_type="csv",\n    query="""\n        SELECT\n            region,\n            AVG(consumption) as avg_consumption,\n            SUM(consumption) as total_consumption,\n            COUNT(*) as count\n        FROM energy_consumption\n        WHERE year >= 2020\n        GROUP BY region\n        ORDER BY total_consumption DESC\n    """\n)\n'})}),"\n",(0,t.jsx)(a.p,{children:"This approach is particularly useful for OpenDataSoft datasets that can be quite large and may benefit from pre-filtering or aggregation before analysis."}),"\n",(0,t.jsx)(a.h2,{id:"detailed-usage-examples",children:"Detailed Usage Examples"}),"\n",(0,t.jsx)(a.h3,{id:"ckan-loader-example",children:"CKAN Loader Example"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\nwith hc.CatSession(hc.CkanDataCatalogues.HUMANITARIAN_DATA_STORE) as session:\n    explorer = hc.CkanCatExplorer(session)\n    loader = hc.CkanLoader()\n\n    # Find data about refugees\n    results = explorer.package_search_condense("refugees", num_rows=10)\n\n    if results:\n        # Find a specific dataset in the results list\n        syria_dataset = next((item for item in results if "syria" in item.get("name", "").lower()), results[0])\n        package_info = explorer.show_package_info(syria_dataset["name"])\n\n        # Extract resource URLs - transforms into the format loader expects\n        resources = explorer.extract_resource_url(package_info)\n        print(resources)\n\n        # Load into a Polars DataFrame (fast for large data)\n        df = loader.polars_data_loader(resources)\n\n        # Or load a specific format if multiple are available\n        csv_df = loader.pandas_data_loader(resources, desired_format="csv")\n\n        # Upload to S3 in raw format (preserves original)\n        s3_path = loader.upload_data(\n            resources,\n            bucket_name="your-bucket",\n            custom_name="refugee-data",\n            mode="raw",\n            storage_type="s3"\n        )\n'})}),"\n",(0,t.jsx)(a.h3,{id:"opendatasoft-loader-example",children:"OpenDataSoft Loader Example"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\nwith hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:\n    explorer = hc.OpenDataSoftCatExplorer(session)\n    loader = hc.OpenDataSoftLoader()\n\n    # Get export options for a dataset\n    data = explorer.show_dataset_export_options("your_dataset_id")\n\n    # The data format will be a list of dicts with format and download_url keys\n    for resource in data:\n        print(f"Format: {resource[\'format\']}, URL: {resource[\'download_url\']}")\n\n    # Load into a Polars DataFrame (some catalogues require an API key)\n    df = loader.polars_data_loader(\n        data,\n        format_type="csv",  # Specify which format to use\n        api_key="your_api_key",  # Some datasets require authentication\n        skip_rows=2  # Skip header rows if needed\n    )\n\n    # Convert to parquet and upload to S3\n    loader.upload_data(\n        data,\n        bucket_name="your-bucket",\n        custom_name="power-networks",\n        format_type="csv",  # Specify which format to use as source\n        mode="parquet",  # Convert to parquet during upload\n        storage_type="s3",\n        api_key="your_api_key"\n    )\n'})}),"\n",(0,t.jsx)(a.h3,{id:"french-government-loader-example",children:"French Government Loader Example"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\nwith hc.CatSession(hc.FrenchGouvCatalogue.GOUV_FR) as session:\n    explorer = hc.FrenchGouvCatExplorer(session)\n    loader = hc.FrenchGouvLoader()\n\n    # Get metadata for a dataset\n    metadata = explorer.get_dataset_meta("your-dataset-id")\n\n    # Get resource metadata\n    resources = explorer.get_dataset_resource_meta(metadata)\n\n    # Resources will be a list of dicts with resource_format and resource_url keys\n    if resources:\n        # Load CSV resource into DataFrame\n        df = loader.polars_data_loader(resources, "csv")\n\n        # For Excel files, you can work with specific sheets\n        if resources[0][\'resource_format\'].lower() in [\'xlsx\', \'xls\']:\n            df = loader.pandas_data_loader(\n                resources,\n                "xlsx",\n                sheet_name="Data Sheet",\n                skip_rows=3  # Skip header information\n            )\n'})}),"\n",(0,t.jsx)(a.h3,{id:"ons-nomis-loader-example",children:"ONS Nomis Loader Example"}),"\n",(0,t.jsx)(a.pre,{children:(0,t.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\nwith hc.CatSession(hc.NomisDataCatalogues.ONS_NOMIS) as session:\n    explorer = hc.NomisCatExplorer(session)\n    loader = hc.ONSNomisLoader()\n\n    # Generate a download URL - this is directly passed to the loader\n    download_url = explorer.generate_full_dataset_download_url("NM_2_1")\n\n    print(f"Download URL: {download_url}")\n\n    # The ONS Nomis files are often complex Excel files\n    # Check available sheets\n    sheets = loader.get_sheet_names(download_url)\n    print(f"Available sheets: {sheets}")\n\n    # Load data from a specific sheet, skipping header rows\n    # ONS Nomis data often requires skipping metadata rows\n    df = loader.polars_data_loader(\n        download_url,\n        sheet_name=sheets[0] if sheets else None,\n        skip_rows=9\n    )\n\n    # Save directly to S3\n    loader.upload_data(\n        download_url,\n        bucket_name="your-bucket",\n        custom_name="nomis-employment-data",\n        mode="parquet",  # Convert to parquet during upload\n        storage_type="s3"\n    )\n'})}),"\n",(0,t.jsx)(a.h2,{id:"implementation-details",children:"Implementation Details"}),"\n",(0,t.jsx)(a.h3,{id:"storage-mechanisms",children:"Storage Mechanisms"}),"\n",(0,t.jsx)(a.p,{children:"Under the hood, loaders use two main storage implementations:"}),"\n",(0,t.jsxs)(a.ol,{children:["\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.code,{children:"S3Uploader"}),": For storing data in AWS S3 buckets"]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.code,{children:"LocalUploader"}),": For storing data in local directories"]}),"\n"]}),"\n",(0,t.jsxs)(a.p,{children:["Both implement the ",(0,t.jsx)(a.code,{children:"StorageTrait"})," protocol, allowing for consistent usage patterns regardless of storage location."]}),"\n",(0,t.jsx)(a.h2,{id:"future-extensions",children:"Future Extensions"}),"\n",(0,t.jsx)(a.p,{children:"Upcoming loader capabilities include:"}),"\n",(0,t.jsxs)(a.ul,{children:["\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"DuckDB Integration"}),": Direct loading into DuckDB for fast local analytics for all loader types. Currently only supported for OpenDataSoft."]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"MotherDuck Cloud Database"}),": Integration with the cloud version of DuckDB. Not yet implemented."]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"More Format Support"}),": Adding support for additional data formats like GeoJSON, Shapefile, etc. Not yet implemented."]}),"\n",(0,t.jsxs)(a.li,{children:[(0,t.jsx)(a.strong,{children:"Incremental Loading"}),": Support for larger datasets by loading data in chunks. Not yet implemented."]}),"\n"]})]})}function p(e={}){const{wrapper:a}={...(0,o.R)(),...e.components};return a?(0,t.jsx)(a,{...e,children:(0,t.jsx)(c,{...e})}):c(e)}},8453:(e,a,r)=>{r.d(a,{R:()=>s,x:()=>i});var n=r(6540);const t={},o=n.createContext(t);function s(e){const a=n.useContext(o);return n.useMemo((function(){return"function"==typeof e?e(a):{...a,...e}}),[a,e])}function i(e){let a;return a=e.disableParentContext?"function"==typeof e.components?e.components(t):e.components||t:s(e.components),n.createElement(o.Provider,{value:a},e.children)}}}]);