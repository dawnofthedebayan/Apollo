---
title: "Goodhart's Law: When a measure becomes a target"
type: evergreen
status: seedling
certainty: hypothesis
tags:
  - evergreen
  - area/general
  - maturity/seedling
  - mental-models
  - systems-thinking
created: 2026-05-09
last-updated: <% tp.date.now("YYYY-MM-DD") %>
sources: []
related: ["The Cobra Effect", "Campbell's Law", "Proxy Fallacy"]
llm-summary: "Goodhart's Law states that once a metric is used as a primary goal or target, people will game the system to achieve it, destroying the metric's value as a true measure of success."
---

# Goodhart's Law: When a Measure Becomes a Target

> [!NOTE] Evergreen — One idea per note. Write in your own words. Never copy-paste.

---

## 💡 The Core Idea

**Goodhart’s Law:** When a measure becomes a target, it ceases to be a good measure.

Originally formulated by British economist Charles Goodhart, it highlights that any statistical relationship will break down once it is used for policy purposes or tied to incentives.

---

## 🧠 Elaboration

Metrics are usually just **proxies** for complex, abstract goals (e.g., "lines of code" is a proxy for "developer productivity"). When there is no pressure, a proxy naturally correlates with the goal. 

However, humans are highly adaptable and naturally optimize for their incentives. Once a metric is turned into a target (especially one tied to rewards, promotions, or punishments), people will optimize for the *metric itself* rather than the *underlying goal*. This leads to "gaming the system." The alignment between the proxy metric and the actual goal degrades, rendering the metric useless—and often actively harmful.

---

## 📐 Evidence & Examples

- **Call Center Metrics:** A call center wants better customer service, so they measure "Average Handle Time" (shorter calls = better). Agents, wanting to hit their target, begin hanging up on customers with complex issues to keep their average time down. The metric improved; customer satisfaction plummeted.
- **Soviet Nail Factories:** A classic historical anecdote. When a state-owned factory was given a target based on the *weight* of nails produced, they made a few giant, useless nails. When the target was changed to the *quantity* of nails, they produced thousands of tiny, microscopic nails.
- **Academic Publishing:** The goal is high-quality scientific progress. The metric is "number of peer-reviewed papers published" (Publish or Perish). This leads to researchers slicing data into the smallest publishable units, p-hacking, and a replication crisis.

---

## ⚡ Implications & Applications

- **Pair Metrics with Counter-Metrics:** Never rely on a single number. If you measure speed, you must also measure quality. (e.g., measure "lines of code" alongside "number of bugs introduced").
- **Keep Metrics as Observations, Not Targets:** Use data to understand the health of a system, but hesitate to directly tie compensation or strict KPIs to highly specific proxy metrics.
- **Rotate Targets:** Frequently change the metrics you use to evaluate performance so individuals cannot settle into a pattern of gaming a single system.
- **Measure the "Why", not just the "What":** Incorporate qualitative feedback and human judgment instead of relying solely on automated quantitative dashboards.

---

## ⚔️ Counterarguments & Limits

- **Perfect Proxies:** Goodhart's law does not apply if the metric is physically inseparable from the goal. For example, if the goal is "lift 100 lbs," measuring the weight on the barbell is a perfect metric that cannot be gamed without achieving the actual goal.
- **Ignorance of the Target:** If the subjects being measured are completely unaware of the metric, they cannot alter their behavior to game it (though ethical and privacy concerns arise here).

---

## 🔗 Linked Notes

**Supports:**
- Systems Thinking limits
- The Principal-Agent Problem
- Unintended consequences in management

**Contradicts:**
- Strict Taylorism (Scientific Management)
- "What gets measured gets managed" (Peter Drucker) - *Note: Drucker's quote often ignores the reality of gaming the system.*

**Is supported by:**
- The Cobra Effect (Perverse incentives)
- Campbell's Law (The sociological equivalent in education and public policy)

---

## 📚 Sources

- Charles Goodhart (1975) - Originally applied to UK monetary policy.
- Marilyn Strathern (1997) - Anthropologist who generalized the phrasing into the popular: *"When a measure becomes a target, it ceases to be a good measure."*

---

## 📝 Revision Log

| Date | Change |
|------|--------|
| 2026-05-09 | Initial draft |

---

## 🤖 LLM Prompt Seed

> Given this idea, find contradictions, strengthen the argument, and suggest related concepts: Goodhart's Law and how optimization degrades proxy metrics.