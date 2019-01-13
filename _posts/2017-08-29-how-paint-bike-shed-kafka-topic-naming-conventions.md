---
layout: post
title:  "How to paint a bike shed: Kafka topic naming conventions"
author: chris
categories: [ kafka ]
image: assets/images/2017-08-29-how-paint-bike-shed-kafka-topic-naming-conventions/bike-shed.jpg
---

Today, I'll be tackling the controversial subject of [Kafka](https://kafka.apache.org/) topic names. Not only will I review various schemes, but I've decided to take a stand on a few issues and outline my reasoning. Get out your brush, and let's [paint this bike shed](https://en.wiktionary.org/wiki/bikeshedding)!

{% include newsletter.html %}

There's surprisingly little guidance on the internet about Kafka topic naming conventions. A [few](https://stackoverflow.com/questions/40714764/what-should-be-naming-convention-of-topic-and-partition-of-kafka) [sparse](https://stackoverflow.com/questions/43726571/what-is-the-best-practice-for-naming-kafka-topics) Stack Overflow questions, and a [couple](http://grokbase.com/t/kafka/users/152r20xg4r/stream-naming-conventions) of [mailing list discussions](https://www.mail-archive.com/dev@samza.apache.org/msg00524.html) are all that pop up on the [first page of Google](https://www.google.com/search?q=kafka+topic+naming+convention). The opinions on the matter vary pretty widely. Some suggestions from the links above include:

* `<root name space>.<product>.<product specific hierarchy>`
* `<app type>.<app name>.<dataset name>.<stage of processing>`
* `<app type>.<dataset name>.<data>`

## Convention types

There are two types of naming conventions: structural and semantic. A good topic naming convention should define both structural and semantic guidelines.

Structural conventions define things like what kind of punctuation to use, or how to format spaces. The most basic structural convention is actually [what Kafka, itself, enforces](https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/internals/Topic.java#L75):

> Valid characters for Kafka topics are the ASCII alphanumerics, '.', '\_', and '-'

You can't escape this. You can further refine it, though, by saying that dashes are used as spaces, or all topics must be camelCase, for example.

Semantic conventions define what fields should go into a topic name, and in what order.

## Potential fields

It turns out that people get pretty creative in the conventions that they come up with. Here are a number of fields that I've seen used or proposed in naming conventions:

* **Product**  
The name of the product that the topic relates to.
* **Schema name**  
The schema name for messages in the topic. Usually corresponds to an [Avro](https://avro.apache.org/) schema name.
* **Namespace**  
Something like org.foo.bar. Usually used in conjunction with schema names.
* **Type**  
What the topic is used for. Examples: ETL, queuing, tracking, user, data push, streaming, etc.
* **Application name**  
The name of the application or service that is producing the message. This is analogous to the consumer name, except on the producer side.
* **Dataset name**  
A name that encompasses data in a collection of topics. Similar to a database name.
* **Processing stage**  
The step in the processing pipeline. Especially useful for stream processing. Examples: filtered, partitioned, joined, etc.
* **Public/private**  
Denotes whether the topic is an internal implementation detail (such as Kafka's \_\_consumer_offsets topic).
* **Security**  
Whether the topic has [AuthN/AuthZ](https://www.conjur.com/blog/2014/07/07/distinguishing-authn-and-authz) enabled.
* **Consumer name**  
The name of the consumer that is meant to consume data from a topic.
* **Partition key**  
The field name by which a topic is partitioned.
* **Partition counts**  
The number of partitions for the topic.
* **Version numbers**  
A number that can be incremented to denote a new version of a topic, such as when a backwards incompatible change is made, or a data migration occurs.
* **Owner/team name**  
The name of owner or team that's responsible for a topic.


## Don't do this

I'm going to be provocative and make some concrete recommendations.

### Don't use fields that change

My biggest advice is to avoid fields that can change over time. This includes things like team name, topic owner, service name, product name, and consumer name.

The rationale for avoiding dynamic fields is that [it's impossible to rename a topic](https://issues.apache.org/jira/browse/KAFKA-2333), and can be painstaking to migrate data to a new topic. When a service is deprecated and removed, for example, the service's name is still in the Kafka topic.

### Don't use fields if data is available elsewhere

The logic here is that if you can get the information from another source, it's best to do so; especially of that other source is actually the source of truth. Two common sources are:

* [Schema registry](http://docs.confluent.io/current/schema-registry/docs/index.html)
* [Kafka metadata](https://kafka.apache.org/protocol#The_Messages_Metadata)

The schema registry can provide you with the information about a schema for a given topic. This is true for both keys and values in the topic. It is also the source of truth for this information.

Kafka brokers provide topic metadata information that include partition count, replication number, security information, etc. Again, Kafka is the source of truth for this information.

### Don't tie topic names to consumers or producers

It's quite likely that a topic is going to have more than one consumer, and it's also possible that whoever is sending messages to a topic will change over time. It doesn't make sense to include either of these in a topic's name because it violates the dynamic field rule, above.

## Do this

So, what should you do? I've had success with a basic and flexible convention:

`<message type>.<dataset name>.<data name>`

Here, valid message type values are left up to the organization to define. Typical types include:

* **logging**  
For logging data (slf4j, syslog, etc)
* **queuing**  
For classical queuing use cases.
* **tracking**  
For tracking events such as user clicks, page views, ad views, etc.
* **etl/db**  
For ETL and [CDC](https://en.wikipedia.org/wiki/Change_data_capture) use cases such as database feeds.
* **streaming**  
For intermediate topics created by stream processing pipelines.
* **push**  
For data that's being pushed from offline (batch computation) environments into online environments.
* **user**  
For user-specific data such as scratch and test topics.

The dataset name is analogous to a database name in traditional RDBMS systems. It's used as a category to group topics together.

The data name field is analogous to a table name in traditional RDBMS systems, though it's fine to include further dotted notation if developers wish to impose their own hierarchy within the dataset namespace.

The appeal of this convention is that it's very similar to a traditional RDBMS style, so it's easy easy for developers to grok. When someone asks what to name a topic, you can always just ask them what they'd name their database/table if it were in an RDBMS, and suggest that as the dataset/data fields.

It's also extensible. If developers or organizations wish to impose their own hierarchy that makes sense for their specific use cases or message types, they can do so by adding extra dotted fields in the data name section.

As far as structure goes, I recommend using snake_case (not camelCase, UpperCamelCase, or lisp-case).

## Enforcing the rules

The most obvious way to enforce a naming convention is to disable [auto.create.topics.enable](https://kafka.apache.org/documentation/#brokerconfigs), and limit who can create topics. Those who create topics are responsible for enforcing the rules, though an automated process for topic creation that forces users to define the various fields as part of a topic's creation is preferred.

If users are allowed to create their own topics, then a script that monitors whether topics conform to expected conventions would at least raise an alert after a violation has already occurred. Unfortunately, this is probably too late.

## Conclusion

That's all I've got for now. I'm interested in knowing how other people format their topic names. Please leave a comment below, or mention me on twitter [@criccomini](https://twitter.com/criccomini).

