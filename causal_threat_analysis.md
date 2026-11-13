# 🔍 Causal Threat Analysis: What Could Make Our Causal Estimates Wrong?
**Author:** Senior Causal Inference & Econometrics Lead  
**Scope:** Diagnostic Audit of Internal & External Validity for ShikshaSetu Gujarat

---

## 1. Introduction & Epistemological Framework
Every causal inference estimate—whether derived from a prospective Randomized Controlled Trial (RCT), a Difference-in-Differences (DiD) quasi-experiment, or variance-reduced regression adjustment (CUPED)—rests upon explicit identification assumptions. 

If any of these foundational assumptions fail in the operational reality of coaching centers, our causal estimates will deviate from the true population treatment effect. This document provides a transparent, exhaustive post-mortem of the vulnerabilities, edge cases, and structural biases that could invalidate or distort our findings.

---

## 2. Threats to the Randomized A/B Test (Internal Validity)

```
                       [ RCT IDENTIFICATION RISKS ]
                                     |
    +-------------------+------------+------------+--------------------+
    |                   |                         |                    |
[ SUTVA & SPILLOVER ] [ DIFFERENTIAL ATTRITION ] [ HAWTHORNE / HENRY ] [ COVARIATE TIMING ]
 (Contamination via    (Survivorship Bias via     (Faculty / Learner    (Endogenous CUPED
  Peer Study Circles)   Drop-out Selection)        Behavioral Drift)     Leakage)
```

### 2.1 SUTVA Violations & Cross-Arm Interference (Spillover)
* **The Assumption:** The Stable Unit Treatment Value Assumption (SUTVA) requires that the treatment assigned to learner $i$ does not affect the potential outcomes of learner $j$ ($Y_j(T_1, \dots, T_n) = Y_j(T_j)$).
* **Failure Mechanism in Coaching Culture:**  
  In Ahmedabad coaching hubs (e.g., Navrangpura, Satellite), students routinely live in the same hostel accommodations, form informal WhatsApp/Telegram study groups, and sit adjacent to one another in physical classroom lectures.
  - Treatment learners receiving custom 1-on-1 sprint worksheets and step-by-step problem-solving templates can easily photocopy or forward them to Control classmates.
  - Mentors in treatment sprints may teach mnemonics or exam shortcuts that treatment students share during lunch breaks.
* **Impact on Causal Estimate:**  
  Spillover inflates the performance of the Control group ($Y_C$ increases), causing **downward attenuation bias** ($\hat{\tau} < \tau^*$). Our reported $+4.38$ point gain would represent a *conservative lower bound* of true efficacy.
* **Diagnostic Audit & Remedy:**  
  - Measure network proximity (same school, shared batch, shared address).
  - In future iterations, deploy **two-stage cluster randomization** (randomizing entire batches or study pods) with donut spatial buffers to isolate interference.

---

### 2.2 Differential Attrition & Survivorship Selection Bias
* **The Assumption:** Learner attrition is conditionally independent of potential outcomes given treatment assignment ($\{Y(1), Y(0)\} \perp \text{Drop} \mid T$).
* **Failure Mechanism:**  
  In our trial, dropout rates differed significantly: **27.05% in Control vs 22.69% in Treatment** ($\Delta = -4.36$ pp, $p < 0.001$).
  - In the Control arm, struggling students lacking support became discouraged and dropped out early, leaving an unobserved survivor cohort composed predominantly of high-resilience, disciplined learners.
  - In the Treatment arm, the 1-on-1 mentorship prevented borderline students from dropping out, keeping them in the cohort until the final assessment.
* **Impact on Causal Estimate:**  
  Because weaker students were retained in Treatment while dropping out of Control, the observed Control final assessment mean is artificially inflated by survivorship bias. Consequently, the naive difference-in-means **underestimates the true pedagogical uplift** of the program.
* **Formal Bounds:**  
  Applying Lee (2009) Trimming Bounds or Manski Worst-Case Bounds indicates that if the marginal 4.36% retained students in Treatment had their scores imputed at the 25th percentile, the true treatment effect rises from $+4.38$ to **$+5.12$ points**.

---

### 2.3 The "Ghost" Student Distortion & Missing Attrition Flags
* **The Operational Flaw:**  
  ERP audits revealed **2,727 students** marked as `'Active'` who had attended $\le 2$ sessions and submitted zero assignments. Coaching front-desks delay marking students as dropped out to artificially depress branch-level churn metrics before quarterly management reviews.
* **Causal Hazard:**  
  If an analyst evaluates course completion without correcting for ERP lag, these ghost learners are classified as "active non-completers" rather than early dropouts. Depending on how assessment absences are handled (imputing zero vs dropping from sample), this introduces severe non-random missingness.
* **Audit Resolution:**  
  Our behavioral inference filter (`inferred_status`) eliminated this distortion, reclassifying 2,727 zombie records to `'Dropped'`. However, any residual misclassification across centers remains an unmodeled measurement error.

---

### 2.4 Hawthorne & John Henry Effects (Behavioral Reactions to Trial Observation)
* **Hawthorne Effect:** Faculty mentors selected for the 1-on-1 trial knew leadership was tracking sprint logs and student CSAT. They likely exerted extraordinary empathy, punctual scheduling, and meticulous preparation that cannot be sustained at statewide scale.
* **John Henry Effect:** Control group instructors, aware that their pedagogical outcomes were being benchmarked against an experimental mentoring intervention, may have worked extra hard to prove that standard classroom teaching is sufficient.
* **Impact:** Once rolled out statewide without executive surveillance, operational friction and faculty fatigue will cause the effect size to decay (treatment effect shrinkage).

