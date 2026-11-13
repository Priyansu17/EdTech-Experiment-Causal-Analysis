# 📋 Experiment Design Document (EDD): ShikshaSetu Gujarat
## Project: Personalized 1-on-1 Mentorship & Live Doubt-Clearing Sprints
**Lead Experimenter:** Senior Causal Inference & Econometrics Lead  
**Stakeholders:** Chief Academic Officer, Chief Executive Officer, Head of Operations  
**Target Organization:** ShikshaSetu Gujarat (Ahmedabad Flagship & Regional Network)  
**Status:** Executed & Ready for Production Review  
**Date:** Academic Term Q4

---

## 1. Executive Summary & Context
ShikshaSetu Gujarat operates 8 primary coaching hubs across Gujarat (4 in Ahmedabad: *Navrangpura, Satellite, Maninagar, Vastrapur*; 4 in Vadodara: *Alkapuri, Sayajigunj, Fatehgunj, Karelibaug*), training over 40,000 students annually across competitive STEM (JEE/NEET), Commerce (CA Foundation), and Secondary Foundation (Classes 9–10) curricula.

Last quarter, Ahmedabad leadership introduced an operational change (*AI-Adaptive Homework & Weekly Doubt Clinics*) and claimed a **+7.53 point increase** in assessment scores based on a naive before-versus-after comparison. However, this naive calculation ignored severe exam-prep seasonality (Gujarat pre-board examination fever), during which student scores state-wide naturally surged by **+4.66 points**, leaving the true causal improvement at only **+2.87 points**.

To prevent unmeasured confounders from distorting future strategic investments, this Experiment Design Document establishes a randomized, controlled trial (RCT) protocol for the next pedagogical initiative: **"Personalized 1-on-1 Peer Mentoring & Live Doubt-Clearing Sprints"**.

---

## 2. Hypothesis Formulation

### 2.1 Theoretical Framework
Educational psychology indicates that unaddressed conceptual doubts create an escalating cognitive deficit, leading to learner frustration, demotivation, and eventual attrition. Providing on-demand, personalized 1-on-1 mentorship sessions combined with structured weekly doubt-clearing sprints should eliminate learning bottlenecks in real-time, thereby improving curriculum comprehension, assessment outcomes, and course persistence.

### 2.2 Formal Statistical Hypotheses
Let $\mu_T$ and $\mu_C$ denote the true population mean of the Standardized Final Assessment Score in the Treatment and Control conditions, respectively. Let $P_T$ and $P_C$ denote the true population Course Completion Rates.

$$\begin{aligned}
\text{Primary Null Hypothesis } (H_0^{(1)}): & \quad \mu_T - \mu_C \le 0 \\
\text{Primary Alternative Hypothesis } (H_1^{(1)}): & \quad \mu_T - \mu_C > 0 \quad (\text{Two-sided test for safety: } \mu_T \neq \mu_C) \\[8pt]
\text{Co-Primary Null Hypothesis } (H_0^{(2)}): & \quad P_T - P_C \le 0 \\
\text{Co-Primary Alternative Hypothesis } (H_1^{(2)}): & \quad P_T - P_C > 0
\end{aligned}$$

---

## 3. Metrics Architecture

A rigorous experimentation program requires a multi-layered metric hierarchy that measures academic efficacy, user persistence, operational viability, and unintended negative consequences.

```
                                      [ EXPERIMENTATION METRIC HIERARCHY ]
                                                        |
      +--------------------------------+----------------+-------------------------------+
      |                                |                                                |
[ PRIMARY METRICS ]          [ SECONDARY METRICS ]                            [ GUARDRAIL METRICS ]
  - Final Assessment Score     - Assignment Submission Rate (%)                 - Early Drop-off Rate (<= Week 3)
  - Course Completion Rate     - On-Time Submission Rate (%)                    - Learner Satisfaction (CSAT 1-5)
                               - Observed Attendance Rate (%)                   - Faculty Overtime Hours / Student
                               - Midterm Assessment Score
```

### 3.1 Primary Metric: Standardized Final Assessment Score
* **Definition:** The learner's score on the comprehensive end-of-course standardized proctored exam ($Y_i \in [0, 100]$).
* **Rationale:** Direct, objective pedagogical measurement of conceptual mastery aligned with state competitive exams.
* **Unit of Analysis:** Individual learner ($i$).

