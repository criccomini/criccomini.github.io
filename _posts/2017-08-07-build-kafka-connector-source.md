---
layout: post
title:  "So, you want to build a Kafka Connector? Source edition."
author: chris
categories: [ kafka ]
image: assets/images/2017-08-07-build-kafka-connector-source/rawpixel-1061399-unsplash.jpg
---

I've been [talking](https://github.com/datamountaineer/stream-reactor/issues/162) to some of the folks at [Data Mountaineer](https://datamountaineer.com/) about their new [Cassandra CDC connector](http://docs.datamountaineer.com/en/latest/cassandra-cdc.html) for [Kafka connect](http://docs.confluent.io/current/connect/intro.html), and I wanted to record some of the nuances that developers should consider when building out a new Kafka connect [source connector](http://docs.confluent.io/3.3.0/connect/javadocs/index.html?org/apache/kafka/connect/source/SourceConnector.html). I'm primarily focusing on source connectors where the upstream source is some kind of database.

{% include newsletter.html %}

## To poll or not to poll

The most basic architectural decision to make is whether the source connector is going to be periodically polling the upstream system using a traditional read mechanism (running `SELECT * FROM...` every 60 seconds) or whether some replication protocol is going to be used ([MySQL binary log](https://dev.mysql.com/doc/refman/5.7/en/binary-log.html), [Cassandra CDC](https://cassandra.apache.org/doc/latest/operating/cdc.html), [MongoDB op_log](https://docs.mongodb.com/manual/core/replica-set-oplog/), etc.). There are some trade-offs between these two approaches, but in general, the replication-based connectors are going to be much more robust for a number of reasons:

1. They can handle [hard deletes](https://www.quora.com/What-is-the-difference-between-soft-delete-and-hard-delete-in-SQL-Informatica-power-center-and-Informatica-cloud).
2. You get to see all updates to a row, not just the the state of the row at each polling interval.
3. They impose fewer schema requirements than polling solutions. Usually, no modify time columns or indices are required.
4. They're more performant, as they're not constantly running queries on the DB.
5. They're lower latency. You usually get updates nearly immediately when they occur, as opposed to having to wait for polling intervals.

Still, there are some upsides to the polling based solutions:

1. They are usually easier to implement.
2. They don't require that the database have exotic replication features. As long as you can read and sort data, polling should work. Not all databases even expose a replication protocol for external use.
3. They can be easier to deploy. Some databases require plugins or daemons to be running on the same machine as the database nodes in order to tap into replication or CDC features. Postgres requires that you build a [server-side C plugin](http://debezium.io/docs/connectors/postgresql/#output-plugin) in order for connectors to tap into its feed. The Cassandra CDC implementation from Data Mountaineers requires running Kafka connect workers on the same nodes as Cassandra, itself.
4. You have to worry less about consistency issues with distributed databases. If you tap into the raw replication feeds, such as Cassandra's CDC files, you might end up exposing duplicate rows, or raw data that downstream consumers will have to de-duplicate or parse.
5. It is easier to snapshot old data. (See below.)

## Oh, you want all the data?

A commonly overlooked feature that's a must-have in most production systems is the ability to snapshot (or bootstrap) data that already exists on the database. This seems obvious, but most implementations I've come across don't consider this at first.

In the case of poll-based solutions, it's fairly straight forward to incrementally load data starting from row zero, but in the case of replication-based solutions, replication feeds do not always expose the ability to start from row zero and load all data going forward.

Debezium, for example, implements a [mysqldump-like](https://issues.jboss.org/browse/DBZ-31) solution for snapshotting the initial data in MySQL. Once the snapshot is done, it flips over to the MySQL binary log. This is necessary because MySQL binary logs do not usually contain an exhaustive list of all modifications for all time; they get truncated like Kafka topics. Doing this dance between snapshot mode and replication mode can be tricky to get right.

Supporting this feature is helpful for end-users because otherwise you only get data going forward. For log-based tables, that might be fine, but for most primary data stores (e.g. users, groups, payment methods, etc.) you generally want all the data in the upstream tables, not just new data.

*Aside: Yelp! Engineering had an interesting snapshot pattern that they discuss in [Streaming MySQL tables in real-time to Kafka](https://engineeringblog.yelp.com/2016/08/streaming-mysql-tables-in-real-time-to-kafka.html). The pattern amounts to making a temporary copy of a table into a [blackhole](https://dev.mysql.com/doc/refman/5.7/en/blackhole-storage-engine.html) storage engine, so they can force all data into the replication feed (binary log, in their case), rather than having two separate implementations for snapshotting versus ongoing replication.*

## Keys, please

Another non-obvious requirement is defining the message keys that are to be persisted into Kafka such that they will work with Kafka's [log compacted](https://kafka.apache.org/documentation/#compaction) topics, and that they will preserve ordering.

### Compaction

When replicating primary data from a database, it makes a lot of sense to have Kafka compact and remove older updates for a given record after some time. This prevents the log from growing too large, yet still gives you the ability to read all of the current data directly from Kafka, rather than having to snapshot data from the source system because it's fallen off the edge of a Kafka's topic's time retention.

An example helps illustrate the usefulness of this feature. If I have an *orders* table with a primary key and a title field, and a given row has:

* INSERT orders (id, title) values (1, "foo")
* UPDATE orders (id, title) values (1, "bar")
* UPDATE orders (id, title) values (1, "baz")

The Kafka topic will likely end up with three messages for this row, one with the value of *foo*, one with *bar*, and one with *baz*. Most users really only care about the most recent value for a given row, and if you're using log compaction, you can have Kafka delete the older messages, such that only the *baz* message remains. In order for this to work, though, the BYTE values for the keys of all three messages must be identical, otherwise Kafka won't be able to tell that the three messages correspond to the same row.

The implication that all keys for a given row must have the exact same byte value is that you can't include any dynamic data in the key. You can't include timestamps, mutation type (INSERT, UPDATE, DELETE), hostname, etc. You should generally keep the key as stripped down as possible, and include everything in the value payload.

A second, perhaps non-obvious, requirement is that the row's primary key be included in the key payload. This is ultimately the field that is going to differentiate one row from another within log compacted topics.

### Partitioning

The second thing to pay attention to with keys is that messages for the same row must be sent to the same partition by the same producer (a connect task, in this case). This is the only way to guarantee that the mutations are seen in order by downstream consumers.

The requirement isn't quite as heavy as the identical-byte one imposed by compaction since you are theoretically able to provide custom partitioners that could, for example, pay attention only to the "id" field in the key. In practice, however, you want stuff to work out of the box with the standard Kafka partitioner, which is going to require that the keys are [hash and mod](https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/clients/producer/internals/DefaultPartitioner.java#L69) correctly.

## Modeling deletes

If your source is feeding off of a traditional database that supports hard deletes (i.e. removing a row from the database), you'll have to figure out how your connector handles this. There are three common options:

* Send a message where the value denotes what was deleted
* Send a message where the value is null
* Don't handle them

Keep in mind that the key for the messages being sent to Kafka should still contain the necessary information to identify the affected row (its primary key).

The nice thing about the first option, where the value includes what was deleted, is that you have the necessary state to see what's changed without querying an outside store — you can see all the row data that's been deleted. The advantage of the second approach (null value) is that it works with log compaction. Kafka will eventually compact out the record, which keeps the topic size manageable.

Note that these two options are not mutually exclusive. In fact, Debezium [first sends a soft delete message, and then follows up with a hard delete](https://issues.jboss.org/browse/DBZ-45) message immediately after. This way, consumers can see what was affected, but Kafka will still compact out the deleted rows.

The last option, ignoring deletes, is what most polling-based solutions implement. If a row has been deleted, there's usually no way for the connector to see it since a polling connector is just retrieving recently modified rows.

## You get a schema!

You need to think through how you map your source database's schemas to the Kafka connect schema types. This is not as easy as it sounds. For example, what's the [right way to handle an UNSIGNED BIGINT](https://issues.jboss.org/browse/DBZ-228)? What if binary values are [not padded properly](https://issues.jboss.org/browse/DBZ-254)? Debezium came across a number of these issues both in their Postgres and MySQL implementations. You also need to pay special attention to logical types. There are [Avro logical types](https://avro.apache.org/docs/1.8.0/spec.html#Logical+Types), [Kafka connect logical types](https://issues.apache.org/jira/browse/KAFKA-2476), and even [connector-level logical types](http://debezium.io/docs/connectors/mysql/#data-types). Understanding what logical types are and how they're used is a must.

### Schema registry

Special attention also needs to be paid to how you mutate your messages' schemas over time. You have to assume that some of your users will also be using Avro and Confluent's schema registry. Some of them will be running the registry with [compatibility checks enabled](http://docs.confluent.io/current/schema-registry/docs/api.html#id1). It's imperative that fields not be added and removed from the messages for a topic in an incompatible way to make your users' life easier. Some of this burden also falls on the user, as they'd be tying the mutation of their upstream DB and table schemas to their downstream Kafka topics.

## So I downloaded this thing…

Lastly, a lot of help needs to be given on how to operate the connector. This goes beyond just how to configure and deploy the connector itself. Often times, the proper way to run these connectors will require deploying a replica cluster or special set of nodes for the upstream database.

At WePay we run a [separate MySQL replica cluster](https://wecode.wepay.com/posts/streaming-databases-in-realtime-with-mysql-debezium-kafka#architecture) for Debezium to feed off of. This has a number of benefits including isolation when snapshots occur, custom configuration for the nodes (e.g. longer binary log retention), and so on. Providing guidance in this area will make your users' lives a lot easier.

Discussing patterns when running in a cloud environment can also be helpful.

## That's all folks

This is an off-the-top-of-my-head list of things to pay attention to. There are probably more, and I welcome feedback. In any case, hopefully this doesn't scare you too much, and leads to more Kafka connectors.