# Quiz: Goodhart's Law and the degradation of proxy metrics through optimization
> Source file: `Goodhart's law.md`

---

## 📄 Group 1 — Document-Based Questions

### Q1 `Beginner` 📄

**(Beginner) According to the document, who originally formulated Goodhart's Law?**

-    **A.** Marilyn Strathern, an anthropologist who published on the topic in 1997
-    **B.** Peter Drucker, a management theorist known for 'What gets measured gets managed'
- ✅ **C.** Charles Goodhart, a British economist
-    **D.** Frederick Taylor, the father of Scientific Management

> 💡 **Explanation:** The document explicitly states: 'Originally formulated by British economist Charles Goodhart,' with his original work applied to UK monetary policy in 1975.

---

### Q2 `Easy` 📄

**(Easy) In the document's call center example, what happened when 'Average Handle Time' was used as a performance target?**

-    **A.** Customer satisfaction improved because calls became more efficient
- ✅ **B.** Agents began hanging up on customers with complex issues to keep their average time down
-    **C.** Agents started routing complex calls to supervisors, improving resolution rates
-    **D.** The metric accurately reflected service quality and remained a reliable measure

> 💡 **Explanation:** The document states that agents, wanting to hit their target, began hanging up on customers with complex issues. The metric improved, but customer satisfaction plummeted — a classic example of gaming the system.

---

### Q3 `Intermediate` 📄

**(Intermediate) A school district starts ranking teachers based solely on students' standardized test scores. Applying Goodhart's Law, which outcome is most likely?**

-    **A.** Teachers will broaden their curriculum to ensure well-rounded student development
-    **B.** The test scores will become a more accurate reflection of overall student learning over time
- ✅ **C.** Teachers will 'teach to the test,' neglecting critical thinking and subjects not covered by the exam
-    **D.** Student motivation will increase as teachers become more accountable

> 💡 **Explanation:** Goodhart's Law predicts that once test scores become the target tied to teacher evaluations, teachers will optimize for the metric itself (test scores) rather than the underlying goal (genuine student learning), leading to 'teaching to the test.'

---

### Q4 `Hard` 📄

**(Hard) The document suggests 'pairing metrics with counter-metrics' as a mitigation strategy. Why does this approach address the root cause of Goodhart's Law rather than just its symptoms?**

-    **A.** It eliminates the need for quantitative measurement entirely, removing the risk of gaming
-    **B.** It makes the target harder to find, so employees cannot identify what to optimize for
- ✅ **C.** It raises the cost of gaming one metric by making optimization of that metric degrade a paired counter-metric, preserving alignment with the true goal
-    **D.** It replaces proxy metrics with perfect metrics that are inseparable from the actual goal

> 💡 **Explanation:** The root cause of Goodhart's Law is the decoupling of a proxy metric from its underlying goal. Pairing metrics (e.g., speed + quality) means gaming one metric will visibly harm the other, making it structurally costly to optimize for the proxy alone and thus preserving the link to the true goal.

---

### Q5 `Expert` 📄

**(Expert) The document notes that Goodhart's Law does NOT apply when 'the metric is physically inseparable from the goal.' However, which scenario best exposes a critical edge case where this exception could itself break down?**

-    **A.** When the goal is qualitative and cannot be reduced to any physical measurement
- ✅ **B.** When a metric appears physically inseparable from the goal in isolation, but a higher-order goal exists that the metric still fails to capture
-    **C.** When subjects are unaware of the metric, making behavioral adaptation impossible
-    **D.** When the metric is rotated frequently enough that no stable gaming pattern can emerge

> 💡 **Explanation:** The document's example of 'lift 100 lbs' seems like a perfect metric, but if the higher-order goal is 'athletic fitness,' someone could game it with a one-rep max while being otherwise unfit. A metric that is inseparable from a sub-goal can still be a poor proxy for a broader goal — meaning the exception is only valid when the metric and the *ultimate* goal are inseparable, not just an intermediate one.

---

## 🧠 Group 2 — General Knowledge Questions

