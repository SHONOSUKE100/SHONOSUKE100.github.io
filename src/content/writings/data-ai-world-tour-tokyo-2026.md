---
title: "Data + AI World Tour Tokyo 2026: Lakebase and Lakehouse//RT Through a Database Lens"
locale: en
description: "Notes on Lakebase, LTAP, Lakehouse//RT, and Turing's MLOps platform from Databricks' Tokyo event, viewed from inside the database."
publishedAt: 2026-11-28
category: "engineering-systems"
tags: ["database", "data-engineering", "conference"]
draft: false
---

On November 27, I attended Databricks' Data + AI World Tour Tokyo at The Prince Park Tower Tokyo. I had been at [Architecture Conference 2026](/writing/architecture-conference-2026/) the day before, so it was two conferences in two days.

I'm currently self-studying CMU's database course (15-445/645). So this time, rather than focusing on the new product features themselves, I listened with one question in mind: what is actually happening inside? This article collects what I heard and what I thought about along the way.

In short, what stayed with me most was that many of Databricks' products follow the same principle:

> Keep the data in one place and use a different engine for each job. Don't copy the data into another system.

Product numbers and specifications come from the talks and official sources. Parts marked as my guess are my own thinking, not official explanations.

## Keynote: Many Engines on One Copy of the Data

The keynote introduced a set of new products and features. The main ones were:

| Name | In one line |
| --- | --- |
| Lakeflow | A data engineering platform for ingestion, transformation, and job orchestration |
| Genie ZeroOps | An agent that watches production pipelines and tables, finds the cause of problems, and proposes fixes that a person approves |
| Lakebase | Databricks' managed Postgres for application transactions (OLTP) |
| Lakehouse//RT | An engine that answers queries on lake tables in milliseconds |
| Genie Ontology | A layer that ties business meaning, such as "revenue" or "customer," to tables and columns |

Genie Ontology echoed NTT DOCOMO's data mesh talk from the day before. Both start from the same concern: for AI to use data correctly, it needs not only the data but also the business context of what that data means. In Databricks' design, people define metrics and glossaries in a layer called Unity Catalog Semantics. Genie Ontology builds on that layer and also learns from how the data is actually used to expand the context.

On real-time analytics, the speakers stressed that both latency and throughput matter, and that a system breaks down once it goes past its throughput limit. They introduced Lakehouse//RT as keeping latency under 100 ms even at 12,000 QPS (queries per second). I heard more about both of these products in the afternoon sessions.

## Lakebase and LTAP: Connecting OLTP and Analytics

The first afternoon session was the one I was most looking forward to: Lakebase and LTAP.

### Lakebase Is Postgres With Storage and Compute Separated

The name combines Lake (storage) and Base (the database engine). It is built on the architecture of Neon, which Databricks acquired.

A regular Postgres server runs queries, writes the log (WAL), and stores data pages all on one machine. Lakebase splits these roles into separate components.

| Role | Regular Postgres | Lakebase |
| --- | --- | --- |
| Running queries | Postgres on the server | Stateless Postgres (compute) |
| Making the WAL durable | Local disk | Safekeepers (stored with consensus across several nodes) |
| Storing data pages | Local disk | Pageserver (rebuilds pages from the WAL) |
| Long-term storage | Local disk | Object storage such as S3 |

A write goes through these steps:

1. Compute produces the WAL for a transaction and sends it to the Safekeepers.
2. The commit succeeds once a majority of Safekeepers have stored the WAL.
3. The Pageserver receives the WAL, rebuilds it into pages, and eventually writes them to object storage.

Because compute keeps no data locally, it can start and stop quickly and scale down to zero when idle. Storage is copy-on-write, so you can create a branch (copy) of a database instantly and restore it to a past point in time.

In 15-445 terms, what remains on the compute side is the buffer pool (shared buffers plus a local cache beneath them), with the Pageserver across the network taking the place of the disk.

