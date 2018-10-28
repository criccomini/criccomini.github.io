---
layout: post
title:  "Killing Subprocesses in Linux/Bash"
author: chris
categories: [ devops, distributed-systems ]
image: assets/images/2012-09-25-kill-subprocesses-linux-bash/jon-tyson-478928-unsplash.jpg
redirect_from:
  - /posts/linux/2012-09-25-kill-subprocesses-linux-bash/
---

Lately, I've been working with [YARN](http://hadoop.apache.org/docs/r0.23.0/hadoop-yarn/hadoop-yarn-site/YARN.html) at LinkedIn. This framework allows you to execute Bash scripts on one or more machines. It's used primarily for Hadoop. When using YARN, you often end up with nested Bash scripts with no parent process ID (PPID) when the NodeManager launches the Bash script. This can be pretty problematic when the NodeManager is shut down, since you must make sure to clean up all child subprocesses via your parent Bash script.

## Understanding Linux subprocesses

Let's start with an example. We'll have two shell scripts: a parent, and a child:

```
$ cat parent.sh 
#!/bin/bash
./child.sh
$ cat child.sh 
#!/bin/bash
sleep 1000
```

Normally, when you launch nested processes from a terminal, you'll see a process tree that looks something like this:

```
UID        PID  PPID  C STIME  TTY         TIME CMD
ubuntu   10911 10701  0 05:07 pts/1    00:00:00 /bin/bash ./parent.sh
ubuntu   10912 10911  0 05:07 pts/1    00:00:00 /bin/bash ./child.sh
ubuntu   10913 10912  0 05:07 pts/1    00:00:00 sleep 1000
```

In this example, a terminal (PID 10701) calls parent.sh, which calls child.sh, which calls sleep 1000. With YARN, you end up with a process tree that looks more like this:

```
UID        PID  PPID  C STIME  TTY         TIME CMD
ubuntu   10966     1  0 05:14 pts/1    00:00:00 /bin/bash ./parent.sh
ubuntu   10967 10966  0 05:14 pts/1    00:00:00 /bin/bash ./child.sh
ubuntu   10968 10967  0 05:14 pts/1    00:00:00 sleep 1000
```

Notice that the PPID of parent.sh is now 1. This is essentially a top-level process that has no parent.

## Unexpected behavior

