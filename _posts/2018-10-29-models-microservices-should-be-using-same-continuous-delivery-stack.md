---
layout: post
title:  "Models and microservices should be running on the same continuous delivery stack"
author: chris
categories: [ devops, machine-learning ]
image: assets/images/2018-10-29-models-microservices-should-be-using-same-continuous-delivery-stack/rawpixel-782053-unsplash.jpg
redirect_to:
  - https://cnr.sh/essays/models-microservices-should-be-using-same-continuous-delivery-stack
---

I've been interested in data science platforms for a long time. My fascination began when I was at LinkedIn, and helped build out the first model building and deployment system for [People You May Know](https://engineering.linkedin.com/teams/data/projects/pymk). At the time, we did feature engineering and training on [Hadoop](https://hadoop.apache.org/), job scheduling on [Azkaban](https://azkaban.github.io/), and model deployment on [Voldemort](https://www.project-voldemort.com/voldemort/).

Things have changed a lot since then. Two posts that have caught my attention lately are the machine learning platforms from Airbnb ([here](https://medium.com/airbnb-engineering/using-machine-learning-to-predict-value-of-homes-on-airbnb-9272d3d4739d)) and Uber ([here](https://eng.uber.com/michelangelo/)). Airbnb has also been talking about [Bighead](https://www.slideshare.net/databricks/bighead-airbnbs-endtoend-machine-learning-platform-with-krishna-puttaswamy-and-andrew-hoh), their [end-to-end ML system](https://cdn.oreillystatic.com/en/assets/1/event/278/Bighead_%20Airbnb_s%20end-to-end%20machine%20learning%20platform%20Presentation.pdf). All of these posts do a great job breaking down all of the different steps involved in machine learning, and how each company built a platform to help developers with the process.

Something that caught my eye, though, is that the deployment pipeline for their models is custom built. Both Airbnb and Uber have a fairly standard [continuous deployment process](https://medium.com/airbnb-engineering/testing-at-airbnb-199f68a0a40d) for [building and deploying](https://eng.uber.com/micro-deploy/) web services. Yet, either deliberately or by accident, they chose to build a separate system for their model deployment pipeline.

This is an interesting peculiarity. I can't recall ever seeing a unified model and service deployment stack. Yet, in the abstract, the deployment needs for models and services are strikingly similar.

{% include newsletter.html %}

## Continuous deployment for models

Let's start by reviewing the continuous delivery process for a microservice.

* Version control
* Build
* Unit test
* Deploy to staging
* Test in staging
* Deploy to production
* Measure and validate

This looks very similar to what you're doing with your models.

### Version control

Models need to live somewhere when they're being developed. You need version control. You need to see who made what changes. Sounds a lot like Git.

### Build

A model needs to be built before it can be deployed. The process of building a model is definitely different from building a microservice. Microservices are built when code changes. Models are built when either data changes or when code changes. In both cases, though, there is a trigger (new data arrival, or a code merge) that causes a model to be retrained or a microservice to be rebuilt.

Microservices are compiled. Models are trained. The training often involves a much more involved sequence that usually requires some kind of orchestration (like Airbnb's [Airflow](https://github.com/apache/incubator-airflow)).

Still, in the abstract, there is an event that triggers a build, and then a sequence of steps that lead to an artifact.
During the build, models, like microservices, need to be assigned a version. Perhaps [semantic versioning](https://semver.org/) isn't quite the best fit, but a versioned artifact is required nonetheless. This makes it easier to track changes, roll forward, roll back, maintain history, etc. [This Bighead slide](https://www.slideshare.net/databricks/bighead-airbnbs-endtoend-machine-learning-platform-with-krishna-puttaswamy-and-andrew-hoh) calls out the challenge of model management explicitly. Versioning (and version control), and things like release notes, are how we handle this on the microservice side of the world.

Both microservices and models need to be deployed to production. They're usually both built (or trained) in a non-production environment. For models, this is usually a modeling (or data warehousing) environment. For microservices, secure build infrastructure is used. The artifacts then get published into a repository. Things get even more interesting if you deploy microservices through Docker. You can layer your data on top of a service's base image to quickly update and deploy model changes. [Data containers](https://hackernoon.com/docker-data-containers-cb250048d162) also look interesting.

### Unit test

After a build is complete, it must be tested. For models, this usually means validating that the model is performing adequately against holdout data. Microservices need to pass their unit tests.

### Deploy to staging

Though it's not common practice, it makes sense to deploy your model to your staging environment before it goes to production. This will exercise the model deployment machinery, and make sure that your staging environment continues to look like production.

### Test in staging

Any integration or user acceptance tests that need to be run can validate that changes in model behavior didn't break anything obvious.

### Deploy to production

After tests pass in staging, it's time to deploy to production. On the microservice side of the fence, this usually involves either a [blue/green deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html) or a [canary release](https://martinfowler.com/bliki/CanaryRelease.html). Most model deployments follow a similar pattern. You deploy the new model, shift traffic over, then remove the old model.

### Measure and validate

Measuring and validating microservices usually involves looking at metric and log information. Are there any anomalies in the logs? Higher WARNs then usual? More exceptions? Has latency spiked, are there fewer/more threads being used, etc?

Again, the same pattern holds for models. The prediction success rate of the model can be measured, and if it dips beyond a threshold, it can be rolled back.

## What happened?

I'm not entirely sure why we ended up here. Two potential explanations are:

* The jump from data science to data engineering to DevOps makes it difficult for teams building data infrastructure to recognize the commonalities with the microservice environment at their organization (c.f. [Conway's law](https://en.wikipedia.org/wiki/Conway's_law)).
* Microservice tooling isn't flexible enough. For example, CI systems tend to model build steps as linear or parallelizable. Model building usually involves much more complex DAGs where tasks have dependencies on one another.

## Same process or same stack

Just because the process for releasing a model can be mapped to a continuous deployment lifecycle doesn't necessarily mean that the same stack should be used for both pipelines. Airflow is a decent orchestrator for model building, but I don't think I'd want to use it to build Java microservices. Likewise, CircleCI probably isn't what you want to use to build a model.

The logical place to start is probably the deployment manager itself. The system that models the continuous deployment lifecycle. It should be possible to use systems like [Spinnaker](https://www.spinnaker.io/) to track the deployment of a model through various environments (testing, staging, production, etc).

Artifact repositories and version control are other places that seem to be likely targets for integration. If you're building models as pickled objects, tarballs, or Docker images, sticking them in a standard artifact repository is quite doable. Storing the models in version control is also obvious.

Measurement and validation also seem to be likely candidates. Placing model performance in your operational charts and graphs is something that should be done anyway, and adding alerting on top of it shouldn't be controversial.

When you add all of this up, it paints a compelling argument for a shared stack. Yes, build and testing probably need to be done on separate systems, but versioning, deployment, measurement and validation all fit nicely with existing devops infrastructure.

## Problems

I admit that it's not all roses. I've already mentioned the differences in the build and test steps. There are other differences, too. Model building is very data-centric. Versioning your data (and providing lineage) is something that's not really modeled in a traditional continuous deployment pipeline (though, static content deployment is perhaps an analogue). [Lambda](https://en.wikipedia.org/wiki/Lambda_architecture)-style, or realtime model training also don't map cleanly to a continuous deployment flow. Still, I argue that there exists a large enough overlap to warrant a shared stack for most of the infrastructure, as I outline above.

## The future

There are signs of hope in the devops and machine learning spaces. GitLab's site has an interesting issue entitled [GitLab/Devops for AI/ML](https://gitlab.com/gitlab-org/gitlab-ce/issues/46161). Gitlab does a fantastic job modeling continuous integration and delivery, and I'd be excited to progress in this area. There are [a lot](https://towardsdatascience.com/deploying-machine-learning-models-with-docker-5d22a4dacb5) of [posts](https://www.udemy.com/deploy-data-science-nlp-models-with-docker-containers/) about [deploying models](http://shop.oreilly.com/product/0636920084334.do) through [Docker](https://medium.com/analytics-vidhya/how-to-deploy-machine-learning-models-using-flask-docker-and-google-cloud-platform-gcp-6e7bf1b339d5), [version control in JupyterHub](https://towardsdatascience.com/version-control-for-jupyter-notebook-3e6cef13392d), and so on. I'm also pretty excited about how [Prefect](https://www.prefect.io/) is [thinking about problems like this](https://medium.com/the-prefect-blog/positive-and-negative-data-engineering-a02cb497583d).

In the meantime, the best path forward is probably to be opportunistic about shared infrastructure. If you find yourself deploying pre-built models, ask why they can't be deployed via the same repository as your microservices. Likewise, when measuring the performance of a model in production, why not see how easy it'd be to use your existing metrics and monitoring infrastructure?
