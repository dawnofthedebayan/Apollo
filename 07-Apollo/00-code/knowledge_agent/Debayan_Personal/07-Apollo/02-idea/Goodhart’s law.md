# Quiz: Goodhart's Law and Metric Gaming
> Source file: `Goodhart's law.md`

---

## 📄 Group 1 — Document-Based Questions

### Q1 `Beginner` 📄

**Beginner | What is Goodhart's Law?**

- ✅ **A.** When a measure becomes a target, it ceases to be a good measure
-    **B.** What gets measured gets managed effectively
-    **C.** Metrics should always be tied to financial incentives
-    **D.** Statistical relationships remain stable under all conditions

> 💡 **Explanation:** Goodhart's Law, as stated in the document, is 'When a measure becomes a target, it ceases to be a good measure.' This captures the core principle that metrics lose their validity when used as targets.

---

### Q2 `Easy` 📄

**Easy | Why do metrics become less effective when turned into targets according to the document?**

-    **A.** Because metrics are inherently inaccurate
- ✅ **B.** Because people optimize for the metric itself rather than the underlying goal
-    **C.** Because targets are always set too high
-    **D.** Because measurement tools become outdated

> 💡 **Explanation:** The document explains that humans naturally optimize for their incentives, so once a metric becomes a target, people optimize for the metric itself rather than the underlying goal, leading to gaming the system.

---

### Q3 `Intermediate` 📄

**Intermediate | A hospital measures 'patient discharge time' to improve efficiency. Doctors start discharging patients earlier than medically advisable. Which mitigation strategy from the document would best address this?**

-    **A.** Increase the discharge time target to make it easier to achieve
- ✅ **B.** Pair the discharge time metric with a counter-metric like readmission rates
-    **C.** Stop measuring discharge time entirely
-    **D.** Make the metric confidential so doctors don't know about it

> 💡 **Explanation:** The document recommends pairing metrics with counter-metrics: 'If you measure speed, you must also measure quality.' Pairing discharge time with readmission rates would prevent gaming by ensuring quality isn't sacrificed for speed.

---

### Q4 `Hard` 📄

**Hard | Why did the Soviet nail factory example demonstrate two different failure modes when targets changed from weight to quantity?**

-    **A.** The factory managers were incompetent in both scenarios
- ✅ **B.** Each metric incentivized optimization along a different dimension, both missing the actual goal of useful nails
-    **C.** The workers deliberately sabotaged production to protest the targets
-    **D.** The measurement tools were inaccurate in both cases

> 💡 **Explanation:** The example shows that weight targets produced few giant useless nails, while quantity targets produced many tiny useless nails. Each metric created different optimization behavior, but both failed to capture the underlying goal of producing useful nails, demonstrating how proxy metrics can be gamed in multiple ways.

---

### Q5 `Expert` 📄

**Expert | According to the document's counterarguments section, under what conditions does Goodhart's Law NOT apply, and what is the critical distinction?**

-    **A.** When metrics are measured frequently enough to detect gaming behavior
- ✅ **B.** When the metric is physically inseparable from the goal itself, making it impossible to game without achieving the actual goal
-    **C.** When financial incentives are removed from the measurement system
-    **D.** When multiple stakeholders are involved in setting the targets

> 💡 **Explanation:** The document states that Goodhart's Law does not apply when 'the metric is physically inseparable from the goal.' The example given is lifting 100 lbs—you cannot game the weight measurement without actually achieving the goal. This represents a perfect proxy rather than an imperfect one that can be optimized independently.

---

## 🧠 Group 2 — General Knowledge Questions

### Q6 `Beginner` 🧠

**Beginner | What field did Charles Goodhart originally work in when he formulated Goodhart's Law?**

-    **A.** Psychology
- ✅ **B.** Economics
-    **C.** Computer Science
-    **D.** Biology

> 💡 **Explanation:** Charles Goodhart was a British economist who originally formulated the law in 1975 in the context of UK monetary policy.

---

### Q7 `Easy` 🧠

**Easy | Which related concept describes situations where incentives produce the opposite of the intended outcome?**

-    **A.** The Butterfly Effect
- ✅ **B.** The Cobra Effect
-    **C.** The Halo Effect
-    **D.** The Dunning-Kruger Effect

> 💡 **Explanation:** The Cobra Effect is a related concept mentioned in the document that describes perverse incentives—situations where well-intentioned incentives produce outcomes opposite to those intended, similar to how Goodhart's Law describes metric gaming.

---

### Q8 `Intermediate` 🧠

**Intermediate | A software company wants to improve code quality. Which approach would LEAST likely fall victim to Goodhart's Law?**

-    **A.** Requiring all developers to write at least 1000 lines of code per week
- ✅ **B.** Measuring code quality through a combination of peer reviews, bug rates, customer satisfaction, and maintainability scores
-    **C.** Tying bonuses directly to the number of commits made to the repository
-    **D.** Setting a target of zero bugs reported in production

> 💡 **Explanation:** Using multiple complementary metrics (peer reviews, bug rates, customer satisfaction, maintainability) makes it harder to game the system because optimizing for one metric at the expense of others would be detected. Single metrics like lines of code, commits, or zero bugs can easily be gamed.

---

### Q9 `Hard` 🧠

**Hard | What is the fundamental difference between Campbell's Law and Goodhart's Law?**

-    **A.** Campbell's Law applies only to educational settings while Goodhart's Law is universal
- ✅ **B.** Campbell's Law emphasizes the corruption of the indicator through social pressure and high stakes, while Goodhart's Law focuses on statistical relationships breaking down when used for policy
-    **C.** Campbell's Law was formulated earlier and Goodhart's Law is just a restatement
-    **D.** Campbell's Law only applies to qualitative measures while Goodhart's Law applies to quantitative ones

> 💡 **Explanation:** While both laws describe similar phenomena, Campbell's Law (1976) specifically emphasizes how social indicators become corrupted when used for social decision-making, particularly highlighting the role of social pressure. Goodhart's Law focuses on how statistical relationships break down when used for policy, originating from monetary economics.

---

### Q10 `Expert` 🧠

**Expert | In machine learning systems, Goodhart's Law manifests as 'reward hacking.' What makes this particularly challenging compared to traditional organizational metrics?**

-    **A.** Machine learning models cannot be monitored as easily as human behavior
- ✅ **B.** AI systems can discover and exploit unintended optimization pathways at superhuman speed and in ways that may be opaque to human observers, making counter-metrics harder to design
-    **C.** Machine learning metrics are always more complex than organizational metrics
-    **D.** AI systems are intentionally designed to game metrics while humans do so accidentally

> 💡 **Explanation:** In AI systems, reward hacking is particularly challenging because ML models can optimize reward functions in unexpected, creative ways that humans might not anticipate, often exploiting edge cases or bugs in the reward specification. The speed and opacity of these optimizations make it harder to design effective counter-metrics before harm occurs, unlike human organizational behavior which is typically more transparent and slower to adapt.

---
