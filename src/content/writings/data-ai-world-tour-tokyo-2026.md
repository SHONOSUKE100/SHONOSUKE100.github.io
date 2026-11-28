---
title: "Data + AI World Tour Tokyo 2026: Reflections"
locale: en
description: "What I heard at Databricks' Tokyo event about Lakebase, Lakehouse//RT, Turing's MLOps platform, and Rakuten's AI governance, and what I took away from the day."
publishedAt: 2026-11-28
category: "engineering-systems"
tags: ["database", "data-engineering", "conference"]
draft: false
---

On November 27, I attended Databricks' Data + AI World Tour Tokyo at The Prince Park Tower Tokyo. I had been at [Architecture Conference 2026](/writing/architecture-conference-2026/) the day before, so it was two conferences in two days.

![Tokyo Tower rising behind a row of yellow ginkgo trees under a clear blue sky](/images/writings/data-ai-world-tour-tokyo-2026/tokyo-tower.jpg)

*Tokyo Tower and ginkgo trees near the venue*

I'm currently self-studying CMU's database course (15-445/645), and I had been looking forward to this event as a chance to see where databases and data platforms are heading.

In this article, I summarize the sessions I attended and my impressions. Many of the technologies were interesting under the hood, and I plan to dig into them in a separate article.

## Keynote

The keynote introduced a set of new products and features. The main ones were:

| Name | In one line |
| --- | --- |
| Lakeflow | A data engineering platform for ingestion, transformation, and job orchestration |
| Genie ZeroOps | An agent that watches production pipelines and tables, finds the cause of problems, and proposes fixes |
| Lakebase | Databricks' managed Postgres for application databases |
| Lakehouse//RT | A real-time analytics engine that answers queries on analytics tables in milliseconds |
| Genie Ontology | A way to tie business meaning, such as "revenue" or "customer," to tables and columns |

Lakeflow brings together ingestion from SaaS tools and databases (Lakeflow Connect), declarative ETL (Lakeflow Declarative Pipelines), and job orchestration (Lakeflow Jobs). The pitch was to handle data pipelines, which tend to get complicated, on a single platform, with all governance under Unity Catalog.

Genie ZeroOps watches production jobs and tables in the background. When it finds something like a data quality problem, it investigates the cause and proposes a fix, which is applied only after a person approves it.

Genie Ontology stood out to me most. It is built in layers on top of Unity Catalog Semantics, which people define:

- **Unity Catalog Semantics**: a layer people define with help from AI. It covers organizing data along business lines (Domains), business concepts and categories (Pages), and reusable KPI definitions (Metrics)
- **Genie Ontology**: combines Semantics with knowledge learned automatically from data and from apps such as Slack and email, and provides it as context across the organization
- **Consumers**: Genie, MCP, SQL, APIs, dashboards, and more can all use this context

At Architecture Conference the day before, NTT DOCOMO's data mesh talk had also discussed using ontologies to connect business terms with data. For AI to use data correctly, it needs not only the data but also the context of what that data means for the business. I ran into the same concern two days in a row.

On real-time analytics, the speakers stressed that both latency and throughput matter, and that a system breaks down once it goes past its throughput limit. They introduced Lakehouse//RT as keeping latency under 100 ms even at 12,000 QPS (queries per second). I heard more about Lakebase and Lakehouse//RT in the afternoon sessions.

## Lakebase and LTAP: An Application Database on Top of the Analytics Platform

The first afternoon session was the one I was most looking forward to: Lakebase and LTAP.

### Lakebase

Lakebase is Postgres provided by Databricks. The name combines Lake (storage) and Base (the database engine), and it is built on technology from Neon, which Databricks acquired.

A regular Postgres server both runs queries and stores the data on one machine. Lakebase separates the two, and the Postgres that runs queries keeps no data locally. Safekeepers, a group of servers, receive and store the log of changes (the WAL). A Pageserver turns that log into data pages, which end up in cloud object storage.

Separating storage and compute makes these things possible:

- Compute can scale down to zero when idle
- You can create a copy (branch) of a database instantly, for example a full copy of production for development or testing
- You can restore a database to a past point in time

### LTAP