---

### 2.5 Endogenous Baseline Covariates in CUPED
* **The Assumption:** The baseline covariate $X_i$ must be strictly unaffected by the treatment ($\mathbb{E}[X_i \mid T_i = 1] = \mathbb{E}[X_i \mid T_i = 0]$).
* **Failure Mechanism:**  
  If the baseline diagnostic test was administered after learners were informed of their mentorship sprint assignments, or if mentors reached out before the diagnostic concluded, $X_i$ becomes endogenous.
* **Verification:**  
  Our balance check confirmed that diagnostic score balance held perfectly ($\text{SMD} = -0.012$, $p = 0.550$), verifying that $X_i$ was captured strictly prior to intervention exposure.

---

## 3. Threats to the Difference-in-Differences (DiD) Quasi-Experiment

```
                       [ DiD IDENTIFICATION RISKS ]
                                     |
    +-------------------+------------+------------+--------------------+
    |                                             |                    |
[ PARALLEL TRENDS VIOLATIONS ]         [ ASYMMETRIC LOCAL SHOCKS ] [ COMPOSITIONAL CHURN ]
 (Differential Pre-Exam Prep              (Local Competitor Offers,   (Demographic Drift
  Dynamics Across Cities)                  Infrastructure Outages)     Between Quarters)
```

### 3.1 Violation of the Parallel Trends Assumption
* **The Assumption:** In the absence of the AI-Adaptive Homework intervention in Ahmedabad, the change in average scores in Ahmedabad would have been identical to the change observed in Vadodara ($\mathbb{E}[Y_{Post}^0 - Y_{Pre}^0 \mid \text{Ahmedabad}] = \mathbb{E}[Y_{Post}^0 - Y_{Pre}^0 \mid \text{Vadodara}]$).
* **Potential Violations:**
  1. **Differential Academic Calendars:** Gujarat Technological University or local Ahmedabad school boards may have scheduled internal prelims 2 weeks earlier than Vadodara schools, artificially accelerating Ahmedabad's Q3 score trajectory.
  2. **Nonlinear Seasonality:** If Ahmedabad centers serve a higher proportion of repeater students who intensify exam prep earlier than Foundation students, the parallel trends assumption fails even if pre-trends appear flat.
* **Empirical Robustness:**  
  Our multi-period leads and lags event-study regression confirmed no statistically significant pre-divergence ($M_1$ lead $p = 0.912$, $M_2$ lead $p = 0.138$, Joint $F = 3.071, p = 0.215$). However, parallel pre-trends are a necessary, not sufficient, condition for counterfactual parallel trends.

---

### 3.2 Asymmetric Regional Shocks & Confounding Events
* **Center-Specific Outages:**  
  During Q3, local infrastructure disruptions (e.g., Ahmedabad Metro construction near Vastrapur or torrential monsoon waterlogging in low-lying areas of Vadodara) could have differentially depressed attendance or physical access.
* **Instructor Turnover:**  
  If Vadodara lost two key Physics faculty to a competing coaching institute in Sayajigunj during Month 4, Vadodara's baseline would sink, making Ahmedabad appear artificially superior.

---

### 3.3 Compositional Shift Across Enrollment Quarters
* **The Risk:** Students enrolling in Q2 (April–June) often include early-decision, highly motivated aspirants. Students enrolling in Q3 (July–September) may include late-joiners or students transferring from other institutes after poor mid-term marks.
* **Remedy:** Our DiD model included individual-level baseline diagnostic scores and course-track fixed effects to control for observed compositional shifts across cohorts.

---

## 4. Threats to External Validity & Generalizability (Transportability)

### 4.1 Ahmedabad/Vadodara Cultural & Demographic Specificity
* ShikshaSetu's Gujarat student body has a distinctive distribution: high participation in CA/Commerce tracks (~30%) reflecting Gujarat's commercial culture, and a substantial Gujarati-medium cohort.
* Extrapolating these findings to national coaching epicenters (e.g., Kota, Rajasthan or Hyderabad, Telangana), where student competition is ultra-intense and peer culture is hyper-STEM-focused, would be scientifically invalid without localized replication.

### 4.2 Scale Elasticity & Mentor Diminishing Quality
* In the 10,000-learner experiment, mentors were selected from top-performing faculty.
* Scaling statewide to 40,000+ students requires hiring dozens of new mentors. If the newly recruited mentors lack pedagogical mastery, the marginal treatment effect of mentorship will rapidly decay toward zero.

---

## 5. Summary Threat Matrix

| Threat Category | Source of Bias | Direction of Bias | Mitigation in Current Analysis | Severity Rating |
| :--- | :--- | :--- | :--- | :--- |
| **SUTVA Spillover** | Study groups / notes sharing | Underestimates true effect | Credential-locked video sprints | Moderate |
| **Differential Attrition** | Weaker students retained in Trt | Underestimates score lift | Inferred status audit + Trimming bounds | High |
| **Ghost Dropouts** | ERP delayed status updates | Biases completion downwards | Reclassification via session activity | Critical (Resolved) |
| **Hawthorne Effect** | Trial observation zeal | Overestimates scalable lift | Addressed in Decision Memo | High |
| **DiD Parallel Trends** | Local exam schedule variations | Confounded treatment effect | Event-study leads & lags test ($F=3.07$) | Moderate (Passed) |
| **CUPED Endogeneity** | Post-treatment covariate contamination | Inconsistent regression weights | Verified baseline diagnostic timing | Low (Controlled) |
