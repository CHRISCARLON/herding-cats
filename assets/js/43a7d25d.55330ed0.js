"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[533],{2021:(e,a,o)=>{o.r(a),o.d(a,{assets:()=>l,contentTitle:()=>d,default:()=>h,frontMatter:()=>t,metadata:()=>r,toc:()=>i});const r=JSON.parse('{"id":"loaders","title":"Data Loaders","description":"HerdingCATs provides various loader classes to retrieve data from catalogues and transform it into useful formats.","source":"@site/docs/loaders.md","sourceDirName":".","slug":"/loaders","permalink":"/herding-cats/docs/loaders","draft":false,"unlisted":false,"tags":[],"version":"current","sidebarPosition":5,"frontMatter":{"sidebar_position":5},"sidebar":"tutorialSidebar","previous":{"title":"ONS Nomis Explorer","permalink":"/herding-cats/docs/explorers/nomis"}}');var n=o(4848),s=o(8453);const t={sidebar_position:5},d="Data Loaders",l={},i=[{value:"Loader Types",id:"loader-types",level:2},{value:"Common Loading Methods",id:"common-loading-methods",level:2},{value:"DataFrame Loaders",id:"dataframe-loaders",level:3},{value:"Cloud Storage Loaders",id:"cloud-storage-loaders",level:3},{value:"CKAN Loader Example",id:"ckan-loader-example",level:2},{value:"OpenDataSoft Loader Example",id:"opendatasoft-loader-example",level:2},{value:"French Government Loader Example",id:"french-government-loader-example",level:2},{value:"ONS Nomis Loader Example",id:"ons-nomis-loader-example",level:2},{value:"Coming Soon",id:"coming-soon",level:2}];function c(e){const a={code:"code",h1:"h1",h2:"h2",h3:"h3",header:"header",li:"li",p:"p",pre:"pre",ul:"ul",...(0,s.R)(),...e.components};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(a.header,{children:(0,n.jsx)(a.h1,{id:"data-loaders",children:"Data Loaders"})}),"\n",(0,n.jsx)(a.p,{children:"HerdingCATs provides various loader classes to retrieve data from catalogues and transform it into useful formats."}),"\n",(0,n.jsx)(a.h2,{id:"loader-types",children:"Loader Types"}),"\n",(0,n.jsx)(a.p,{children:"There are different loader classes for each catalogue type:"}),"\n",(0,n.jsxs)(a.ul,{children:["\n",(0,n.jsxs)(a.li,{children:[(0,n.jsx)(a.code,{children:"CkanLoader"})," - For CKAN catalogue data"]}),"\n",(0,n.jsxs)(a.li,{children:[(0,n.jsx)(a.code,{children:"OpenDataSoftLoader"})," - For OpenDataSoft catalogue data"]}),"\n",(0,n.jsxs)(a.li,{children:[(0,n.jsx)(a.code,{children:"FrenchGouvLoader"})," - For French Government catalogue data"]}),"\n",(0,n.jsxs)(a.li,{children:[(0,n.jsx)(a.code,{children:"NomisLoader"})," - For ONS Nomis data"]}),"\n"]}),"\n",(0,n.jsx)(a.h2,{id:"common-loading-methods",children:"Common Loading Methods"}),"\n",(0,n.jsx)(a.p,{children:"All loader classes support these standard methods:"}),"\n",(0,n.jsx)(a.h3,{id:"dataframe-loaders",children:"DataFrame Loaders"}),"\n",(0,n.jsx)(a.pre,{children:(0,n.jsx)(a.code,{className:"language-python",children:"# Load data into a Polars DataFrame\ndf_polars = loader.polars_data_loader(resources)\n\n# Load data into a Pandas DataFrame\ndf_pandas = loader.pandas_data_loader(resources)\n"})}),"\n",(0,n.jsx)(a.h3,{id:"cloud-storage-loaders",children:"Cloud Storage Loaders"}),"\n",(0,n.jsx)(a.pre,{children:(0,n.jsx)(a.code,{className:"language-python",children:'# Load data into AWS S3\nloader.aws_s3_data_loader(\n    resources,\n    bucket_name="your-bucket",\n    s3_key="path/to/file.parquet",\n    save_as_parquet=True\n)\n'})}),"\n",(0,n.jsx)(a.h2,{id:"ckan-loader-example",children:"CKAN Loader Example"}),"\n",(0,n.jsx)(a.pre,{children:(0,n.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\nwith hc.CatSession(hc.CkanDataCatalogues.HUMANITARIAN_DATA_STORE) as session:\n    explorer = hc.CkanCatExplorer(session)\n    loader = hc.CkanLoader()\n\n    # Find data about refugees\n    results = explorer.package_search_condense("refugees", num_rows=1)\n    if results:\n        # Get package information\n        package_info = explorer.show_package_info(results[0])\n\n        # Extract resource URLs\n        resources = explorer.extract_resource_url(package_info)\n\n        # Load into a Polars DataFrame\n        df = loader.polars_data_loader(resources)\n\n        # Specify a particular format if the resource has multiple options\n        df = loader.pandas_data_loader(resources, desired_format="csv")\n'})}),"\n",(0,n.jsx)(a.h2,{id:"opendatasoft-loader-example",children:"OpenDataSoft Loader Example"}),"\n",(0,n.jsx)(a.pre,{children:(0,n.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\nwith hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:\n    explorer = hc.OpenDataSoftCatExplorer(session)\n    loader = hc.OpenDataSoftLoader()\n\n    # Get export options for a dataset\n    data = explorer.show_dataset_export_options("your_dataset_id")\n\n    # Load into a Polars DataFrame (some catalogues require an API key)\n    df = loader.polars_data_loader(data, format_type="csv", api_key="your_api_key")\n'})}),"\n",(0,n.jsx)(a.h2,{id:"french-government-loader-example",children:"French Government Loader Example"}),"\n",(0,n.jsx)(a.pre,{children:(0,n.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\nwith hc.CatSession(hc.FrenchGouvCatalogue.GOUV_FR) as session:\n    explorer = hc.FrenchGouvCatExplorer(session)\n    loader = hc.FrenchGouvLoader()\n\n    # Get metadata for a dataset\n    metadata = explorer.get_dataset_meta("your-dataset-id")\n\n    # Get resource metadata\n    resources = explorer.get_dataset_resource_meta(metadata)\n\n    # Load the first resource into a DataFrame\n    if resources:\n        df = loader.polars_data_loader(resources[0], "csv")\n'})}),"\n",(0,n.jsx)(a.h2,{id:"ons-nomis-loader-example",children:"ONS Nomis Loader Example"}),"\n",(0,n.jsx)(a.pre,{children:(0,n.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\nwith hc.CatSession(hc.NomisDataCatalogues.ONS_NOMIS) as session:\n    explorer = hc.NomisCatExplorer(session)\n    loader = hc.NomisLoader()\n\n    # Generate a download URL\n    download_url = explorer.generate_full_dataset_download_url("NM_2_1")\n\n    # Check available sheets (for Excel files)\n    sheets = loader.get_sheet_names(download_url)\n\n    # Load data from a specific sheet, skipping header rows\n    df = loader.polars_data_loader(\n        download_url,\n        sheet_name=sheets[0] if sheets else None,\n        skip_rows=9\n    )\n'})}),"\n",(0,n.jsx)(a.h2,{id:"coming-soon",children:"Coming Soon"}),"\n",(0,n.jsx)(a.p,{children:"Additional loader functionality:"}),"\n",(0,n.jsxs)(a.ul,{children:["\n",(0,n.jsx)(a.li,{children:"DuckDB integration"}),"\n",(0,n.jsx)(a.li,{children:"MotherDuck cloud database integration"}),"\n"]})]})}function h(e={}){const{wrapper:a}={...(0,s.R)(),...e.components};return a?(0,n.jsx)(a,{...e,children:(0,n.jsx)(c,{...e})}):c(e)}},8453:(e,a,o)=>{o.d(a,{R:()=>t,x:()=>d});var r=o(6540);const n={},s=r.createContext(n);function t(e){const a=r.useContext(s);return r.useMemo((function(){return"function"==typeof e?e(a):{...a,...e}}),[a,e])}function d(e){let a;return a=e.disableParentContext?"function"==typeof e.components?e.components(n):e.components||n:t(e.components),r.createElement(s.Provider,{value:a},e.children)}}}]);