### 3.2 Co-Primary Metric: Course Completion Rate
* **Definition:** Binary indicator ($C_i \in \{0, 1\}$) denoting whether a learner attended $\ge 70\%$ of core curriculum sessions and took the final assessment.
* **Formula:** $\text{Completion Rate} = \frac{\sum_{i=1}^N C_i}{N}$.
* **Rationale:** A coaching chain's long-term lifetime value (LTV), brand reputation, and word-of-mouth depend heavily on student persistence through the final lecture.

### 3.3 Secondary Metrics (Mechanism Validation)
1. **Assignment Submission Rate:** Total milestone assignments submitted divided by total assigned ($m = 3$). Validates homework engagement.
2. **Weekly Attendance Rate:** Percentage of valid recorded and live sessions attended ($A_i \in [0, 100\%]$).
3. **Midterm Assessment Score:** Intermediate evaluation score at week 5.

### 3.4 Guardrail & Health Metrics (Safety Tripwires)
1. **Early Drop-off Rate (Week $\le 3$):** Percentage of students completely disengaging before week 4.  
   *Threshold:* Treatment must not increase early attrition (Tolerance: $\Delta \le 0.0$ pp).
2. **Learner Satisfaction (CSAT):** End-of-course survey rating on a 1–5 Likert scale.  
   *Threshold:* CSAT $\ge 3.8 / 5.0$.
3. **Faculty Overtime Hours per Student:** Average weekly overtime hours logged by instructors and mentors per enrolled student.  
   *Threshold:* Overtime increase must not exceed $+25\%$ ($+0.12$ hrs/learner).  
   *Critical Alert:* If overtime doubles, the initiative is operationally unsustainable without dedicated adjunct hiring.

---

## 4. Unit of Randomization & Spillover Mitigation

### 4.1 Unit of Randomization Selection
* **Option A: Learner-Level Randomization within Batches (Selected Design):**  
  Within each center and course track, learners are randomized $1:1$ into Treatment (access to 1-on-1 mentorship sprints) or Control (standard classroom curriculum and existing open doubt hours).
* **Option B: Batch-Level Cluster Randomization:**  
  Entire batches assigned as Treatment or Control. While cluster randomization prevents within-classroom chatter, it introduces severe intra-class correlation (ICC: $\rho_{ICC} \approx 0.08–0.12$), inflating variance by the design effect $\text{VIF} = 1 + (m - 1)\rho_{ICC} \approx 3.4\times$, which would require tripling the sample size.

### 4.2 SUTVA (Stable Unit Treatment Value Assumption) & Spillover Protection
* **Risk:** Treatment learners sharing personalized mentorship notes or study plans with Control classmates in hostel dorms or unofficial WhatsApp study groups.
* **Mitigation:**
  1. Mentorship is delivered via 1-on-1 private video sprints and individual diagnostics tied to student login credentials.
  2. Proprietary sprint worksheets are watermarked with learner ID.
  3. Contamination audit: Track whether Control students attempt to access doubt booking links (instrumentation logging).

---

## 5. Statistical Power Analysis & Sample Size Sizing

### 5.1 Power Formulation for Continuous Primary Metric
The sample size required per experimental arm ($n$) for a continuous endpoint is given by:

$$n = \frac{2 \left(Z_{\alpha/2} + Z_{\beta}\right)^2 \sigma^2}{\Delta^2}$$

Where:
* Significance level: $\alpha = 0.05 \implies Z_{\alpha/2} = 1.95996$ (two-sided)
* Statistical Power: $1 - \beta = 0.80 \implies Z_{\beta} = 0.84162$
* Historical Standard Deviation: $\sigma = 12.13$ points (derived from clean historical control data)
* Total sample size: $N_{total} = 2n$

### 5.2 Power Formulation for Binary Co-Primary Metric
For course completion proportion ($p_1 = 0.590$, target $p_2 = 0.630 \implies \Delta = 0.040$):

$$n_{bin} = \frac{\left(Z_{\alpha/2} \sqrt{2 \bar{p}(1 - \bar{p})} + Z_\beta \sqrt{p_1(1-p_1) + p_2(1-p_2)}\right)^2}{\Delta^2}$$

### 5.3 Power Table & Duration Estimates
ShikshaSetu enrolls approximately **1,500 students per week** across its 8 campuses.

