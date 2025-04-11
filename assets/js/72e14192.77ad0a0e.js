"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[814],{795:(e,a,n)=>{n.r(a),n.d(a,{assets:()=>l,contentTitle:()=>i,default:()=>u,frontMatter:()=>o,metadata:()=>t,toc:()=>d});const t=JSON.parse('{"id":"quick-start","title":"Quick Start Guide","description":"Get up and running with HerdingCATs in minutes.","source":"@site/docs/quick-start.md","sourceDirName":".","slug":"/quick-start","permalink":"/herding-cats/docs/quick-start","draft":false,"unlisted":false,"tags":[],"version":"current","sidebarPosition":2,"frontMatter":{"sidebar_position":2},"sidebar":"tutorialSidebar","previous":{"title":"Introduction to HerdingCATs","permalink":"/herding-cats/docs/intro"},"next":{"title":"Supported Catalogues","permalink":"/herding-cats/docs/catalogues"}}');var r=n(4848),s=n(8453);const o={sidebar_position:2},i="Quick Start Guide",l={},d=[{value:"Basic Usage Pattern",id:"basic-usage-pattern",level:2},{value:"Example: Finding Data in CKAN",id:"example-finding-data-in-ckan",level:2},{value:"Example: Loading Data into a DataFrame",id:"example-loading-data-into-a-dataframe",level:2},{value:"Example: Loading Data to Cloud Storage",id:"example-loading-data-to-cloud-storage",level:2},{value:"Next Steps",id:"next-steps",level:2}];function c(e){const a={a:"a",code:"code",h1:"h1",h2:"h2",header:"header",li:"li",ol:"ol",p:"p",pre:"pre",ul:"ul",...(0,s.R)(),...e.components};return(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)(a.header,{children:(0,r.jsx)(a.h1,{id:"quick-start-guide",children:"Quick Start Guide"})}),"\n",(0,r.jsx)(a.p,{children:"Get up and running with HerdingCATs in minutes."}),"\n",(0,r.jsx)(a.h2,{id:"basic-usage-pattern",children:"Basic Usage Pattern"}),"\n",(0,r.jsx)(a.p,{children:"All interactions with HerdingCATs follow this pattern:"}),"\n",(0,r.jsxs)(a.ol,{children:["\n",(0,r.jsxs)(a.li,{children:["Create a ",(0,r.jsx)(a.code,{children:"CatSession"})," with your chosen data catalogue"]}),"\n",(0,r.jsx)(a.li,{children:"Use an explorer to find and inspect data"}),"\n",(0,r.jsx)(a.li,{children:"Use a loader to retrieve and transform data"}),"\n"]}),"\n",(0,r.jsx)(a.h2,{id:"example-finding-data-in-ckan",children:"Example: Finding Data in CKAN"}),"\n",(0,r.jsx)(a.pre,{children:(0,r.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\n# Create a session with a predefined catalogue\nwith hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:\n    # Create an explorer for the catalogue\n    explorer = hc.CkanCatExplorer(session)\n\n    # Check the catalogue health\n    health = explorer.check_site_health()\n    print(f"Catalogue status: {health}")\n\n    # Search for packages containing "climate"\n    results = explorer.package_search_condense("climate", 5)\n\n    # Get more detailed info about the first result\n    if results:\n        detailed_info = explorer.show_package_info(results[0])\n        print(f"Found dataset: {detailed_info.get(\'title\')}")\n'})}),"\n",(0,r.jsx)(a.h2,{id:"example-loading-data-into-a-dataframe",children:"Example: Loading Data into a DataFrame"}),"\n",(0,r.jsx)(a.pre,{children:(0,r.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\n# Create session and explorer\nwith hc.CatSession(hc.CkanDataCatalogues.LONDON_DATA_STORE) as session:\n    explorer = hc.CkanCatExplorer(session)\n\n    # Find a dataset about air quality\n    results = explorer.package_search_condense("air quality", 1)\n\n    if results:\n        # Get detailed info\n        package_info = explorer.show_package_info(results[0])\n\n        # Extract resource URLs\n        resources = explorer.extract_resource_url(package_info)\n\n        # Create a loader\n        loader = hc.CkanLoader()\n\n        # Load into a Polars DataFrame\n        df = loader.polars_data_loader(resources)\n\n        # Or load into a Pandas DataFrame\n        # df = loader.pandas_data_loader(resources)\n\n        print(f"Loaded {len(df)} rows of data")\n'})}),"\n",(0,r.jsx)(a.h2,{id:"example-loading-data-to-cloud-storage",children:"Example: Loading Data to Cloud Storage"}),"\n",(0,r.jsx)(a.pre,{children:(0,r.jsx)(a.code,{className:"language-python",children:'import HerdingCats as hc\n\n# Create session, explorer, and find data (as above)\nwith hc.CatSession(hc.OpenDataSoftDataCatalogues.UK_POWER_NETWORKS) as session:\n    explorer = hc.OpenDataSoftCatExplorer(session)\n\n    # Get export options for a dataset\n    data = explorer.show_dataset_export_options("your_dataset_id")\n\n    # Create loader\n    loader = hc.OpenDataSoftLoader()\n\n    # Load directly to S3\n    loader.aws_s3_data_loader(\n        data,\n        bucket_name="your-bucket-name",\n        s3_key="data/your-file.parquet",\n        format_type="parquet"\n    )\n'})}),"\n",(0,r.jsx)(a.h2,{id:"next-steps",children:"Next Steps"}),"\n",(0,r.jsx)(a.p,{children:"Check out the following sections to learn more:"}),"\n",(0,r.jsxs)(a.ul,{children:["\n",(0,r.jsxs)(a.li,{children:[(0,r.jsx)(a.a,{href:"./catalogues",children:"Supported Catalogues"})," - See all available data sources"]}),"\n",(0,r.jsxs)(a.li,{children:[(0,r.jsx)(a.a,{href:"./explorers/ckan",children:"CKAN Explorer Guide"})," - Learn about CKAN data exploration"]}),"\n",(0,r.jsxs)(a.li,{children:[(0,r.jsx)(a.a,{href:"./loaders",children:"Data Loaders"})," - Learn about all data loading options"]}),"\n"]})]})}function u(e={}){const{wrapper:a}={...(0,s.R)(),...e.components};return a?(0,r.jsx)(a,{...e,children:(0,r.jsx)(c,{...e})}):c(e)}},8453:(e,a,n)=>{n.d(a,{R:()=>o,x:()=>i});var t=n(6540);const r={},s=t.createContext(r);function o(e){const a=t.useContext(s);return t.useMemo((function(){return"function"==typeof e?e(a):{...a,...e}}),[a,e])}function i(e){let a;return a=e.disableParentContext?"function"==typeof e.components?e.components(r):e.components||r:o(e.components),t.createElement(s.Provider,{value:a},e.children)}}}]);