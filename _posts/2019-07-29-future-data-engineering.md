---
layout: post
title:  "The Future of Data Engineering"
author: chris
categories: [ kafka, machine-learning, data-engineering ]
featured: true
hidden: true
image: assets/images/2019-07-29-future-data-engineering/mathilda-khoo-HLA3TAFQuQs-unsplash.jpg
---

I have been thinking lately about where we’ve come in data engineering over the past few years, and about what the future holds for work in this area. Most of this thought has been framed in the context of what some of our teams are doing at WePay, but I believe the framework below applies more broadly, and is worth sharing.

Data engineering’s job is to help an organization move and process data. This generally requires two different systems, broadly speaking: a data pipeline, and a data warehouse. The data pipeline is responsible for moving the data, and the data warehouse is responsible for processing it. I acknowledge that this is a bit overly simplistic. You can do processing in the pipeline itself by doing transformations between extraction and loading with batch and stream processing. The “data warehouse” now includes many storage and processing systems (Flink, Spark, Presto, Hive, BigQuery, Redshift, etc), as well as auxiliary systems such as data catalogs, job schedulers, and so on. Still, I believe the paradigm holds.

The industry is working through changes in how these systems are built and managed. There are four areas, in particular, where I expect to see shifts over the next few years.

* Timeliness: From batch to realtime
* Connectivity: From one:one bespoke integrations to many:many
* Centralization: From centrally managed to self-serve tooling
* Automation: From manually managed to automated tooling

{% include newsletter.html %}

## From batch to realtime
Both data pipelines and data processing have been batch-based in the past. Data was transported between systems in batch ETL snapshots, and data was processed in a periodic cadence, which was managed by a job scheduler (Airflow, Oozie, Azkaban, Luigi).

We are now shifting to both realtime data pipelines and realtime data processing systems. Change data capture systems such as Debezium, as well as the robust connector ecosystem in Kafka have made realtime data pipelines possible. Stream processing has gone through a renaissance over the last five years, and there are now more realtime data processing systems than I can keep track of. The combination of these factors means that the ingress (extraction), processing (transformation), and egress (loading) can all happen in realtime.

The trade off right now seems to be in cost and complexity. If a company is getting a data warehouse off the ground, and needs an immediate 4-6 week impact, it’s a heavy load to set up a realtime pipeline. Batch is still much easier to get up and running. I expect that this will change over the next few years as tooling in the realtime area continues to mature, and cloud hosting continues to grow.

