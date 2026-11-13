# 📐 Engineering & Methodological Specification
## Project: ShikshaSetu Gujarat Causal Inference & Experimentation Platform
**Document Version:** 1.2.0  
**Status:** Approved for Production  
**Lead Architect:** Senior Causal Inference & Econometrics Lead  
**Scope:** Automated Pipeline, Data Hygiene Engine, Econometric Modelers, and Decision Support System

---

## 1. System Overview & Architecture

The ShikshaSetu Gujarat Experimentation Platform is an enterprise causal inference pipeline designed to evaluate educational initiatives, deconfound seasonal trends from observational records, and execute randomized controlled trials (RCTs).

```
+--------------------------------------------------------------------------------------------------+
|                                    DATA INGESTION & AUDIT LAYER                                   |
|                                                                                                  |
|   raw_enrolments.parquet        raw_attendance.parquet        raw_assignments.parquet            |
|       (30,450 rows)                 (240,000 rows)                 (90,000 rows)                 |
|             |                             |                              |                       |
|             v                             v                              v                       |
|   [Deduplication Engine]        [Missingness Audit]           [Submission Aggregator]            |
|   (Eliminates 450 dupes)        (7.93% recorded vs 3.06% live) (Submissions & on-time scores)    |
|             \                             |                              /                       |
|              +----------------------------+-----------------------------+                        |
|                                           |                                                      |
|                                           v                                                      |
|                           [Ghost Student Inferred Classifier]                                    |
|                      (Reclassifies 2,727 zombie records to Dropped)                              |
|                                           |                                                      |
|                                           v                                                      |
|                            cleaned_learner_mart.parquet                                          |
|                                    (30,000 rows)                                                 |
+-------------------------------------------+------------------------------------------------------+
                                            |
         +----------------------------------+-----------------------------------+
         |                                                                      |
         v                                                                      v
+----------------------------------------+            +----------------------------------------+
|       OBSERVATIONAL / DiD ENGINE       |            |          ACTIVE A/B TEST ENGINE        |
| (Historical Cohort: 20,000 Learners)   |            | (Experiment Cohort: 10,000 Learners)   |
|                                        |            |                                        |
|  - 2x2 DiD Panel Regression            |            |  - Sample Ratio Mismatch (SRM) Test    |
|  - Cluster-Robust Standard Errors      |            |  - Covariate Balance Audit (SMDs)      |
|  - Multi-Period Event Study            |            |  - Welch's Two-Sample t-test           |
|  - Parallel Trends Pre-Test (Wald F)   |            |  - Non-Parametric Bootstrap (2,000x)   |
|                                        |            |  - Heterogeneous Subgroup Engine       |
+----------------------------------------+            |  - CUPED Variance Reduction Engine     |
                                                      +----------------------------------------+
                                                                      |
                                                                      v
                                                      +----------------------------------------+
                                                      |       EXECUTIVE DECISION ENGINE        |
                                                      |  - Guardrail Tripwire Verification     |
                                                      |  - Financial ROI & Staffing Model      |
                                                      |  - Action: CONDITIONAL GO / EXTEND     |
                                                      +----------------------------------------+
```

---

## 2. Data Schema & Anomaly Specifications

### 2.1 Raw Enrolment Schema (`raw_enrolments.parquet`)
* **`enrollment_id`** (VARCHAR[16], Primary Key): Unique transaction identifier (e.g., `ENR_000001`).
* **`learner_id`** (VARCHAR[12], Foreign Key): Unique student identifier (e.g., `LRN_000001`).
* **`batch_id`** (VARCHAR[24]): Batch identifier (e.g., `BATCH_AHM_M1_JEE_01`).
* **`city`** (VARCHAR[16]): Campus location (`Ahmedabad` or `Vadodara`).
* **`center_id`** (VARCHAR[32]): Specific physical facility (`Ahmedabad_Navrangpura`, `Vadodara_Alkapuri`, etc.).
* **`month`** (INTEGER, Range 1–7): Enrollment intake month (1–6: Historical DiD; 7: Active Experiment).
* **`cohort_type`** (VARCHAR[24]): Cohort classification (`historical_did` or `active_ab_experiment`).
* **`course_track`** (VARCHAR[24]): Academic track (`JEE_NEET_STEM`, `Commerce_CA`, `Foundation_9_10`).
* **`baseline_diagnostic_score`** (FLOAT, Range 0.0–100.0): Pre-treatment orientation score ($X$).
* **`baseline_attendance_rate`** (FLOAT, Range 0.0–100.0): Initial attendance percentage.
* **`experiment_variant`** (VARCHAR[16]): Arm assignment (`Control`, `Treatment`, or `Not_In_Experiment`).
* **`official_status`** (VARCHAR[16]): Raw ERP status (`Active`, `Completed`, `Dropped`).

