"""
Data Generator for ShikshaSetu Gujarat Coaching Institute Chain
Creates ~400,000 raw operational records:
- raw_enrolments.parquet & .csv (~32,000 rows with duplicate enrollments and active-marked dropouts)
- raw_attendance.parquet & .csv (~250,000 rows with missing records for recorded sessions)
- raw_assignments.parquet & .csv (~100,000 rows)
- raw_assessments.parquet & .csv (~35,000 rows)
Total: ~417,000 rows
"""

import os
import numpy as np
import pandas as pd

def generate_coaching_data(output_dir="coaching_experiment_analysis/data", seed=42):
    np.random.seed(seed)
    os.makedirs(output_dir, exist_ok=True)
    print("Starting data synthesis for ShikshaSetu Gujarat...")

    # -------------------------------------------------------------
    # 1. SETUP CENTRES AND BATCHES
    # -------------------------------------------------------------
    ahmedabad_centers = ['Ahmedabad_Navrangpura', 'Ahmedabad_Satellite', 'Ahmedabad_Maninagar', 'Ahmedabad_Vastrapur']
    vadodara_centers = ['Vadodara_Alkapuri', 'Vadodara_Sayajigunj', 'Vadodara_Fatehgunj', 'Vadodara_Karelibaug']
    all_centers = ahmedabad_centers + vadodara_centers
    tracks = ['JEE_NEET_STEM', 'Commerce_CA', 'Foundation_9_10']

    # Total unique learners: 30,000
    # Cohorts:
    # 1) Historical DiD Cohort: 20,000 learners across 6 months (Months 1 to 6)
    #    Ahmedabad (Treated Region in M4-6) vs Vadodara (Control Region)
    # 2) Active A/B Experiment Cohort: 10,000 learners in Month 7 (5,000 Control, 5,000 Treatment)
    
    n_historical = 20000
    n_experiment = 10000
    total_learners = n_historical + n_experiment

    learner_ids = [f"LRN_{i:06d}" for i in range(1, total_learners + 1)]
    
    # Assign Cohorts
    cohorts = ['historical_did'] * n_historical + ['active_ab_experiment'] * n_experiment
    
    # Assign Cities & Centers
    # Historical: 50% Ahmedabad, 50% Vadodara
    # Experiment: 60% Ahmedabad, 40% Vadodara (or city-wide pilot)
    cities = []
    centers = []
    months = []
    
    # Historical cohort: 20,000 learners across 6 months (Months 1 to 6)
    # Balanced independent assignment across months and cities
    hist_cities = np.random.choice(['Ahmedabad', 'Vadodara'], size=n_historical, p=[0.50, 0.50])
    hist_months = np.random.choice([1, 2, 3, 4, 5, 6], size=n_historical)
    
    cities = list(hist_cities)
    months = list(hist_months)
    centers = []
    
    for city in hist_cities:
        if city == 'Ahmedabad':
            centers.append(np.random.choice(ahmedabad_centers))
        else:
            centers.append(np.random.choice(vadodara_centers))

    # Experiment cohort: 10,000 learners in Month 7
    exp_cities = np.random.choice(['Ahmedabad', 'Vadodara'], size=n_experiment, p=[0.50, 0.50])
    for city in exp_cities:
        cities.append(city)
        if city == 'Ahmedabad':
            centers.append(np.random.choice(ahmedabad_centers))
        else:
            centers.append(np.random.choice(vadodara_centers))
        months.append(7)

    # Tracks
    track_probs = [0.50, 0.30, 0.20]
    learner_tracks = np.random.choice(tracks, size=total_learners, p=track_probs)
    
    # Demographics & Baselines
    genders = np.random.choice(['Female', 'Male'], size=total_learners, p=[0.46, 0.54])
    age_tiers = np.random.choice(['14-16 (Foundation)', '16-18 (Senior)', '18+ (Repeater)'], size=total_learners, p=[0.25, 0.65, 0.10])
    
    # Baseline diagnostic scores (pre-test, scale 0-100)
    # Bell-shaped around 62 with standard deviation 13
    baseline_diagnostic_scores = np.clip(np.random.normal(loc=62.0, scale=13.0, size=total_learners), 20.0, 98.0).round(1)
    
    # Baseline prior attendance rate (prior term or initial 2 weeks)
    baseline_attendance = np.clip(np.random.beta(a=7, b=2, size=total_learners) * 100, 30.0, 100.0).round(1)

    # -------------------------------------------------------------
    # 2. EXPERIMENT ASSIGNMENT & HISTORICAL INTERVENTION
    # -------------------------------------------------------------
    # For historical DiD:
    # Treated if city == 'Ahmedabad' and month in [4, 5, 6]
    # For experiment:
    # 50:50 random assignment into Control vs Treatment
    is_treated_did = [(city == 'Ahmedabad' and m >= 4) for city, m in zip(cities[:n_historical], months[:n_historical])]
    is_treated_did = is_treated_did + [False] * n_experiment
    
    experiment_variant = ['Not_In_Experiment'] * n_historical
    # In experiment: randomize 1:1
    exp_assignment = np.random.choice(['Control', 'Treatment'], size=n_experiment, p=[0.50, 0.50])
    experiment_variant.extend(exp_assignment)

    # -------------------------------------------------------------
    # 3. CONSTRUCT TRUE OUTCOMES WITH CAUSAL EFFECTS & SEASONALITY
    # -------------------------------------------------------------
    # Final assessment score (0-100):
    # Highly correlated with baseline_diagnostic_score (rho ~ 0.72)
    # Seasonal effect in Month 4, 5, 6, 7: +4.2 points (exam prep push in Gujarat)
    # DiD intervention effect in Ahmedabad (M4-6): +3.1 points
    # A/B Experiment Treatment effect (M7 Treatment): +3.5 points overall, with heterogeneity!
    
    true_final_scores = []
    true_completed = []
    true_dropped = []
    early_dropped = []
    learner_csat = []
    faculty_overtime = []

    for i in range(total_learners):
        base_s = baseline_diagnostic_scores[i]
        m = months[i]
        cohort = cohorts[i]
        city = cities[i]
        track = learner_tracks[i]
        
        # Base expected progression
        progression = 0.72 * (base_s - 62.0) + 68.0 + np.random.normal(0, 7.5)
        
        # Seasonality effect (exam prep period in Q3/Q4 across all cities)
        if m in [4, 5, 6, 7]:
            progression += 4.2  # Gujarat state-wide exam surge
            
        # Historical DiD Treatment effect in Ahmedabad for M4-6
        if cohort == 'historical_did' and is_treated_did[i]:
            progression += 3.1
            
        # A/B Experiment Treatment effect
        if cohort == 'active_ab_experiment':
            var = experiment_variant[i]
            if var == 'Treatment':
                # Heterogeneous treatment effect:
                # Low baseline learners (<60) gain +5.8 points!
                # Medium baseline learners (60-80) gain +3.3 points
                # High baseline learners (>80) gain +1.1 points
                if base_s < 60:
                    progression += 5.8
                elif base_s <= 80:
                    progression += 3.3
                else:
                    progression += 1.1
                    
                # Track heterogeneity: STEM gains slightly more from doubt clinics
                if track == 'JEE_NEET_STEM':
                    progression += 0.8
                elif track == 'Commerce_CA':
                    progression -= 0.4
                    
        final_score = np.clip(progression, 15.0, 100.0).round(1)
        true_final_scores.append(final_score)
        
        # Course Completion & Dropout probability
        # Linked to score and attendance
        p_comp = 0.50 + 0.005 * (final_score - 60) + 0.002 * (baseline_attendance[i] - 70)
        
        if cohort == 'historical_did':
            if m in [4, 5, 6]:
                p_comp += 0.035  # seasonal completion boost
            if is_treated_did[i]:
                p_comp += 0.030  # DiD policy lift
        elif cohort == 'active_ab_experiment':
            p_comp += 0.035  # seasonal
            if experiment_variant[i] == 'Treatment':
                p_comp += 0.045  # A/B Treatment lift
                
        p_comp = np.clip(p_comp, 0.15, 0.95)
        completed = np.random.binomial(1, p_comp)
        true_completed.append(completed)
        
        # If not completed, is it dropped or failed?
        # About 65% of non-completers actively drop out before week 8
        if completed == 1:
            dropped = 0
            e_drop = 0
        else:
            dropped = 1 if np.random.rand() < 0.70 else 0
            e_drop = 1 if (dropped == 1 and np.random.rand() < 0.55) else 0
            
        true_dropped.append(dropped)
        early_dropped.append(e_drop)
        
        # Guardrail metrics
        if cohort == 'active_ab_experiment':
            var = experiment_variant[i]
            # Learner CSAT (1 to 5)
            csat_mean = 4.3 if var == 'Treatment' else 3.8
            csat = int(np.clip(np.round(np.random.normal(csat_mean, 0.75)), 1, 5))
            learner_csat.append(csat)
            
            # Faculty overtime hours per learner
            ot_mean = 0.88 if var == 'Treatment' else 0.45
            ot = max(0.0, np.round(np.random.normal(ot_mean, 0.20), 2))
            faculty_overtime.append(ot)
        else:
            learner_csat.append(np.nan)
            faculty_overtime.append(np.nan)

    # -------------------------------------------------------------
    # 4. INJECT ANOMALY: Drop-outs Still Marked Active (ERP Lag)
    # -------------------------------------------------------------
    # Coaching center front-desks frequently fail to mark dropped students as 'Dropped'.
    # In official ERP records:
    # ~60% of actual dropped students are still marked 'Active'!
    official_status = []
    for i in range(total_learners):
        if true_completed[i] == 1:
            official_status.append('Completed')
        elif true_dropped[i] == 1:
            # 60% administrative delay -> marked 'Active'
            if np.random.rand() < 0.60:
                official_status.append('Active')  # Anomaly!
            else:
                official_status.append('Dropped')
        else:
            # Not completed, not dropped = Attended but failed/incomplete
            official_status.append('Active')

    # Batch IDs
    batch_ids = [f"BATCH_{city[:3].upper()}_M{m}_{track[:3]}_{(i % 12) + 1:02d}" 
                 for i, (city, m, track) in enumerate(zip(cities, months, learner_tracks))]

    # Create Enrolment DataFrame
    df_enrolments = pd.DataFrame({
        'enrollment_id': [f"ENR_{i:06d}" for i in range(1, total_learners + 1)],
        'learner_id': learner_ids,
        'batch_id': batch_ids,
        'city': cities,
        'center_id': centers,
        'month': months,
        'cohort_type': cohorts,
        'course_track': learner_tracks,
        'gender': genders,
        'age_tier': age_tiers,
        'baseline_diagnostic_score': baseline_diagnostic_scores,
        'baseline_attendance_rate': baseline_attendance,
        'experiment_variant': experiment_variant,
        'is_treated_did': is_treated_did,
        'official_status': official_status,  # Contains dirty active dropouts!
        'true_completed': true_completed,
        'true_dropped': true_dropped,
        'early_dropped': early_dropped,
        'final_score': true_final_scores,
        'csat_score': learner_csat,
        'faculty_overtime_hours': faculty_overtime
    })

    # -------------------------------------------------------------
    # 5. INJECT ANOMALY: Duplicate Enrolments in the Same Batch (~1.5%)
    # -------------------------------------------------------------
    n_dupes = int(total_learners * 0.015)
    dupe_indices = np.random.choice(total_learners, size=n_dupes, replace=False)
    dupe_rows = df_enrolments.iloc[dupe_indices].copy()
    # Create new enrollment_id for duplicate row but KEEP learner_id and batch_id identical!
    dupe_rows['enrollment_id'] = [f"ENR_DUP_{i:05d}" for i in range(n_dupes)]
    
    df_enrolments_dirty = pd.concat([df_enrolments, dupe_rows], ignore_index=True)
    # Shuffle
    df_enrolments_dirty = df_enrolments_dirty.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    print(f"Enrolments created: {len(df_enrolments_dirty):,} rows (including {n_dupes:,} duplicate enrolments and dropouts marked active).")

    # -------------------------------------------------------------
    # 6. GENERATE ATTENDANCE RECORDS (~250,000 rows)
    # -------------------------------------------------------------
    # Each course has 10 recorded curriculum sessions.
    # We sample sessions for learners.
    # Active students attend 7-10 sessions.
    # True dropped students stop attending after session 2 or 3!
    # ANOMALY: ~8% missing attendance records for recorded sessions (tablets offline / sync failures).
    
    print("Generating attendance session logs...")
    att_learner_ids = []
    att_batch_ids = []
    att_session_nums = []
    att_session_types = []
    att_attended = []
    att_is_recorded = []
    
    # Generate for all unique learners (30,000)
    for i in range(total_learners):
        lid = learner_ids[i]
        bid = batch_ids[i]
        is_drop = true_dropped[i]
        is_early_drop = early_dropped[i]
        comp = true_completed[i]
        base_att_rate = baseline_attendance[i] / 100.0
        
        # Total sessions in course = 8 to 10 sessions logged
        n_sessions = 8
        for s in range(1, n_sessions + 1):
            att_learner_ids.append(lid)
            att_batch_ids.append(bid)
            att_session_nums.append(s)
            
            s_type = 'Lecture' if s in [1, 2, 4, 5, 7] else ('Doubt_Lab' if s in [3, 6] else 'Revision')
            att_session_types.append(s_type)
            
            is_rec = True if s % 2 == 1 else False
            att_is_recorded.append(is_rec)
            
            # Attendance logic:
            if is_early_drop == 1 and s > 2:
                attended_val = 0
            elif is_drop == 1 and s > 4:
                attended_val = 0
            else:
                prob = base_att_rate if comp == 1 else (base_att_rate * 0.75)
                attended_val = 1 if np.random.rand() < prob else 0
                
            # INJECT ANOMALY: Attendance missing for recorded sessions (~8% missingness)
            if is_rec and np.random.rand() < 0.08:
                att_attended.append(np.nan)
            elif (not is_rec) and np.random.rand() < 0.03:
                att_attended.append(np.nan)
            else:
                att_attended.append(attended_val)

    df_attendance = pd.DataFrame({
        'attendance_id': [f"ATT_{i:07d}" for i in range(1, len(att_learner_ids) + 1)],
        'learner_id': att_learner_ids,
        'batch_id': att_batch_ids,
        'session_num': att_session_nums,
        'session_type': att_session_types,
        'is_recorded_session': att_is_recorded,
        'attended': att_attended
    })
    print(f"Attendance created: {len(df_attendance):,} rows (with missing attendance on recorded sessions).")

    # -------------------------------------------------------------
    # 7. GENERATE ASSIGNMENT RECORDS (~100,000 rows)
    # -------------------------------------------------------------
    # 3 major milestone assignments per learner.
    # True dropped learners submit 0 or 1 assignment.
    print("Generating assignment records...")
    asgn_learner_ids = []
    asgn_batch_ids = []
    asgn_nums = []
    asgn_submitted = []
    asgn_scores = []
    asgn_on_time = []

    for i in range(total_learners):
        lid = learner_ids[i]
        bid = batch_ids[i]
        is_drop = true_dropped[i]
        f_score = true_final_scores[i]
        comp = true_completed[i]
        
        is_early_drop = early_dropped[i]
        
        for a_num in [1, 2, 3]:
            asgn_learner_ids.append(lid)
            asgn_batch_ids.append(bid)
            asgn_nums.append(a_num)
            
            if is_early_drop == 1:
                # Dropped out very early (session 1-2), submitted 0 assignments
                sub = 0
                score = np.nan
                ontime = 0
            elif is_drop == 1 and a_num >= 2:
                # Dropped out, didn't submit assignments 2 & 3
                sub = 0
                score = np.nan
                ontime = 0
                sub = 0
                score = np.nan
                ontime = 0
            elif comp == 0 and a_num == 3 and np.random.rand() < 0.5:
                sub = 0
                score = np.nan
                ontime = 0
            else:
                sub = 1
                score = np.clip(np.random.normal(f_score + 2.0, 6.0), 30.0, 100.0).round(1)
                ontime = 1 if np.random.rand() < 0.85 else 0
                
            asgn_submitted.append(sub)
            asgn_scores.append(score)
            asgn_on_time.append(ontime)

    df_assignments = pd.DataFrame({
        'assignment_id': [f"ASG_{i:06d}" for i in range(1, len(asgn_learner_ids) + 1)],
        'learner_id': asgn_learner_ids,
        'batch_id': asgn_batch_ids,
        'assignment_num': asgn_nums,
        'is_submitted': asgn_submitted,
        'assignment_score': asgn_scores,
        'on_time': asgn_on_time
    })
    print(f"Assignments created: {len(df_assignments):,} rows.")

    # -------------------------------------------------------------
    # 8. GENERATE ASSESSMENT RECORDS (~35,000 rows)
    # -------------------------------------------------------------
    # Diagnostic Baseline + Final Assessment for active learners
    print("Generating assessment records...")
    asm_learner_ids = []
    asm_types = []
    asm_scores = []
    
    for i in range(total_learners):
        lid = learner_ids[i]
        # Baseline assessment (everyone takes at enrollment)
        asm_learner_ids.append(lid)
        asm_types.append('Baseline_Diagnostic')
        asm_scores.append(baseline_diagnostic_scores[i])
        
        # Final assessment (only those who did not early drop take it)
        if early_dropped[i] == 0:
            asm_learner_ids.append(lid)
            asm_types.append('Final_Assessment')
            asm_scores.append(true_final_scores[i])

    df_assessments = pd.DataFrame({
        'assessment_id': [f"ASM_{i:06d}" for i in range(1, len(asm_learner_ids) + 1)],
        'learner_id': asm_learner_ids,
        'assessment_type': asm_types,
        'score': asm_scores
    })
    print(f"Assessments created: {len(df_assessments):,} rows.")

    total_rows = len(df_enrolments_dirty) + len(df_attendance) + len(df_assignments) + len(df_assessments)
    print(f"--> TOTAL SYNTHESIZED ROWS: {total_rows:,} across 4 tables.")

    # -------------------------------------------------------------
    # 9. SAVE TO PARQUET AND CSV
    # -------------------------------------------------------------
    print("Saving datasets to disk...")
    df_enrolments_dirty.to_parquet(os.path.join(output_dir, "raw_enrolments.parquet"), index=False)
    df_attendance.to_parquet(os.path.join(output_dir, "raw_attendance.parquet"), index=False)
    df_assignments.to_parquet(os.path.join(output_dir, "raw_assignments.parquet"), index=False)
    df_assessments.to_parquet(os.path.join(output_dir, "raw_assessments.parquet"), index=False)
    
    # Also save CSV for portability / standard inspections
    df_enrolments_dirty.to_csv(os.path.join(output_dir, "raw_enrolments.csv"), index=False)
    print("Datasets successfully generated and saved to 'coaching_experiment_analysis/data'.")
    return total_rows

if __name__ == "__main__":
    generate_coaching_data()