## Connectivity
Connecting upstream data sources to the data warehouse used to mean adding an entirely new bespoke integration for each one-to-one connection between systems. [Jay Kreps](https://twitter.com/jaykreps)’ seminal post, [The Log: What every software engineer should know about real-time data’s unifying abstraction](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying), illustrates this well:

![Complex data pipeline](assets/images/2019-07-29-future-data-engineering/datapipeline_complex.png "Complex data pipeline")

The post also goes into detail about the future of data integration. It was written in 2013, and a lot of what is predicted and proposed is just coming to fruition today. The launch of [Confluent](https://www.confluent.io/), [Kafka Connect](https://docs.confluent.io/current/connect/index.html), and the connector ecosystem now mean that there are many viable connectors to attach to an existing Kafka data pipeline.

I suspect we’ll begin to see this architectural approach take hold. Detaching ingress from egress, and both from transform means that data pipelines can begin to take advantage of [Metcalfe’s law](https://en.wikipedia.org/wiki/Metcalfe%27s_law), where adding a new system to the pipeline will be both cheaper and more valuable than it was before.

I’m aware that the paragraphs above are quite Kafka-centric, but I want to note that this approach need not be realtime (though I believe it will be). In [Airflow](https://github.com/apache/airflow/), for example, you currently see a GoogleCloudStorageHook, a BigQueryHook, and then a one-to-one operator: GoogleCloudStorageToBigQueryOperator. Untangling ingest from egress fully, so that a staging area in a common format exists would go a long way in improving even batch-based ETL.

This pattern will also allow us to embrace more fine-grained data systems. Once it’s cheap to attach new systems to the pipeline, the value of adding a new specialized system to the ecosystem will outweigh its cost. As a result, I expect to see more usage of niche data processing systems such as graph databases, realtime OLAP systems, search indices, and the like. The pattern will also allow for more experimentation, since attaching a new system to the pipeline and then discovering it doesn’t meet your need is much cheaper than it used to be. (This is a theme that I've already covered in a post from earlier this year, [Kafka is your escape hatch ](https://riccomini.name/kafka-escape-hatch).)

The cloud also adds an interesting wrinkle to the connectivity story. The dream of having your data integration story amount to a series of checkboxes in an AWS console is not yet realized, and I don’t expect that we’ll see a full integration amongst all systems in each cloud provider any time soon. The idea of full integration between cloud providers in a point-and-click UI seems even farther off. Lastly, integrating cloud and non-cloud (or even third-party hosted) systems will still require work.

For these reasons, I think cloud-based third-party solutions such as [Stitch](https://www.stitchdata.com/) will continue to be valuable. This also means that the realtime Kafka architecture that I describe above will be the most mature solution if you can afford to build and operate it.

## Automation & decentralization
The last two items in my list, automation and centralization, really go hand-in hand. Most organizations have a single data engineering and/or data warehousing team that manages the data pipeline and data warehouse. When a request comes into these teams, they need to evaluate the request across two criteria:

* What can we do (technical)
* What may we do (policy)

In my experience, a centralized team will usually have some automation, but it will be mostly focused on technical automation. This is natural, as it’s more in an engineering team’s wheel house. This kind of work usually means replacing operational [toil](https://landing.google.com/sre/sre-book/chapters/eliminating-toil/) with automation; activities like adding a new connector, setting up monitoring or data quality checks, creating a new database or table, granting permission, and so on.

There is, however, a second type of toil that I believe data engineering has not yet automated: policy toil.  This kind of drudgery involves making decision about who can have access to what data, how long data should be persisted, what kind of sensitive data is allowed to be in which data systems, and in which geographies data may reside. Data engineering is usually not the team that ultimately decides the answers to these questions, but they often must act as a liason or driver when finding the answers. This usually means navigating requests through other parts of the organization such as security, compliance, and legal.

This kind of work is already important because of regulation such as [GDPR](https://eugdpr.org/) and [CCPA](https://www.caprivacy.org/). If I add government regulation to the ongoing expansion of tech beyond traditional software companies, and into areas such as health and finance (see [Why Software Is Eating the World](https://a16z.com/2011/08/20/why-software-is-eating-the-world/)), it is inevitable that the importance of automating policy toil will only grow.

Policy automation will require focus in areas that are usually neglected in less mature data ecosystems. Tooling such as Lyft’s [Amundsen](https://eng.lyft.com/amundsen-lyfts-data-discovery-metadata-engine-62d27254fbb9), [Apache Ranger](https://ranger.apache.org/), and Google’s [Data Catalog](https://cloud.google.com/data-catalog/) will need to be adopted. Policy enforcement such as audits, [DLP](https://en.wikipedia.org/wiki/DLP), sensitive data detection, retention enforcement, and access control management will all need to be fully automated.

As automation matures in both the technical and policy areas, the next logical question will be: why do we need a single team to manage this? If tools are enforcing policy guidelines, and automating the data pipeline, why not empower teams around the organization to directly manage their data pipelines and data warehouses?

On the data pipeline front, decentralization will mean that any team may decide to plug into the existing data pipeline, provided that they conform to (automatically enforced) technical and policy guidelines. In the data warehouse, teams will be able to create databases, datasets, data marts, and data lakes as their needs arise (some of this already exists today). This will cause a lot of complexity, confusion, and duplication, which is why tooling (such as those listed above) is such an important prerequisite to decentralization.

The topic of decentralization is something that’s covered in greater detail in [Zhamak Dehghani](https://twitter.com/zhamakd)’s post, [How to Move Beyond a Monolithic Data Lake to a Distributed Data  Mesh](https://martinfowler.com/articles/data-monolith-to-mesh.html), and I invite you to read it. Due to the [cognitive load](https://techbeacon.com/app-dev-testing/forget-monoliths-vs-microservices-cognitive-load-what-matters) required to manage a more complex data ecosystem, I suspect the only scalable and efficient way forward will be through automation and decentralization. This will, in some ways, look like the [CI/CD](https://en.wikipedia.org/wiki/CI/CD) and monolith-to-micro-service migration we’ve seen play out over the past decade in the application layer.

## Conclusion
All of this leaves me optimistic. There’s a lot left to do, and with that a lot of opportunity. I expect data engineering to grow in organizations to meet these demands.  Open source communities will continue to expand, and new projects and startups will be built. All of this should lead to massive efficiency gains for organizations as a whole, and hopefully more rigorous data management practices.
