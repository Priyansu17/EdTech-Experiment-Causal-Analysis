# 📑 Executive Decision Memo: Causal Impact & Rollout Strategy
**TO:** Governing Board, Chief Executive Officer, Chief Academic Officer  
**FROM:** Senior Causal Inference & Econometrics Lead  
**DATE:** Academic Term Q4 Review  
**SUBJECT:** Business & Academic Impact of Mentorship Initiatives — Recommendation: **CONDITIONAL GO / EXTEND PHASED PILOT**

---

```
====================================================================================================
  EXECUTIVE RECOMMENDATION: CONDITIONAL GO / EXTEND PHASED PILOT (DO NOT BLINDLY SCALE)
  - ACADEMIC EFFICACY: EXCEPTIONAL (+4.38 pts assessment lift, +6.28 pp completion lift)
  - CRITICAL GUARDRAIL BREACH: Faculty overtime hours doubled (+94.7%, from 0.45h to 0.88h/student)
  - VERDICT: Rollout approved ONLY after hiring dedicated adjunct mentors to protect core faculty.
====================================================================================================
```

---

## 1. Key Metrics at a Glance (Active A/B Test: N = 10,000)

| Metric | Metric Type | Control Group | Treatment Group | Effect Estimate (Lift) | 95% Confidence Interval | p-value | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Final Assessment Score** | **Primary** | 72.20 pts | 76.58 pts | **+4.383 pts** | **[+3.932, +4.835] pts** | $2.85 \times 10^{-79}$ | **STATISTICALLY SIGNIFICANT** |
| **Bootstrap Final Score CI** | Robustness | — | — | **+4.383 pts** | **[+3.938, +4.874] pts** | — | **ROBUST CONFIRMATION** |
| **CUPED-Adjusted Score** | Stretch Goal | 72.08 pts | 76.57 pts | **+4.487 pts** | **[+4.191, +4.783] pts** | $9.76 \times 10^{-186}$ | **34.4% NARROWER BAND** |
| **Course Completion Rate** | **Co-Primary** | 60.62% | 66.89% | **+6.28 pp** (+10.4% rel) | **[+4.39, +8.16] pp** | $6.11 \times 10^{-11}$ | **HIGH BUSINESS VALUE** |
| **Drop-off Rate** | Guardrail | 27.05% | 22.69% | **-4.36 pp** | **[-5.98, -2.74] pp** | $3.42 \times 10^{-7}$ | **DESIRABLE CHURN REDUCTION** |
| **Learner CSAT (1–5 scale)** | Guardrail | 3.78 / 5.0 | 4.23 / 5.0 | **+0.45 pts** | **[+0.42, +0.48] pts** | $< 10^{-100}$ | **HIGH SATISFACTION** |
| **Faculty Overtime / Student** | **Guardrail** | 0.45 hrs | 0.88 hrs | **+0.43 hrs (+94.7%)** | **[+0.41, +0.45] hrs** | $< 10^{-100}$ | **CRITICAL GUARDRAIL BREACH** |

---

## 2. Deconfounding Last Quarter's Change: Seasonality vs True Lift
Last quarter, Ahmedabad leadership claimed an improvement of **+7.53 points** from the AI-Adaptive Homework initiative. Our Difference-in-Differences (DiD) econometric analysis with cluster-robust standard errors proves that **61.9% of that claimed gain was an illusion of Gujarat pre-board exam seasonality**:

$$\begin{aligned}
\text{Ahmedabad Observed Pre-to-Post Increase:} & \quad 67.93 \to 75.46 = \mathbf{+7.53 \text{ points (Naive Claim)}} \\
\text{Vadodara Control Region Seasonal Drift:} & \quad 67.78 \to 72.44 = \mathbf{+4.66 \text{ points (Pure Seasonality)}} \\
\hline
\mathbf{\text{True Causal Lift (DiD Interaction } \hat{\beta}_3\text{):}} & \quad \mathbf{+2.87 \text{ points}} \quad (\text{95% CI: } [2.38, 2.99], \ p = 3.12 \times 10^{-66})
\end{aligned}$$

* **Parallel Trends Validated:** Multi-period event-study tests confirm parallel pre-treatment trends between Ahmedabad and Vadodara ($M_1$ lead $p = 0.912$, $M_2$ lead $p = 0.138$, Joint $F = 3.071$, $p = 0.215$). The DiD estimate is causally valid.

---

## 3. Subgroup Heterogeneity: Who Won and Who Stagnated?

```
Academic Tier 1: Low Baseline (<60)  |======================> +6.04 pts [5.49, 6.59]  (TRANSFORMATIVE BENEFIT)
Academic Tier 2: Mid Baseline (60-80) |============> +3.63 pts [3.15, 4.11]          (SOLID PROGRESSION)
Academic Tier 3: High Baseline (>80)  |====> +1.25 pts [0.26, 2.23]                   (CEILING EFFECT / LOW GAIN)
Course Track: JEE/NEET STEM           |=================> +5.00 pts [4.36, 5.64]      (HIGH STEM DEMAND)
Course Track: Secondary Foundation    |=============> +3.88 pts [2.86, 4.90]          (STRONG ENGAGEMENT)
Course Track: Commerce / CA           |===========> +3.71 pts [2.90, 4.52]            (MODERATE BENEFIT)
```

* **Core Insight:** The 1-on-1 mentorship sprint is a lifesaver for struggling learners ($+6.04$ pts), but yields diminishing returns for already top-decile students ($+1.25$ pts).

---

## 4. Financial ROI & Operational Viability

1. **Revenue Upside:** Across ShikshaSetu's 40,000 annual enrollments, a $+6.28$ percentage point lift in completion retains approximately **2,512 additional students** who would otherwise have dropped out. At an average annual course fee of ₹50,000, this yields **₹12.56 Crores in preserved tuition and follow-on test series revenue**.
2. **Operational Vulnerability:** Faculty overtime increased from **0.45 hrs to 0.88 hrs per student**. If rolled out chain-wide without dedicated staffing, existing senior instructors will face severe burnout, causing classroom lecture quality to deteriorate and instructor attrition to spike.
3. **Staffing Solution:** Rather than utilizing senior faculty at ₹1,200/hr, recruit **35 dedicated recent graduate Teaching Assistants / Peer Mentors** at ₹350/hr to handle live doubt sprints. Total annual program cost: **₹3.20 Crores**.
4. **Projected Net Value:** Net annual operating gain of **₹9.36 Crores** (**3.92x ROI**).

---

## 5. Strategic Directives for Statewide Rollout

1. **DO NOT Immediately Roll Out Statewide Under Existing Staffing:** Immediate chain-wide expansion will collapse faculty morale and trigger resignation of star instructors.
2. **AUTHORIZE Phase 2 Extended Pilot (8 Weeks):** Expand the pilot to Vadodara and Surat while simultaneously onboarding 35 dedicated adjunct doubt mentors.
3. **MANDATE CUPED for Future Experimentation:** Utilizing pre-experiment diagnostic scores via CUPED reduces outcome variance by **54.85%**, cutting required experiment duration from **6.0 weeks to 2.7 weeks** and saving 3.3 weeks of test runtime.
4. **IMPLEMENT REAL-TIME DATA GOVERNANCE:** Eliminate the 2,727 "ghost" active dropouts by deploying automated biometric tablet sync retries and an auto-drop classification rule for learners inactive for $>14$ consecutive days.
