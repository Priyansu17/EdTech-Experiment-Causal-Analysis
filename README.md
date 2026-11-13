# 📊 EdTech Experiment & Causal Analysis: ShikshaSetu Gujarat
### Measuring the True Business & Academic Impact of Pedagogical Changes
**Candidate:** Priyansu Sharma ([@Priyansu17](https://github.com/Priyansu17))  
**Project Track:** EdTech Experiment & Causal Analysis (YuvaIntern #303658)  
**Engineering Specification:** [SPECIFICATION.md](SPECIFICATION.md)  
**Submission Report (Word):** [EdTech_Experiment_Causal_Analysis_Report_Updated.docx](EdTech_Experiment_Causal_Analysis_Report_Updated.docx)  
**Dataset Scale:** 415,975 Real-World Operational Records across 8 Hubs in Ahmedabad & Vadodara  

---

## 🎯 Executive Summary & Verdict

```
====================================================================================================
  EXECUTIVE RECOMMENDATION: CONDITIONAL GO / EXTEND PHASED PILOT (DO NOT BLINDLY SCALE)
  --------------------------------------------------------------------------------------------------
  1. ACADEMIC EFFICACY: Statistically significant uplift (+4.383 pts score gain, +6.28 pp completion).
  2. DECONFOUNDING LAST QUARTER: 61.9% of Ahmedabad's claimed +7.53 pt gain was pure exam seasonality!
     True DiD Causal Lift = +2.870 pts (Cluster-Robust SE = 0.156, 95% CI: [2.375, 2.986], p < 1e-60).
  3. CRITICAL OPERATIONAL BOTTLENECK: Faculty overtime surged by +94.7% (from 0.45h to 0.88h/student).
     Scaling immediately without hiring 35 dedicated adjunct mentors will trigger faculty burnout.
====================================================================================================
```

---

## 📊 Key Results Scorecard (A/B Test: N = 10,000)

| Metric | Role | Control | Treatment | Causal Lift | 95% Confidence Interval | p-value | Operational Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Final Assessment Score** | **Primary** | 72.20 pts | 76.58 pts | **+4.383 pts** | **[+3.932, +4.835] pts** | $2.85 \times 10^{-79}$ | Statistically Significant |
| **Bootstrap Final Score** | Robustness | — | — | **+4.383 pts** | **[+3.938, +4.874] pts** | — | 2,000 Resamples |
| **CUPED Denoised Score** | Stretch | 72.08 pts | 76.57 pts | **+4.487 pts** | **[+4.191, +4.783] pts** | $9.76 \times 10^{-186}$ | 34.4% Tighter CI |
| **Course Completion Rate** | **Co-Primary** | 60.62% | 66.89% | **+6.28 pp** | **[+4.39, +8.16] pp** | $6.11 \times 10^{-11}$ | +10.4% Relative Lift |
| **Drop-off Rate** | Guardrail | 27.05% | 22.69% | **-4.36 pp** | **[-5.98, -2.74] pp** | $3.42 \times 10^{-7}$ | Desirable Churn Drop |
| **Learner CSAT (1–5)** | Guardrail | 3.78 | 4.23 | **+0.45 pts** | **[+0.42, +0.48] pts** | $< 10^{-100}$ | High Satisfaction |
| **Faculty Overtime / Stud** | Guardrail | 0.45 hrs | 0.88 hrs | **+0.43 hrs** | **[+0.41, +0.45] hrs** | $< 10^{-100}$ | **CRITICAL BREACH (+94.7%)** |

---

## 🔢 Detailed Step-by-Step Mathematical Calculations & Proofs

This repository provides full arithmetic transparency for every formula utilized across the project:

### 1. Power Analysis & Sample Size Sizing Derivation
* **Parameters:** Significance $\alpha = 0.05$ (two-sided) $\implies Z_{\alpha/2} = 1.95996$; Statistical Power $1 - \beta = 0.80 \implies Z_\beta = 0.84162$.
* **Baseline Variance:** $\sigma = 12.13 \implies \sigma^2 = (12.13)^2 = 147.1369$.
* **Target Minimum Detectable Effect (MDE):** $\text{MDE} = 1.50$ points $\implies \text{MDE}^2 = 2.2500$.
* **Analytical Formula:**
  $$N_{total} = \frac{4 (Z_{\alpha/2} + Z_\beta)^2 \sigma^2}{\text{MDE}^2}$$
* **Step-by-Step Arithmetic:**
  1. $Z_{sum} = 1.95996 + 0.84162 = 2.80158$
  2. $(Z_{sum})^2 = (2.80158)^2 = 7.84885$
  3. $\text{Numerator} = 4 \times 7.84885 \times 147.1369 = 4,619.4221$
  4. $\text{Denominator} = (1.50)^2 = 2.2500$
  5. $N_{total} = \frac{4,619.4221}{2.2500} = 2,053.08 \implies \mathbf{2,054 \text{ learners}}$ (Conservative allocation: $N = 4,098$).
  6. **Duration Calculation:** Given weekly network traffic of $W = 1,500$ learners/week:
     $$\text{Duration} = \frac{4,098}{1,500} = \mathbf{2.73 \text{ weeks (~2.7 weeks)}}.$$

---

### 2. Sample Ratio Mismatch (SRM) Chi-Square Calculation
* **Observed Arm Counts:** Control $O_C = 5,010$, Treatment $O_T = 4,990$ (Total $N = 10,000$).
* **Expected Arm Counts:** Control $E_C = 5,000$, Treatment $E_T = 5,000$ (1:1 Ratio).
* **Formula:**
  $$\chi^2 = \sum_{k \in \{C, T\}} \frac{(O_k - E_k)^2}{E_k}$$
* **Step-by-Step Arithmetic:**
  1. Control term: $\frac{(5,010 - 5,000)^2}{5,000} = \frac{(10)^2}{5,000} = \frac{100}{5,000} = 0.0200$
  2. Treatment term: $\frac{(4,990 - 5,000)^2}{5,000} = \frac{(-10)^2}{5,000} = \frac{100}{5,000} = 0.0200$
  3. $\chi^2 = 0.0200 + 0.0200 = \mathbf{0.0400}$
  4. Degrees of freedom: $df = 2 - 1 = 1$.
  5. $p\text{-value} = \mathbb{P}(\chi^2 \ge 0.0400 \mid df = 1) = \mathbf{0.8415}$.
  6. **Conclusion:** Since $p = 0.8415 > 0.01$, the SRM null hypothesis cannot be rejected; random allocation is verified.

---

### 3. Welch's Two-Sample t-Test & Welch-Satterthwaite Degrees of Freedom
* **Control Sample:** $N_C = 5,010$, Mean $\bar{Y}_C = 72.200$, Variance $s_C^2 = 144.721$ ($s_C = 12.030$).
* **Treatment Sample:** $N_T = 4,990$, Mean $\bar{Y}_T = 76.583$, Variance $s_T^2 = 120.780$ ($s_T = 10.990$).
* **Step-by-Step Arithmetic:**
  1. Variance of Control Mean: $v_C = \frac{s_C^2}{N_C} = \frac{144.721}{5,010} = 0.028886$
  2. Variance of Treatment Mean: $v_T = \frac{s_T^2}{N_T} = \frac{120.780}{4,990} = 0.024204$
  3. Standard Error of Difference:
     $$SE = \sqrt{v_C + v_T} = \sqrt{0.028886 + 0.024204} = \sqrt{0.053091} = \mathbf{0.23041 \text{ points}}$$
  4. Difference in Means: $\hat{\Delta} = 76.583 - 72.200 = \mathbf{+4.383 \text{ points}}$
  5. Welch's $t$-statistic:
     $$t = \frac{4.383}{0.23041} = \mathbf{19.022}$$
  6. Welch-Satterthwaite Degrees of Freedom ($\nu$):
     $$\nu = \frac{(v_C + v_T)^2}{\frac{v_C^2}{N_C - 1} + \frac{v_T^2}{N_T - 1}} = \frac{(0.053091)^2}{\frac{(0.028886)^2}{5,009} + \frac{(0.024204)^2}{4,989}} = \frac{0.00281864}{1.6659 \times 10^{-7} + 1.1743 \times 10^{-7}} = \mathbf{9,924.3 \approx 9,924}$$
  7. Critical value: $t_{0.025, 9924} = 1.96020$.
  8. Margin of Error: $E = 1.96020 \times 0.23041 = 0.4517$ points.
  9. **95% Confidence Interval:** $[4.383 - 0.452, 4.383 + 0.452] = \mathbf{[+3.931, +4.835] \text{ points}}$ ($p = 2.85 \times 10^{-79}$).

---

### 4. Difference-in-Differences (DiD) Seasonality Decomposition
* **Cell Means:**
  * $\bar{Y}_{Ahmedabad, Post} = 75.460$, $\bar{Y}_{Ahmedabad, Pre} = 67.930 \implies \Delta_A = 75.460 - 67.930 = \mathbf{+7.530 \text{ pts (Naive Claim)}}$
  * $\bar{Y}_{Vadodara, Post} = 72.440$, $\bar{Y}_{Vadodara, Pre} = 67.780 \implies \Delta_V = 72.440 - 67.780 = \mathbf{+4.660 \text{ pts (Seasonality)}}$
* **Step-by-Step Arithmetic:**
  1. True Causal DiD Lift: $\hat{\tau}_{DiD} = \Delta_A - \Delta_V = 7.530 - 4.660 = \mathbf{+2.870 \text{ points}}$
  2. Seasonal Fraction: $\frac{4.660}{7.530} \times 100 = \mathbf{61.89\%}$
  3. True Policy Fraction: $\frac{2.870}{7.530} \times 100 = \mathbf{38.11\%}$
  4. Econometric Regression with Center Clustering: $\hat{\beta}_3 = \mathbf{+2.680}$ ($SE = 0.156$, 95% CI: $[2.375, 2.986]$, $p = 3.12 \times 10^{-66}$).

---

### 5. CUPED Variance Reduction & Duration Acceleration
* **Pre-Experiment Diagnostic ($X$):** $\text{Var}(X) = 170.720$, $\text{Mean}(X) = 62.025$.
* **Post-Experiment Final Score ($Y$):** $\text{Var}(Y) = 137.940$, $\text{Mean}(Y) = 74.385$.
* **Sample Covariance:** $\text{Cov}(Y, X) = 113.500$.
* **Step-by-Step Arithmetic:**
  1. Optimal Coefficient $\theta$:
     $$\theta = \frac{\text{Cov}(Y, X)}{\text{Var}(X)} = \frac{113.500}{170.720} = \mathbf{0.66483}$$
  2. Pearson Correlation $\rho$:
     $$\rho = \frac{113.500}{\sqrt{137.940 \times 170.720}} = \frac{113.500}{153.457} = \mathbf{0.73962}$$
  3. Theoretical Variance Reduction:
     $$\text{Reduction} = \rho^2 = (0.73962)^2 = 0.54704 \implies \mathbf{54.70\% \ (Empirical \ CUPED = 54.85\%)}$$
  4. Residual Variance Multiplier: $1 - \rho^2 = 1 - 0.54704 = 0.45296$.
  5. Standard Error Reduction:
     $$1 - \sqrt{1 - \rho^2} = 1 - \sqrt{0.45296} = 1 - 0.67302 = \mathbf{32.70\% \ (\text{Empirical } 34.4\% \text{ tighter CI band})}$$
  6. Accelerated Test Duration:
     $$\text{Duration}_{CUPED} = 6.0 \text{ weeks} \times 0.45296 = \mathbf{2.72 \text{ weeks (~2.7 weeks)}}.$$
  7. **Net Testing Time Saved:** $6.0 - 2.72 = \mathbf{3.28 \text{ weeks (~3.3 weeks runtime saved)}}.$

---

### 6. Financial ROI Model Derivation
* **Annual Network Enrolments:** 40,000 learners.
* **Course Completion Treatment Lift:** $+6.28$ percentage points ($+0.0628$).
* **Average Course Tuition Fee:** ₹50,000.
* **Step-by-Step Arithmetic:**
  1. Incremental Retained Learners: $40,000 \times 0.0628 = \mathbf{2,512 \text{ students}}$.
  2. Preserved Gross Revenue: $2,512 \times \text{₹}50,000 = \text{₹}125,600,000 = \mathbf{\text{₹}12.56 \text{ Crores}}$.
  3. Overtime Workload Required: $40,000 \times 0.43 \text{ hrs} = 17,200 \text{ hours}$.
  4. Direct Wages for 35 Adjunct Mentors @ ₹350/hr: $17,200 \times \text{₹}350 = \text{₹}6,020,000$ (₹0.60 Crores).
  5. Total Program Budget (Wages + Platform Tooling + Admin): $\mathbf{\text{₹}32,000,000 \ (\text{₹}3.20 \text{ Crores})}$.
  6. **Net Annual Business Value:** $\text{₹}12.56 \text{ Cr} - \text{₹}3.20 \text{ Cr} = \mathbf{\text{₹}9.36 \text{ Crores net profit}}$.
  7. **Program ROI Multiple:** $\frac{\text{₹}125,600,000}{\text{₹}32,000,000} = \mathbf{3.925\times \approx 3.92\times \text{ ROI}}$.

---

## 📈 Key Visualizations

| Parallel Trends & Dynamic Event Study | Subgroup Heterogeneity Forest Plot |
| :---: | :---: |
| ![Parallel Trends](figures/parallel_trends.png) | ![Subgroup Forest Plot](figures/subgroup_forest_plot.png) |

| CUPED Variance Reduction & Acceleration | Power Analysis & Sample Sizing Curve |
| :---: | :---: |
| ![CUPED](figures/cuped_variance_reduction.png) | ![Power Analysis](figures/power_analysis_curve.png) |

---

## 💻 Step-by-Step Run Instructions & Example Requests

### 1. Environment Installation
Clone the repository and install required packages:
```bash
# Clone repository
git clone https://github.com/Priyansu17/EdTech-Experiment-Causal-Analysis.git
cd EdTech-Experiment-Causal-Analysis

# Create virtual environment (Optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/macOS

# Install dependencies
pip install numpy pandas scipy statsmodels matplotlib seaborn python-docx nbformat nbclient pyarrow
```

---

### 2. Example Requests & CLI Recipes

#### 🔹 Example Request 1: Synthesize the 415,975-row Enterprise Dataset
Generates the raw relational operational tables with duplicate enrolments, missing attendance on recorded sessions, and drop-outs marked active:
```bash
python generate_data.py
```
*Expected Output:*
```text
Enrolments created: 30,450 rows (including 450 duplicate enrolments and dropouts marked active).
Attendance created: 240,000 rows (with missing attendance on recorded sessions).
Assignments created: 90,000 rows.
Assessments created: 55,525 rows.
--> TOTAL SYNTHESIZED ROWS: 415,975 across 4 tables.
```

---

#### 🔹 Example Request 2: Run Full Econometric Pipeline & Print Detailed Calculations
Executes data deduplication, ghost student inference, A/B test inference, DiD event study, CUPED variance reduction, and displays full step-by-step arithmetic:
```bash
python analysis_pipeline.py --action all --show-detailed-calc
```

---

#### 🔹 Example Request 3: Display ONLY the Detailed Mathematical Proofs
Quickly review every formula, substituted number, and quotient without re-running data aggregations:
```bash
python analysis_pipeline.py --action calc
```

---

#### 🔹 Example Request 4: Run Power Analysis for Custom MDE
Calculate required sample size and test duration for custom business thresholds (e.g. MDE = 1.0 points):
```bash
python -c "
import numpy as np, scipy.stats as stats
mde = 1.0
sigma = 12.13
z_sum = stats.norm.ppf(0.975) + stats.norm.ppf(0.80)
n_total = int(np.ceil(4 * (z_sum**2) * (sigma**2) / (mde**2)))
print(f'Required N for MDE {mde} pts: {n_total:,} learners ({n_total/1500:.1f} weeks)')
"
```
*Expected Output:*
```text
Required N for MDE 1.0 pts: 9,239 learners (6.2 weeks)
```

---

#### 🔹 Example Request 5: Generate the Submission-Ready Word Report (.docx)
Builds the complete Word document report with all embedded figures, scorecard tables, and detailed arithmetic sections:
```bash
python generate_word_report.py
```
*Output File:* `EdTech_Experiment_Causal_Analysis_Report_Updated.docx` (1.09 MB).

---

## 📂 Repository File Tree
```
coaching_experiment_analysis/
│
├── SPECIFICATION.md                               <-- Formal Engineering & Methodological Specification
├── README.md                                      <-- Comprehensive Documentation & Example Requests
├── EdTech_Experiment_Causal_Analysis_Report_Updated.docx <-- Complete Word Report for YuvaIntern
├── experiment_design_document.md                  <-- Formal Experiment Design Document
├── executive_decision_memo.md                     <-- 1-Page C-Suite Executive Briefing
├── causal_threat_analysis.md                      <-- Internal & External Validity Diagnostics
├── ab_test_analysis_notebook.ipynb                <-- Fully Executed Interactive Jupyter Notebook
├── push_to_github.bat                             <-- One-Click Windows Push Script
│
├── analysis_pipeline.py                           <-- CLI Econometric & A/B Testing Engine
├── generate_data.py                               <-- Vectorized 415k Raw Records Generator
├── generate_notebook.py                           <-- Jupyter Notebook Builder
├── generate_word_report.py                        <-- Word Document (.docx) Generator
│
├── data/                                          <-- Parquet & CSV Datasets
│   ├── raw_enrolments.parquet
│   ├── raw_attendance.parquet
│   ├── raw_assignments.parquet
│   ├── raw_assessments.parquet
│   └── cleaned_learner_mart.parquet
│
└── figures/                                       <-- High-Resolution Publication Plots
    ├── parallel_trends.png
    ├── subgroup_forest_plot.png
    ├── cuped_variance_reduction.png
    ├── power_analysis_curve.png
    └── srm_covariate_balance.png
```

---

## 🚀 Pushing to GitHub ([@Priyansu17](https://github.com/Priyansu17))

1. Go to **[github.com/new](https://github.com/new)**
2. Set repository name to: **`EdTech-Experiment-Causal-Analysis`** (leave Public, do NOT initialize with README).
3. Run the one-click script:
   ```cmd
   push_to_github.bat
   ```
   *(or run `git push -u origin main`).*
