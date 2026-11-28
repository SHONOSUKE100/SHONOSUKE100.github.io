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
| Genie ZeroOps | An agent that watches production pipelines and tables, finds the cause of problems, and proposes fixes that a person approves |
| Lakebase | Databricks' managed Postgres for application databases |
| Lakehouse//RT | A real-time analytics engine that answers queries on analytics tables in milliseconds |
| Genie Ontology | A way to tie business meaning, such as "revenue" or "customer," to tables and columns |

Genie Ontology stood out to me. At Architecture Conference the day before, NTT DOCOMO's data mesh talk had also discussed using ontologies to connect business terms with data. For AI to use data correctly, it needs not only the data but also the context of what that data means for the business. I ran into the same concern two days in a row.

## Lakebase: An Application Database on Top of the Analytics Platform

The first afternoon session was the one I was most looking forward to: Lakebase.

Lakebase is Postgres provided by Databricks. It is built on technology from Neon, which Databricks acquired, and its key feature is that storage and compute are separated. As a result, compute can scale down to zero when idle, and you can create a copy (branch) of a database instantly.

The session also introduced LTAP. Until now, using data from an application database for analytics usually meant building a pipeline that pulls out changes and moves them to an analytics platform. With LTAP, the data Lakebase stores is also converted automatically into a format suited to analytics (Parquet). Analytics engines can then read it directly without the data being moved. LTAP was described as "coming soon."

Connecting application data with analytics data is a recurring headache in data platforms. The idea of storing the data in both forms at write time, instead of moving it, was interesting to me. It was fun to see the difference between row and columnar storage, which I've been studying in the course, turned into a product like this.

## Turing: The MLOps Platform Behind Autonomous Driving AI

Next was a session by Turing, a startup building fully autonomous driving.

Turing is developing an end-to-end driving model, a single neural network that goes from camera video to driving decisions. With this approach, the model is only as good as the quantity and quality of its data. So they work backward from the model's weaknesses to decide what data to collect next, and even plan driving routes to capture those scenes. They build five to ten models a day.

Databricks is used to prepare the collected driving data for training. A few of their practices stood out:

- **Keep video as video**: They used to save each frame as an image, which made the data five to ten times larger. Now they store the video as is and decode it into images on the GPU during training.
- **Build datasets from config files**: A training dataset can be created just by passing a CSV file and a YAML config. Because the definition stays as a file, they can trace which data each model was trained on.
- **Test against known-good data**: They keep outputs verified as correct and compare against them in CI whenever the pipeline changes.
- **Make code easy for AI agents to change**: Processing is split into small steps with clear inputs and outputs. That makes it easier to hand changes to coding agents and easier to review them.

When people think of autonomous driving, they tend to focus on the model itself. This session, though, was about the system for collecting data, preparing it, and running training again and again. It made clear to me that how quickly a model can improve depends on how the data platform is built.

## Lakehouse//RT: Real-Time Analytics Without Copying

The last session I attended was on Lakehouse//RT.

When you want to show live analytics in a dashboard or an application, the usual approach has been to copy the data into a separate system such as ClickHouse. That approach has costs: the data is duplicated, permission management is split, and maintaining the copy takes work.

Lakehouse//RT is an engine that aims to read analytics tables directly, without copying, and answer in milliseconds. The talk cited a minimum latency of 10 ms and 12,000 queries per second (vendor-reported figures). It is read-only and positioned for handling large numbers of short queries, not for batch jobs that read through large amounts of data.

## Rakuten: Governance When AI Writes Data

Rakuten's talk explained that AI now writes data as well as reads it, which raises the bar for governance. They described four things that were missing:

1. Visibility into who uses which models and agents, and how much
2. A way to trace what an agent did internally
3. Guardrails that stop dangerous inputs and outputs
4. Access control

The answer presented was Unity AI Gateway. Data is governed by Unity Catalog, and the use of AI such as models and agents is governed by Unity AI Gateway.

At Architecture Conference the day before, I had also heard about giving AI agents their own identities and permissions. The more work we hand to AI, the more we need ways to decide who can do what, and how far. That was a thread running through both days.

## Final Thoughts

What stayed with me most was that many of Databricks' products follow the same principle:

> Keep the data in one place and use a different engine for each job. Don't copy the data into another system.

There is an engine for each use, including application databases (Lakebase), batch processing, interactive analytics, and real-time analytics (Lakehouse//RT), and they all read the same data. LTAP and Lakehouse//RT are both ways to get rid of the data copies that used to be taken for granted.

It was also fun to see concepts I'm learning in the course, such as separating storage and compute, row vs. columnar storage, and caching, show up one after another in real products. I went to hear product announcements, but at times it felt like a continuation of my database class.

I plan to look into how each of these technologies works in a separate article.

### References

- [Lakebase Architecture — Databricks Documentation](https://docs.databricks.com/aws/en/oltp/projects/architecture)
- [Dispelling LTAP myths — Databricks Blog](https://www.databricks.com/blog/dispelling-ltap-myths)
