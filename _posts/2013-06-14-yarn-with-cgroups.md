---
layout: post
title:  "Using YARN with Cgroups"
author: chris
image: assets/images/2013-06-14-yarn-with-cgroups/terra-evans-721293-unsplash.jpg
redirect_from:
  - /posts/hadoop/2013-06-14-yarn-with-cgroups/
---

I'm still a novice with Cgroups, but I thought it would be worth documenting how to set YARN up with them, since there seems to be a surprising lack of documentation on how to get this stuff going. I'm going to show you how to:

* Check if Cgroups is installed on your machine
* Configure YARN to run use Cgroups

Note that this tutorial is written based on a RHEL 6 environment. You won't be able to use the CGroup features unless you're on Linux.

## What are Cgroups?

Cgroups are a Linux kernel module that allow you to control resource usage (CPU, disk, etc) at a per-process level, to provide performance guarantees when running in a shared environment.

The two best places to get a high level view of Cgroups are:

* [https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt](https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt)
* [Red Hat Enterprise Linux 6 Resource Management Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Resource_Management_Guide/Red_Hat_Enterprise_Linux-6-Resource_Management_Guide-en-US.pdf)
* [https://wiki.archlinux.org/index.php/Cgroups](https://wiki.archlinux.org/index.php/Cgroups)
* [http://en.wikipedia.org/wiki/Cgroups](http://en.wikipedia.org/wiki/Cgroups)

*You should definitely read the first two documents, which are the kernel documentation, and RHEL 6 documentation for Cgroups. The remainder of the post assumes you've read these documents.*

Currently (as of 2.0.5-alpha), YARN only supports Cgroups CPU isolation (using a property called cpu.shares, which I'll get into later). There are future plans to add more features to the CPU isolation (in 2.1.0-beta; [YARN-610](https://issues.apache.org/jira/browse/YARN-600), [YARN-799](https://issues.apache.org/jira/browse/YARN-799), [YARN-810](https://issues.apache.org/jira/browse/YARN-810)), and also support other resources, such as disk, and network.

## Setting up Cgroups

Cgroups is fairly OS-specific, so you'll need to do research into whether your particular OS and Kernel have Cgroups setup and installed. For this tutorial, I used RHEL 6 with the following kernel:

<script src="https://gist.github.com/5784586.js"> </script>

Ubuntu also has Cgroup support rolled into it (See [Docker](http://www.docker.io/)). You can verify whether Cgroups is installed by checking if /proc/cgroups exists.

<script src="https://gist.github.com/5784621.js"> </script>

Another way to check if Cgroups exist is by looking for the mount point where Cgroups end up. In [RHEL 6](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Resource_Management_Guide/Red_Hat_Enterprise_Linux-6-Resource_Management_Guide-en-US.pdf), this defaults to /cgroup. The mount point might also be in /sys/fs/cgroup on other setups.

You'll probably also want to install libcgroup, which comes with some handy tools (as mentioned in the RHEL 6 documents, linked above).

<script src="https://gist.github.com/5784697.js"> </script>

Finally, you'll want to setup a CPU directory inside the Cgroup root folder (if one doesn't already exist), so YARN can use it to mount its CPU hierarchies.

<script src="https://gist.github.com/5784740.js"> </script>

Once you've established that Cgroups is installed (or installed it), and configured the CPU directory, it's time to setup YARN's NM and RM to use it.

## Setting up YARN with Cgroups

To use YARN with CGroups, all you really need to do is configure it to use the LinuxContainerExecutor (LCE), instead of the DefaultContainerExecutor, that ships with it out of the box. Once you configure the LCE, you just need to flip a few switches to get the LCE using Cgroups.

*To setup LCE for YARN, start by reading [Hadoop MapReduce Next Generation - Cluster Setup](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/ClusterSetup.html).*

In your yarn-site.xml, you need to add the following configurations:

<script src="https://gist.github.com/5784750.js"> </script>

Make sure to set the last configuration value according to the group that your YARN users will run under (e.g. hadoop). 

You'll probably also want to configure the YARN NM to support more than one virtual core. By default, the NM only allows one virtual core to be used.

<script src="https://gist.github.com/5784838.js"> </script>

All this is doing is mapping some number of virtual cores to your machine's physical cores. This is useful because it lets you run different kinds of machines in the same YARN cluster (e.g. some with CPUs that are 2x as fast as others), and still have a standard "core" that developers can use to reason about how much CPU they need.

Setup your container-executor, and container-executor.cfg file (see the [ClusterSetup](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/ClusterSetup.html) link for details):

<script src="https://gist.github.com/5785070.js"> </script>

Finally, if you're running YARN 2.0.5-beta, or prior, you'll need to patch your hadoop-yarn-server-nodemanager-2.0.5-alpha.jar with [YARN-600](https://issues.apache.org/jira/browse/YARN-600), which actually updates cpu.shares with the proper percentage.

Now, when you turn on the YARN RM and NM, your jobs can use Cgroups!

<script src="https://gist.github.com/5784890.js"> </script>

## Example

By default, containers will use one virtual core, which means that they'll all get /cgroup/cpu/hadoop-yarn/container_id/cpu.shares set to 1024. You can experiment with these files pretty easily, and see how Cgroups works.

Start a single YARN container. Make the code in this containers just spin to waste CPU. I was having my containers hash random strings in a loop.

<script src="https://gist.github.com/5784924.js"> </script>

When you run `top`, you should see that the process is using nearly 100% of a single core. This might be surprising to you if you're running more than one virtual core per physical core. For example, if you had a pcore:vcore ratio of 1:2, wouldn't you expect a single container to get at most 50% of a core? As it turns out, Cgroups defaults to being optimistic. It lets you use as much CPU is available, and only begins throttling things back when the CPU is 100% utilized. Have a look at this [RFC](http://lwn.net/Articles/336127) for details. This can be changed using Linux's completely fair scheduler (see [YARN-810](https://issues.apache.org/jira/browse/YARN-810)).

To continue the test, run 1 more container than you have cores on your machine (in this example, my machine has 8 cores, so I run a total of 9 containers). When you run `top`, you should see that all processes are fighting for CPU with roughly the same CPU usage for each process.

To activate Cgroups manually, run this command for one of your containers:

<script src="https://gist.github.com/5784941.js"> </script>

What we've just done is assign a very small fraction of the total CPU available to the YARN NM (10 / (10 + 8 * 1024) = .1%) to container_1371055675984_0001_01_000002.

If you run `top`, you should now see something like this:

<script src="https://gist.github.com/5784993.js"> </script>

As you can see, the CPU usage for PID 16708 is at 2.3%, while all of the others are maxing out near 100%! If you were to set the cpu.shares back to 1024, you'd see that the process once again gets its fair share.

## CGroups in Code

Now that we've shown that Cgroups can work manually, you'll probably want to update your YARN code to actually use them. This part is pretty trivial. You just need to call the setVirtualCores method on the [Resource](http://hadoop.apache.org/docs/current/api/org/apache/hadoop/yarn/api/records/Resource.html) class when making container resource requests in YARN.

Make sure that whatever you request is within the minimum and maximum vcore boundaries defined in [yarn-default.xml](http://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-common/yarn-default.xml).

## Bumps in the Road

Here are some problems that I encountered, along the way.

* YARN was not updating cpu.shares. This is fixed in YARN-600.
* Invalid argument exception when AM starts up. This is triggered by the container-executor, and is fixed in YARN-799.
* YARN AM was failing to localize. This is because the usercache directory that YARN uses was owned by the YARN NM username. When switching to LCE, that directory must be owned by the user running the job. Deleting usercache entirely and restarting the YARN NMs solved the problem.
* YARN ignoring my container-executor.cfg file. It turns out that, by default, container-executor is hard-coded to use ../etc/hadoop/container-executor.cfg. If you want to put your container-executor elsewhere, you'll need to re-build container executor.

<script src="https://gist.github.com/5785113.js"> </script>

When running the code initially, I was getting an "invalid argument" error when my YARN AM started. This turns out to be triggered when YARN tries to write to /cgroup/cpu/hadoop-yarn/container_id/cgroup.procs. This file was initially read-only, and only recently, in the Linux kernel, has it become read-write. There is a Jira open (YARN-799) to resolve this.
