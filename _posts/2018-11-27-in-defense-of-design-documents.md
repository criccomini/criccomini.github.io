---
layout: post
title:  "In defense of design documents"
author: chris
categories: [ engineering-field-manual ]
featured: true
hidden: true
image: assets/images/2018-11-27-in-defense-of-design-documents/annie-spratt-746981-unsplash.jpg
---

Design documents aren't just a chore; something that you begrudgingly slog through before getting to the fun work of writing code. Writing a design document might be challenging, but it should be a productive exercise that gets everyone on the same page. Let's start with what a design document is.

{% include newsletter.html %}

Design documents come in all sorts of flavors. Some of them are tens or even hundreds of pages long, while others might be a few paragraphs. Some are very formal or academic, while others are quite casual. One important area of distinction is whether a design document is being written before the code has been implemented, or whether it's being written for an existing piece of software. Documents written before implementation tend to be more exploratory and persuasive, while documents written after tend to be more about description. This document focuses on design documents that have not yet been implemented, though a lot of the content here applies just as much to design documents for existing code.

## The document

There isn't a one-size-fits-all template for design documents, but most include a combination of sections such as:

* Introduction, problem statement, justification for changes, goal, interested parties
* Review of existing implementation, surrounding ecosystem, related work
* High-level/architectural design, discussion of other potential designs, tradeoffs
* Lower-level implementation details, security, high availability, scalability, durability

Most large open source projects have some semi-formal process for design documents, and they can be a good place to look for inspiration and examples.

* [PEPs](https://www.python.org/dev/peps/) (Python enhancement proposals)
* [KIPs](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals) (Kafka improvement proposals)
* [JSRs](https://jcp.org/en/jsr/all) (Java specification requests)

This should give a flavor for what design documents and specifications can look like. But why write one?

* To force the designer to think rigorously about what they're building
* To help others understand what is to be built, why it should be built, and how it will work.

## The designer

The designer can sometimes be an overlooked party in design documents. First-level thinking will view the design document as expressing what the designer already knows. This should not be the case. The design document should be used as a tool by the designer to think rigorously about what it is that they're proposing to build. The writer should do a brain dump of what they think should be built, why, and how. Then, they should attack their own proposal. What are the alternatives? What business processes have been overlooked? An honest exploration will lead to a more robust document.

## The developers

Other developers involved in the project need to know about changes being made. Obviously, if the designer is enlisting others help implement the proposed changes, the developers are going to need to know what to build. But even if developers are not going to be involved in the changes, they will be valuable to the process. They each have a different perspective, which is extremely valuable. Not only does each developer have a different understanding of a system, they also have different knowledge about the surrounding ecosystem, and a different thought process. Including developers can lead to alternative proposals, exposure of gaps in the design, or improvements to the existing design. All of this is invaluable.

## The users

Users also bring a unique perspective, and should be included when writing a design document. It's not worth belaboring the point of unique perspectives, but suffice it to say that users often have a very different view of the system from developers. Their involvement is key.

Note that, for some designs, there may be different classes of users. For example, a user for a database might be a developer writing a service that interacts with a database, or it might be an operator that runs the database. Each type of user, again, comes to the table with different needs and thoughts.

## Conclusion

The list of parties above is not exhaustive. Others, such as managers, might also need to be involved. Still, this only further underscores the importance of good design documentation.

At its core, design documents are about managing change. Expressing what's being done, why, and how are all important. Even more important is getting all interested parties on board and in sync. All of this will reduce risk and help others be productive.