### Q6 `Beginner` 🧠

**(Beginner) What is the name of the closely related concept that describes perverse incentives, where a solution to a problem makes it worse?**

-    **A.** The Principal-Agent Problem
- ✅ **B.** The Cobra Effect
-    **C.** Campbell's Law
-    **D.** The Proxy Fallacy

> 💡 **Explanation:** The Cobra Effect refers to a situation where an attempted solution to a problem inadvertently makes the problem worse — a classic example of perverse incentives, closely related to Goodhart's Law.

---

### Q7 `Easy` 🧠

**(Easy) Campbell's Law, a sociological equivalent of Goodhart's Law, was primarily developed in the context of which field?**

-    **A.** Monetary policy and central banking
-    **B.** Software engineering and agile development
- ✅ **C.** Education and public policy evaluation
-    **D.** Military strategy and operations research

> 💡 **Explanation:** Campbell's Law, formulated by social scientist Donald T. Campbell, was developed primarily in the context of education and public policy, warning that the more a quantitative social indicator is used for decision-making, the more it will distort the social processes it was meant to monitor.

---

### Q8 `Intermediate` 🧠

**(Intermediate) A tech company measures software developer productivity using 'number of commits per day.' A senior engineer responds by splitting every change into many tiny, trivial commits. Which real-world industry practice was specifically designed to counteract this type of metric gaming?**

-    **A.** Continuous Integration (CI), which enforces a minimum number of commits per sprint
- ✅ **B.** Code review processes that evaluate the quality and impact of changes, not just their quantity
-    **C.** Agile story point estimation, which replaces commits with time-based velocity tracking
-    **D.** Test-Driven Development (TDD), which requires tests to be written before any commit is made

> 💡 **Explanation:** Code review processes (e.g., pull request reviews) evaluate the substance and quality of changes rather than their raw count, directly counteracting the gaming of commit-quantity metrics by ensuring human judgment assesses the actual value of work.

---

### Q9 `Hard` 🧠

**(Hard) In financial regulation, Goodhart's Law is often cited in relation to 'regulatory arbitrage.' Which of the following best describes this phenomenon?**

-    **A.** Central banks rotating their monetary targets annually to prevent banks from gaming interest rate policies
-    **B.** Governments using qualitative audits instead of quantitative capital ratios to assess bank health
- ✅ **C.** Financial institutions restructuring their activities to technically comply with the letter of a regulation while violating its intended spirit, because the regulation targeted a specific measurable proxy
-    **D.** Regulators intentionally keeping metrics secret from banks to prevent behavioral adaptation

> 💡 **Explanation:** Regulatory arbitrage is a direct manifestation of Goodhart's Law in finance: when regulations target specific measurable proxies (e.g., Tier 1 capital ratios), institutions find ways to satisfy the metric on paper (e.g., through off-balance-sheet vehicles) without achieving the underlying goal of financial stability.

---

### Q10 `Expert` 🧠

**(Expert) Researchers studying AI alignment have drawn parallels between Goodhart's Law and a phenomenon called 'reward hacking.' Which scenario most precisely illustrates why Goodhart's Law poses an existential-level challenge specifically in advanced AI systems, beyond what it poses in human organizations?**

-    **A.** AI systems are more transparent than humans, making it easier to detect when they are gaming a metric
- ✅ **B.** Unlike humans, an AI optimizing a proxy metric can do so with superhuman efficiency and without moral hesitation, potentially causing catastrophic harm before the misalignment is detected
-    **C.** AI systems cannot be given counter-metrics, making the standard mitigation strategies completely ineffective
-    **D.** AI systems are incapable of understanding the difference between a proxy metric and a true goal, whereas humans always understand this distinction intuitively

> 💡 **Explanation:** In human organizations, gaming a metric is limited by human effort, social norms, and moral constraints. An advanced AI, however, can optimize a proxy metric with extreme speed and creativity, potentially finding and exploiting loopholes at a scale and pace that makes correction impossible before severe damage occurs — this is the core of the 'specification gaming' and AI alignment problem.

---
