---
layout: post
title:  "Kafka change data capture breaks database encapsulation"
author: chris
categories: [ kafka, distributed-systems ]
featured: true
hidden: true
image: assets/images/2018-11-05-kafka-change-data-capture-breaks-database-encapsulation/bjorn-kamfjord-379952-unsplash.jpg
---

Realtime [change data capture](https://en.wikipedia.org/wiki/Change_data_capture) (CDC) is becoming a popular architecture for [data integration](https://en.wikipedia.org/wiki/Data_integration) and [data pipelines](https://en.wikipedia.org/wiki/Pipeline_(computing)). The rise of [Kafka connect](https://docs.confluent.io/current/connect/index.html), in particular, has triggered a lot of interest in the subject. In realtime CDC, a database's changes (inserts, updates, and deletes) are available as a stream of mutations for downstream consumers to tail.

## Schema evolution

Problems begin to arise when schema evolution enters the picture. Developers are used to thinking of their databases as nicely encapsulated private data stores. If they want to evolve a schema, they should be able to. Typical use cases involve renaming a field, adding a new field, removing an old field, or changing data types. All of these can pose problems for the Kafka ecosystem. Removing required fields, for example, is a forwards incompatible change. Downstream consumers expect the field to be there. Similarly, changing a field from an integer to a string will also break downstream code that's expecting to get integers values.

[Confluent](https://www.confluent.io/) offers a nice [schema registry](https://www.confluent.io/confluent-schema-registry/) that helps to protect against this. The registry offers [backwards, forwards, and full compatibility checks](https://docs.confluent.io/current/avro.html#forward-compatibility). If a producer violates the schema rules, for example dropping a required field, the schema registry will reject the change, which will cause the producer to fail producing its messages.

But where does this leave us? Telling a developer, "you're not allowed to change your database schema," isn't good enough. Even worse, the schema registry is disconnected from the source database schema, so the developer will likely be able to evolve the schema anyway. This will cause the pipeline to break, since the source Kafka connector will not be able to produce the new messages. We need a way to manage schema evolution, even when changes are incompatible.

### Library API migrations

At LinkedIn, we had a tool that allowed us to manage library migrations. The premise was much the same as what I've outlined above. A library owner makes a change, and wants to migrate all the users of the library to the new version. The tool would allow us to:

* Find all of the library users.
* Determine which versions each user was on.
* Automatically trigger a pull request with the library version upgrade.
* Run CI tests with the upgraded library.
* Nag service owners to upgrade the library.
* Track upgrade progress.

Obviously, if the library change resulted in an incompatible API change, the various services using the library would fail to compile, and their CI tests would fail. The tool helped track this as well.

The library migration pattern outlined above is appealing because it allows developers the flexibility to evolve their library while not breaking downstream users. Unfortunately, things aren't quite as straight forward in the streaming world. With libraries, a developer can make changes and commit them to the library while services continue to use older versions of the library. The two can co-exist at the same time. This is not the case with streaming. The second a producer decides to send data to a new topic, or stop sending certain fields, downstream consumers will be affected, and potentially break.

### Service API migrations

There's another place where this problem appears. Developers managing web service APIs also have to solve this problem. The web services have the same problem as the Kafka pipeline, though. If a web service decides to alter its API in an incompatible way, all of the invoking services must be upgraded. This can't be done in lock-step, though, due to the nature of distributed systems. Either the client or the server must go first (if you want to avoid downtime). If the client goes first, it will break since the new API is not yet available on the server. If the server goes first, the client will break since the old API is no longer available. Instead, a web service must expose both the old and new API for some period of time, until all of the legacy systems can be migrated to the new API. This is typically managed through some combination of API versioning, request re-writing, and proxies. This is what the Kafka ecosystem needs.

## Your data model is an API

The service API use case can be loosely mapped to Kafka by thinking of the source DB's data model as a versioned API. In fact, the Confluent schema registry already versions APIs on a per-topic basis. Most DB schema management systems ([Liquibase](https://www.liquibase.org/), [Flyway](https://flywaydb.org/), [Alembic](https://bitbucket.org/zzzeek/alembic)) also version DB schemas. When the source DB decides that it wants to evolve its schema, it's akin to a version change in a web service's API. If the version change is forwards incompatible (a major version change in *semantic versioning* terms), a migration needs to occur.

<center>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Using <a href="https://twitter.com/apachekafka?ref_src=twsrc%5Etfw">@apachekafka</a> connect makes developers think about data models as an API. Although it can be uncomfortable, it&#39;s just exposing what&#39;s always been the case: downstream consumers of the data depend on your data model. You need to think about how it evolves over time.</p>&mdash; Chris Riccomini (@criccomini) <a href="https://twitter.com/criccomini/status/953354007912898560?ref_src=twsrc%5Etfw">January 16, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</center>

In the web service model, the migration would probably consist of deploying the new version of the web service along side the old version and routing API calls through a proxy. Based on the calls, the proxy could then route legacy calls to the old service instances, and new calls to the new service instances. Once all services are migrated, the old services could be deprecated and torn down.

A similar solution can be implemented by transforming data in the CDC pipeline. The high-level approach is to emit the new data to a new topic in Kafka, and then use a transformation to consume the new data, and emit it to the old topic so that legacy consumers will continue to receive updates until they're migrated.

## Managing schema migrations

An example data warehousing pipeline follows.

![source db, kafka, destination db](assets/images/2018-11-05-kafka-change-data-capture-breaks-database-encapsulation/example-data-warehousing.png "CDC example: data warehousing")

A mutation in a source DB is consumed by a Kafka source connector. It's then emitted to Kafka as a fully schema'd Avro message. A Kafka sink connector then consumes the message and inserts it into the destination data warehouse DB. Transformations can be placed at any point in this flow.

* Transformations can reside in the source DB through the use of triggers and materialized views.
* [Single message transforms](https://cwiki.apache.org/confluence/display/KAFKA/KIP-66%3A+Single+Message+Transforms+for+Kafka+Connect) allow transformations to be placed in Kafka connect on either the ingest or egress side of the flow.
* A stream processing system such as [Flink](https://flink.apache.org/), [Spark streaming](https://spark.apache.org/), [Kafka streams](https://kafka.apache.org/documentation/streams/)/[KSQL](https://www.confluent.io/product/ksql/), or [Samza](https://samza.apache.org/) can be used to implement transformations inside Kafka.
* Transformations can be placed in the destination database, itself.

### Source DB transformations

The system persisting data in the source DB can choose to write to a new table in addition to the legacy table. Triggers or transactional INSERTs can be used to keep the two tables in sync.

### Kafka source connector transformations

Multiple source connectors can be run. The legacy source connector can be deployed to include a *single message transform* that alters the new schema back into the legacy format. A second source connector can run and emit to a new topic. Once consumers are migrated from the old topic to the new topic, the legacy connector can be shut down.

### Kafka transformations

Much like the pattern above, when data evolves in a non-compatible way, it can be emitted to a new topic. A stream processor can then be deployed to consume the new data, transform it into a format that's forwards compatible, and emit the messages to the old topic.

### Kafka sink connector transformations

Sink connectors can be deployed much the same way as source connectors. When a data model is evolved, a second sink connector can be deployed pointing to the new topic. A transformation can be set in either the new sink connector or the legacy sink connector. If the transformation is set in the new sink connector, it can emit its records to the same destination as the legacy connector, and the legacy connector can simply be shut down. If the transformation is set in the legacy sink connector, it can continue to emit to the legacy destination, while the new connector emits to a new destination (for example, a new table in the data warehouse). 

### Destination DB transformations

Lastly, transformations can be done in the destination DB. This is the standard ELT approach to the problem. Views can be created in the destination database to modify the data as is required to make legacy requests continue to execute properly.

### Private topics

A variation on the theme above is to think of a source DB's topics as private topics. Compatibility checks could be completely disabled. Only transformers would be allowed to consume from the private topics. These transformers could then emit data to "public" topics. As the schemas changed in the private topic, the transformers could be updated to munge data into formats that were compatible with the legacy public topics.

## Truly incompatible changes

This approach is not perfect, though. If data has truly been dropped, for example, there's likely nothing that the transformation will be able to do to add it back in. It might be possible for the transformation logic to fetch data from a third party (such as another database or web service), but in some cases, the data is simply not available anywhere else. In cases like this, it seems that the best that can be done is to put a tombstone value into the field, and determine which consumers will be affected. Still, forcing developers to think about these issues is important, even if it means the extra overhead of having to coordinate with downstream consumers.

## Beyond CDC

Thus far, the focus has been exclusively on CDC use cases where the upstream message producer is a database of some sort. The scope of this problem can be expanded, though, to any producer, not just databases. In such a case, the solutions look largely the same.

The producer can decide to double write to both an old and new topic, in which case the transformation would be applied in the source producer. The consumer can decide to apply the transformations on the client side, by double-deploying the consumer to have one group read from only the legacy topic, and the other group reading from only the new topic. Lastly, transformations can be applied in Kafka, again with a stream processing framework of some sort. Some of these solutions, such as consumer-side transformations, will involve more coordination than others, but they're all doable.

## Tools in this area

There have been some developments in this area. We hosted a [meetup](https://www.meetup.com/WePay-Engineering-Meetup/events/248205670/) at [WePay](https://wepay.com) earlier this year, where [Carl Steinbach](https://twitter.com/cwsteinbach) discussed [Dali](https://engineering.linkedin.com/blog/topic/dali) (see [video](https://www.youtube.com/watch?v=-xIai_FvcSk&t=15s)), an abstraction for managing data views in both offline and streaming environments.

I've also begun to see some discussions pop up around [dynamic data pipelines on top of Kafka connect](https://multithreaded.stitchfix.com/blog/2018/09/05/datahighway/). Systems like this could be expanded to model transformations and schema migrations as part of the pipeline as well.

The bad news is that there don't seem to be any existing platforms or frameworks to manage this problem easily. The good news is that all of the building blocks that we need are widely available. DB schema management frameworks, single message transforms, stream processing frameworks, and schema registries all help. They just need to be integrated to solve this problem.