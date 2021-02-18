---
layout: post
title:  "Research in cell, animal, and human software simulation can speed up experimentation"
author: chris
categories: [ machine-learning ]
image: assets/images/2019-01-15-research-cell-animal-human-software-simulation-speed-up-experimentation/louis-reed-747388-unsplash.jpg
redirect_to:
  - https://cnr.sh/essays/research-cell-animal-human-software-simulation-speed-up-experimentation
---

I recently came across a [Wired story about Jim Allison](https://www.wired.com/story/meet-jim-allison-the-texan-who-just-won-a-nobel-cancer-breakthrough/), a Nobel Prize winning researcher in cancer immunotherapy. The story is a long form piece that's half character study, and half high-level biology. The article sparked my interest. Specifically, how engineering might be able to accelerate the way in which medical research is conducted.

{% include newsletter.html %}

Last week, I interviewed an engineering candidate that was very focused on how quickly we ship our software. Specifically, how long it took to get a piece of code to production once it'd been written. This is a common area of concern in software engineering. We, as an industry, have spent a lot of time improving the iteration speed. In fact, most of modern [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration) and [deployment](https://en.wikipedia.org/wiki/Continuous_deployment) methods are designed to help accelerate the feedback loop between a change and the outcome of the change. We're at the point where waiting even hours can seem like an eternity.

Contrast this with the Wired article. Descriptions of multi-month experiments and random ideas abound. It seems some pivotal parts of Dr. Allison's discoveries happened almost by accident, or over long and arduous periods of time. I'm by no means trying to denigrate the work; I'm wondering aloud how things would look if we pointed software at some of these problems.

Naively, there seem to be (at least) three areas where software could play a major role:

* Gathering data
* Narrowing the search space of potential experiments to run
* Running the experiments

There are surely more areas, too. I'm just at the beginning of trying to understand the state of the art, but I'm very excited about what I've come across so far. I left a post on Twitter, and got an interesting set of responses:

<center>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Is any research going into cell, animal, or even human software simulation to speed up (or replace) experiments?<br><br>After reading about Jim Allison’s work on immunotherapy in Cancer, it seems like speeding up iteration when testing medical hypothesis would be a game changer.</p>&mdash; Chris Riccomini (@criccomini) <a href="https://twitter.com/criccomini/status/1080698158450016257?ref_src=twsrc%5Etfw">January 3, 2019</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</center>

Some things that I'm looking at now:

* **Companies**  
[Calico Labs](https://www.calicolabs.com/), [Recursion Pharmaceuticals](https://www.recursionpharma.com/), [Spring Discovery](https://www.springdisc.com/), [Zymergen](https://www.zymergen.com/)
* **Labs**  
[Pande Lab](https://pande.stanford.edu/), [Isaac Kohane](https://twitter.com/zakkohane/status/1081181707561250817), [Hammer Lab](http://www.hammerlab.org/)
* **Concepts**  
[Protein folding](https://en.wikipedia.org/wiki/Protein_folding), [In silico experiments](https://en.wikipedia.org/wiki/In_silico)

I'd love to find some introductory books. I also want to learn more about the economics of this space. Things like different monetization strategies (patents, licenses, etc), as well as fund raising and capital requirements. In the academic setting, understanding fund raising is interesting to me, too. Day dreaming, I can imagine all sorts of great things. Something akin to [Verilog](https://en.wikipedia.org/wiki/Verilog), but for cellular systems. Simulators (like newtonian physics simulators) for cellular, animal, or even human systems. Automated wet labs (a la [Zymergen](https://www.zymergen.com/)). AI for [cancer screening](https://twitter.com/azeem/status/1083301736050245634). The list goes on, and this field seems to be in the early days. Very exciting!

If you work in this area or follow it at all, I'd love to hear your thoughts and any pointers on places that I can look to learn more!