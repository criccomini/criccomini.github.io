---
layout: post
title:  "Managing Kafka topic configuration"
author: chris
categories: [ kafka, distributed-systems ]
image: assets/images/2019-02-04-managing-kafka-topic-configuration/beatriz-perez-moya-111685-unsplash.jpg
---

The lack of tooling available for managing Kafka topic configuration has been in the back of my mind for a while. It seems like a fairly obvious need, but there doesn't appear to be much available. Unsurprisingly, I'm not the only person to recognize this need:

<center>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Even better, add a database to store topic and config info as a source of truth.<br><br>And then open source it. One of the big missing pieces is the ability to manage SoT information across multiple clusters.</p>&mdash; Todd Palino ツ (@bonkoif) <a href="https://twitter.com/bonkoif/status/1090784183025364992?ref_src=twsrc%5Etfw">January 31, 2019</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</center>

In this post, I'm going to take a look at Kafka's various configuration needs, and what a topic configuration management tool might look like.

{% include newsletter.html %}

Kafka is a large beast, and has a fair amount of configuration to be managed across a number of different systems. These configurations fall into quite a few categories:

* **Broker configuration**  
Ports, ZooKeeper connection, topic defaults, etc.
* **Client configuration**  
Producer and consumer timeouts, encoder/decoder, etc.
* **Topic configuration**  
Security ACLs, partition count, etc.
* **Schema configuration**  
Key/value schema, compatibility level, partition key, etc.

Now, some observations. First, SREs have gotten pretty good at managing server and client configuration, so I don't think it's worth spending a lot of time here. Tools like [Salt](https://www.saltstack.com/), [Ansible](https://www.ansible.com/), [Puppet](https://puppet.com/), [Chef](https://www.chef.io/), [Terraform](https://www.terraform.io/) and others can all help get a server or client off the ground with the appropriate configuration.

I also deliberately left out a bunch of the surrounding ecosystem. [REST proxy](https://docs.confluent.io/current/kafka-rest/docs/index.html) and [schema registry](https://docs.confluent.io/current/schema-registry/docs/index.html) need some configuration, but they look fairly similar to the way you'd handle broker configuration. [Kafka connect](https://docs.confluent.io/current/connect/index.html), on the other hand, is a fairly unique system that [requires some thought](https://multithreaded.stitchfix.com/blog/2018/09/05/datahighway/) when it comes to configuration. I'm leaving that aside, as I think it's worth of its own post.

This leaves us with topic and schema configuration, which is where I want to focus. I believe the best place to start for ideas is to take a look at the needs of a traditional RDBMS:

* **DB server configuration**  
Folder paths, timeouts, packet sizes, etc.
* **DB client configuration**  
Timeouts, user/password, etc.
* **DDL**  
Table schema, partitioning, indexing, etc.
* **DML**  
INSERT, UPDATE, DELETE

The Kafka configuration use cases map pretty clearly to the RDBMS space. The server and client configurations are 1:1. Kafka's topic and schema management stuff maps to DDL. Interestingly, looking at RDBMS, something non-obvious gets exposed: the idea of running DML migrations to insert/delete specific messages.

The best place to look is how traditional databases manage DDL and DML. The space is rich with tooling to solve these issues. A few examples are [Liquibase](https://www.liquibase.org/), [Flyway](https://flywaydb.org/), and [Alembic](https://alembic.sqlalchemy.org/en/latest/). There are a lot more, but they tend to look fairly similar. These tools usually comprise:

* A language for defining schema and configuration (SQL, YAML, XML, JSON, etc).
* A file structure to define a sequence of migrations that are run one after the next. Usually, this is just a list of files with checksums or ID numbers to identify and order them.
* A persistence mechanism for tracking which migrations have already been run on a DB (usually stored in a table).
* A set of tools to execute migrations, check status, roll back, etc.

Borrowing these ideas and mapping them into the Kafka space would work fairly well. The schema language would just be Avro (or whatever serialization format you're using). The configs can be defined using the key/value pairs that Kafka already defines as part of its configuration. All of this could be stored in a file structure that orders changes. Lastly, a topic could be use for persistence to track the migrations that have already executed, and a set of CLI tools very similar to those in Liquibase or Flyway could be written to run the commands. The tools could speak to the brokers via the [AdminClient](https://kafka.apache.org/20/javadoc/index.html?org/apache/kafka/clients/admin/AdminClient.html) or directly to the schema registry as needed.

Topic partition assignments could even be managed this way. When a topic is created, partition assignments can be set. Future partition migrations could happen via configuration changes that are tracked in [VCS](https://en.wikipedia.org/wiki/Version_control) and executed in the tool.

It would also be interesting to support DML-like features such as inserting or deleting messages into specific topics. I've seen this need several times, and it usually ends with SREs running a one-off script, or using the [kafka-console-producer.sh](https://kafka.apache.org/quickstart#quickstart_send) to get messages where they need to be. Having these changes revision controlled and tracked as part of the topic's configuration would be quite useful.

Most companies seem to solve these problems in house, and I haven't seen much tooling make its way into the open source ecosystem. If you're aware of any, please let me know. If not, perhaps this post will inspire a new tool set for Kafka topic configuration management.

## Update

Some great conversation popped up on Twitter. Here a list of tools that exist in this area:

* [Stream Registry](https://homeaway.github.io/stream-registry/)
* [Kafka Security Manager](https://github.com/simplesteph/kafka-security-manager)
* [Kafkawize](https://github.com/kafkawize/kafkawize)
* [Terraform Kafka Provider](https://github.com/Mongey/terraform-provider-kafka#kafka_topic)