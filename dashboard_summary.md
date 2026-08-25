# NetSage AI Dashboard & Evaluation Summary

## 1. Case Breakdown by Domain & Concept
* **Total Cases Analyzed:** 30
* **OSI Layer Distribution:**
  * **Layer 3 (Network):** 12 cases (40.0%)
  * **Layer 2 (Data Link):** 9 cases (30.0%)
  * **Layer 7 (Application):** 4 cases (13.3%)
  * **Layer 4 (Transport):** 3 cases (10.0%)[cite: 1]
  * **Cross-Layer (L2/L3, L3/L4):** 2 cases (6.7%)[cite: 1]

* **Severity Breakdown:**
  * **High Severity:** 16 cases (53.3%)[cite: 1]
  * **Medium Severity:** 11 cases (36.7%)[cite: 1]
  * **Low Severity:** 3 cases (10.0%)[cite: 1]

---

## 2. AI Performance & Agreement Metrics

| Review Decision | Count | Percentage | Operational Impact |
| :--- | :--- | :--- | :--- |
| **Accepted (Direct Fit)** | 22 | 73.3% | Diagnosis & CLI commands applied directly[cite: 1]. |
| **Edited (Refined)** | 5 | 16.7% | Root cause correct, commands tailored by human[cite: 1]. |
| **Rejected (Incorrect)** | 3 | 10.0% | Rule checker or human overridden AI false diagnostic[cite: 1]. |
| **Total Human Agreement** | **27 / 30** | **90.0%** | **High diagnostic baseline with safety guardrails.** |

---

## 3. Rule Checker Accuracy
* **Deterministic Rule Detection Rate:** 100% on standard static errors (Admin Down, DHCP Scope Exhaustion, Missing VLANs)[cite: 1].
* **Pre-Execution Filtering:** Flagged 8 configuration errors prior to LLM processing, saving API latency and token cost[cite: 1].
