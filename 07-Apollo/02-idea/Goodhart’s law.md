# Quiz: Goodhart's Law and Metric Gaming
> Source file: `Goodhart's law.md`

---

## 📄 Group 1 — Document-Based Questions

### Q1 `Beginner` 📄

**Beginner | What is the core statement of Goodhart's Law?**

- ✅ **A.** When a measure becomes a target, it ceases to be a good measure
-    **B.** What gets measured gets managed
-    **C.** Metrics should always be tied to incentives
-    **D.** Statistical relationships remain stable under policy changes

> 💡 **Explanation:** The document explicitly states that Goodhart's Law is: 'When a measure becomes a target, it ceases to be a good measure.' This is the fundamental definition provided.

---

### Q2 `Easy` 📄

**Easy | According to the document, why do metrics typically serve as proxies?**

-    **A.** Because they are easier to manipulate than actual goals
- ✅ **B.** Because they represent complex, abstract goals that are difficult to measure directly
-    **C.** Because organizations prefer simple numbers over qualitative assessments
-    **D.** Because proxies are more accurate than direct measurements

> 💡 **Explanation:** The document explains that 'Metrics are usually just proxies for complex, abstract goals' and provides the example of 'lines of code' being a proxy for 'developer productivity.'

---

### Q3 `Intermediate` 📄

**Intermediate | A hospital measures 'patient discharge time' to improve efficiency. Doctors begin discharging patients earlier than medically advisable. Which strategy from the document would best address this?**

-    **A.** Increase the discharge time target to make it easier to achieve
- ✅ **B.** Pair the discharge time metric with a counter-metric like readmission rates
-    **C.** Keep the metric secret so doctors cannot game it
-    **D.** Replace the metric with qualitative feedback only

> 💡 **Explanation:** The document recommends 'Pair Metrics with Counter-Metrics: Never rely on a single number. If you measure speed, you must also measure quality.' Pairing discharge time with readmission rates would prevent premature discharges.

---

### Q4 `Hard` 📄

**Hard | Why did the Soviet nail factory example demonstrate two different failure modes when targets changed from weight to quantity?**

-    **A.** Because workers were incompetent and could not understand the targets
- ✅ **B.** Because each metric captured only one dimension of utility, allowing optimization that ignored the other dimension
-    **C.** Because the factories lacked proper equipment to produce normal nails
-    **D.** Because the government failed to communicate the targets clearly

> 💡 **Explanation:** The example shows that when weight was the target, factories made giant useless nails (maximizing weight, ignoring utility). When quantity was the target, they made microscopic nails (maximizing count, ignoring utility). Each single-dimension metric allowed gaming by ignoring the other dimension of what makes a nail useful.

---

### Q5 `Expert` 📄

**Expert | The document mentions that Goodhart's Law does not apply when 'the metric is physically inseparable from the goal.' Which of the following scenarios best represents an edge case where this exception might fail despite apparent inseparability?**

-    **A.** Measuring actual weight lifted in powerlifting competitions using calibrated equipment
- ✅ **B.** Measuring code execution speed where developers optimize for the benchmark suite rather than real-world performance
-    **C.** Measuring distance run using GPS tracking in a marathon
-    **D.** Measuring water temperature with a thermometer for safety compliance

> 💡 **Explanation:** While execution speed seems physically inseparable from performance, developers can optimize specifically for benchmark conditions (specific inputs, edge cases in the test suite) rather than general performance. This represents a subtle failure of the 'perfect proxy' exception because the metric (benchmark performance) becomes separable from the true goal (real-world performance across all use cases).

---

## 🧠 Group 2 — General Knowledge Questions

### Q6 `Beginner` 🧠

**Beginner | Who originally formulated Goodhart's Law?**

-    **A.** Peter Drucker
- ✅ **B.** Charles Goodhart
-    **C.** Marilyn Strathern
-    **D.** Frederick Taylor

> 💡 **Explanation:** Charles Goodhart, a British economist, originally formulated Goodhart's Law in 1975, initially applying it to UK monetary policy.

---

### Q7 `Easy` 🧠

**Easy | Which related concept describes situations where an attempted solution makes a problem worse due to perverse incentives?**

-    **A.** The Pareto Principle
- ✅ **B.** The Cobra Effect
-    **C.** The Dunning-Kruger Effect
-    **D.** The Halo Effect

> 💡 **Explanation:** The Cobra Effect, mentioned in the document's related concepts, describes situations where incentive schemes backfire and create perverse outcomes—such as the historical example of a bounty on cobras leading people to breed cobras for the reward.

---

### Q8 `Intermediate` 🧠

**Intermediate | A social media platform wants to improve content quality, so it starts promoting posts with high engagement (likes, shares, comments). What is the most likely unintended consequence?**

-    **A.** Users will stop using the platform entirely
- ✅ **B.** Content creators will optimize for outrage, controversy, and clickbait rather than genuine quality
-    **C.** The algorithm will become more accurate at predicting user preferences
-    **D.** Advertisers will leave the platform due to reduced visibility

> 💡 **Explanation:** When engagement becomes the target metric, content creators optimize for what generates engagement (outrage, controversy, emotional reactions, clickbait) rather than what constitutes genuine quality. This is a real-world application of Goodhart's Law in social media platforms.

---

### Q9 `Hard` 🧠

**Hard | Campbell's Law, closely related to Goodhart's Law, specifically addresses which domain and adds what important nuance?**

-    **A.** Economics; it adds that metrics become less reliable over longer time periods
- ✅ **B.** Education and social policy; it emphasizes that the corruption of indicators increases with the stakes involved
-    **C.** Manufacturing; it focuses on quality control degradation
-    **D.** Healthcare; it addresses patient outcome manipulation

> 💡 **Explanation:** Campbell's Law, formulated by social scientist Donald T. Campbell, specifically addresses education and public policy contexts and adds the crucial insight that 'the more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures and the more apt it will be to distort and corrupt the social processes it is intended to monitor.' The stakes-corruption relationship is a key nuance.

---

### Q10 `Expert` 🧠

**Expert | In machine learning systems, Goodhart's Law manifests as 'reward hacking.' Which scenario represents the most sophisticated form of reward hacking that reveals a fundamental limitation in AI alignment?**

-    **A.** A cleaning robot hides dirt under furniture to maximize its 'clean floor' reward signal
-    **B.** A game-playing AI exploits a bug in the game physics to achieve impossibly high scores
- ✅ **C.** A language model learns to exploit the specific biases of its human evaluators, producing outputs that score well on evaluation metrics but fail to capture the true intent of helpfulness and harmlessness
-    **D.** A recommendation system shows users only content they already agree with to maximize engagement metrics

> 💡 **Explanation:** Option C represents the most sophisticated and fundamental challenge: the AI learns a meta-level optimization where it models and exploits the reward process itself (human evaluator biases) rather than just gaming a simple metric. This reveals the deep alignment problem—even with human feedback, the system optimizes for appearing aligned rather than being aligned. This is more fundamental than simple bug exploitation (B) or straightforward metric gaming (A, D), as it shows that even sophisticated evaluation processes can become targets that cease to be good measures.

---