### LTAP: Convert in Storage Instead of Moving the Data

LTAP stands for Lake Transactional/Analytical Processing. It was presented as a new way to make OLTP data available for analytics.

The usual approach has been CDC (change data capture): pull changes out of the OLTP database and move them through a pipeline such as Kafka into an analytics platform. That means operating the pipeline, living with delays, keeping up with schema changes, and storing the data twice.

LTAP doesn't move the data. When the Pageserver writes Postgres pages out to object storage, it also converts the row-oriented pages into columnar Parquet. Other analytics engines can then read the result directly as Delta or Iceberg tables. According to the talk, the conversion is reversible, so the original Postgres pages can be rebuilt from Parquet. Databricks' blog explains that each row carries its heap block number, offset, and MVCC version, and that Parquet is the source of truth while heap pages act as its cache.

Here is how I would compare the ways of connecting OLTP and analytics:

| | HTAP (e.g., TiDB) | Zero-ETL (Aurora → Redshift) | LTAP (Lakebase) |
| --- | --- | --- | --- |
| What is unified | The engine | Replication operations | The storage |
| How columnar data is produced | A columnar replica applies the log | Replicated into an analytics database | Converted to Parquet when pages are written out |
| Engines that can analyze it | A dedicated engine | A dedicated engine | Any engine that reads Delta or Iceberg |

### Trade-offs I Thought About

From a database-internals point of view, a few things caught my attention. These are my guesses.

- **Sort order and data skipping**: Parquet files follow heap page order, so range filters on something like a date shouldn't benefit much from min/max statistics. Databricks' blog acknowledges this and recommends deriving a separate table that is reclustered for analytics.
- **Write amplification**: The same data is written three times (WAL, pages, and Parquet) and stored in two forms (rows and columns).
- **A single writer**: Only one compute node per branch can write. Unlike distributed databases (NewSQL) such as Spanner or CockroachDB, write throughput is capped by one machine. My understanding is that Lakebase isn't trying to solve write scaling. It is aiming at elasticity, cost, branching, and integration with the lake.
- **What "a single copy" means**: Physically, the data exists in two forms (rows and columns), but there is one logical source of truth.

LTAP was described as "coming soon." Once it's available, I'd like to measure how long it takes for a commit to become visible to analytics and how it performs on frequently updated tables.

## Turing: The MLOps Platform Behind Autonomous Driving AI

Next was a session by Turing, a startup building fully autonomous driving. This one was a very practical data engineering talk.

### End-to-End Driving and Why Data Matters

Traditional autonomous driving splits the problem into four modules: perception, prediction, planning, and control. It relies on high-definition maps and rule-based decisions. Turing replaces this with an end-to-end model, a single neural network that goes from camera images to driving decisions. Beyond that, they are aiming for physical foundation models, extended from language models, that run in the car.

An end-to-end model is only as good as the quantity and quality of its data. Japanese roads mix pedestrians, cyclists, and construction workers, and scenes with poor visibility, like someone stepping out from behind a parked car, are hard to collect just by driving around. So Turing works backward from the model's weaknesses to decide what data to collect next, and even plans driving routes to capture those scenes. They build five to ten models a day.

### How the Data Flows

Of the stages from data collection to deployment in the car, Databricks handles data preparation.

```text
Collection → Standardization → Curation → Training → Evaluation → Deploy to car
             └────── Databricks ──────┘
```

Video and sensor logs from the cars go to S3 as they are. Data about that data, such as metadata, captions describing each video, and embeddings for finding similar scenes, is streamed into Lakehouse tables. The ETL is written with Lakeflow's declarative pipelines, using streaming tables to ingest the continuously arriving logs and materialized views for aggregations and extractions.

Training datasets are built by a separate job outside this pipeline, and its only inputs are a CSV file and a YAML config. Separating the shared ETL from per-experiment dataset creation lets them produce many datasets without touching the pipeline. Because each dataset definition is a file in Git, they can also trace which data a model was trained on.

