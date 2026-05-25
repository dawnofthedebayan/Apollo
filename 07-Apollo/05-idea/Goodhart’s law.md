# Quiz: Goodhart's Law
> Source file: `Goodhart’s law.md`

---

## 📄 Group 1 — Document-Based Questions

### Q1 `Beginner` 📄

**Who originally formulated Goodhart's Law?**

-    **A.** Marilyn Strathern
- ✅ **B.** Charles Goodhart
-    **C.** Peter Drucker
-    **D.** Frederick Taylor

> 💡 **Explanation:** The document states that Goodhart's Law was originally formulated by British economist Charles Goodhart.

---

### Q2 `Easy` 📄

**According to the document, what happens to a proxy metric when it is turned into a target tied to incentives?**

-    **A.** It becomes a more accurate measure of the underlying goal
- ✅ **B.** People optimize for the metric itself rather than the underlying goal
-    **C.** The metric becomes physically inseparable from the goal
-    **D.** The metric remains unchanged but people work harder

> 💡 **Explanation:** The document explains that once a metric is turned into a target tied to incentives, people will optimize for the metric itself rather than the underlying goal, degrading the metric's value.

---

### Q3 `Intermediate` 📄

**A software company wants to improve code quality and decides to measure 'number of bugs fixed per week' as a key performance indicator tied to bonuses. Based on Goodhart's Law, what is the most likely unintended consequence?**

-    **A.** Developers will write more bug-free code from the start
- ✅ **B.** Developers may introduce trivial, easy-to-fix bugs to inflate their bug-fix count
-    **C.** The company will see a steady improvement in overall software quality
-    **D.** Developers will ignore the metric and focus on their work

> 💡 **Explanation:** This applies the core idea of Goodhart's Law: when a metric (bugs fixed) becomes a target tied to incentives, people will game the system to achieve the metric, potentially by introducing trivial bugs to fix, rather than improving actual code quality.

---

### Q4 `Hard` 📄

**Why does the document suggest that the Soviet nail factory example illustrates the failure of using a single metric as a target?**

-    **A.** Because the factory workers were not skilled enough to produce standard nails
-    **B.** Because the factory was state-owned and lacked profit incentives
- ✅ **C.** Because each change in the metric (weight vs. quantity) led to extreme, useless outcomes that satisfied the metric but not the goal
-    **D.** Because the nails were made of poor-quality materials

> 💡 **Explanation:** The document describes how targeting weight led to giant useless nails, and targeting quantity led to microscopic nails. Each metric was 'achieved' but the actual goal (useful nails) was not met, demonstrating how a single metric can be gamed.

---

### Q5 `Expert` 📄

**The document mentions that Peter Drucker's quote 'What gets measured gets managed' is often contrasted with Goodhart's Law. Based on the document's analysis, what is the most accurate evaluation of this contrast?**

-    **A.** Drucker's quote is always correct and Goodhart's Law is a rare exception
- ✅ **B.** Drucker's quote ignores the reality of gaming the system, which Goodhart's Law highlights
-    **C.** Both ideas are identical and describe the same phenomenon
-    **D.** Goodhart's Law disproves Drucker's quote entirely in all situations

> 💡 **Explanation:** The document explicitly notes that Drucker's quote 'often ignores the reality of gaming the system,' which is the central insight of Goodhart's Law. This is a nuanced evaluation — not a complete refutation, but a critical limitation.

---

## 🧠 Group 2 — General Knowledge Questions

### Q6 `Beginner` 🧠

**What is the most well-known, simple statement of Goodhart's Law?**

-    **A.** What gets measured gets managed
- ✅ **B.** When a measure becomes a target, it ceases to be a good measure
-    **C.** Correlation does not imply causation
-    **D.** All models are wrong, but some are useful

> 💡 **Explanation:** This is the widely recognized popular phrasing of Goodhart's Law, attributed to anthropologist Marilyn Strathern.

---

### Q7 `Easy` 🧠

**Which of the following concepts is most closely related to Goodhart's Law and describes perverse incentives leading to counterproductive outcomes?**

-    **A.** Occam's Razor
- ✅ **B.** The Cobra Effect
-    **C.** The Pareto Principle
-    **D.** The Dunning-Kruger Effect

> 💡 **Explanation:** The Cobra Effect is a classic example of perverse incentives where an attempted solution makes the problem worse, directly related to Goodhart's Law. The document also lists it as a related concept.

---

### Q8 `Intermediate` 🧠

**In modern healthcare, hospitals are sometimes measured on patient readmission rates, with penalties for high rates. Based on Goodhart's Law, what is a plausible real-world gaming behavior that could emerge?**

-    **A.** Hospitals invest more in preventive care to keep patients healthy
- ✅ **B.** Hospitals may keep patients admitted longer or delay discharge to avoid a readmission being counted
-    **C.** Doctors prescribe more effective medications to reduce complications
-    **D.** Patients are given better follow-up care instructions

> 💡 **Explanation:** When readmission rates become a penalized target, hospitals may game the system by keeping patients longer (so any return is not a 'readmission' within the window) or delaying discharge, rather than improving actual care quality.

---

### Q9 `Hard` 🧠

**A common criticism of Goodhart's Law is that it can be overstated. In which scenario would Goodhart's Law be LEAST applicable?**

-    **A.** A sales team is measured on number of customer calls made per day
-    **B.** A student's grade is based on a single final exam score
- ✅ **C.** A factory is measured on the purity of a chemical compound, where purity is tested by an independent lab
-    **D.** A teacher's bonus is tied to student standardized test scores

> 💡 **Explanation:** If the metric (chemical purity) is physically inseparable from the goal (producing pure chemicals) and is verified by an independent third party, it is much harder to game without actually achieving the goal. This aligns with the 'Perfect Proxies' counterargument mentioned in the document.

---

### Q10 `Expert` 🧠

**In the context of machine learning, Goodhart's Law manifests when a model is optimized on a specific evaluation metric (e.g., accuracy on a test set) that diverges from the true objective. What advanced technique is specifically designed to mitigate this problem by training the model to directly optimize for a downstream metric using a differentiable approximation?**

-    **A.** Gradient clipping
- ✅ **B.** Reinforcement Learning from Human Feedback (RLHF)
-    **C.** Dropout regularization
-    **D.** Principal Component Analysis (PCA)

> 💡 **Explanation:** RLHF is specifically designed to align model outputs with complex human preferences rather than a simple proxy metric. It uses human feedback as a reward signal, attempting to bypass the Goodhart effect where models would otherwise optimize a narrow metric (like next-word prediction) at the expense of helpfulness, honesty, and harmlessness.

---
