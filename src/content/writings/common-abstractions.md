---
title: "Why “They Look Similar” Is a Dangerous Reason to Abstract"
locale: en
description: "DRY and SRP work together when abstraction follows shared knowledge and shared reasons for change."
publishedAt: 2026-07-25
category: "software-design"
tags: ["dry", "srp", "architecture"]
draft: false
---

Similar code often creates an urge to extract a shared function, class, or component. That instinct is understandable, especially when DRY is treated as a rule against all repetition. But visual similarity alone is not evidence that two pieces of code belong behind the same abstraction.

The difficult part of design is separating duplicated text from duplicated knowledge.

## DRY is about knowledge

DRY is often shortened to “do not repeat code,” but its more useful interpretation is: give each piece of knowledge one authoritative representation. If the same business rule is expressed in several places, a future change may require updating all of them. Missing one update creates inconsistency and bugs.

That does not imply that every pair of similar-looking operations expresses the same knowledge. Two flows can share a sequence of steps while serving different business rules, different users, or different policies. Their resemblance may be temporary or accidental.

Extracting them too early can hide that distinction and turn a simple change into a negotiation over a shared, increasingly generic interface.

## SRP is about the reason to change

The Single Responsibility Principle is not a command to make every class tiny or to give every module only one method. A more practical definition is that a module should have one reason to change, or be responsible to one actor.

An actor can be a person, team, customer group, or organizational role whose needs drive a change. When one module must change for several unrelated actors, a modification for one concern can disrupt another. The module has become a meeting point for policies that should evolve independently.

Separating modules by their reasons for change protects each concern from unrelated changes elsewhere.

## DRY and SRP are complementary

These principles point at different risks:

- DRY prevents the same knowledge from drifting across multiple locations.
- SRP prevents unrelated knowledge from being coupled inside one module.

The tension appears when a shared abstraction combines code that only looks alike. The resulting helper often gains configuration options, conditionals, and exceptions as the callers diverge. It may remove duplicated lines while creating a component with many conflicting reasons to change.

Before extracting shared code, ask whether it represents a stable idea that is independent of the callers' business logic. A pure utility with a clear, durable contract is a good candidate. A common shape produced by different policies is usually not.

## Duplicate briefly when the boundary is uncertain

Temporary duplication can be cheaper than a wrong abstraction. Repeated code allows different use cases to evolve independently until the genuinely shared behavior becomes obvious. Once the same knowledge and the same reason for change are visible, extraction is based on evidence rather than on appearance.

This is particularly important when working with AI coding tools. Agents can identify superficial patterns quickly, but they cannot infer every domain boundary unless that context is explicit. A codebase should make the reasons behind separation and sharing understandable, not merely compact.

## Conclusion

Systems remain valuable because they can change. DRY and SRP help preserve that changeability when they are applied to knowledge, actors, and future decisions rather than to line counts alone. Good abstractions protect a stable idea; they do not simply collect code that happens to look similar today.

Originally published on [Medium](https://medium.com/@xiangchitian26/why-they-look-similar-is-a-dangerous-reason-to-abstract-19a8384bb24d).
