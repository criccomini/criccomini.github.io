---
layout: post
title:  "One big cluster, or many small ones?"
author: chris
categories: [ devops, distributed-systems ]
image: assets/images/2017-08-14-one-big-cluster-many-small-ones/john-barkiple-539580-unsplash.jpg
redirect_to:
  - https://cnr.sh/essays/one-big-cluster-many-small-ones
---

I bumped into something recently that seems to recur at every company I work for. Should we run one big cluster, or many smaller ones? The discussion is usually triggered when you have more than one team that wants to use the infrastructure in question.

{% include newsletter.html %}

The question is, should an organization run a single instance of the infrastructure, or many physically separate instances (sometimes called federation, though it’s an overloaded term). This question holds true for both clustered solutions ([Kafka](https://kafka.apache.org/), [Hadoop](https://hadoop.apache.org/), [Cassandra](https://cassandra.apache.org/), etc.) and more traditional single node infrastructure ([MySQL](https://www.mysql.com/), [Postgres](https://www.postgresql.org/), etc.).

My most recent foray into the discussion centered around MySQL deployments, but I’ve seen the same discussion play out for Hadoop, Kafka, and some other internal database stuff when I was at LinkedIn.

People sometimes feel pretty strongly about the right approach. In the end, as usual, it’s a trade off, and the right answer is dependent on a lot of variables. That said, you should consider at least the following when thinking through this problem:

* Isolation
* Security
* Scalability
* Migration
* Automation
* Deployment heterogeneity
* SLAs
* Workload
* Cost
* Conway’s law
* Multi-region

Let’s take a look at these.

## Isolation

How comfortable are you with one user affecting another user on the system? Isolation can include data isolation, package isolation, query isolation, CPU isolation, network isolation, and a lot more. I’m going to split isolation into several categories: performance, security, and deployment.

### Performance

Some systems provide very robust isolation when it comes to performance. This makes it much easier for teams to share resources, as you can cap the amount of disk, CPU, memory, and network (or slot usage, if in a cluster) that’s being used. Other systems have very little support in this area. You might find yourself boxed into having to deploy many clusters to provide the necessary performance isolation that you need.

### Security

Consider whether it’s safe for workloads to have access to each other’s resources (data, cpu, network, filesystem, etc). This is everything from the file system, to the network, to memory. Even if access is restricted, is it might not be acceptable to run on the same physical machine.

There might also be hard-requirements on network isolation. [PCI DSS](https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard) is a common example where you’re forced to segment networks, and keep infrastructure as separate as possible.

### Deployment

Deployment isolation includes the kinds of things a user needs to run their workload. Do they need GPUs attached? Do they need scipy, numpy, nltk, or fortran installed? If your running in a shared cluster, are you installing this stuff on every machine? Are you going to have a subset of machines with the required resources, and use tagging or queues to force jobs on to specific nodes. Can you share these nodes with other teams if they’re not being used at a given moment? It’s important to think through each team’s requirements, as well as what the infrastructure itself can support.

What about package deployment? I need version 7 of some package, but some other team needs version 11. They’re API incompatible. Are we running on the same classpath? Are the packages installed system-wide? I want Python 3, but someone else wants Python 2. [Docker](https://www.docker.com/) is definitely helping in this area, but it’s still something to consider.

## Scalability

If your infrastructure isn’t going to scale horizontally, you can shard vertically, but eventually you’re going to bump up against hard limits. This is going to force you to split things up. On the flip side, if the infrastructure in question scales out, running a single shared deployment becomes a real possibility.

## Migration

How easy is it to migrate from a single cluster to many, or vice-versa. Is it easy to shift one user off to their own system if they begin causing problems? Is it easy to shift many users into a single system if it begins to cost too much? Discussing how migration works can also help lessen the importance of a one vs. many discussion: if it’s easy to migrate users, starting one way doesn’t mean you’re stuck that way forever if you change your mind.

## Automation

If it’s difficult to automate the deployment and operation of a system, the fewer the better. Deploying a separate cluster manually can be a painstaking process, and is probably going to be unacceptable. If it’s going to be difficult to automate, the fewer clusters the better, usually.

Early on in Kafka’s development, deployment automation was quite complicated. Scripts had to execute a “clean shutdown” for a broker, and coordinate deployments so that only one or two nodes were offline at a time. Partition location also had to be taken into account to prevent partitions from going offline. This is heavy duty stuff, and needs to be fully automated. Doing this kind of work manually, or on dozens of different clusters is usually not acceptable.

## SLAs

Some teams might have workloads that are mission critical. If the infrastructure they need is down, someone’s getting paged at 3 a.m. Other teams might have workloads where it is acceptable to have an hour or more of downtime. Putting these workloads on the same cluster can cause the [SLAs](https://en.wikipedia.org/wiki/Service-level_agreement) between the two workloads to bleed together. The smaller the footprint of mission critical infrastructure, the better.

## Cost

Running many smaller clusters often leads to less utilization. Since resources aren’t shared, systems tend to sit idle more often. Systems like [Mesos](https://mesos.apache.org/) and [Kubernetes](https://kubernetes.io/) are helping in this area, as are cloud hosted systems that can be turned on and off as needed.

Software licensing is also something to consider. The more machines and the less utilization, the more expensive licensing can get under some structures.

## Conway’s law

As unfortunate as it is, sometimes you have to think about team and organization structure. It’s common, for example, to deploy [Airflow](https://github.com/apache/incubator-airflow/) with a 1:1 mapping to teams; one for the data science team, one for the profile team, etc. Sometimes this is for organization reasons (different ops teams, for example). Sometimes it’s a reflection of different requirements for SLAs, workload, hardware, and so on.

## Multi-region

Are you running your company out of multiple regions? Does the system support multi-regional deployments? Is the latency acceptable when replicating between regions? You might be forced into one deployment per-region depending on requirements.

## Middle ground

In the end, the right solution is usually somewhere in the middle. It’s rare to truly have just one cluster. Usually, you at least end up with a production and non-production cluster. Then maybe you split by region or SLA, or something. It’s also rare to truly have one cluster per-user, though cloud-based solutions like RDS and EMR are making that more common. The best thing to do is think things through, have an informed discussion with everybody, and be flexible.