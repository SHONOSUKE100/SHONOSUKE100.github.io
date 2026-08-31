---
title: "Why Abstracting 'Because They Look Similar' Is Dangerous"
locale: en
description: "DRY and SRP achieve true synergy when abstractions align with shared knowledge and common reasons for change."
publishedAt: 2026-07-25
category: "software-design"
tags: ["dry", "srp", "architecture"]
draft: false
---

When we see similar-looking code, we often feel an urge to extract a common function, class, or component. This instinct is understandable, especially when DRY (Don't Repeat Yourself) is treated as a rule that forbids any duplication. However, just looking similar is not evidence that two pieces of code should be hidden behind the same abstraction.

The challenge in design lies in distinguishing between "duplicated text" and "duplicated knowledge."

## DRY Is a Principle About "Knowledge"

While DRY is often abbreviated as "don't duplicate code," a more useful interpretation is that "every piece of knowledge must have a single, unambiguous, authoritative representation within a system." If the same business rule is expressed in multiple places, you will have to update all of them when making future changes. Forgetting to update even one leads to inconsistencies and bugs.

That doesn't mean every pair of similar-looking operations represents the same knowledge. Two flows might happen to share the same sequence of steps while serving different business rules, different users, or different policies. Their similarity might be temporary or purely coincidental.

Extracting an abstraction prematurely hides these differences, turning what should be a simple change into a chore of adjusting a shared, bloated, generic interface.

## SRP Is a Principle About "Reasons for Change"

The Single Responsibility Principle (SRP) is not a mandate to make every class microscopic or to ensure every module has only one method. A more practical definition is that "a module should have one, and only one, reason to change, and should be responsible to a single actor."

An actor refers to a person, team, customer group, or organizational role with a need that drives changes. If a single module must be changed for multiple unrelated actors, a fix for one concern risks breaking another. The module becomes an "intersection" of policies that should evolve independently.

By separating modules based on their reasons for change, you protect each concern from unrelated changes elsewhere.

## DRY and SRP Complement Each Other

These principles point out different risks:

- DRY prevents the same knowledge from being scattered across multiple places.
- SRP prevents unrelated knowledge from being coupled within a single module.

Tension arises when we couple code that merely looks similar through a shared abstraction. The resulting helper functions tend to accumulate configuration options, conditional branches, and exception handling as their callers diversify. While you might reduce the number of duplicated lines, you end up creating a component with many conflicting reasons to change.

Before extracting common code, ask yourself if it represents a stable concept independent of the callers' business logic. Pure utilities with clear, enduring contracts are good candidates. Common shapes produced by different policies usually are not.

## When Boundaries Are Blurry, Accept Temporary Duplication

Temporary duplication is far cheaper than the wrong abstraction. Keeping code duplicated allows different use cases to evolve independently until the behavior that truly needs to be shared becomes clear. Only when the same knowledge and the same reason for change are obvious should you extract them—based on solid reasoning, not appearance.

This is especially important when using AI coding tools. AI agents can quickly identify superficial patterns, but they cannot infer all domain boundaries unless the context is made explicit. A codebase should not just be compact; it should be kept in a way that the reasoning behind separation and sharing remains understandable.

## Conclusion

Systems remain valuable because they can be changed. DRY and SRP help maintain that changeability when applied to knowledge, actors, and future decisions, rather than just lines of code. A great abstraction protects a stable concept; it does not simply gather code that happens to look similar today.

The original article was published on [Medium](https://medium.com/@xiangchitian26/why-they-look-similar-is-a-dangerous-reason-to-abstract-19a8384bb24d).
