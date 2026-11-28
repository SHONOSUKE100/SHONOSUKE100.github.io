---
title: "Architecture Conference 2026: Reflections"
locale: en
description: "What I took away from Architecture Conference 2026, from design principles and AI agents to data mesh and the C4 model."
publishedAt: 2026-11-28
category: "software-design"
tags: ["architecture", "conference", "ai"]
draft: false
---

On November 26, I attended [Architecture Conference 2026](https://architecture-con.findy-tools.io/2026), hosted by Findy at Haneda Airport.

I also attended this conference last year, which sparked my interest in software architecture. At the same time, I realized how challenging architecture was and how much I still needed to learn, both in terms of technical skills and business domain knowledge.

A year later, I found myself able to understand the discussions much more deeply. Over the past year, I have had opportunities to study software architecture through my onboarding at work, learning Java, and reading books such as *Clean Architecture* and other books on design patterns.

Meanwhile, the rapid advancement of AI has made me rethink how we design software and approach software development.

Two ideas from last year's conference have stayed with me:

- "Garbage in, garbage out."
- "AI is an accelerator."

AI is becoming increasingly capable of performing tasks that previously required significant human effort.

In this era, I believe it is increasingly important to communicate effectively with both humans and AI, make implicit knowledge explicit, reduce ambiguity, establish clear contracts, and document our design decisions.

Ultimately, we need to build systems that are maintainable and adaptable to change over the long term.

In this article, I would like to share some of the key insights and reflections from the sessions I attended.

## Rethinking Design Principles: What Should Change and What Should Stay?

**Martin Fowler (Thoughtworks) & Kazutoshi Ono (Credit Saison)**

This keynote explored the origins of software design principles, including design patterns, refactoring, and Extreme Programming, and discussed their relevance in the age of AI.

### Key Takeaways and Reflections

- I discovered a valuable learning resource: Martin Fowler's website.
- Design patterns help developers understand and apply complex concepts such as object-oriented programming. I was interested to learn that early software design patterns were inspired by Christopher Alexander's pattern language and applied to user interface design in Smalltalk.
- I learned about Smalltalk, a programming language that played an important role in the history of object-oriented programming.
- Extreme Programming integrates project management with technical practices such as automated testing and continuous integration. Similarly, AI is transforming not only how we write code but also how we manage software development.
- I found the concept of an expert generalist particularly interesting. Expert generalists combine deep technical knowledge with curiosity, the ability to learn across domains, collaboration skills, and a focus on customer needs.

My interpretation is that having advanced technical skills in a narrow field alone may no longer be enough to create value in the age of AI. The ability to understand problems from different perspectives and collaborate with people who have different areas of expertise is becoming increasingly important.

### References

- [Martin Fowler's Website](https://martinfowler.com/)
- [Expert Generalists — Martin Fowler et al.](https://martinfowler.com/articles/expert-generalist.html)
- [Extreme Programming — Martin Fowler](https://martinfowler.com/bliki/ExtremeProgramming.html)
- [Using Pattern Languages for Object-Oriented Programs — Kent Beck and Ward Cunningham](https://c2.com/doc/oopsla87.html)

## Designing Architecture for Production-Ready AI Agents

**Keisuke Tsukagoshi (Google Cloud)**

This session focused on four architectural challenges of running AI agents in production: quality and evaluation, responsibilities and boundaries, security and permissions, and cost and latency.

### Key Takeaways and Reflections

- What I found particularly interesting was that delegating internal business processes to AI encourages organizations to make implicit knowledge and decision-making criteria explicit. AI can therefore help reduce dependence on individual employees rather than simply automate their work.
- I learned about progressive disclosure, an approach that initially provides agents with an overview and makes detailed instructions and knowledge available only when needed. This allows for more efficient use of the context window.
- I also found the concept of Agent Identity interesting. Assigning a unique identity and specific permissions to each agent allows us to apply traditional access control principles, such as the principle of least privilege, to AI agents.
- Defining clear interfaces and data contracts is essential for AI agents. A2A can be used for agent-to-agent communication, while MCP connects agents to external tools and resources. Structured inputs and outputs can help reduce ambiguity between these components.
- Security constraints and deterministic business rules should be enforced outside the LLM rather than relying solely on prompts.
- Human approval can gradually shift from reviewing every individual action to defining evaluation criteria and handling exceptional cases.

My biggest takeaway is that introducing AI agents is not simply about automating existing processes. It is also an opportunity to rethink and formalize how knowledge, responsibilities, permissions, and decisions are structured within an organization.

### References

- [Agentic AI Summit — Google Cloud](https://cloudonair.withgoogle.com/events/agentic-ai-summit-26-fall)
- [Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
- [A2A and MCP — A2A Protocol Documentation](https://a2a-protocol.org/latest/topics/a2a-and-mcp/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Learning from AWS AI-DLC v2: Designing Domain Boundaries for AI

**Junichi Kato (IDEO PLUS)**

This session explored how to ensure that AI-generated code respects domain boundaries and architectural principles by integrating domain knowledge, design constraints, and validation into AI-driven development workflows.

### Key Takeaways and Reflections

- Passing functional tests does not necessarily mean that the implementation respects architectural principles or domain boundaries.
- Domain primitives and type systems can make business rules and constraints explicit rather than relying solely on documentation or prompts.
- I learned how AI-DLC can be extended with domain-specific design rules, automated validation mechanisms called sensors, and approval gates to detect architectural violations.
- AI-DLC provides a continuous feedback loop through which architectural knowledge and design rules can be incorporated into the development workflow.
- I learned about Reverse Spec Flow, an approach that extracts specifications from existing code and uses them as a foundation for redesigning or modernizing systems.
- The speaker also discussed the potential of formal methods to detect inconsistencies in specifications before implementation, which could reduce unnecessary rework and AI token consumption.

The value of AI-DLC is not simply faster development. It can also allow engineers to spend more time on product value, domain modeling, architecture, and decision-making.

My biggest takeaway is that we should not simply automate implementation with AI. We should also design the development process itself to preserve architectural knowledge and ensure that important design constraints are respected.

### References

- [Presentation Slides — Junichi Kato](https://speakerdeck.com/j5ik2o/archcon2026)
- [AI-Driven Development Life Cycle Workflows — AWS](https://github.com/awslabs/aidlc-workflows)
- [Introducing Reverse Spec Flow — AWS Blog](https://aws.amazon.com/jp/blogs/news/aidm-introducing-reverse-spec-flow/)

## Self-Healing Architecture in Hybrid VM and Container Environments

**Seontaek Noh & Nobuyuki Morimoto (ZEAL)**

This session introduced a self-healing architecture that combines automated recovery, AI-assisted diagnosis, and human decision-making in hybrid VM and container environments.

### Key Takeaways and Reflections

- Incident response can be divided into three layers: automated recovery, AI-assisted diagnosis, and human decision-making.
- What I found particularly interesting was the decision-making framework based on business impact, service-level objectives (SLOs), and the reversibility of recovery operations.
- The appropriate level of automation depends not only on technical feasibility but also on the potential consequences of incorrect recovery actions.
- This also made me think about how fault injection could be used to evaluate recovery rates, mean time to recovery (MTTR), and the effectiveness of AI-assisted diagnosis.
- The goal is not to automate everything but to determine which responsibilities can safely be delegated to systems and AI.

My biggest takeaway is that designing automation also means designing its boundaries and deciding where human judgment must remain.

### References

- [ZEAL at Architecture Conference 2026](https://www.zdh.co.jp/topics/20261125/)
- [Site Reliability Engineering — Google](https://sre.google/sre-book/table-of-contents/)
- [Chaos Engineering Principles](https://principlesofchaos.org/)

## Building Authentication and Authorization Platforms In-House: Architecture for Business Growth

**Makoto Fuchiwaki (Nikkei), Takayuki Kurata (freee), Kazuya Shida (Linc'well), and Tatsuo Kudo (Authlete)**

This panel discussion explored how companies design authentication and authorization platforms by combining in-house development with external services based on their business and technical requirements.

### Key Takeaways and Reflections

- Building an authentication and authorization platform does not have to be a binary choice between building and buying. We can make these decisions at the component level.
- I learned how Authlete provides OAuth and OpenID Connect protocol processing and token management through APIs, allowing companies to retain control over their own authentication logic and user experience.
- Nikkei's case was particularly memorable to me. I had learned from *Clean Architecture* that high cohesion and low coupling make software easier to change. This session gave me a new perspective: these principles also make it easier to extract components, replace them with external services, or bring them back in-house.
- freee's case made me realize that architectural decisions can also address organizational challenges. By delegating specialized functionality to external services, companies can reduce their dependence on scarce in-house expertise and make their systems easier to maintain as team members change.
- Linc'well's case demonstrated how combining external services with in-house development can provide a consistent user experience across multiple products.

My biggest takeaway is that good architecture provides flexibility not only in software design but also in business decisions, resource allocation, and organizational change.

High cohesion and low coupling can therefore help organizations adapt to changes in both technology and their workforce.

### References

- [Authlete — Headless OAuth/OIDC Engine](https://www.authlete.com/ja/product)
- [OpenID Connect Core Specification](https://openid.net/specs/openid-connect-core-1_0.html)
- [OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [The Clean Architecture — Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## Data Products in the AI Era: Designing an Owner-Driven Self-Service Data Platform

**Yuya Matsubara (NTT DOCOMO)**

This session introduced NTT DOCOMO's ongoing transition from a centralized data platform to a data mesh architecture, focusing on domain ownership, self-service infrastructure, and AI-driven data engineering.

### Key Takeaways and Reflections

- As data volume and use cases grow, a centralized data team can become a bottleneck. This is not simply a technical problem but also an organizational one.
- Data mesh shifts responsibility to the domains that produce and understand the data. Data should be treated as a product, with clear ownership, quality standards, and business context.
- I learned about zero-copy data sharing, which allows consumers to access shared data without creating unnecessary physical copies. I also learned about the role of open table formats such as Apache Iceberg in improving interoperability across data platforms.
- What I found particularly interesting was the importance of incentives. Assigning ownership alone is not enough. Data owners should also be recognized for the value their data creates.
- The central data team's role shifts from directly processing data to enabling and supporting individual domains through a self-service platform and shared governance standards.
- AI can reduce the burden of data engineering, while deterministic CI checks and human approval help maintain reliability.
- I also learned how ontologies can help connect business terminology, data, workflows, and decision-making rules, providing richer context for AI systems and further automation.

My biggest takeaway is that building a scalable data platform requires designing not only technology but also organizational responsibilities and incentives.

Well-structured data and business context are becoming even more valuable in the age of AI.

### References

- [Data Mesh Principles and Logical Architecture — Zhamak Dehghani](https://martinfowler.com/articles/data-mesh-principles.html)
- [Apache Iceberg](https://iceberg.apache.org/)
- [Secure Data Sharing — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-sharing-intro)

## Building with Customers, Not for Each Customer: Organization and Design of Multi-Tenant SaaS

**Yuki Ozasa (CEO & VPoE, Anti-Pattern Inc.)**

This session explored how SaaS companies can collaborate closely with customers without falling into the trap of customer-specific development.

Drawing on the experience of building SaaSus Platform, the speaker discussed Forward Deployed Engineering (FDE), product decision-making, organizational design, and multi-tenant architecture.

### Key Takeaways and Reflections

- AI makes it faster and cheaper to build features, but the cost and responsibility of ensuring reliability, security, and long-term operation remain.
- Forward Deployed Engineers and product engineers complement each other. FDEs discover and validate customer needs, while product teams turn those insights into reusable product capabilities.
- Focusing too heavily on individual customer requests can lead to excessive customization, while focusing too much on an ideal product can create a gap between the product and the market.
- I found the concept of dynamic reteaming particularly interesting. Allowing product engineers to work directly on customer projects helps them understand customer problems and how their product creates value in practice.
- Customer-specific requirements can be addressed through configuration, public APIs, extensions, or separate implementations while maintaining a shared core product.
- I learned about bridge architecture through SaaSus Platform's approach of sharing computing resources while isolating tenant data at the AWS account level.
- Separating pricing from entitlements and using feature flags can help maintain flexibility without creating separate codebases for individual customers.

My biggest takeaway is that building with customers does not mean implementing everything they request. It means understanding their underlying problems and translating them into sustainable product value.

### References

- [SaaSus Platform](https://saasus.io/)
- [Anti-Pattern Engineering Blog](https://tech.anti-pattern.co.jp/)
- [Silo, Pool, and Bridge Models — AWS SaaS Lens](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/silo-pool-and-bridge-models.html)
- [SaaS Monetization Explorations — Yuki Ozasa](https://speakerdeck.com/oztick139/saas-monetization-explorations)

## The C4 Model: Building a Shared Understanding Between Humans and AI Agents

**Simon Brown**

This keynote explored how to communicate software architecture effectively through the C4 model, Diagrams as Code, Models as Code, and Architecture Decision Records (ADRs).

These practices can help humans and AI agents develop a shared understanding of system structures, boundaries, and architectural decisions.

### Key Takeaways and Reflections

- I learned that one way to understand the significance of an architectural decision is to consider the cost of changing it. Architecture diagrams help us not only communicate these decisions but also make them.
- Before this session, I was unfamiliar with the C4 model. I particularly liked the analogy of zooming in and out of a map. I sometimes mix different levels of abstraction when creating architecture diagrams, so separating them into distinct views was an insightful approach.
- I learned the difference between Diagrams as Code and Models as Code. Tools like Structurizr allow us to generate multiple views from a single architecture model, making it easier to maintain consistency.
- Beyond diagrams, I learned about arc42 and Simon Brown's Software Guidebook. These approaches help document architectural context, design principles, constraints, and other knowledge that cannot be easily understood from source code alone.
- Text-based architecture models and documentation can be maintained alongside source code, managed through version control, and made accessible to AI agents.
- Integrating documentation, diagrams, ADRs, and AGENTS.md can help humans and AI agents develop a shared understanding of the system.
- Architectural fitness functions can help continuously verify whether the implementation satisfies specified architectural characteristics and constraints.

My biggest takeaway is that architecture is not just about designing systems. It is also about making architectural knowledge explicit, shareable, and verifiable for both humans and AI agents.

### References

- [The C4 Model — Simon Brown](https://c4model.com/)
- [Structurizr](https://structurizr.com/)
- [Why "as code"? — Structurizr Documentation](https://docs.structurizr.com/as-code)
- [The Software Guidebook — Simon Brown](https://leanpub.com/documenting-software-architecture)
- [arc42](https://arc42.org/)
- [Architecture Decision Records](https://adr.github.io/)
- [AGENTS.md](https://agents.md/)

## Final Thoughts

Throughout the conference, I noticed several recurring themes:

- Designing systems that can adapt to change.
- Making implicit knowledge and decision-making criteria explicit.
- Defining clear responsibilities, interfaces, and boundaries.
- Understanding the relationship between software architecture and organizational structures.
- Establishing mechanisms to verify architectural decisions continuously.

As AI continues to accelerate software development, I believe that understanding what to build, why we build it, and how to maintain it over time will become increasingly important.

Rather than making software architecture less important, AI seems to be making the knowledge and decisions behind software architecture even more valuable.

I still have a lot to learn, but attending this conference for the second time gave me a valuable opportunity to reflect on my growth over the past year and discover new areas to explore.

Beyond the sessions, I really enjoyed visiting the sponsor booths and having technical conversations with people from different companies. It was exciting to exchange ideas, discuss technologies, and learn from people with different backgrounds and areas of expertise.

I had a great time at the conference, and I'm already looking forward to attending again next year!
