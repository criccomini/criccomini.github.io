---
layout: post
title:  "Yes, you still need a QA team (but not for writing your tests)"
author: chris
categories: [ devops ]
featured: true
hidden: true
image: assets/images/2019-02-19-yes-you-still-need-qa-team-not-for-writing-tests/simson-petrol-133138-unsplash.jpg
redirect_to:
  - https://cnr.sh/essays/yes-you-still-need-qa-team-not-for-writing-tests
---

I was having lunch with a friend of mine recently where we were talking about a discussion he'd been having with a [QA](https://en.wikipedia.org/wiki/Quality_assurance#Software_development) manager that he was interviewing. The discussion was about the role of QA in a modern engineering organization. The candidate had responded that they viewed their role like that of security. I found this really thought provoking, and I want to unpack it a little bit.

{% include newsletter.html %}

Security does a lot, but there are three areas in particular that I think are relevant to QA:

* Setting and enforcing policy
* Security testing
* Tooling

The security wing of an organization is often responsible for setting and enforcing security policies. Everything from supported encryption algorithms to data access policies to supported third party software. QA should be doing the same thing, but with a focus on quality. What are the appropriate policies to get a product to an acceptable level of quality? SLA times for defects, code coverage policies, code smell policies, testing requirements and the like are all in scope.

The second area with some relevance is in testing. Note here that I pre-pended the word *security*. Security engineers do not write your unit tests. Nor do they write your integration tests. They do, however get involved with black box (or white box) penetration testing and security validation. They run scans on your network, work with third party penetration testers, and such. QA should be doing something similar, but for the products being built: [*functional* testing](https://en.wikipedia.org/wiki/Functional_testing). Functional testing should be done at the product-level (as opposed to service level). This looks very similar to black box penetration testing, except we're validating that a product works as expected, instead of checking whether it's secure (as expected).

Finally, tooling. In the realm of security, this might include libraries developers can use to encrypt their data, or services that are responsible for vending secrets. In QA-land, tooling should include things like comparing logs or metrics when rolling out a new canary or blue/green deployment against the older version(s) of a service. It might include performance tests suites for running tests against internal infrastructure, or test frameworks (such as [ducktape](https://github.com/confluentinc/ducktape)) for running distributed tests. Production infrastructure such as [Chaos Monkey](https://github.com/Netflix/chaosmonkey) can also be run by QA.

Tooling can also include portions of the [CI/CD](https://en.wikipedia.org/wiki/CI/CD) pipeline. For example, QA might own test infrastructure such as [Jenkins](https://jenkins.io/), [CircleCI](https://circleci.com/), [TravisCI](https://travis-ci.org/), [TeamCity](https://www.jetbrains.com/teamcity/), etc. They shouldn't own the actual tests being run (that should be the dev teams), but providing first-class CI tooling for validating software quality can have a dramatic impact on an engineering organization's velocity.

As you can see, this all leaves QA with a lot to do!