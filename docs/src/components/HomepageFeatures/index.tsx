import type { ReactNode } from "react";
import clsx from "clsx";
import Heading from "@theme/Heading";
import styles from "./styles.module.css";

type FeatureItem = {
  title: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: "Explore Open Data",
    description: (
      <>
        Navigate the open data ecosystem with support for CKAN, OpenDataSoft,
        and other bespoke data catalogue APIs.
      </>
    ),
  },
  {
    title: "Find the Data You Need",
    description: (
      <>
        Search across multiple data catalogues with a unified interface. Access
        datasets from government portals, energy providers, and humanitarian
        sources.
      </>
    ),
  },
  {
    title: "Transform & Load Data",
    description: (
      <>
        Convert open datasets to Pandas or Polars DataFrames, or load directly
        to cloud storage for further analysis with minimal effort.
      </>
    ),
  },
];

const accentColors = ["#5e9dd5", "#6abf69", "#d4a05e"];

function Feature({
  title,
  description,
  index,
}: FeatureItem & { index: number }) {
  return (
    <div className={clsx("col col--4")}>
      <div
        className="text--center padding-horiz--md"
        style={{
          background: "rgba(40, 40, 40, 0.6)",
          borderRadius: "12px",
          padding: "1.5rem",
          margin: "0.5rem",
          boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
          border: "1px solid rgba(200, 200, 200, 0.1)",
          borderLeft: `4px solid ${accentColors[index]}`,
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          transition: "all 0.3s ease",
        }}
      >
        <Heading
          as="h3"
          style={{
            marginBottom: "1rem",
            color: accentColors[index],
          }}
        >
          {title}
        </Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

function CodeExample() {
  const pythonCode = (
    <>
      <span style={{ color: "#ff79c6" }}>import</span>{" "}
      <span style={{ color: "#8be9fd" }}>HerdingCats</span>{" "}
      <span style={{ color: "#ff79c6" }}>as</span>{" "}
      <span style={{ color: "#8be9fd" }}>hc</span>
      {"\n\n"}
      <span style={{ color: "#ff79c6" }}>def</span>{" "}
      <span style={{ color: "#50fa7b" }}>main</span>():
      {"\n"}
      <span style={{ color: "#f8f8f2", marginLeft: "20px" }}>
        <span style={{ color: "#6272a4" }}>
          # Create a session with a predefined catalogue
        </span>
        {"\n"}
        <span style={{ color: "#ff79c6" }}>with</span>{" "}
        <span style={{ color: "#8be9fd" }}>hc</span>.
        <span style={{ color: "#50fa7b" }}>CatSession</span>(
        <span style={{ color: "#8be9fd" }}>hc</span>.
        <span style={{ color: "#f1fa8c" }}>CkanDataCatalogues</span>.
        <span style={{ color: "#bd93f9" }}>LONDON_DATA_STORE</span>)
        <span style={{ color: "#ff79c6" }}>as</span>{" "}
        <span style={{ color: "#f8f8f2" }}>session</span>:{"\n"}
        <span style={{ marginLeft: "20px" }}>
          <span style={{ color: "#6272a4" }}>
            # Create an explorer for the catalogue
          </span>
          {"\n"}
          <span style={{ color: "#f8f8f2" }}>explorer</span> ={" "}
          <span style={{ color: "#8be9fd" }}>hc</span>.
          <span style={{ color: "#50fa7b" }}>CkanCatExplorer</span>(
          <span style={{ color: "#f8f8f2" }}>session</span>){"\n\n"}
          <span style={{ color: "#6272a4" }}># Create a data loader</span>
          {"\n"}
          <span style={{ color: "#f8f8f2" }}>data_loader</span> ={" "}
          <span style={{ color: "#8be9fd" }}>hc</span>.
          <span style={{ color: "#50fa7b" }}>CkanLoader</span>()
          {"\n\n"}
          <span style={{ color: "#6272a4" }}># Check the catalogue health</span>
          {"\n"}
          <span style={{ color: "#f8f8f2" }}>package</span> ={" "}
          <span style={{ color: "#f8f8f2" }}>explorer</span>.
          <span style={{ color: "#50fa7b" }}>show_package_info</span>(
          <span style={{ color: "#f1fa8c" }}>"use-of-force"</span>){"\n\n"}
          <span style={{ color: "#6272a4" }}># Extract the resource URLs</span>
          {"\n"}
          <span style={{ color: "#f8f8f2" }}>extracted_data</span> ={" "}
          <span style={{ color: "#f8f8f2" }}>explorer</span>.
          <span style={{ color: "#50fa7b" }}>extract_resource_url</span>(
          <span style={{ color: "#f8f8f2" }}>package</span>){"\n\n"}
          <span style={{ color: "#6272a4" }}>
            # Take the 8th resource from the list
          </span>
          {"\n"}
          <span style={{ color: "#f8f8f2" }}>data_to_load</span> ={" "}
          <span style={{ color: "#f8f8f2" }}>extracted_data</span>[
          <span style={{ color: "#bd93f9" }}>7</span>]{"\n\n"}
          <span style={{ color: "#6272a4" }}># Upload the data to AWS S3</span>
          {"\n"}
          <span style={{ color: "#6272a4" }}>
            # This uses the "raw" but you can specify "parquet" as well
          </span>
          {"\n"}
          <span style={{ color: "#f8f8f2" }}>data_loader</span>.
          <span style={{ color: "#50fa7b" }}>upload_data</span>({"\n"}
          <span style={{ marginLeft: "20px" }}>
            <span style={{ color: "#f8f8f2" }}>data_to_load</span>,{"\n"}
            <span style={{ color: "#f1fa8c" }}>"your-bucket-name"</span>,{"\n"}
            <span style={{ color: "#f1fa8c" }}>"your-custom-name"</span>,{"\n"}
            <span style={{ color: "#f1fa8c" }}>"raw"</span>
            {"\n"}
            <span style={{ color: "#f1fa8c" }}>"s3"</span>
            {"\n"}
          </span>
          )
        </span>
      </span>
      {"\n\n"}
      <span style={{ color: "#ff79c6" }}>if</span>{" "}
      <span style={{ color: "#f8f8f2" }}>__name__</span> =={" "}
      <span style={{ color: "#f1fa8c" }}>"__main__"</span>:{"\n"}
      <span style={{ marginLeft: "20px" }}>
        <span style={{ color: "#50fa7b" }}>main</span>()
      </span>
    </>
  );

  return (
    <div className="container">
      <div
        style={{
          marginTop: "3rem",
          marginBottom: "3rem",
          backgroundColor: "#282a36",
          borderRadius: "12px",
          boxShadow: "0 8px 16px rgba(0, 0, 0, 0.3)",
          overflow: "hidden",
          border: "1px solid rgba(255, 255, 255, 0.1)",
        }}
      >
        <div
          style={{
            padding: "10px 20px",
            backgroundColor: "#44475a",
            display: "flex",
            alignItems: "center",
          }}
        >
          <div style={{ display: "flex", gap: "8px", marginRight: "auto" }}>
            <div
              style={{
                width: "12px",
                height: "12px",
                borderRadius: "50%",
                backgroundColor: "#ff5555",
              }}
            ></div>
            <div
              style={{
                width: "12px",
                height: "12px",
                borderRadius: "50%",
                backgroundColor: "#f1fa8c",
              }}
            ></div>
            <div
              style={{
                width: "12px",
                height: "12px",
                borderRadius: "50%",
                backgroundColor: "#50fa7b",
              }}
            ></div>
          </div>
          <span
            style={{
              fontSize: "14px",
              color: "#f8f8f2",
              fontFamily: "monospace",
            }}
          >
            example.py
          </span>
        </div>
        <pre
          style={{
            padding: "20px",
            margin: 0,
            overflow: "auto",
            backgroundColor: "transparent",
            fontSize: "14px",
            lineHeight: "1.5",
            borderRadius: "0 0 8px 8px",
            fontFamily: "monospace",
          }}
        >
          {pythonCode}
        </pre>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div
        className="container"
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          minHeight: "40vh",
          paddingTop: "2rem",
          paddingBottom: "3rem",
        }}
      >
        <div className="row text--center" style={{ margin: "0 auto" }}>
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} index={idx} />
          ))}
        </div>

        <div
          style={{
            textAlign: "center",
            marginTop: "6rem",
            marginBottom: "1rem",
          }}
        >
          <Heading as="h2" style={{ color: "#d4838f" }}>
            Try it Yourself
          </Heading>
          <p style={{ maxWidth: "600px", margin: "1rem auto" }}>
            Getting started with HerdingCATs is simple. Below is a complete
            example showing how to access and upload data from the London Data
            Store.
          </p>
        </div>

        <CodeExample />
      </div>
    </section>
  );
}
