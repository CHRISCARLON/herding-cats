import type { ReactNode } from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import HomepageFeatures from "@site/src/components/HomepageFeatures";
import Heading from "@theme/Heading";

import styles from "./index.module.css";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className="row">
          <div className="col col--12 text--center">
            <Link
              className="button button--secondary button--lg"
              to="/docs/quick-start"
            >
              Quick Start 🐈‍⬛
            </Link>
          </div>
        </div>
        <div className="row" style={{ marginTop: "16px" }}>
          <div className="col col--12 text--center">
            <pre
              className="prism-code"
              style={{
                background: "#282c34",
                padding: "12px 20px",
                borderRadius: "6px",
                margin: "0 auto",
                display: "inline-block",
              }}
            >
              <code className="language-bash">uv add HerdCats</code>
            </pre>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Discover and explore open data catalogues with ease."
    >
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
