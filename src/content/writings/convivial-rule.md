---
title: "To Avoid Being Used by Rules"
locale: en
description: "Rule design: creating, reviewing, and letting go"
publishedAt: 2026-08-29
category: "design"
tags: ["conviviality", "design", "rule"]
draft: false
---

## Rule Design: Creating, Reviewing, and Letting Go

In organizations, there are sometimes rules for which no one can explain the reason.

"Because this has always been the procedure," "Because we’ll be in trouble if something happens," "Because it’s a rule, so please follow it." When told this, it is difficult to question further. There may have been a pressing reason when the rule was first created. However, even as circumstances change, only the rule remains, and before we know it, following the rule itself has become the job.

Rules are originally tools to solve problems. We want to stabilize quality. We want to prevent accidents. We want to enable people from different standpoints to collaborate. These objectives come first, and rules are created as a means to achieve them.

However, when rules are used for a long time, the relationship between means and ends can become inverted. Instead of rules helping human judgment, humans begin to act simply to maintain the rules.

Are we using rules? Or are we being used by them?

In this article, I will explore rules through three actions: "creating," "reviewing," and "letting go." The goal is not simply to reduce the number of rules. Rather, it is to create a state where humans can understand the purpose, make judgments, and adapt their relationship with rules according to the situation, all while maintaining necessary control.

## 1. Creating

### What Do Rules Solve?

In *Rule Design: Maximizing Organizational Performance*, Yuki Anzai and Tasuku Mizuno divide organizational rules into "rules of control" and "rules of creation."

Rules of control are used to prevent problems and maintain order and reproducibility. They distinguish between what is permitted and what is forbidden, and define necessary procedures and responsible parties. They are indispensable in areas where variance in judgment can lead to serious damage, such as compliance, accounting, information security, and safety management.

Rules of creation are used to confront problems for which the correct answer is not yet known. Instead of avoiding failure entirely, they define an acceptable range of loss and allow for small-scale experimentation within that boundary. They delegate roles and authority to the front lines, updating judgments as results are shared.

If rules of control clarify "what to do and what not to do," rules of creation can be said to clarify "within what scope and what can be tried."

For example, a system that requires multiple approvals every time a new project is launched aims to prevent major failures. However, increasing the number of approvers does not necessarily reduce failures. Reviews can become a mere formality, and accountability can become diffused. Meanwhile, the frequency of experimentation and the speed of decision-making tend to drop.

With rules of creation, boundaries are set—such as "under 300,000 yen," "no personal information handled," or "share results within two weeks"—allowing the front lines to experiment using their own judgment within that scope. Even in organizations that appear free, there are agreements such as "listen to differing opinions," "test small," "do not hide failures," and "the decision-maker must reflect on the results." Instead of prescribing detailed actions, they define how judgments should be made.

This is not a question of which is superior, control or creation. Control is suited for work where reproducibility of procedures is critical. Creation is suited for work with high uncertainty that requires adapting to change. Even within the same organization, accounting processes may require control, while new initiatives require creation.

The problem arises when we try to solve every issue with rules of control without first verifying the nature of the problem. Every time something happens, we add more approvers, add more reporting items, and ban exceptions. While the organization may appear safer, it may actually be losing its speed of judgment and its ability to discover problems.

### Designing with the Intention to Redesign

It is difficult to create a perfect rule from the start. At the time of creation, we do not know what the future environment will look like or how people will react. Nevertheless, we design systems under the assumptions that "these conditions will continue" and "if we put this rule in place, people will act this way."

Adaptive institutional design, introduced by Takahiro Ezaki in *Rule Design Deciphered Through Mathematical Model Thinking*, starts from the premise that the world cannot be perfectly predicted or controlled. What is important is not just getting predictions right, but ensuring that the system can be changed when predictions turn out to be wrong.

When creating a rule, first define the goal and identify possible options. Instead of immediately jumping to prohibitions or mandates, consider what you want to achieve and whether there are non-rule alternatives. There is no need to regulate human behavior in detail for problems that can be solved through warning signs, education, system-level controls, or information sharing.

Next, assemble the basic rule. Decide who is targeted, which judgments should be standardized, and from what point onward decisions should be left to the front lines. At this stage, also write down the assumptions required for the rule to function.

For example, suppose you are creating a rule for using generative AI services within a company. A rule like "use only approved services" assumes that the approval process is fast enough and that the reviewers understand the services the front lines actually need.

If new services emerge one after another and reviews take months, that assumption collapses. The more people follow the rule, the more work grinds to a halt, potentially driving users to unofficial workarounds (shadow IT). This is not simply a problem of "low employee awareness." It is highly likely that the design of the rule no longer fits the changing environment.

Therefore, we should incorporate the following elements from the very beginning:

| Element to Design | Example: Generative AI Usage Rule |
| --- | --- |
| Goal | Enable the use of generative AI in business operations while protecting confidential information |
| Assumptions | Reviews can be completed in a short period of time |
| Metrics to Observe | Number of days for review, number of exception requests, number of incidents, reports of unofficial usage |
| Triggers for Update | Review period exceeds a certain number of days, exception requests continuously increase |
| Response After Trigger | Introduce simplified reviews for low-risk use cases, revise approval criteria |
| Conditions for Suspension/Abolition | The goal can be achieved through other technical measures, or the target services are no longer used |

Decide not only on the procedures for normal operations but also on how to respond when assumptions fail. If a major incident occurs, temporarily narrow the scope of use. Once the situation stabilizes and safe operations are confirmed, return the judgment to the front lines.

This is easy to understand if we think of it like software. A system where you only write the happy path, without monitoring, exception handling, or rollbacks, would be too terrifying to run. Yet, when it comes to organizational rules, we design them under the assumption that they will continue to function perfectly forever. It is precisely systems that deal with humans and society that need mechanisms to detect failures and roll back if necessary.

## 2. Reviewing

### When Rules Become the Organizational Norm

Edgar Schein viewed organizational culture through three levels: visible artifacts and behaviors, espoused values, and underlying, unconscious assumptions.

Applying this framework to rules, we can see that rules not only reflect organizational culture but can also reinforce underlying assumptions through their operation.

Rules initially appear as visible artifacts, such as regulations or approval workflows. They are accompanied by explanations like "to protect quality" or "to ensure fair judgment." As these operations are repeated, ideas like "acting without a manager's approval is dangerous" or "allowing exceptions will disrupt order" can become unquestioned assumptions.

Once things reach this stage, reviewing a rule is no longer a simple procedural change. This is because questioning the rule is perceived as an act of denying the organization's values or past decisions.

Discrepancies can also arise between stated goals and actual behavior. An organization might champion "welcoming challenges" while maintaining multi-stage approvals to avoid failure. It might say "we trust the front lines" while demanding detailed reports. Even if the espoused values remain, daily actions are driven in a different direction by the rules.

Ivan Illich described the turning point where the expansion of institutions or technology exceeds its original benefits and begins to undermine its very purpose as the "second watershed." It is the kind of inversion where transportation ceases to merely assist movement, and instead, society as a whole begins to spend its time and space maintaining transportation systems.

Something similar happens with rules. Rules created to assist judgment end up stripping away the opportunity to judge. Forms designed to make accident reporting easier become so complex that they discourage reporting. Criteria meant to ensure fair judgment become so granular that individual circumstances can no longer be considered.

Being "used by rules" does not only refer to a state of having many prohibitions. It means not knowing what a rule is for, not being able to choose other methods, and not being able to propose changes even when something feels wrong. When people lose these three things—purpose, options, and participation in change—they can no longer choose their relationship with rules.

### Making Review a System

Simply writing "review periodically" usually results in no review at all. This is because who is responsible for the review remains ambiguous, and daily operations take priority. What is needed is to define "under what conditions, to what extent they must change, who will review, and which rule will be examined."

In this article, I refer to the rules that govern the procedures for changing rules as "meta-rules." Meta-rules include the timing of reviews, who can propose changes, how exceptions are handled, who decides on changes, conditions for temporary suspension, and conditions for abolition.

What is important here is not to make compliance rate the sole metric of success. If you strengthen surveillance and penalties, superficial compliance rates might rise. However, if problems are hidden, responses to exceptions are delayed, and people can only act within prescribed boundaries, the organization is losing other vital capabilities.

When evaluating rules, we need to look at least at three outcomes.

First, was the goal achieved? If it is a rule to reduce accidents, we should look at whether accidents or damages actually decreased, not just the submission rate of reports.

Second, how much burden did the operation create? Check the time required for approvals, the number of input fields, the volume of inquiries, and the number of exception requests.

Third, what happened to the capabilities of the people and the organization? Look at whether the number of people who can make independent judgments has increased, or if a state of dependency—where people cannot act without a rule—has intensified.

### Does It Support Human Agency?

The concepts of autonomy, competence, and relatedness from Self-Determination Theory provide clues for thinking about how rules affect humans.

Autonomy does not mean being free to decide anything; it is the feeling that one is acting based on one's own will. Even with rules imposed from the outside, autonomy can be maintained if people understand their purpose and accept them with personal conviction.

Competence refers to the feeling that one's judgments and actions lead to results, and that one can exercise and develop necessary abilities. Relatedness is the feeling of being accepted by others and collaborating within a framework of trust.