### 2.2 Attendance Schema (`raw_attendance.parquet`)
* **`attendance_id`** (VARCHAR[16], Primary Key): Session attendance identifier (e.g., `ATT_0000001`).
* **`learner_id`** (VARCHAR[12], Foreign Key): Associated student ID.
* **`session_num`** (INTEGER, Range 1–8): Sequence index of curriculum session.
* **`session_type`** (VARCHAR[16]): Session pedagogy (`Lecture`, `Doubt_Lab`, `Revision`).
* **`is_recorded_session`** (BOOLEAN): Digital session flag (`True` indicates asynchronous recorded session).
* **`attended`** (FLOAT, Nullable): Binary attendance value ($1.0 = \text{Attended}, 0.0 = \text{Absent}, \text{NaN} = \text{Missing Log}$).

### 2.3 Data Cleansing Algorithms & Predicates

#### Anomaly 1: Duplicate Enrolment Resolution
$$\text{Duplicate Predicate: } \text{Count}(\text{enrollment\_id}) > 1 \quad \text{grouped by } (\text{learner\_id}, \text{batch\_id})$$
* **Resolution Specification:** Retain record with lowest primary key timestamp; archive duplicate entry.
* **Performance:** 450 duplicate rows pruned (1.48% table density reduction).

#### Anomaly 2: "Ghost" Active Dropout Reclassification
$$\text{Ghost Predicate: } (\text{official\_status} == \text{'Active'}) \ \wedge \ (\text{last\_session\_attended} \le 2) \ \wedge \ (\text{assignments\_submitted} \le 1)$$
* **Resolution Specification:** Reclassify `inferred_status` $\leftarrow$ `'Dropped'`.
* **Performance:** 2,727 active zombie records successfully reclassified to dropped status.

#### Anomaly 3: Attendance Missingness Handling
* **Recorded Session Offline Loss:** $\mathbb{P}(\text{Attended is NaN} \mid \text{Recorded} = \text{True}) = 7.93\%$.
* **In-Person Loss:** $\mathbb{P}(\text{Attended is NaN} \mid \text{Recorded} = \text{False}) = 3.06\%$.
* **Imputation Specification:** MCAR test verified ($p > 0.10$). Valid session attendance rates computed over non-null recorded denominator:
  $$\text{Observed Attendance Rate} = \frac{\sum \text{attended}_{valid}}{\sum \mathbb{I}(\text{attended is not NaN})} \times 100$$

---

## 3. Mathematical & Econometric Specifications

### 3.1 Power Analysis & Sample Size Sizing Specification
For continuous metric (Final Score $Y$) with significance level $\alpha = 0.05$ ($Z_{\alpha/2} = 1.95996$) and statistical power $1 - \beta = 0.80$ ($Z_\beta = 0.84162$):

$$N_{total} = \frac{4 (Z_{\alpha/2} + Z_\beta)^2 \sigma^2}{\text{MDE}^2}$$

* **Historical Variance:** Baseline variance derived from clean observational controls: $\sigma = 12.13 \implies \sigma^2 = 147.137$.
* **Constant Factor:** $4 \times (1.95996 + 0.84162)^2 = 4 \times (2.80158)^2 = 4 \times 7.84887 = 31.3955$.
* **Sample Size Equation:** $N_{total} = \frac{31.3955 \times 147.137}{\text{MDE}^2} = \frac{4,619.45}{\text{MDE}^2}$.
* **Duration Specification:** Given weekly enrolment throughput $W = 1,500$ students/week:
  $$\text{Duration (weeks)} = \frac{N_{total}}{W}$$

### 3.2 Sample Ratio Mismatch (SRM) Specification
* **Test:** Pearson Goodness-of-Fit $\chi^2$ test with equal allocation ($\pi = 0.50$):
  $$\chi^2 = \sum_{k \in \{C, T\}} \frac{(O_k - E_k)^2}{E_k}, \quad df = 1$$