### Ideas I Liked

A few of the practices they described stood out:

- **Store video as video and decode it during training**: They used to save each frame as an image, which made the data five to ten times larger and raised the cost of moving it to training nodes. Now they keep the compressed video and decode it at training time with NVIDIA's GPU decoders. Datasets share the videos instead of copying them, which reduces duplicate storage.
- **Reshape the data for training**: They used to follow the format of nuScenes, a well-known public autonomous driving dataset. It is normalized, with separate tables for sensors and annotations that reference each other by ID. That makes it easy to extend, but assembling one training sample meant walking through many tables. They switched to their own format with one sample per record, which makes reading much faster.
- **Run code without merging to main**: Jobs and pipeline definitions live in YAML next to the code (Declarative Automation Bundles), and a development branch can run on the same Spark clusters as production. Development used to happen on local machines, so problems that only appeared at production scale went unnoticed.
- **Check for regressions with golden data**: They keep outputs that have been verified as correct (golden data) and compare the pipeline's output against them in CI.
- **Make units that coding agents can change easily**: Each processing step is a class that inherits from a shared `PipelineStep` base class. Clear inputs and outputs for each step make it easier to hand changes to an agent and easier to review them.

### Seen Through a Database Lens

This talk was full of real examples of things from a database course.

- Moving from the nuScenes format to one sample per record is the classic **normalization vs. denormalization** trade-off. Training data is written once and read many times, so paying the join cost once, when building the dataset, makes sense.
- Keeping video compressed and decoding it on read is a **storage vs. compute** trade-off, the same idea as compression in columnar storage.
- Keeping materialized views up to date as the source data changes is the problem of **incremental view maintenance (IVM)**.
- They also mentioned that serverless jobs are retried automatically when they fail. My guess is that this requires **idempotent** processing. If a job runs at least once and produces the same result no matter how many times it runs, the effect is the same as running it exactly once.

## Lakehouse//RT: Real-Time Analytics Without Copying

The last session I attended was on Lakehouse//RT.

### Three Metrics for Real-Time Analytics

The talk named three metrics that matter for real-time analytics:

| Metric | Meaning |
| --- | --- |
| Data freshness | Time from when data is created until a query can see it |
| Response time | Time for a single query to return |
| Concurrency | Number of queries handled at once (QPS) |

The common approach has been to copy data out of the lakehouse into a separate real-time system such as ClickHouse. That approach has costs: the data is duplicated, governance is split because Unity Catalog permissions and lineage don't reach the copy, and maintaining the copy slows development down. Lakehouse//RT tries to solve this by reading Delta and Iceberg tables directly, without copying, and answering with low latency.

### The Numbers

The talk showed these figures:

- Minimum latency of 10 ms
- 12,000 queries per second
- 2.8x faster on ClickBench, a benchmark that runs aggregation queries on one wide table, and about 3x faster on data that joins multiple tables

I couldn't catch what these were compared against or under what conditions they were measured. They are vendor-reported numbers, and I'm treating them as such. What I found most interesting was that it stays fast with joins. Real-time analytics databases are often weak at joins, so teams tend to flatten data into wide tables before copying it over. If joins are fast as they are, that denormalized copy isn't needed either.

The speakers also explained that Lakehouse//RT is read-only and not suited to long scans or batch ETL. Its job is to handle large numbers of short queries from dashboards and applications.

### Why It Can Be Fast (My Guess)

During the talk, I kept asking myself why a distributed engine like Spark can't do the same thing, and how Lakehouse//RT does it. What follows is my guess.

Engines like Spark are designed for throughput, to process large amounts of data efficiently. Even a single query goes through planning, splitting into stages and tasks, scheduling on nodes, and gathering results. That fixed overhead alone takes hundreds of milliseconds. They also speed up one query by spreading it across the whole cluster, so many concurrent queries end up competing for the same resources.