Good rules support these three needs as much as possible while establishing necessary constraints. Even if a rule successfully enforces compliance, if the people involved cannot understand the reasons, cannot exercise their abilities, and are constantly monitoring one another, that rule may be weakening human activity.

What is crucial is not to view rules as programs designed to manipulate humans as desired. Rules are also scaffolds for people to make judgments and collaborate together. There must be room left for people to participate in their creation, raise objections, redesign them according to the situation, and let them go when they have served their purpose.

## 3. Letting Go

### A Company That Reduces Detailed Rules and Delegates Judgment

Reducing pre-approvals for expenses. Not having the company uniformly specify the number of vacation days employees can take. Not always requiring managers to make critical decisions.

Wouldn't such a company fall into chaos?

Netflix has reduced many pre-approvals and detailed regulations, including those for expenses and vacation. This philosophy was introduced in *No Rules Rules* by Reed Hastings and Erin Meyer, and is carried forward in Netflix's current Culture Memo.

However, this does not mean Netflix has abandoned all control or responsibility. The shared principle regarding expenses is brief:

> Act in Netflix’s best interests.

Fixed budgets offer clarity. Within that limit, employees can spend with peace of mind. However, when the budget amount becomes the standard for spending, people begin to judge based on "is it under the limit?" rather than "is it truly necessary?" In some cases, spending the remaining budget becomes the goal itself.

Under Netflix's principle, simply staying within a certain dollar amount does not count as making a judgment. The individual must think for themselves whether the expenditure is necessary for the company, whether there is a better way, and whether they can explain it to their colleagues. By reducing detailed rules, the responsibility of judgment actually becomes heavier.

Here lies a slightly counterintuitive aspect of "No Rules." While it seems to eliminate rules, it actually relies on a strong, shared understanding of purpose and context. The more you reduce detailed regulations, the more clearly you must define what you are aiming for, what you value, and what level of risk is acceptable.

"No Rules" does not mean the absence of control. It is a transition from a state where behavior is controlled by detailed regulations to a state where behavior is aligned through shared context and human judgment.

### Conditions Required to Reduce Control

What Netflix has emphasized before reducing control is talent density and candor. And what is required of managers in place of detailed control is sharing the context necessary for good judgment.

In Netflix's terms, talent density refers to a state where highly capable people work and collaborate effectively with one another. It also becomes important that they can understand the purpose, make decisions in uncertain situations, and explain the reasoning behind them.

However, Netflix is also known for its rigorous talent policy of maintaining talent density through hiring and talent turnover. If other organizations adopt this philosophy, it is dangerous to understand it simply as "eliminating low performers." If a culture of hiding failures and viewing colleagues as competitors emerges, it will destroy the candor that is required next.

We should separate explaining Netflix's system from deciding what to adopt in our own organizations. Beyond hiring, there are ways to foster an organization's decision-making capacity through information sharing, learning opportunities, role design, and decision-making experience.

Candor serves as a mechanism to correct free judgments. If there are detailed rules, you can check "whether procedures were followed." If you reduce procedures, people must be able to point out to each other "whether that judgment truly aligns with the objective."

Candor is not the same as saying whatever comes to mind. It addresses actions and judgments rather than personality, provides evidence, and is delivered in a way that helps the other person improve. If employees cannot voice disagreement to their managers, substantial control remains in place even if authority is decentralized.

Context includes the organization's goals, priorities, budgets, risks, past failures, and legal or ethical constraints. Asking employees to "make your own decisions" while managers hold all the information is not delegation; it is closer to abandonment.

The role of the manager shifts from approving every action to providing the materials necessary for good judgment. Netflix's slogan "Context, not Control" represents this shift. However, this does not mean managers do not need to be involved in the work. They must intervene in situations where serious damage or ethical issues could arise, and provide advice and feedback on a daily basis.

### Who Decides in the End?

When authority is handed to the front lines, another problem can arise. In the process of listening to everyone's opinions, no one is able to make a decision. Consensus-building takes time, and accountability for the results becomes ambiguous.

At Netflix, an "Informed Captain" is designated for each major decision. The person responsible for the project becomes the decision-maker, rather than a manager deciding simply because of their rank.

An Informed Captain is not someone who decides arbitrarily. They gather necessary information, listen to the opinions of experts and stakeholders, and actively seek out dissenting views. Only then do they make the final judgment. After the results become clear, they reflect on what went well and what went wrong.

This mechanism lies between top-down centralization and unanimous consensus. It decentralizes decision-making to the front lines while keeping "who decides" completely clear.

Freedom does not mean acting however one pleases. It is the ability to use one's own judgment within a shared purpose and context. Responsibility, too, does not merely mean punishing individuals who fail. It means listening to necessary opinions, explaining one's reasoning, verifying results, and changing subsequent judgments if errors are found. It is about taking ownership of this entire process.