* **Rejection Boundary:** $\alpha_{SRM} = 0.01$. If $p < 0.01$, halt pipeline and log critical telemetry error.

### 3.3 Welch's Two-Sample t-Test Specification
Because treatment may alter outcome dispersion ($\sigma_T^2 \neq \sigma_C^2$), Student's t-test is strictly forbidden; Welch's t-test is mandatory:

$$t = \frac{\bar{Y}_T - \bar{Y}_C}{\sqrt{\frac{s_T^2}{N_T} + \frac{s_C^2}{N_C}}}$$

Degrees of freedom computed via the Welch-Satterthwaite equation:

$$\nu = \frac{\left(\frac{s_T^2}{N_T} + \frac{s_C^2}{N_C}\right)^2}{\frac{\left(\frac{s_T^2}{N_T}\right)^2}{N_T - 1} + \frac{\left(\frac{s_C^2}{N_C}\right)^2}{N_C - 1}}$$

### 3.4 Non-Parametric Bootstrap Resampling Specification
* **Iteration Count:** $B = 2,000$ independent Monte Carlo draws with replacement.
* **Vectorized Matrix Sampling:** Generate index matrices $\mathbf{I}_C \in \mathbb{N}^{B \times N_C}$ and $\mathbf{I}_T \in \mathbb{N}^{B \times N_T}$.
* **Confidence Interval:** Percentile method:
  $$\text{CI}_{95\%} = \left[ Q_{0.025}(\hat{\Delta}^*), \ Q_{0.975}(\hat{\Delta}^*) \right]$$

### 3.5 Difference-in-Differences (DiD) Specification
Panel OLS regression with center cluster-robust covariance matrix:

$$Y_{icmt} = \beta_0 + \beta_1 \text{Ahmedabad}_c + \beta_2 \text{Post}_t + \beta_3 (\text{Ahmedabad}_c \times \text{Post}_t) + \mathbf{X}_{ic}'\boldsymbol{\gamma} + \varepsilon_{icmt}$$

* **Cluster-Robust Variance:** $G = 8$ center clusters:
  $$\mathbf{V}_{cluster} = \left(\mathbf{X}'\mathbf{X}\right)^{-1} \left( \sum_{g=1}^G \mathbf{X}_g' \mathbf{e}_g \mathbf{e}_g' \mathbf{X}_g \right) \left(\mathbf{X}'\mathbf{X}\right)^{-1}$$
* **Parallel Trends Test:** Multi-period dynamic event study taking Month 3 as baseline reference:
  $$Y_{ict} = \alpha_c + \lambda_t + \sum_{m \in \{1, 2, 4, 5, 6\}} \delta_m \left(\text{Ahmedabad}_c \times \mathbb{I}(t = m)\right) + \mathbf{X}'\boldsymbol{\gamma} + \varepsilon_{ict}$$
  Joint Wald Test null hypothesis: $H_0: \delta_1 = 0 \ \wedge \ \delta_2 = 0$.

### 3.6 CUPED Variance Reduction Specification
* **Denoised Estimator:**
  $$\tilde{Y}_i = Y_i - \hat{\theta} (X_i - \bar{X}), \quad \text{where } \hat{\theta} = \frac{\widehat{\text{Cov}}(Y, X)}{\widehat{\text{Var}}(X)}$$
* **Variance Contraction:**
  $$\text{Var}(\tilde{Y}) = \text{Var}(Y) (1 - \rho_{XY}^2)$$
* **Duration Multiplier:**
  $$\text{Duration}_{CUPED} = \text{Duration}_{raw} \times (1 - \rho_{XY}^2)$$

---

## 4. CLI Execution Interface Specifications

The analysis suite exposes a unified CLI interface in `analysis_pipeline.py`:

```bash
python analysis_pipeline.py [--action {all,clean,power,ab_test,did,subgroups,cuped}]
                           [--mde MDE]
                           [--power POWER]
                           [--alpha ALPHA]
                           [--bootstrap-resamples BOOTSTRAP_RESAMPLES]
                           [--show-detailed-calc]
                           [--data-dir DATA_DIR]
                           [--fig-dir FIG_DIR]
```

### Exit Codes:
* `0`: Pipeline completed successfully with all guardrails satisfied.
* `1`: Critical SRM violation ($p < 0.01$).
* `2`: Severe guardrail breach detected (e.g., faculty overtime doubling).
* `3`: Data schema or parquet read failure.
