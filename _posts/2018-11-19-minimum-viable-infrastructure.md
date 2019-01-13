---
layout: post
title:  "Minimum viable infrastructure"
author: chris
categories: [ distributed-systems, engineering-field-manual ]
image: assets/images/2018-11-19-minimum-viable-infrastructure/nick-grant-705798-unsplash.jpg
---

We've been discussing building some new infrastructure at work. The project involves writing some fresh code and interfacing with some other systems that we've never used before. There are a lot of unknowns. During a discussion about the project, I found myself making the statement, **"Your goal is to build the smallest amount of the system while still providing value to at least one user."**

{% include newsletter.html %}

This is not a new idea. We see this pattern all over the place in software development. The term [premature optimization](https://en.wikipedia.org/wiki/Program_optimization#When_to_optimize),  was coined by Donald Knuth in 1974.

> We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%. 

The trick here is knowing which 3% to implement. If you don't know, the easiest way to find out is to run your code with no optimization and start fixing the slowest parts of the code first. This is risky, though. If the code is part of a critical path, slow code might be intolerable. So, you need to be selective about which users you start with. This combination of user selectivity and limiting implementation scope is well documented in the [Minimum viable product](https://en.wikipedia.org/wiki/Minimum_viable_product) philosophy.

> A minimum viable product has just those core features sufficient to deploy the product, and no more. Developers typically deploy the product to a subset of possible customers - such as early adopters thought to be more forgiving, more likely to give feedback, and able to grasp a product vision from an early prototype or marketing information. This strategy targets avoiding building products that customers do not want and seeks to maximize information about the customer per amount of money spent.

Build the least amount of the product, be selective of your users, and gather as much information as possible.

How does this approach look when developing new infrastructure? A good place to start is with the first use case. An ideal first user is one who is either not on the critical path of the application or whose usage can be [feature flagged](https://martinfowler.com/articles/feature-toggles.html). Removing your infrastructure from the critical path should be obviously important since it will limit the impact of a failure should things go wrong.

The user should also derive real value from your software. This should go without saying. There might be an intermediate stage where you [dark launch](https://launchdarkly.com/blog/why-leading-companies-dark-launch/), but the final first milestone that's shipped to production should solve a real problem.

Lastly, the user should require a minimum set of features in your software. This is a big one. Doing this right means you'll do less (useless) work. Limiting the feature set also means you'll have to make fewer architectural decisions, which means more design flexibility going forward. The more decisions that are made, the harder it's going to be to change them going forward. This is especially true in areas where data persistence is concerned. If you're in a low information state, giving yourself more flexibility is key.

This concept can be extended beyond building a single piece of infrastructure, too. I came across a [talk](https://speakerdeck.com/nzoschke/minimum-viable-infrastructure) and [blog post](https://nzoschke.github.io/mvi/
) by [Noah Zoschke](https://twitter.com/nzoschke) that discuss minimum viable infrastructure at the architectural level: what are the minimum pieces of infrastructure that you need to build the product that you want to build? This is an important question to ask, and I think we infrastructure developers would benefit from the lessons learned by our product counterparts.