Freedom without context is abandonment. Responsibility without authority is a shifting of the burden. For freedom and responsibility to coexist, information, authority, and necessary resources must be handed over together.

### Do Not Import Netflix's System As-Is

Reading about Netflix makes one want to immediately eliminate vacation policies and approval workflows. However, mimicking only the surface of the system is dangerous.

In *The Culture Map*, Erin Meyer argues that disagreeing with managers, negative feedback, and decision-making methods differ by country and region. However, we must also avoid applying country-level tendencies directly to individuals or specific organizations. Even within the same country, culture varies by organization and team.

In an organization where it is difficult to directly voice disagreement to managers, suddenly declaring "let's speak candidly" or "let's make our own decisions" is unlikely to work. Candor can turn into aggressive language, and delegation can become an abandonment of responsibility by managers.

What is needed is not Netflix's system itself, but establishing the conditions that make the system work in a way that fits your own organization. If it is difficult to disagree in public, allow dissenting views to be raised in 1-on-1s or in writing. If you delegate judgment, clearly specify the decision-maker and advisors. If you reduce expense approvals, share the company's financial situation and decision criteria beforehand. Test in a small scope first, and ensure you can roll back if problems arise.

Adapting to culture does not mean giving up on change. It means finding a way for candor and delegation to function within your own organization. Here, too, the concept of adaptive institutional design is useful.

### Criteria for Letting Go of Rules

Deciding whether to abolish a rule cannot be based solely on "because it's a hassle" or "because we want to be a free organization." At the very least, we should verify the following questions:

1. Does the problem that the rule was intended to solve still exist?
2. Do the benefits of the rule outweigh its operational costs, such as approval time and workload?
3. Have exception requests or workarounds become normalized, creating a gap between reality and the rule?
4. Can the goal be achieved through less burdensome methods, such as education, information sharing, or technical controls?
5. Is the damage that might occur if the rule is abolished acceptable or recoverable?
6. Before full abolition, can we test it by narrowing the scope or suspending it temporarily?
7. Is it decided what to observe after abolition, and who will respond if problems arise?

"Letting go" is not doing nothing. Confirming the function that the rule served, transitioning it to another method, and observing the results are all part of the design.

## What Remains Beyond Rules

We do not need to let go of all rules. In safety, compliance, information security, prevention of discrimination and harassment, and protection of rights, we must clearly define minimum prohibitions, responsible parties, rights, and responses to incidents. However, even in these areas, controlling every action with detailed regulations is not always the best approach.

The question we should ask is not whether there are too many or too few rules. Rather, does the problem require control or creation? Does it require detailed procedures, or can it be handled through principles and judgment? Do the assumptions of the current rules still hold true? While the rules achieve their goals, what kind of burdens or decline in capabilities are they causing?

A good rule is not one that is followed forever. It is a rule that people create as needed, review according to the situation, and let go of when its role is finished.

Beyond following the rules, do human judgment, growth, trust, and collaboration remain? If only compliance with the rules remains, then it is time to rebuild our relationship with our tools.

## References

1. Yuki Anzai and Tasuku Mizuno, *Rule Design: Maximizing Organizational Performance*, Discover 21, 2026.
2. Takahiro Ezaki, *Rule Design Deciphered Through Mathematical Model Thinking: Science of Organizations and Human Behavior*, Socym, 2022.
3. Reed Hastings and Erin Meyer, *No Rules Rules: Netflix and the Culture of Reinvention*, translated by Nami Hijikata, Nikkei Publishing, 2020.
4. Erin Meyer, *The Culture Map: Breaking Through the Invisible Boundaries of Global Business*, supervised translation by Megumi Taoka, translated by Takeshi Higuchi, Eiji Press, 2015.
5. Hisato Ogata, *Convivial Technology: Toward a Society Where Humans and Technology Coexist*, BNN, 2021.
6. Ivan Illich, *Tools for Conviviality*, translated by Kyoji Watanabe and Risa Watanabe, Chikumashobo, 2015.
7. Edgar H. Schein and Peter A. Schein, *Organizational Culture and Leadership*, 5th Edition, Wiley, 2016.
8. Warren E. Walker, S. Adnan Rahman and Jonathan Cave, “Adaptive Policies, Policy Analysis, and Policy-making,” *European Journal of Operational Research*, Vol. 128, No. 2, 2001, pp. 282–289.
9. Richard M. Ryan and Edward L. Deci, “Self-Determination Theory and the Facilitation of Intrinsic Motivation, Social Development, and Well-Being,” *American Psychologist*, Vol. 55, No. 1, 2000, pp. 68–78.
10. Netflix, “Netflix Culture Memo,” https://jobs.netflix.com/culture
