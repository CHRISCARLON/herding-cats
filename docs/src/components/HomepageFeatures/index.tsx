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

function Feature({ title, description }: FeatureItem) {
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
            color: "var(--ifm-color-primary-lighter)",
          }}
        >
          {title}
        </Heading>
        <p>{description}</p>
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
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
