---
layout: post
title:  "Kafka Consumer Memory Tuning"
author: chris
categories: [ distributed-systems, kafka ]
image: assets/images/2012-10-05-kafka-consumer-memory-tuning/rawpixel-741689-unsplash.jpg
redirect_from:
  - /posts/kafka/2012-10-05-kafka-consumer-memory-tuning/
---

Yesterday, I had a process that was consuming a single Kafka topic. I was running it in our "staging" environment, and everything worked great. My heap space for the process was set to 512 megabytes (`-Xmx512M`). When I moved this process to production, my process would fail with an out of memory exception. I was seeing:

```
java.lang.OutOfMemoryError: Java heap space
BoundedByteBufferReceive [ERROR] OOME with size 4800026
java.lang.OutOfMemoryError: GC overhead limit exceeded
FetcherRunnable [ERROR] error in FetcherRunnable
```

Let's review what happened, and how to fix it.

***WARNING: This is for the legacy Java Kafka consumer.***

##  Buffers

When you create a Kafka consumer, you first instantiate a Kafka connector ([ConsumerConnector.scala](https://github.com/kafka-dev/kafka/blob/master/core/src/main/scala/kafka/consumer/ConsumerConnector.scala)). Then, you create multiple threads that feed off of one or more topics:

```java
// create 4 partitions of the stream for topic "test", to allow 4 threads to consume
Map<String, List<KafkaStream<Message>>> topicMessageStreams = 
    consumerConnector.createMessageStreams(ImmutableMap.of("test", 4));
List<KafkaStream<Message>> streams = topicMessageStreams.get("test");
```

Internally, Kafka creates a buffer for each thread attached to the ConsumerConnector. In this case, there are four threads, and therefore four buffers. These buffers, which are queues, are populated asynchronously until they are "full". When your code reads from a stream, Kafka dequeues from the stream/thread's queue, and gives you a message. 

{% include newsletter.html %}

##  Tuning memory usage

Two important questions arise from this:

* When are the queues full?
* What are the queues populated with?

A queue is full when it reaches the configured maximum queue size (queuedchunks.max). That is, if queuedchunks.max=10, then the queue will be full when 10 objects are in it.

This leads me to question number two: What are these objects that the queue is populated with? It turns out, *they are not messages*. Instead, they are fetched byte buffers that contain *multiple messages*. The size of these byte buffers is determined by the configuration parameter: fetch.size.

So, to calculate how much memory your consumer is going to take, you have to use this formula:

```
(number of consumer threads) * (queuedchunks.max) * (fetch.size)
```

For example, if you have 24 threads, a max queue size of 10, and a fetch.size of 1.2 megabytes, your consumer is going to take 288 megabytes of heap space (24 threads * 10 fetches * 1.2 megabytes/fetch) if all queues are full.

If you run out of space, you have a few options: increase heap space, reduce your consumer threads, or lower your fetch size or max queue size. Obviously, different tunings have different affects on your throughput. With fewer buffers, or fewer fetches per queue, you might negatively impact your throughput.

##  What happened to my process?

The number of threads in my process was dependent on how many partitions the topic had that I was consuming from. When I moved from staging to production, the Kafka cluster I was consuming from had far more brokers, and far more partitions per topic. As a result, the memory footprint of my process drastically changed. I went from 22 threads to 32, which changed my heap usage from 264 megabytes to 384 megabytes. This was enough to set my process' total memory usage over 512 megabytes, which caused the out of memory exceptions.