| Minimum Detectable Effect (MDE) | Metric Type | Required Sample ($N_{total}$) | Test Duration @ 1,500/week | Strategic Feasibility |
| :--- | :--- | :--- | :--- | :--- |
| **0.80 score pts** | Continuous | 14,410 learners | 9.6 weeks | Too long; exceeds academic quarter |
| **1.00 score pts** | Continuous | 9,222 learners | 6.1 weeks | Viable for full-term test |
| **1.50 score pts** | Continuous | 4,098 learners | 2.7 weeks | Optimal balance of speed and precision |
| **2.00 score pts** | Continuous | 2,306 learners | 1.5 weeks | Fast, but risks missing subtle effects |
| **+3.0 percentage points** | Binary (Completion) | 8,240 learners | 5.5 weeks | Standard enterprise benchmark |
| **+4.0 percentage points** | Binary (Completion) | 4,680 learners | 3.1 weeks | Target operational benchmark |

**Target Experiment Parameters:**  
* Target Sample Size: **10,000 learners** (5,000 Treatment, 5,000 Control)
* Baseline Duration: **6.0 weeks**
* Guaranteed Power: $> 95\%$ power to detect a $+1.5$ point score gain, and $> 88\%$ power to detect a $+3.5$ pp completion lift.

---

## 6. Pre-Experiment Variance Reduction Plan (CUPED)

To maximize statistical efficiency without extending student exposure, we integrate **CUPED (Controlled-experiment Using Pre-Experiment Data)** (Deng et al., 2013).

### 6.1 Mathematical Formulation
Let $Y_i$ be the post-treatment final assessment score, and $X_i$ be the pre-experiment baseline diagnostic score administered during orientation. The CUPED-adjusted outcome is:

$$\tilde{Y}_i = Y_i - \hat{\theta} \left(X_i - \mathbb{E}[X]\right), \quad \text{where } \hat{\theta} = \frac{\widehat{\text{Cov}}(Y, X)}{\widehat{\text{Var}}(X)}$$

### 6.2 Variance Reduction & Time Acceleration Factor
$$\text{Var}(\tilde{Y}) = \text{Var}(Y) \left(1 - \rho_{XY}^2\right)$$
Empirical correlation between diagnostic baseline and final scores is $\rho \approx 0.7406$.
$$\text{Variance Reduction} = \rho^2 = (0.7406)^2 \approx 54.85\%$$
$$\text{Effective Sample Size Multiplier} = 1 - \rho^2 = 0.4515$$
**Operational Payoff:** With CUPED, the required runtime to detect the target effect drops from **6.0 weeks to 2.7 weeks** (saving **3.3 weeks of runtime**), minimizing unnecessary control student deprivation.

---

## 7. Execution Protocol & Quality Safeguards

### 7.1 Sample Ratio Mismatch (SRM) Detection Protocol
* Daily automated Chi-Square Goodness-of-Fit test comparing observed counts $(O_C, O_T)$ against theoretical expectation $(0.50, 0.50)$:
  $$\chi^2 = \frac{(O_C - E_C)^2}{E_C} + \frac{(O_T - E_T)^2}{E_T}, \quad df = 1$$
* **Action Threshold:** If $p < 0.01$, immediately freeze assignment pipelines, audit routing load-balancers, and inspect batch enrolment sync queues.

### 7.2 Data Cleaning & Operational Hygiene Protocol
1. **Deduplication Filter:** Check uniqueness on `(learner_id, batch_id)`. Retain the initial registration timestamp and archive duplicate transaction records.
2. **Ghost Student Inferred Status Reclassification:** Reconcile students marked `official_status == 'Active'` who attend $\le 2$ sessions and submit 0 assignments to `inferred_status = 'Dropped'`.
3. **Missing Data Imputation:** For recorded sessions experiencing tablet sync outages, document missingness mechanism (MCAR verified) and employ center-by-track conditional mean imputation.

### 7.3 Stopping & Safety Rules
* **Futility Stopping:** If after 3 weeks ($N \ge 4,000$), the estimated lift is negative with $p < 0.05$, terminate early.
* **Safety Violation:** If faculty overtime exceeds $+50\%$ or learner early drop-off surges in treatment by $\ge +2.0$ pp, trigger emergency operational review.