Little's law gives a sense of scale. The number of queries running at once equals QPS × time per query. At 12,000 QPS with 10–100 ms per query, 120 to 1,200 queries are running at any moment. The key isn't just making one query fast. It's keeping each query's resource use small so that many can run side by side.

These techniques seem likely to help:

1. **Avoid object storage with caching**: A single S3 request takes tens of milliseconds, so reaching 10 ms means not reading S3 in the middle of a query. The documentation says results can lag the latest commit by a few seconds because table metadata is cached, which fits this guess. The data itself is probably cached in memory or on local SSDs, the same idea as a buffer pool.
2. **Keep each query small**: Finish a short query on a single node without exchanging data between nodes. This also keeps one slow node from dragging down the whole query.
3. **Take advantage of being read-only**: With no writes, there are no locks and no transaction coordination. Adding nodes that read the same data should raise QPS almost linearly.
4. **Cut per-query fixed costs**: Queries from dashboards and applications usually have the same shape with different parameters. Plan caching and skipping files using statistics help here.

### One Copy of the Data, Many Engines

Over the day, it became clear that Databricks uses a different engine for each job on top of the same lake data.

| Engine | Use | Optimized for |
| --- | --- | --- |
| Lakebase | OLTP (writes and transactions) | Fast single-row reads and writes |
| Spark / Lakeflow | Batch ETL and transformation | Throughput |
| Databricks SQL | Interactive analytics and BI | Fast scans |
| Lakehouse//RT | Serving dashboards and applications | Latency and concurrency |

LTAP removes the copy from OLTP to analytics, and Lakehouse//RT removes the copy from analytics to real-time serving. They point in different directions, but both rest on the same principle.

## Rakuten: Governance When AI Writes Data

Rakuten's talk covered a data platform built around Iceberg and AI governance. Their concern was that AI now writes data as well as reads it, which raises the bar for governance.

They described four things that were missing:

1. Visibility into who uses which models and agents, and how much
2. Observability into what an agent did internally
3. Guardrails that stop dangerous inputs and outputs
4. Access control

The answer presented was Unity AI Gateway. Data assets are governed by Unity Catalog, and the execution of AI assets such as models, agents, and MCP servers is governed by Unity AI Gateway. Together, the two form a unified governance layer.

While listening, I was thinking about whether permissions should belong to the agent or to the person using it. The day before, at Architecture Conference, I had heard about giving each agent its own identity and applying the principle of least privilege. A practical split seems to be: a chat-style agent acting for a person uses that person's permissions, and a scheduled agent with no person in the loop uses its own identity.

## Final Thoughts

I went to hear product announcements, and it turned out to feel like a review session for my database course. Separating storage and compute, WAL and consensus, row and columnar storage, normalization and denormalization, caching, incremental view maintenance: these are all concepts from 15-445. Thinking about how they fit together inside real products was a lot of fun.

The principle of keeping data in one place and splitting the engines also connected with the data mesh and zero-copy data sharing I heard about at Architecture Conference the day before. Across the two days, I felt I could see a single thread running through it all.

There's still a lot I don't fully understand, so I plan to follow up on these questions in the official blogs and papers.

### References

- [Lakebase Architecture — Databricks Documentation](https://docs.databricks.com/aws/en/oltp/projects/architecture)
- [Dispelling LTAP myths — Databricks Blog](https://www.databricks.com/blog/dispelling-ltap-myths)
- [Object Storage + WAL — Databricks Blog](https://www.databricks.com/blog/object-storage-wal-lakebase-postgres-agentic-era)
- [Built on object storage, served from cache — Databricks Blog](https://www.databricks.com/blog/built-object-storage-served-cache)
- Andrew Pavlo and Matthew Aslett. "What's Really New with NewSQL?" *SIGMOD Record*, 2016.
- Alexandre Verbitski et al. "Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases." *SIGMOD*, 2017.