In both of these examples, it seems intuitive that killing the top level parent would result in all of the children being cleaned up. There are a [number of ways to kill a process](http://en.wikipedia.org/wiki/Kill_(command)), so let's start with:

```
$ kill -9 10966

UID        PID  PPID  C STIME  TTY         TIME CMD
ubuntu   10966     1  0 05:14 pts/1    00:00:00 /bin/bash ./parent.sh
ubuntu   10967 10966  0 05:14 pts/1    00:00:00 /bin/bash ./child.sh
ubuntu   10968 10967  0 05:14 pts/1    00:00:00 sleep 1000
```

As expected, killing the parent does not clean up any children:

```
UID        PID  PPID  C STIME  TTY         TIME CMD
ubuntu   10967     1  0 05:14 pts/1    00:00:00 /bin/bash ./child.sh
ubuntu   10968 10967  0 05:14 pts/1    00:00:00 sleep 1000
```

Let's try sending a kill signal that's not quite as strong as kill -9. For a list of possible signals, try running:

```
$ kill -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL       5) SIGTRAP
 6) SIGABRT      7) SIGBUS       8) SIGFPE       9) SIGKILL     10) SIGUSR1
11) SIGSEGV     12) SIGUSR2     13) SIGPIPE     14) SIGALRM     15) SIGTERM
16) SIGSTKFLT   17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
21) SIGTTIN     22) SIGTTOU     23) SIGURG      24) SIGXCPU     25) SIGXFSZ
26) SIGVTALRM   27) SIGPROF     28) SIGWINCH    29) SIGIO       30) SIGPWR
31) SIGSYS      34) SIGRTMIN    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3
38) SIGRTMIN+4  39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12 47) SIGRTMIN+13
48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14 51) SIGRTMAX-13 52) SIGRTMAX-12
53) SIGRTMAX-11 54) SIGRTMAX-10 55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7
58) SIGRTMAX-6  59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
63) SIGRTMAX-1  64) SIGRTMAX
```

Now, let's try this again with a normal [SIGHUP](http://en.wikipedia.org/wiki/SIGHUP) kill. One might expect that sending such a soft kill signal should result in the child processes being cleaned up.

```
$ kill -SIGHUP 10967

UID        PID  PPID  C STIME  TTY         TIME CMD
ubuntu   10968     1  0 05:14 pts/1    00:00:00 sleep 1000
```

As you can see, even SIGHUP does not kill the child processes; it leaves the sleep call orphaned with a PPID of 1.

So, how can we do this properly?

## Traps

One solution is to [use traps](http://stackoverflow.com/questions/2525855/how-to-propagate-a-signal-through-an-arborescence-of-scripts-bash) in the Bash script. A trap is a way to say "do this before exiting" in a Bash script. For example, we might add the following line to parent.sh and child.sh:

```
trap 'kill $(jobs -p)' EXIT
```

Now, if we kill the parent, all children will be cleaned up! Obviously, this only works with softer kill signals, such as SIGHUP. For example, if we have this process tree:

```
UID        PID  PPID  C STIME  TTY         TIME CMD
ubuntu   11049 10758  0 05:31 pts/2    00:00:00 /bin/bash ./parent.sh
ubuntu   11050 11049  0 05:31 pts/2    00:00:00 /bin/bash ./child.sh
ubuntu   11051 11050  0 05:31 pts/2    00:00:00 sleep 1000
```

You can execute:

```
$ kill 11049
$ ps -ef | grep sleep
```

And you will see that sleep is no longer running!

## Top-level trap

A variation of having a trap in each Bash file is to have a single top-level trap that uses 'ps' to find children:

```bash
kill_child_processes() {
    isTopmost=$1
    curPid=$2
    childPids=`ps -o pid --no-headers --ppid ${curPid}`
    for childPid in $childPids
    do
        kill_child_processes 0 $childPid
    done
    if [ $isTopmost -eq 0 ]; then
        kill -9 $curPid 2> /dev/null
    fi
}

# Ctrl-C trap. Catches INT signal
trap "kill_child_processes 1 $$; exit 0" INT
```

This is a less than ideal solution, but it does work. For details, see [this page](http://stas-blogspot.blogspot.com/2010/02/kill-all-child-processes-from-shell.html).

## Kill PPIDs

Running traps everywhere can be kind of clunky, and error prone. A cleaner approach is to use the kill command, and provide a parent process ID (PPID) instead of a process ID. To do this, the syntax gets funky. You use a negative of the parent process ID, like so:

```
$ kill -- -<PPID>
```

For example, with this process tree:

```
UID        PID  PPID  C STIME  TTY         TIME CMD
ubuntu   11096     1  0 05:36 ?        00:00:00 /bin/bash ./parent.sh
ubuntu   11097 11096  0 05:36 ?        00:00:00 /bin/bash ./child.sh
ubuntu   11098 11097  0 05:36 ?        00:00:00 sleep 1000
```

You would run:

```
$ kill -- -11096
$ ps -ef | grep sleep
```

As you can see, killing with a PPID automatically cleans all subprocesses, including nested subprocesses!

## exec

Another handy trick is to use [exec](http://linux.die.net/man/3/exec) when nesting Bash calls. Exec replaces the "current" process with the "child" process. This doesn't always work, but for our example (parent, child, sleep), it certainly does. Let's make parent and child look like this, respectively:

```
$ cat parent.sh
#!/bin/bash
exec ./child.sh
$ cat child.sh
#!/bin/bash
exec sleep 1000
```

Notice the "exec" command preceding the child.sh and sleep calls. Let's have a look at the process tree:

```
$ ps -ef | grep parent
$ ps -ef | grep child
$ ps -ef | grep sleep
ubuntu   11155 10758  0 05:41 pts/2    00:00:00 sleep 1000
```

As you can see, only a 'sleep' process exists. The parent.sh script "becomes" child.sh, and child.sh "becomes" sleep. This makes it very easy to clean up child processes, because there are none! To clean up, you simply kill the 'sleep' process. This is the method that I use with YARN, since I'm executing nested Bash calls that lead to a single Java process.

## Python

If you're not strictly tied to Bash, you might be interested in Python's [psutil](http://code.google.com/p/psutil/) library. It [can be used to kill all subprocess](http://stackoverflow.com/questions/1230669/subprocess-deleting-child-processes-in-windows) for a given process ID.

## setsid

One other minor note. You might be wondering how you end up with a PPID of 1. Obviously, kill -9'ing will do it. You can also use a command called [setsid](http://linux.die.net/man/2/setsid). This is what YARN does when its NodeManager executes a child process. To try and execute parent.sh with a PPID of 1, execute:

```
setsid ./parent.sh
```

For further reading, check the [nohup](http://en.wikipedia.org/wiki/Nohup) wiki, which can be used as an alternative to setsid.