The session also introduced LTAP (Lake Transactional/Analytical Processing).

Until now, using data from an application database for analytics usually meant pulling out changes with CDC (change data capture) and building a pipeline to move them to an analytics platform. That means operating the pipeline, waiting for data to arrive, and keeping up when table structures change.

LTAP doesn't move the data. When the Pageserver writes data out to object storage, it also converts it into a columnar format suited to analytics (Parquet). The converted data can be read directly by analytics engines as Delta or Iceberg tables. According to the talk, the conversion is reversible, so the original Postgres data can be rebuilt from Parquet. LTAP was described as "coming soon."

Connecting application data with analytics data is a recurring headache in data platforms. The idea of storing the data in both forms at write time, instead of moving it, was interesting to me. It was fun to see the difference between row and columnar storage, which I've been studying in the course, turned into a product like this.

## Turing: The MLOps Platform Behind Autonomous Driving AI

Next was a session by Turing, a startup building fully autonomous driving. The talk overlapped with Turing's tech blog post, "[Building a machine learning dataset platform with Databricks Declarative Automation Bundles](https://zenn.dev/turing_motors/articles/46b5560dce0e3a)" (in Japanese), so I've included some of what I learned from it as well.

### Data Determines Performance

Traditional autonomous driving splits the problem into four modules: perception, prediction, planning, and control. It relies on high-definition maps and rule-based decisions. Turing is developing an end-to-end model, a single neural network that goes from camera video to driving decisions. Beyond that, they are aiming for physical foundation models, extended from language models, that run in the car.

With this approach, the model is only as good as the quantity and quality of its data. Japanese roads mix pedestrians, cyclists, and construction workers, and scenes with poor visibility, like someone stepping out from a blind spot, are hard to collect just by driving around. So Turing works backward from the model's weaknesses to decide what data to collect next, and even plans driving routes to capture those scenes. They build five to ten models a day.

### Moving Dataset Creation to Databricks

Of the stages from data collection to deployment in the car, Databricks handles preparing the collected driving data for training.

Previously, they combined AWS services to cut images out of the videos and generate metadata in the format of nuScenes, a well-known public autonomous driving dataset. According to the blog, building a dataset from 500 hours of driving data took more than half a day. Saving every frame as its own file also produced an enormous number of files.

The new platform changes this in several ways:

- **Store video as video and decode it during training**: According to the talk, cutting video into images made the data five to ten times larger. Now the video is stored as is and decoded into images with NVIDIA's GPU decoders during training. Dataset creation can focus on preparing metadata.
- **Use a format suited to training**: The nuScenes format splits sensors and annotations into separate tables. That makes it easy to extend, but assembling one training sample means walking through many tables. The new format puts one sample in one record and writes it out as a MosaicML Streaming Dataset (MDS), which needs fewer files and reads quickly during training.
- **Build datasets from config files**: The only inputs are a CSV listing scene IDs and a YAML file of parameters. Because the definition stays as a file, they can trace which data each model was trained on.

According to the blog, a 500-hour dataset can now be built in 60 minutes or less, depending on conditions.

### How They Develop

The development practices described in the talk and the blog were interesting too:

- **Manage job definitions as code**: With Declarative Automation Bundles (formerly Databricks Asset Bundles), job definitions and runtime environments live in YAML alongside the code. They can switch between a per-developer environment, production, and an integration-test environment, and try a development branch on the same Spark clusters as production without merging to main. Production deploys happen in CI when a Git tag is pushed.
- **Test against known-good data**: Integration tests compare the pipeline's output with comparison data prepared in advance. This caught problems such as changes in table structure and issues from dependency updates.
- **Split processing into small steps**: Each step is a class that inherits from a shared `PipelineStep` base class. Each step declares which tables it uses as input, and new processing can be added just by adding a new step. The talk also mentioned that this structure makes it easier to hand changes to coding agents.

They also shared the challenges of running on serverless compute, along with concrete workarounds. Caching isn't available, so intermediate results are written out to a table. Installing dependencies took more than five minutes, and preparing packages in advance cut it to two. Failed jobs are retried automatically, so they track each dataset's status to prevent duplicate runs.

When people think of autonomous driving, they tend to focus on the model itself. This session, though, was about the system for collecting data, preparing it, and running training again and again. It made clear to me that how quickly a model can improve depends on how the data platform is built.

## Lakehouse//RT: Real-Time Analytics Without Copying

The last session I attended was on Lakehouse//RT.

### Three Metrics for Real-Time Analytics

The talk named three metrics that matter for real-time analytics:

| Metric | Meaning |
| --- | --- |
| Data freshness | Time from when data is created until a query can see it |
| Response time | Time for a single query to return |
| Concurrency | Number of queries handled at once |

### Problems With the Usual Approach

When you want to show live analytics in a dashboard or an application, the usual approach has been to copy the data into a separate system such as ClickHouse. The talk listed three problems with this:

1. **Duplicate data**: The same data lives in two places, which adds storage cost
2. **Split governance**: Unity Catalog permissions and lineage don't apply to the copy
3. **Slower development**: Operating another system and maintaining the copy takes time

Lakehouse//RT tries to solve these by reading analytics tables (Delta or Iceberg) directly, without copying, and answering in milliseconds. Because the data isn't converted into a proprietary format, there's no lock-in, and permissions and lineage stay consistent under Unity Catalog.

### Numbers and Positioning

The talk showed these figures:

- Minimum latency of 10 ms
- 12,000 queries per second
- 2.8x faster on ClickBench, a benchmark that runs aggregation queries on one wide table, and about 3x faster on data that joins multiple tables

The talk didn't say what these were compared against, so I'm treating them as vendor-reported numbers. Real-time analytics databases like ClickHouse are often weak at joins, so I'm personally interested in the claim that it stays fast with joins.

The talk was also clear about what it is for:

| Good fit | Not a good fit |
| --- | --- |
| Many concurrent reads that finish in milliseconds to seconds | Long scans that read through large amounts of data |
| Dashboards, application APIs, user-facing analytics | Batch ETL, writes, and transformations |

Batch jobs over large amounts of data stay with the existing engines, and Lakehouse//RT focuses on handling large numbers of short queries.

## Rakuten: Governance When AI Writes Data

Rakuten's talk covered a data platform built around Iceberg and AI governance.

Their concern was that AI now writes data as well as reads it, which raises the bar for governance. They described four things that were missing:

1. Visibility into who uses which models and agents, and how much
2. A way to trace what an agent did internally (observability)
3. Guardrails that stop dangerous inputs and outputs
4. Access control

The answer presented was Unity AI Gateway. Its features include managing AI costs, routing requests, tracking usage, security and access control, and a registry of AI assets. Data assets such as tables and files are governed by Unity Catalog, and the execution of AI assets such as models, agents, MCP servers, and skills is governed by Unity AI Gateway. Together, these two pillars form a unified governance layer.

At Architecture Conference the day before, I had also heard about giving AI agents their own identities and permissions and applying the principle of least privilege. The more work we hand to AI, the more we need ways to decide who can do what, and how far. That was a thread running through both days.

## Final Thoughts

What stayed with me most was that many of Databricks' products follow the same principle:

> Keep the data in one place and use a different engine for each job. Don't copy the data into another system.

There is an engine for each use, including application databases (Lakebase), batch processing, interactive analytics, and real-time analytics (Lakehouse//RT), and they all read the same data. LTAP removes the copy from application databases to analytics, and Lakehouse//RT removes the copy from analytics to real-time serving.

It was also fun to see concepts I'm learning in the course, such as separating storage and compute, row vs. columnar storage, normalization vs. denormalization, and caching, show up one after another in real products and case studies. I went to hear product announcements, but at times it felt like a continuation of my database class.

I plan to look into how each of these technologies works in a separate article.

### References

- [Lakebase Architecture — Databricks Documentation](https://docs.databricks.com/aws/en/oltp/projects/architecture)
- [Dispelling LTAP myths — Databricks Blog](https://www.databricks.com/blog/dispelling-ltap-myths)
- [Building a machine learning dataset platform with Databricks Declarative Automation Bundles — Turing Tech Blog (in Japanese)](https://zenn.dev/turing_motors/articles/46b5560dce0e3a)
