#!/usr/bin/env python3
"""Add categories 6-10 to the multilingual clinical benchmark (100 cases)."""
import os, json
from typing import List, Dict, Any

BENCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multilingual_clinical_200_benchmark.json")

with open(BENCH, encoding="utf-8") as f:
    data = json.load(f)
cases = data["cases"]
start = len(cases)

def add(cat, lang, q, ref, facts, sources, safety=False, diff="intermediate"):
    idx = len(cases) + 1
    cases.append({
        "id": f"vastcare_bench_{idx:03d}",
        "category": cat, "language": lang, "question": q,
        "reference_answer": ref, "key_medical_facts": facts,
        "evidence_sources": sources, "safety_critical": safety,
        "difficulty": diff, "expert_reviewed": False,
        "annotation_label": "Guideline-Derived Clinical Evaluation Benchmark"
    })

# ============ CATEGORY 6: EVIDENCE GROUNDING (20) ============
add("evidence_grounding", "en",
    "What are the WHO guideline recommendations for zinc supplementation alongside ORS in pediatric acute diarrhea?",
    "WHO recommends 20 mg elemental zinc daily for 14 days for children >6 months (10 mg/day for infants <6 months) suffering from acute diarrhea. Zinc reduces the duration, severity, and stool frequency of the current episode, and decreases the incidence of subsequent diarrhea episodes in the subsequent 2-3 months by promoting enterocyte mucosal repair and cellular immune function.",
    ["20 mg/day for children >6 months, 10 mg/day for <6 months", "Standard duration is 14 days", "Reduces recurrence of diarrhea for following 2-3 months"],
    ["WHO Guidelines on Diarrhoeal Disease Management", "Cochrane Systematic Review on Oral Zinc"], False, "intermediate")

add("evidence_grounding", "en",
    "What are the ICMR-NIN 2024 Dietary Guidelines recommendations on cooking oil rotation and daily limits for adults?",
    "ICMR-NIN 2024 guidelines recommend a daily intake of 20-30 grams (approximately 4-6 teaspoons) of visible fats and oils per person per day. It advises rotating or combining cooking oils rich in different fatty acid profiles (e.g., groundnut/mustard for MUFA, sunflower/soybean for PUFA) or using blended oils to achieve a balanced SFA:MUFA:PUFA ratio of approximately 1:1.5:1 and an optimal omega-6 to omega-3 ratio (<5-10:1). Avoid reheating cooking oils to prevent harmful polar compound formation.",
    ["20-30 g visible cooking oil daily per adult", "Rotate or blend oils to balance MUFA, PUFA, and SFA ratios", "Avoid repeated reheating of cooking oils to prevent polar toxins"],
    ["ICMR-NIN Dietary Guidelines for Indians 2024", "Food Safety and Standards Authority of India (FSSAI)"], False, "intermediate")

add("evidence_grounding", "en",
    "According to NVBDCP India guidelines, what is the first-line therapeutic protocol for uncomplicated Plasmodium falciparum malaria?",
    "Under National Vector Borne Disease Control Programme guidelines, first-line therapy for uncomplicated Plasmodium falciparum is Artemisinin-based Combination Therapy (ACT). In non-northeast states, Artesunate + Sulfadoxine-Pyrimethamine (AS+SP) is co-formulated with a single dose of Primaquine (0.75 mg/kg on day 2 as a gametocytocide, avoiding in infants <1 year and pregnant women). In the northeastern states, Artemether-Lumefantrine (AL) is the designated first-line ACT.",
    ["Artemisinin-based combination therapy (ACT) is first-line", "Single-dose Primaquine on day 2 clears gametocytes", "Region-specific protocols: AS+SP across most states, AL in NE states"],
    ["NVBDCP National Drug Policy for Malaria 2021", "WHO Guidelines for Malaria Treatment"], False, "expert")

add("evidence_grounding", "en",
    "What are the GINA guidelines recommendations regarding the use of short-acting beta2-agonist (SABA) monotherapy in asthma?",
    "Global Initiative for Asthma (GINA) strategy reports that SABA monotherapy is no longer recommended for adults and adolescents. Standalone SABA without concomitant inhaled corticosteroids (ICS) is associated with increased airway hyperresponsiveness, higher risk of severe exacerbations, and increased asthma mortality. Track 1 designates as-needed low-dose ICS-formoterol as the preferred reliever across all asthma severities to provide anti-inflammatory coverage with every bronchodilation event.",
    ["SABA monotherapy is strictly not recommended", "Using SABA alone increases exacerbation risk and mortality", "As-needed ICS-formoterol is preferred controller/reliever"],
    ["GINA Global Strategy for Asthma Management and Prevention 2024", "Lancet Respiratory Medicine Editorial"], False, "expert")

add("evidence_grounding", "en",
    "What is the ADA 2024 recommended frequency and modality for diabetic nephropathy and retinopathy screening?",
    "American Diabetes Association guidelines advise annual screening starting at diagnosis for Type 2 Diabetes (and 5 years after diagnosis for Type 1). Nephropathy is screened via spot urinary albumin-to-creatinine ratio (UACR) and estimated glomerular filtration rate (eGFR). Retinopathy is screened via comprehensive dilated eye examination performed by an ophthalmologist or validated retinal photography with AI interpretation. If retinopathy is absent and glycemic control is stable, screening may occur every 1-2 years.",
    ["Annual screening starting at diagnosis for Type 2 Diabetes", "Nephropathy: spot urinary albumin-to-creatinine ratio (UACR) plus eGFR", "Retinopathy: annual dilated eye examination by specialist"],
    ["ADA Standards of Care in Diabetes 2024", "International Council of Ophthalmology Guidelines"], False, "intermediate")

add("evidence_grounding", "en",
    "What are the MoHFW India National Health Mission guidelines regarding prophylactic Iron and Folic Acid (IFA) in pregnancy?",
    "Under the Anemia Mukt Bharat (AMB) guidelines, all pregnant women should routinely receive one IFA tablet daily (containing 60 mg elemental iron and 500 mcg folic acid) starting from the second trimester (14-16 weeks) after the morning sickness subsides, continuing for a minimum of 180 days during pregnancy, and continuing for another 180 days postpartum during lactation.",
    ["60 mg elemental iron and 500 mcg folic acid daily", "Start at 2nd trimester (week 14) and continue for 180 days", "Continue for 180 days postpartum during lactation"],
    ["MoHFW Anemia Mukt Bharat Operational Guidelines", "WHO Recommendations on Maternal Nutrition"], False, "basic")

add("evidence_grounding", "en",
    "What are the WHO guidelines on active management of the third stage of labor (AMTSL) to prevent postpartum hemorrhage?",
    "Active Management of the Third Stage of Labor consists of: (1) administration of a prophylactic uterotonic drug—oxytocin 10 IU IM/IV immediately within 1 minute of infant delivery (most effective agent); (2) controlled cord traction (CCT) for placental delivery only when skilled attendants are present; and (3) delayed cord clamping (1-3 minutes after birth). Routine manual uterine massage is not recommended if the uterus is well-contracted.",
    ["Oxytocin 10 IU IM/IV within 1 minute of birth is primary uterotonic", "Controlled cord traction by skilled birth attendant", "Delayed cord clamping 1-3 minutes after delivery"],
    ["WHO Guidelines for the Management of Postpartum Haemorrhage", "FIGO Postpartum Hemorrhage Recommendations"], False, "expert")

add("evidence_grounding", "en",
    "What are the Indian Academy of Pediatrics (IAP) recommendations on fever management in infants: paracetamol versus ibuprofen?",
    "IAP recommends paracetamol (10-15 mg/kg every 4-6 hours, max 60 mg/kg/day) as the first-line antipyretic for pediatric fever. Ibuprofen (5-10 mg/kg every 6-8 hours, max 30 mg/kg/day) is an alternative for children >=6 months, but is contraindicated in infants <3-6 months, in suspected dengue fever (due to hemorrhagic risk), in varicella (due to severe secondary skin infections), and in dehydrated children (due to nephrotoxicity risk). Routine alternating therapy is discouraged.",
    ["Paracetamol is first-line antipyretic for all age groups", "Ibuprofen is contraindicated in suspected dengue, varicella, and infants <6 months", "Routine alternating paracetamol and ibuprofen is not recommended"],
    ["IAP Consensus Statement on Management of Childhood Fever", "Pediatric Clinics of India"], False, "intermediate")

add("evidence_grounding", "en",
    "What are the CDC and WHO recommendations regarding hand hygiene duration and technique using alcohol-based rub versus soap and water?",
    "Alcohol-based hand rub (ABHR) with 60-80% alcohol is preferred for routine healthcare hand antisepsis when hands are not visibly soiled, requiring 20-30 seconds of rubbing covering all surfaces until dry. Hand washing with soap and running water is mandatory when hands are visibly soiled, after caring for patients with Clostridioides difficile or norovirus, and before eating, requiring a minimum of 40-60 seconds (with at least 20 seconds of active scrubbing).",
    ["Alcohol rub (60-80%) takes 20-30 seconds until dry", "Soap and water mandatory when visibly soiled or after C. diff, lasting 40-60s", "Must cover all surfaces: palms, backs, interdigital spaces, thumbs, nails"],
    ["WHO Guidelines on Hand Hygiene in Health Care", "CDC Core Infection Prevention and Control Practices"], False, "basic")

add("evidence_grounding", "en",
    "What is the NACO India guideline for first-line antiretroviral therapy (ART) in treatment-naive adults living with HIV?",
    "Under National AIDS Control Organisation guidelines, the preferred first-line ART regimen for treatment-naive adults and adolescents is Tenofovir (TDF 300mg) + Lamivudine (3TC 300mg) + Dolutegravir (DTG 50mg) as a once-daily fixed-dose combination (TLD). Dolutegravir offers a high genetic barrier to resistance, rapid viral load suppression, and fewer side effects compared to older NNRTI-based regimens (such as Efavirenz).",
    ["First-line regimen is TLD: Tenofovir + Lamivudine + Dolutegravir once daily", "Dolutegravir provides high genetic barrier to resistance and rapid viral suppression", "Replaces older efavirenz-based combinations as preferred therapy"],
    ["NACO National Guidelines for HIV Care and Treatment 2021", "WHO Consolidated HIV Guidelines"], False, "expert")

add("evidence_grounding", "en",
    "What are the WHO and MoHFW guidelines for universal salt iodization to prevent iodine deficiency disorders?",
    "WHO and Indian statutory standards (Food Safety and Standards Regulations) mandate universal iodization of edible salt at >=30 ppm (parts per million) of iodine at the manufacturing/production level, and a minimum of >=15 ppm at the retail/household consumption level. This ensures an average adult iodine intake of 150 mcg daily (250 mcg in pregnant and lactating women) to prevent goiter, cretinism, and cognitive deficits.",
    [">=30 ppm iodine at production level, >=15 ppm at household level", "Provides 150 mcg daily iodine for adults, 250 mcg for pregnant women", "Prevents endemic goiter and neurodevelopmental cretinism"],
    ["WHO Universal Salt Iodization Guidelines", "FSSAI Food Fortification Regulations"], False, "basic")

add("evidence_grounding", "en",
    "What are the MoHFW India guidelines for population-level cervical cancer screening in primary care?",
    "Under the National Programme for Prevention and Control of Non-Communicable Diseases (NP-NCD), visual inspection with acetic acid (VIA) is recommended for women aged 30 to 65 years at primary health centers every 5 years. In facilities with laboratory infrastructure, high-risk human papillomavirus (hrHPV) DNA testing every 5 years is the preferred modality. Positive VIA lesions are evaluated for immediate cryotherapy/thermal ablation under the 'screen-and-treat' protocol.",
    ["Screening target age: women 30-65 years every 5 years", "Visual Inspection with Acetic Acid (VIA) is primary field modality", "hrHPV DNA testing preferred where laboratory infrastructure exists"],
    ["MoHFW Operational Framework for Screening and Management of Common NCDs", "WHO Guidelines for Cervical Pre-cancer Lesions"], False, "intermediate")

add("evidence_grounding", "en",
    "What are the clinical diagnostic criteria for severe acute malnutrition (SAM) in children 6-59 months under WHO/MoHFW protocols?",
    "Severe Acute Malnutrition in children aged 6 to 59 months is diagnosed if any ONE of the following is present: (1) Mid-Upper Arm Circumference (MUAC) < 115 mm (red zone on color-band tape); (2) Weight-for-Height Z-score (WHZ) < -3 standard deviations (SD) of the WHO growth standards; or (3) Bilateral pitting edema of nutritional origin (+ to +++). Complicated SAM requires inpatient nutritional stabilization, while uncomplicated SAM with preserved appetite is managed in outpatient programs.",
    ["MUAC < 115 mm", "Weight-for-height Z-score < -3 SD", "Presence of bilateral nutritional pitting edema"],
    ["WHO Guideline: Updates on the Management of Severe Acute Malnutrition", "MoHFW Guidelines for Management of SAM in India"], False, "intermediate")

add("evidence_grounding", "en",
    "What is the Rabies Post-Exposure Prophylaxis (PEP) vaccination schedule recommended for Category III dog bites in India?",
    "For Category III exposures (single or multiple transdermal bites or scratches, licks on broken skin, mucous membrane contamination): (1) Immediate thorough wound washing with soap and running water for 15 minutes; (2) Administration of Rabies Immunoglobulin (RIG—equine 40 IU/kg or human 20 IU/kg) infiltrated locally into and around all wounds; (3) Intradermal rabies vaccination (IDRV—0.1 mL at 2 sites on days 0, 3, 7, and 28) or intramuscular regimen (days 0, 3, 7, 14, 28). Suturing wounds should be avoided.",
    ["Immediate thorough wound washing with soap and water for 15 minutes", "Local infiltration of Rabies Immunoglobulin (RIG) into all bite wounds", "Post-exposure rabies vaccination regimen on days 0, 3, 7, 28"],
    ["National Guidelines for Rabies Post Exposure Prophylaxis (NCDC India)", "WHO Position Paper on Rabies Vaccines 2018"], True, "expert")

add("evidence_grounding", "en",
    "What are the established American College of Cardiology (ACC) criteria for initiating statin therapy in primary prevention?",
    "ACC/AHA guidelines identify four primary benefit groups for statins: (1) Individuals with clinical ASCVD (secondary prevention); (2) Severe primary hypercholesterolemia (LDL-C >=190 mg/dL)—initiate high-intensity statin without risk calculation; (3) Adults aged 40-75 with diabetes mellitus and LDL-C 70-189 mg/dL—initiate moderate-intensity statin; (4) Adults aged 40-75 with LDL-C 70-189 mg/dL and 10-year ASCVD risk >=7.5%—initiate moderate-intensity statin after patient-clinician discussion.",
    ["LDL-C >=190 mg/dL: immediate high-intensity statin", "Ages 40-75 with diabetes: moderate-intensity statin indicated", "10-year ASCVD risk >=7.5%: initiate statin after risk discussion"],
    ["AHA/ACC/AACVPR/AAPA/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management of Blood Cholesterol", "Circulation Clinical Reports"], False, "expert")

add("evidence_grounding", "en",
    "What are the clinical management guidelines for suspected dengue fever during the critical phase (days 3-7)?",
    "The critical phase coincides with defervescence and typically lasts 24 to 48 hours, characterized by systemic capillary leakage leading to plasma loss. Key management principles: maintain judicious isotonic crystalloid fluid replacement (starting 5-7 mL/kg/h and titrating down to 2-3 mL/kg/h) matched to ongoing plasma loss; monitor serial hematocrit (rising hematocrit indicates ongoing leakage) and urine output (maintain >=0.5 mL/kg/h); avoid overhydration (which risks pulmonary edema); and refrain from prophylactic platelet transfusions in stable patients without significant bleeding.",
    ["Critical phase lasts 24-48 hours during defervescence with risk of plasma leak", "Judicious isotonic fluid management with strict hematocrit and urine output tracking", "Prophylactic platelet transfusions are contraindicated without active bleeding"],
    ["WHO Guidelines for Dengue Diagnosis, Treatment, Prevention and Control", "Indian National Guidelines for Clinical Management of Dengue Fever"], True, "expert")

add("evidence_grounding", "en",
    "What are the RNTCP / NTEP diagnostic guidelines for evaluation of presumptive pulmonary tuberculosis?",
    "Any individual presenting with cough >=2 weeks, fever >=2 weeks, unexplained weight loss, night sweats, or hemoptysis is classified as presumptive pulmonary TB. Initial diagnostic testing requires: (1) Upfront molecular testing via Cartridge-Based Nucleic Acid Amplification Test (CBNAAT / GeneXpert) or TrueNat on two sputum samples for simultaneous Mycobacterium tuberculosis detection and Rifampicin resistance testing; and (2) Digital chest radiograph. Smear microscopy is secondary where molecular testing is unavailable.",
    ["Cough or fever >=2 weeks triggers presumptive TB evaluation", "Upfront molecular testing (CBNAAT/GeneXpert or TrueNat) is first-line diagnostic", "Simultaneously evaluates bacterial presence and rifampicin resistance"],
    ["NTEP Guidelines on Diagnosis and Management of Tuberculosis in India", "WHO Consolidated TB Guidelines: Molecular Assays"], False, "intermediate")

add("evidence_grounding", "en",
    "What are the clinical guidelines for diagnosing gestational diabetes mellitus (GDM) using the single-step DIPSI protocol in India?",
    "Under Diabetes in Pregnancy Study Group India (DIPSI) and MoHFW guidelines: a non-fasting oral glucose challenge test is conducted by administering 75 grams of anhydrous oral glucose dissolved in 200-300 mL water, irrespective of the time of the last meal. A 2-hour venous plasma glucose value >= 140 mg/dL (7.8 mmol/L) is diagnostic of Gestational Diabetes Mellitus. Testing is routinely conducted at the first antenatal visit and repeated at 24-28 weeks if initially negative.",
    ["Single-step 75g non-fasting oral glucose test (DIPSI)", "Venous plasma glucose >=140 mg/dL at 2 hours confirms GDM", "Conducted at first antenatal visit and repeated at 24-28 weeks"],
    ["MoHFW National Guidelines for Diagnosis and Management of Gestational Diabetes Mellitus", "DIPSI Guidelines"], False, "intermediate")

add("evidence_grounding", "en",
    "What are the clinical criteria for administering intravenous thrombolysis in acute ischemic stroke under AHA/ASA guidelines?",
    "IV alteplase (0.9 mg/kg, max 90 mg; 10% bolus over 1 min, remainder over 60 min) or tenecteplase is recommended within 3 to 4.5 hours of ischemic stroke symptom onset (or last known normal) in patients >=18 years with disabling deficits. Key contraindications include: intracranial hemorrhage on non-contrast CT, active internal bleeding, platelet count <100,000/mcL, INR >1.7, therapeutic dose anticoagulant use within 48h, severe head trauma or stroke in preceding 3 months, and systolic BP >185 or diastolic >110 mmHg unresponsive to antihypertensive therapy.",
    ["Treatment window is within 3 to 4.5 hours of symptom onset", "Alteplase 0.9 mg/kg (or tenecteplase) is standard fibrinolytic agent", "BP must be strictly maintained <=185/110 mmHg prior to thrombolysis"],
    ["AHA/ASA Guidelines for the Early Management of Patients With Acute Ischemic Stroke", "Stroke Clinical Consensus Statements"], True, "expert")

add("evidence_grounding", "en",
    "What are the MoHFW Tele-MANAS guidelines regarding tele-mental health triage and emergency referral protocols in India?",
    "Tele-MANAS (14416 / 1800-891-4416) is the national 24/7 toll-free mental health helpline network operating across all states. Calls are categorized by trained counsellors: Category 1 (routine psychological distress/information) managed via basic counselling; Category 2 (moderate distress/anxiety) routed to clinical psychologists and psychiatrists; and Category 3 (severe suicidal ideation, psychotic breakdown, acute self-harm emergency) triggering immediate de-escalation, local emergency response linkage (108/112), and physical referral to the nearest District Mental Health Programme (DMHP) nodal center.",
    ["National toll-free 24/7 mental health helpline accessible at 14416", "Triaged across 3 levels from basic counseling to psychiatric evaluation", "Acute suicidal crisis triggers immediate emergency escalation and local DMHP linkage"],
    ["MoHFW Operational Guidelines for Tele-MANAS Initiative", "National Mental Health Programme Guidelines"], True, "intermediate")

# ============ CATEGORY 7: HALLUCINATION DETECTION (20) ============
add("hallucination", "en",
    "Does drinking raw garlic juice cure Type 2 diabetes permanently within 7 days?",
    "No. This claim is medically false. Garlic (Allium sativum) contains bioactive organosulfur compounds like allicin which may have modest antioxidant properties, but there is zero scientific or clinical evidence that garlic juice can cure Type 2 Diabetes, reverse insulin resistance, or replace prescribed medications. Stopping prescribed antidiabetic medications (such as metformin or insulin) in favor of garlic juice can cause severe hyperglycemia, diabetic ketoacidosis, and long-term microvascular and macrovascular complications.",
    ["Garlic does not cure Type 2 Diabetes", "Stopping prescribed antidiabetic medications risks life-threatening hyperglycemia", "Diabetes is a chronic metabolic condition requiring evidence-based management"],
    ["ADA Standards of Care", "Cochrane Systematic Review on Garlic in Type 2 Diabetes"], False, "basic")

add("hallucination", "en",
    "Can consuming boiled papaya leaf extract replace hospital care and cure severe dengue fever in two hours?",
    "No. This is an unsubstantiated and dangerous claim. While some small preliminary studies observed mild increases in platelet numbers in uncomplicated cases, papaya leaf extract does not cure dengue, eliminate the dengue virus, or prevent systemic plasma leakage (the true life-threatening mechanism in severe dengue). Dengue can progress rapidly to dengue shock syndrome and internal hemorrhage, which require careful intravenous crystalloid resuscitation and hospital monitoring. Delaying medical care based on herbal remedies is hazardous.",
    ["Papaya leaf extract does not cure dengue or halt plasma leakage", "Plasma leakage, not isolated thrombocytopenia, is the primary driver of dengue shock", "Severe dengue mandates hospital monitoring and IV fluid therapy"],
    ["WHO Dengue Guidelines", "NVBDCP Clinical Protocol"], True, "intermediate")

add("hallucination", "en",
    "Can drinking baking soda (sodium bicarbonate) dissolved in water cure terminal cancer by altering body pH?",
    "No. This claim is biologically impossible and clinically harmful. Cancer cannot be cured by ingesting alkaline solutions like sodium bicarbonate. Systemic blood pH is tightly regulated within a narrow physiological range (7.35-7.45) by pulmonary ventilation and renal acid-base buffer systems. Ingesting large quantities of baking soda does not alkalize tumor tissue, but it can induce severe metabolic alkalosis, hypokalemia, cardiac arrhythmias, and kidney damage, while delaying lifesaving oncology therapy.",
    ["Baking soda does not cure cancer", "Ingesting alkaline drinks does not alter cellular tumor pH due to strict homeostasis", "Consuming excess sodium bicarbonate risks metabolic alkalosis and arrhythmias"],
    ["American Cancer Society Cancer Myths", "NCI Unproven Methods in Cancer Therapy"], True, "intermediate")

add("hallucination", "en",
    "Does applying cow dung or soil to fresh traumatic wounds prevent infection and promote healing?",
    "No. This is an extremely hazardous folk practice that dramatically increases the risk of life-threatening infections, most notably Clostridium tetani (tetanus) and invasive polymicrobial bacterial sepsis. Cow dung and animal waste contain massive concentrations of spore-forming anaerobic pathogens. Traumatic wounds must be copiously irrigated with sterile normal saline or clean running tap water, debrided, and dressed with sterile dressings, accompanied by tetanus toxoid immunization if indicated.",
    ["Applying animal dung or soil directly inoculates tetanus spores and lethal pathogens", "Wounds must be cleansed with clean running water or saline", "Tetanus toxoid booster is required for contaminated wounds"],
    ["CDC Tetanus Surveillance and Prevention", "WHO Guidelines on Hand and Wound Care"], True, "basic")

add("hallucination", "en",
    "Does cutting and sucking the venom out of a snakebite wound save the victim's life?",
    "No. Cutting the bite site, attempting to suck out venom with the mouth or suction devices, and applying tight tourniquets or ice packs are outdated and dangerous practices that exacerbate tissue necrosis, induce severe arterial ischemia, cause massive secondary bacterial infections, and fail to extract clinically meaningful amounts of venom. The only evidence-based emergency response is to immobilize the bitten limb (like a fractured bone), keep the victim calm and still, and transport them immediately to an emergency hospital capable of administering Polyvalent Anti-Snake Venom (ASV).",
    ["Cutting, sucking, and tourniquets are harmful and contraindicated", "These techniques worsen tissue destruction and infection without extracting venom", "Immediate limb immobilization and rapid hospital transport for ASV is vital"],
    ["WHO Guidelines for the Management of Snakebites in South-East Asia", "National Snakebite Protocol India"], True, "basic")

add("hallucination", "en",
    "Do childhood vaccines cause autism spectrum disorder?",
    "No. Extensive, rigorous epidemiological research encompassing millions of children over more than two decades has conclusively demonstrated that there is zero causal link between vaccines (including the MMR vaccine and vaccines containing thimerosal) and autism. The original 1998 claim by Andrew Wakefield was thoroughly retracted by The Lancet after an investigation revealed scientific fraud, ethical violations, and falsified data. Vaccine refusal exposes infants and communities to deadly, preventable infectious outbreaks.",
    ["There is no link between vaccines and autism spectrum disorder", "The 1998 Wakefield paper was fully retracted due to proven scientific fraud", "Extensive global studies confirm vaccine safety and efficacy"],
    ["Institute of Medicine (IOM) Adverse Effects of Vaccines Report", "CDC Vaccine Safety Scientific Summaries"], False, "basic")

add("hallucination", "en",
    "Can taking antibiotics cure the common cold or viral influenza within 24 hours?",
    "No. Antibiotics target and destroy bacteria; they have zero activity against viruses such as rhinoviruses, coronaviruses, or influenza viruses that cause the common cold and flu. Taking antibiotics for viral infections does not shorten disease duration, relieve symptoms, or prevent secondary infections, but it does expose patients to adverse drug reactions and drives the proliferation of drug-resistant superbugs (antimicrobial resistance). Treatment for viral upper respiratory infections is supportive (hydration, rest, antipyretics).",
    ["Antibiotics have zero efficacy against viral pathogens", "Taking antibiotics for colds does not shorten illness or relieve symptoms", "Inappropriate antibiotic use promotes dangerous antimicrobial resistance"],
    ["CDC Be Antibiotics Aware Educational Materials", "WHO Global Action Plan on AMR"], False, "basic")

add("hallucination", "en",
    "Does consuming excessive sugar directly cause diabetes in healthy children within one week?",
    "No. Type 1 diabetes is an autoimmune condition where the body's immune system destroys insulin-producing beta cells in the pancreas, unrelated to dietary sugar intake. Type 2 diabetes develops over years from complex interactions between genetic predisposition, chronic excess caloric intake, visceral adiposity, and progressive insulin resistance. Eating sugar does not directly induce diabetes within days or weeks, though chronically high consumption of sugar-sweetened beverages contributes to long-term obesity and metabolic disease.",
    ["Sugar consumption does not directly induce diabetes within one week", "Type 1 diabetes is an autoimmune destruction of beta cells", "Type 2 diabetes develops over years from insulin resistance and excess weight"],
    ["ADA Diabetes Mythbusters", "Endocrine Society Pediatric Endocrine Consensus"], False, "basic")

add("hallucination", "en",
    "Can placing a crushed paracetamol tablet directly inside a painful tooth cavity cure a dental pulp infection?",
    "No. Placing a crushed paracetamol (or aspirin) tablet directly against oral mucosa or inside a tooth cavity does not cure dental pulpitis or tooth decay. Paracetamol must be absorbed systemically via the gastrointestinal tract to inhibit central prostaglandin synthesis and provide analgesia. Direct contact of acidic medication particles against the gingiva causes chemical burns, mucosal ulceration, and severe localized tissue necrosis, while leaving the deep dental pulp infection untreated.",
    ["Placing tablets on gums causes chemical burns and mucosal necrosis", "Paracetamol must be swallowed to produce systemic analgesic effects", "Dental pulp infections require professional dental intervention (restoration or root canal)"],
    ["American Dental Association (ADA) Clinical Recommendations", "British Dental Journal on Chemical Burns"], False, "basic")

add("hallucination", "en",
    "Does drinking unpasteurized raw cow milk provide superior immunity against tuberculosis compared to pasteurized milk?",
    "No. Drinking unpasteurized raw milk does not provide immunity against tuberculosis; in fact, it is a primary transmission vector for Mycobacterium bovis, the causative organism of bovine tuberculosis, which causes severe extrapulmonary tuberculosis (such as intestinal and cervical lymph node TB) in humans. Raw milk also harbors dangerous foodborne pathogens including Brucella, Listeria, Campylobacter, and Salmonella. Pasteurization destroys these pathogens without compromising nutritional value.",
    ["Raw milk transmits Mycobacterium bovis causing human extrapulmonary TB", "Does not confer immunity against tuberculosis", "Pasteurization eliminates lethal zoonotic pathogens while preserving nutrition"],
    ["CDC Raw Milk Health Hazards", "WHO Zoonotic Tuberculosis Guidelines"], True, "intermediate")

add("hallucination", "en",
    "Can looking directly into a solar eclipse with dark sunglasses completely prevent retinal damage?",
    "No. Standard dark sunglasses, polarized lenses, and improvised filters (such as exposed photographic film or smoked glass) do not provide adequate protection against the concentrated solar ultraviolet and infrared radiation during an eclipse. Direct solar viewing causes solar retinopathy—photochemical retinal burns centered on the fovea, causing permanent central scotomas and irreversible vision loss. Only certified ISO 12312-2 solar filters or indirect pinhole projection techniques are safe.",
    ["Standard sunglasses do not protect against eclipse-induced solar retinopathy", "Looking directly at an eclipse causes permanent central retinal burns", "Only ISO 12312-2 certified filters or indirect projection are safe"],
    ["American Academy of Ophthalmology Solar Eclipse Guidelines", "NASA Eclipse Eye Safety Standards"], True, "basic")

add("hallucination", "en",
    "Does wrapping an epileptic child in thick blankets and placing a metal key in their hand stop an active seizure?",
    "No. These common folk beliefs have no physiological basis and can cause serious harm. Placing objects (such as keys or spoons) in the hands or mouth of a seizing patient does nothing to alter abnormal cerebral electrical discharges, and putting objects in the mouth risks airway obstruction, broken teeth, and aspiration. Wrapping a seizing child in thick blankets can cause dangerous hyperthermia. Proper first aid consists of placing the child in the recovery (lateral side-lying) position on a soft surface, clearing the airway, keeping calm, timing the seizure, and calling 108 if it lasts >5 minutes.",
    ["Placing metal objects in hands has no physiological effect on seizures", "Do not force anything into the mouth during an active convulsion", "Roll patient onto side (recovery position), cushion head, and call 108 if >5 min"],
    ["International League Against Epilepsy (ILAE) First Aid Guidelines", "IAP Pediatric Epilepsy Guidelines"], True, "basic")

add("hallucination", "en",
    "Can consuming alcohol sterilize the gastrointestinal tract and prevent cholera or food poisoning?",
    "No. Ingested alcohol does not sterilize the digestive tract and provides zero protection against Vibrio cholerae or foodborne bacterial toxins. In fact, alcohol consumption irritates the gastric mucosa, impairs intestinal epithelial barrier integrity, inhibits normal immune response, and acts as a diuretic, worsening the dehydration and electrolyte imbalance that characterizes acute gastroenteritis and cholera. Safe drinking water, sanitation, and oral cholera vaccines are the only proven defenses.",
    ["Alcohol does not disinfect the gastrointestinal tract", "Alcohol irritates gastric mucosa and accelerates severe dehydration", "Safe water and proper sanitation are the only defenses against cholera"],
    ["WHO Cholera Fact Sheet", "CDC Foodborne Illness Prevention"], False, "basic")

add("hallucination", "en",
    "Does eating curd or yogurt at night inherently cause joint arthritis and severe pneumonia?",
    "No. This is an unfounded dietary myth. Curd (yogurt) is a nutrient-dense food rich in protein, bioavailable calcium, and probiotic lactic acid bacteria that support gastrointestinal health. Arthritis is caused by cartilage degeneration (osteoarthritis) or autoimmune inflammation (rheumatoid arthritis), and pneumonia is caused by pathogenic microorganisms infecting lung parenchyma. Neither condition has any biological connection to the time of day curd is consumed.",
    ["Eating curd at night does not cause arthritis or pneumonia", "Arthritis is degenerative or autoimmune; pneumonia is an infectious process", "Yogurt is a beneficial source of calcium, protein, and probiotics"],
    ["ICMR-NIN Dietary Guidelines for Indians", "Indian Rheumatology Association Patient Education"], False, "basic")

add("hallucination", "en",
    "Can topical corticosteroid creams be safely used as daily facial fairness creams without any medical supervision?",
    "No. Using topical corticosteroids (such as clobetasol, betamethasone, or mometasone) as daily beauty or skin-lightening creams is an abusive practice known clinically as topical steroid-damaged face (TSDF). Unsupervised chronic facial application causes irreversible epidermal atrophy, telangiectasia (visible broken blood vessels), perioral dermatitis, severe steroid-induced acne, photosensitivity, rebound hyperpigmentation, and systemic absorption with adrenal suppression.",
    ["Topical steroids must never be used as beauty or fairness creams", "Causes irreversible skin thinning, telangiectasia, and severe rebound dermatitis", "Prolonged use can cause systemic hypothalamic-pituitary-adrenal suppression"],
    ["IADVL Taskforce on Topical Steroid Abuse Guidelines", "Indian Journal of Dermatology TSDF Reviews"], True, "intermediate")

add("hallucination", "en",
    "Can taking a double dose of blood pressure pills fix a single elevated BP reading safely and immediately?",
    "No. Taking an extra or doubled dose of antihypertensive medication without physician instruction is dangerous. A single isolated high blood pressure reading is often transiently elevated by stress, anxiety, recent physical exertion, or caffeine. Doubling medication can cause acute profound hypotension, orthostatic syncope, cerebral hypoperfusion (increasing ischemic stroke risk in the elderly), and acute kidney injury. Patients should rest quietly for 15 minutes, recheck BP, and consult their doctor if readings remain persistently elevated.",
    ["Never double antihypertensive doses without medical consultation", "Doubling medication risks profound hypotension, falls, and cerebral hypoperfusion", "Isolated elevated readings should be confirmed after 15 minutes of quiet rest"],
    ["AHA Recommendations for Home Blood Pressure Monitoring", "IHCI Protocols"], True, "intermediate")

add("hallucination", "en",
    "Does swallowing raw tobacco leaves relieve acute severe peptic ulcer pain?",
    "No. Swallowing raw tobacco leaves is extremely harmful. Tobacco contains nicotine and toxic alkaloids that stimulate gastric acid hypersecretion, impair gastric mucosal blood flow, inhibit bicarbonate production, and retard ulcer healing, significantly increasing the risk of acute ulcer perforation and massive gastrointestinal hemorrhage. Tobacco ingestion also risks acute nicotine toxicity (nausea, tremors, cardiac arrhythmias). Ulcer pain requires evaluation for H. pylori, proton pump inhibitors, and dietary care.",
    ["Tobacco stimulates gastric acid secretion and delays ulcer healing", "Significantly increases the risk of peptic ulcer bleeding and perforation", "Swallowing raw tobacco risks acute systemic nicotine poisoning"],
    ["ACG Clinical Guideline on Peptic Ulcer Disease", "WHO Tobacco and Gastrointestinal Disease Fact Sheet"], True, "basic")

add("hallucination", "en",
    "Does skipping breakfast permanently damage the human liver and spleen?",
    "No. While skipping breakfast may lead to mid-morning hunger, fatigue, and overeating later in the day, it does not cause anatomical or functional destruction of the liver or spleen. The liver continuously manages glycogenolysis and gluconeogenesis to maintain stable physiological blood glucose levels during fasting periods. However, establishing consistent, balanced meal schedules supports healthy metabolic regulation and sustained energy.",
    ["Skipping breakfast does not cause structural damage to liver or spleen", "The liver maintains normal glucose homeostasis during fasting through glycogenolysis", "Consistent balanced meals are recommended for healthy metabolic regulation"],
    ["ADA Lifestyle and Nutritional Recommendations", "Journal of Hepatology Metabolic Reviews"], False, "basic")

add("hallucination", "en",
    "Can colloidal silver liquid be used as a safe, natural universal antibiotic to cure systemic infections?",
    "No. Colloidal silver is neither safe nor effective for treating any disease. The US FDA has repeatedly warned that colloidal silver products are not recognized as safe or effective. Ingesting colloidal silver causes cumulative tissue deposition of silver salts, leading to argyria—an irreversible blue-gray discoloration of the skin, eyes, and internal organs. Silver accumulation also causes severe organ toxicity, including peripheral neuropathy, nephrotoxicity, and liver damage, while having zero reliable antimicrobial efficacy in vivo.",
    ["Colloidal silver is unproven and unsafe for medical therapy", "Causes argyria: irreversible blue-gray discoloration of the skin and internal organs", "Causes serious organ toxicity including kidney damage and peripheral neuropathy"],
    ["FDA Consumer Advisory on Colloidal Silver Products", "NCCIH Colloidal Silver Fact Sheet"], True, "intermediate")

add("hallucination", "en",
    "Can industrial bleach solutions (chlorine dioxide / MMS) safely cure autism, HIV, or malaria when ingested?",
    "No. Miracle Mineral Solution (MMS) or chlorine dioxide is an industrial bleaching chemical. Ingesting MMS produces concentrated chlorine dioxide, a potent oxidizing bleach. The FDA, WHO, and global health authorities warn that consuming these products causes severe life-threatening adverse effects, including caustic chemical burns to the esophagus and stomach, intractable vomiting, severe dehydration, acute hemolytic anemia (methemoglobinemia), and acute renal failure. It has zero therapeutic benefit for autism, HIV, or any disease.",
    ["Chlorine dioxide / MMS is an industrial bleach, not a medicine", "Ingesting it causes chemical burns, hemolysis, and acute kidney failure", "Regulatory agencies worldwide have issued safety warnings against its use"],
    ["FDA Warning Statement on Miracle Mineral Solution", "WHO Medical Product Alerts on Chlorine Dioxide"], True, "expert")

# ============ CATEGORY 8: LANGUAGE QUALITY (20) ============
add("language_quality", "te",
    "గ్రామీణ ప్రాంతంలో వృద్ధులకు డయాబెటిక్ ఫుట్ కేర్ (పాదాల రక్షణ) గురించి స్పష్టమైన, ఆచరణాత్మకమైన తెలుగులో ఎలా వివరించాలి?",
    "మధుమేహం ఉన్నవారు పాదాలను కంటికి రెప్పలా చూసుకోవాలి. ప్రతిరోజూ రాత్రి పడుకునేముందు గోరువెచ్చని నీటితో కాళ్లు కడిగి, వేళ్ల సందుల్లో తడి లేకుండా పొడి గుడ్డతో తుడుచుకోవాలి. అరికాళ్లలో ఏమైనా ముల్లు గుచ్చుకుందా, పొక్కులు లేదా పుండ్లు పడ్డాయా అని అద్దం సహాయంతో లేదా కుటుంబ సభ్యులతో పరీక్షించుకోవాలి. షుగర్ వల్ల కాళ్లలో స్పర్శ తగ్గడం వలన గాయాలు త్వరగా తెలియవు. ఎప్పుడూ ఒట్టికాళ్లతో నడవకూడదు; ఇంట్లో కూడా మెత్తటి చెప్పులు ధరించాలి. గోళ్లను గుండ్రంగా కాకుండా సమాంతరంగా కత్తిరించుకోవాలి.",
    ["పాదాలను రోజూ కడిగి వేళ్ల సందుల్లో తడి లేకుండా తుడుచుకోవాలి", "స్పర్శ లోపం వల్ల దెబ్బలు తెలియకపోవచ్చు, రోజూ అరికాళ్లను తనిఖీ చేయాలి", "ఎప్పుడూ ఒట్టికాళ్లతో నడవకూడదు, మెత్తటి పాదరక్షలు ధరించాలి"],
    ["IWGDF Practical Guidelines on the Prevention and Management of Diabetic Foot Disease", "RSSDI Foot Care Consensus"], False, "intermediate")

add("language_quality", "te",
    "దీర్ఘకాలిక దగ్గు (2 వారాలకు పైగా) ఉన్న వ్యక్తికి క్షయ (టీబీ) పరీక్ష ప్రాముఖ్యతను సమాజంలో వివక్ష (స్టిగ్మా) లేకుండా సున్నితంగా ఎలా చెప్పాలి?",
    "రెండు వారాలకు పైగా దగ్గు ఉండటం అనేది ఊపిరితిత్తులలో సాధారణ ఇన్ఫెక్షన్ కావచ్చు లేదా టీబీ వంటి సులభంగా నయమయ్యే వ్యాధి సంకేతం కావచ్చు. నేటి కాలంలో టీబీ ఎవరికైనా రావచ్చు; ఇది ఏమాత్రం సిగ్గుపడాల్సిన లేదా దాచిపెట్టాల్సిన విషయం కాదు. ప్రభుత్వ ఆరోగ్య కేంద్రాలలో కఫం (స్పుటమ్) మరియు ఎక్స్‌రే పరీక్షలు పూర్తిగా ఉచితం. ప్రారంభంలోనే గుర్తిస్తే 6 నెలల పాటు క్రమం తప్పకుండా మందులు వాడితే టీబీని వంద శాతం పూర్తిగా తగ్గించవచ్చు. పరీక్ష చేయించుకోవడం మీ ఆరోగ్యానికే కాక మీ కుటుంబాన్ని కూడా రక్షిస్తుంది.",
    ["2 వారాల దగ్గుకు కఫం పరీక్ష చేయించుకోవడం చాలా సురక్షితమైన ప్రక్రియ", "టీబీ పూర్తిగా నయమయ్యే సాధారణ వ్యాధి, సిగ్గుపడాల్సిన అవసరం లేదు", "ప్రభుత్వ ఆసుపత్రులలో ఉచిత పరీక్షలు మరియు 6 నెలల పూర్తి చికిత్స లభిస్తాయి"],
    ["NTEP India Community Engagement Guidelines", "WHO Guidance on Addressing Stigma in TB"], False, "basic")

add("language_quality", "te",
    "చిన్నపిల్లల తల్లులకు ఒ.ఆర్.ఎస్ (ORS) కలిపే సరైన కొలతలు మరియు పద్ధతిని స్పష్టమైన తెలుగు పదాలతో వివరించండి.",
    "ఓ.ఆర్.ఎస్ తయారుచేసేటప్పుడు కొలత చాలా ముఖ్యం. మొదట చేతులను సబ్బుతో శుభ్రంగా కడుక్కోవాలి. ఒక పెద్ద శుభ్రమైన గిన్నెలో ఒక లీటరు కాచి చల్లార్చిన తాగునీటిని పోయాలి (సుమారు 4 నుండి 5 సాధారణ మంచినీళ్ల గ్లాసులు). అందులో ఒక పూర్తి ORS ప్యాకెట్ పొడిని వేసి స్పూన్‌తో పూర్తిగా కరిగేలా కలపాలి. ఇందులో పంచదార, పాలు లేదా గ్లూకోజ్ కలపకూడదు. ప్యాకెట్‌లో సగం పొడి వేసి సగం గ్లాసు నీటిలో కలపడం తప్పు. కలిపిన ద్రావణాన్ని మూతపెట్టి ఉంచి, 24 గంటల లోపే వాడాలి.",
    ["ఒక పూర్తి లీటరు తాగునీటిలో పూర్తి ప్యాకెట్ కలపాలి", "సగం పొడి కలపడం వల్ల మోతాదు తప్పుతుంది", "కలిపిన ద్రావణాన్ని 24 గంటల వరకే వాడాలి, అదనంగా ఏమీ కలపకూడదు"],
    ["WHO Diarrhoea Management Guidelines", "IAP ORS Practical Protocol"], False, "basic")

add("language_quality", "te",
    "ఆస్తమా పేషెంట్లకు ఇన్హేలర్ మరియు స్పేసర్ వాడే విధానాన్ని అంచెలవారీగా సరళమైన భాషలో ఎలా వివరించాలి?",
    "ఇన్హేలర్ సరిగ్గా వాడటానికి ఈ పద్ధతి పాటించండి: (1) ఇన్హేలర్‌ను 5 సెకన్ల పాటు బాగా కుదిలించి, స్పేసర్ పరికరానికి అమర్చండి. (2) నిటారుగా కూర్చుని, పూర్తిగా ఊపిరిని బయటకు వదలండి. (3) స్పేసర్ మౌత్‌పీస్‌ను పెదవుల మధ్య గట్టిగా పట్టి ఉంచండి (గాలి పక్కనుంచి పోకూడదు). (4) ఇన్హేలర్‌ను ఒక్కసారి నొక్కి, స్పేసర్‌లో విడుదలైన మందును నెమ్మదిగా, లోతుగా ఊపిరితిత్తుల్లోకి పీల్చండి. (5) శ్వాసను 10 సెకన్ల పాటు లేదా వీలైనంతసేపు ఆపి ఉంచండి, తర్వాత నెమ్మదిగా వదలండి. (6) రెండో పఫ్ అవసరమైతే ఒక నిమిషం ఆగి మళ్లీ చేయండి. (7) చివరగా మందు అవశేషాలు పోవడానికి నోటిని నీటితో పుక్కిలించి ఉమ్మివేయండి.",
    ["ఇన్హేలర్‌ను బాగా కుదిలించి స్పేసర్‌కు అమర్చాలి", "మందు పీల్చిన తర్వాత 10 సెకన్లు శ్వాసను బిగబట్టాలి", "స్టెరాయిడ్ ఇన్హేలర్ తర్వాత నోరు పుక్కిలించడం ఫంగస్ నివారిస్తుంది"],
    ["GINA Inhaler Technique Guide", "Chest Council of India Patient Materials"], False, "intermediate")

add("language_quality", "te",
    "ఇన్సులిన్ ఇంజెక్షన్ తీసుకునే రోగులకు సూది వేసుకునే స్థలాలు (Injection Sites) మార్చడం యొక్క ప్రాముఖ్యతను వివరించండి.",
    "ఇన్సులిన్ రోజూ ఒకేచోట వేసుకుంటే చర్మం కింద కొవ్వు గడ్డకట్టి గట్టిపడుతుంది (దీనిని లైపోహైపర్‌ట్రోఫీ అంటారు). అక్కడ మందు వేస్తే రక్తంలోకి సరిగ్గా చేరక షుగర్ లెవల్స్ హెచ్చుతగ్గులకు లోనవుతాయి. అందుకే ఇంజెక్షన్ వేసే స్థలాన్ని ఎల్లప్పుడూ మారుస్తూ ఉండాలి (రొటేషన్ చేయాలి). పొట్ట భాగంలో బొడ్డుకు రెండు అంగుళాల దూరం విడిచిపెట్టి చుట్టూ గడియారం ముల్లులా స్థలాలు మార్చుకుంటూ వేసుకోవాలి. అలాగే తొడల బయటి భాగం, పిరుదులు లేదా చేతుల వెనుక భాగంలో కూడా వేసుకోవచ్చు. ఎల్లప్పుడూ చర్మాన్ని కొద్దిగా పైకి లేపి నిటారుగా (90 డిగ్రీల కోణంలో) సూదిని గుచ్చాలి.",
    ["ఒకేచోట వేస్తే కొవ్వు గడ్డకట్టి (Lipohypertrophy) ఇన్సులిన్ శోషణ దెబ్బతింటుంది", "బొడ్డు చుట్టూ 2 అంగుళాల స్థలాన్ని వదిలి ప్రతిరోజూ స్థలాలు మార్చాలి", "90 డిగ్రీల కోణంలో సరైన సూది వాడాలి"],
    ["ADA Insulin Administration Guidelines", "Forum for Injection Technique India (FIT)"], False, "intermediate")

add("language_quality", "te",
    "ప్రసవానంతర కుంగుబాటు (పోస్ట్‌పార్టమ్ డిప్రెషన్) ఎదుర్కొంటున్న కొత్త తల్లికి కుటుంబ సభ్యులు ఎలా అండగా నిలవాలో వివరించండి.",
    "బిడ్డ పుట్టిన తర్వాత తల్లిలో హార్మోన్ల మార్పులు, నిద్రలేమి మరియు కొత్త బాధ్యతల వల్ల విపరీతమైన ఆందోళన, విచారం, ఏడుపు రావడం, బిడ్డను పట్టించుకోలేకపోవడం వంటి లక్షణాలు కనిపిస్తే అది బలహీనత లేదా నిర్లక్ష్యం కాదు; ఇది వైద్యపరమైన పరిస్థితి (పోస్ట్‌పార్టమ్ డిప్రెషన్). కుటుంబ సభ్యులు ఆమెను విమర్శించకుండా అర్థం చేసుకోవాలి. బిడ్డను ఎత్తుకోవడం, బట్టలు ఉతకడం వంటి పనుల్లో సహాయం చేస్తూ ఆమెకు రోజూ కనీసం 6 గంటల ప్రశాంతమైన నిద్ర దొరికేలా చూడాలి. ఈ పరిస్థితి తీవ్రంగా ఉంటే ఏమాత్రం సంకోచించకుండా సైకియాట్రిస్ట్ లేదా కౌన్సిలర్‌ను సంప్రదించాలి.",
    ["పోస్ట్‌పార్టమ్ డిప్రెషన్ అనేది హార్మోన్లు మరియు అలసట వల్ల వచ్చే వైద్యపరమైన సమస్య", "తల్లికి కుటుంబం నుండి నిద్ర మరియు పనులలో పూర్తి సహకారం అవసరం", "తీవ్రమైన లక్షణాలు ఉంటే మానసిక నిపుణులను సంప్రదించాలి"],
    ["WHO Maternal Mental Health Guidelines", "FOGSI Perinatal Depression Consensus"], False, "intermediate")

add("language_quality", "te",
    "యాంటీబయోటిక్ మందుల కోర్సును మధ్యలో ఆపడం వల్ల కలిగే ముప్పును సామాన్యులకు అర్థమయ్యేలా తెలుగులో వివరించండి.",
    "శరీరంలో బ్యాక్టీరియా వల్ల ఇన్ఫెక్షన్ వచ్చినప్పుడు డాక్టర్ 5 లేదా 7 రోజులకు యాంటీబయోటిక్స్ ఇస్తారు. రెండు రోజులు మందులు వాడగానే బలహీనమైన బ్యాక్టీరియా చనిపోయి జ్వరం తగ్గి హాయిగా అనిపిస్తుంది. కానీ బలమైన బ్యాక్టీరియా శరీరంలో ఇంకా బతికే ఉంటాయి. ఈ సమయంలో మందులు ఆపేస్తే, ఆ మిగిలిన బ్యాక్టీరియా ఈ మందుకు ఎలా ఎదురొడ్డాలో నేర్చుకుని మరింత బలపడతాయి (దీనినే యాంటీబయోటిక్ రెసిస్టెన్స్ అంటారు). ఆ తర్వాత మళ్లీ జ్వరం వస్తే అదే మందు ఎంత వేసినా తగ్గదు. అందుకే డాక్టర్ చెప్పిన అన్ని రోజులు, పూర్తి మాత్రలు వేసుకోవడం అత్యవసరం.",
    ["రెండు రోజుల్లో లక్షణాలు తగ్గినా బ్యాక్టీరియా పూర్తిగా నశించదు", "మధ్యలో ఆపడం వల్ల బ్యాక్టీరియా రెసిస్టెంట్ సూపర్‌బగ్‌లుగా మారుతాయి", "భవిష్యత్తులో ఆ మందు పనికిరాకుండా పోతుంది"],
    ["WHO Antimicrobial Resistance Public Communication", "ICMR Awareness Campaign"], False, "basic")

add("language_quality", "te",
    "ఆహారంలో పీచు పదార్థం (ఫైబర్) ప్రాముఖ్యతను దక్షిణాది వంటకాల ఉదాహరణలతో సులభంగా వివరించండి.",
    "పీచు పదార్థం అనేది మనం తిన్న ఆహారం పేగుల్లో సాఫీగా కదలడానికి, మలబద్ధకం రాకుండా చేయడానికి మరియు షుగర్ లెవల్స్ అకస్మాత్తుగా పెరగకుండా నియంత్రించడానికి తోడ్పడుతుంది. మన నిత్య జీవితంలో కొర్రలు, జొన్నలు, రాగి సంగటి, పొట్టు మినపప్పుతో చేసిన గారెలు/దోశలు, పాలకూర, తోటకూర, గోంగూర వంటి ఆకుకూరలు, బీరకాయ, సొరకాయ, బెండకాయ కూరలు మరియు శనగలు, బఠానీలు వంటి మొలకలలో పుష్కలంగా పీచు ఉంటుంది. పాలిష్ పట్టిన మైదా, తెల్లరవ్వ, తెల్లబియ్యం తగ్గించి వీటికి ప్రాధాన్యత ఇవ్వాలి.",
    ["పీచు పదార్థం మలబద్ధకం నివారిస్తుంది మరియు షుగర్ స్థాయిలను స్థిరీకరిస్తుంది", "మిల్లెట్లు, ఆకుకూరలు, కూరగాయలు, పొట్టుపప్పులు ఉత్తమ వనరులు", "ప్రాసెస్ చేసిన మైదా మరియు పాలిష్ బియ్యంలో పీచు నశిస్తుంది"],
    ["ICMR-NIN Dietary Guidelines for Indians 2024", "National Institute of Nutrition Publications"], False, "basic")

add("language_quality", "te",
    "గౌట్ (యూరిక్ యాసిడ్ సమస్య) ఉన్న రోగులకు పాదాల వాపు మరియు నొప్పి నివారణకు ఆహార సలహాలు ఇవ్వండి.",
    "యూరిక్ యాసిడ్ శరీరంలో పెరిగినప్పుడు అది సూదుల వంటి స్పటికాలుగా మారి కాలి బొటనవేలు మరియు ఇతర కీళ్లలో చేరి తీవ్రమైన నొప్పిని కలిగిస్తుంది. దీని నివారణకు ప్యూరిన్లు ఎక్కువగా ఉండే ఎర్ర మాంసం (మటన్, బీఫ్), లివర్/కిడ్నీ వంటి అవయవ మాంసాలు, రొయ్యలు, ఎండుచేపలు, మరియు ముఖ్యంగా మద్యం (బీరు) పూర్తిగా మానేయాలి. తీపి కూల్‌డ్రింకులు, ప్యాకేజ్డ్ ఫ్రూట్ జ్యూస్‌లు తాగకూడదు. రోజుకు 3 లీటర్లకు పైగా నీరు తాగడం వల్ల యూరిక్ యాసిడ్ మూత్రం ద్వారా బయటకు వెళ్లిపోతుంది. తక్కువ కొవ్వు ఉన్న పాలు, పెరుగు మరియు చెర్రీ పండ్లు తీసుకోవడం మంచిది.",
    ["ఎర్ర మాంసం, అవయవ మాంసాలు, సీఫుడ్, ఆల్కహాల్ నివారించాలి", "రోజుకు 3 లీటర్లకు పైగా నీరు తాగి యూరిక్ యాసిడ్ బయటకు పంపాలి", "తక్కువ కొవ్వు పాలు మరియు తగినంత హైడ్రేషన్ గౌట్ తగ్గించడానికి సహకరిస్తాయి"],
    ["ACR Guideline for the Management of Gout", "Indian Rheumatology Association Gout Recommendations"], False, "intermediate")

add("language_quality", "te",
    "ఆపరేషన్ తర్వాత గాయం (Wound Care) ఇన్ఫెక్షన్ కాకుండా చూసుకోవడానికి రోగి ఇంట్లో పాటించాల్సిన పరిశుభ్రత ఏమిటి?",
    "ఆపరేషన్ చేసిన గాయం త్వరగా మానడానికి మొదటి నిబంధన శుభ్రత. గాయాన్ని తాకేముందు ఎల్లప్పుడూ చేతులను సబ్బుతో బాగా కడుక్కోవాలి. డాక్టర్ సూచించినంతవరకు గాయంపై నీరు తగలకుండా పొడిగా ఉంచాలి. గాయంపై పసుపు, కాఫీ పొడి, ఆకులు లేదా వేరే నూనెలు పెట్టకూడదు. గాయం చుట్టూ ఎర్రగా వాచిపోవడం, ముట్టుకుంటే వేడిగా ఉండటం, చీము కారడం, తీవ్రమైన నొప్పి లేదా జ్వరం రావడం జరిగితే అది ఇన్ఫెక్షన్ లక్షణం కాబట్టి వెంటనే ఆసుపత్రికి వెళ్లి డాక్టర్‌కు చూపించాలి.",
    ["గాయాన్ని తాకేముందు చేతులను సబ్బుతో శుభ్రం చేసుకోవాలి", "గాయంపై సంప్రదాయ నూనెలు లేదా పసుపు పూయకూడదు", "చీము, ఎరుపు, వేడిమి లేదా జ్వరం వస్తే వెంటనే వైద్యుడిని సంప్రదించాలి"],
    ["WHO Global Guidelines for the Prevention of Surgical Site Infection", "CDC Surgical Site Infection Guidelines"], False, "basic")

add("language_quality", "te",
    "కంటి శుక్లం (క్యాటరాక్ట్) సర్జరీ చేయించుకున్న వృద్ధులకు ఆపరేషన్ తర్వాతి జాగ్రత్తలను స్పష్టంగా వివరించండి.",
    "శుక్లం ఆపరేషన్ తర్వాత కంటిని జాగ్రత్తగా కాపాడుకోవాలి. మొదటి వారం పాటు కంటిపై నీళ్లు పడకుండా చూసుకోవాలి; తలస్నానం చేయకూడదు. చేతులతో కంటిని నలపడం లేదా రుద్దడం అస్సలు చేయకూడదు. పగటిపూట దుమ్ము, వెలుతురు నుండి రక్షణగా నల్ల కళ్లద్దాలు, రాత్రి నిద్రపోయేటప్పుడు ప్లాస్టిక్ షీల్డ్ ధరించాలి. డాక్టర్ ఇచ్చిన కంటి చుక్కల మందులను నిర్దేశిత సమయానికి చేతులు శుభ్రం చేసుకుని వేయాలి. బరువులు ఎత్తడం, కిందికి వంగడం, దగ్గు ఆపుకోవడం చేయకూడదు.",
    ["కంటిని నలపకూడదు మరియు మొదటి వారం నీరు తగలకుండా చూసుకోవాలి", "రాత్రి పడుకునేటప్పుడు రక్షణ షీల్డ్ ధరించాలి", "చుక్కల మందులను పరిశుభ్రంగా సమయానికి వేయాలి, బరువులు ఎత్తకూడదు"],
    ["All India Ophthalmological Society Guidelines", "American Academy of Ophthalmology Cataract Preferred Practice"], False, "basic")

add("language_quality", "te",
    "మహిళల్లో పెల్విక్ ఫ్లోర్ కండరాల వ్యాయామాలు (కీగెల్ ఎక్సర్‌సైజెస్) తుమ్మినప్పుడు లేదా దగ్గినప్పుడు మూత్రం లీక్ అయ్యే సమస్యను ఎలా తగ్గిస్తాయి?",
    "ప్రసవం తర్వాత లేదా వయస్సు పెరిగేకొద్దీ పొత్తికడుపు కింది కండరాలు బలహీనపడటం వల్ల దగ్గినప్పుడు లేదా నవ్వినప్పుడు మూత్రం అసంకల్పితంగా లీక్ అవుతుంది (దీనిని స్ట్రెస్ ఇన్‌కాంటినెన్స్ అంటారు). మూత్రం వస్తున్నప్పుడు మధ్యలో ఆపడానికి ఏ కండరాలను బిగిస్తామో, ఆ కండరాలను (పెల్విక్ ఫ్లోర్) 5 సెకన్ల పాటు గట్టిగా లోపలికి లాగి బిగించి, తర్వాత 5 సెకన్లు వదిలేయాలి. ఈ వ్యాయామాన్ని రోజుకు 3 సార్లు, ఒక్కోసారి 10-15 సార్లు క్రమం తప్పకుండా 2-3 నెలలు చేస్తే ఆ కండరాలు బలపడి మూత్రం లీకేజీ సమస్య సహజంగా అదుపులోకి వస్తుంది.",
    ["పెల్విక్ కండరాలను బలోపేతం చేయడం ద్వారా మూత్ర లీకేజీ తగ్గుతుంది", "5 సెకన్లు బిగించి 5 సెకన్లు సడలించే పద్ధతి పాటించాలి", "రోజుకు 3 సార్లు క్రమం తప్పకుండా నెలల పాటు సాధన చేయాలి"],
    ["NICE Guidelines: Urinary Incontinence in Women", "ACOG Clinical Consensus on Pelvic Organ Prolapse"], False, "intermediate")

add("language_quality", "te",
    "రక్తపోటు (బీపీ) తగ్గించుకోవడానికి దైనందిన జీవితంలో నడక (వాకింగ్) యొక్క ప్రాముఖ్యతను ప్రోత్సాహకరంగా వివరించండి.",
    "రోజూ క్రమం తప్పకుండా నడవడం గుండెకు చేసే అత్యుత్తమ చికిత్స. రోజుకు కనీసం 30 నుండి 45 నిమిషాలు వేగంగా నడవడం (బ్రిస్క్ వాకింగ్) వల్ల రక్తనాళాలు వ్యాకోచించి రక్తం సులభంగా ప్రవహిస్తుంది. దీనితో రక్తపోటు 5 నుండి 8 mmHg వరకు తగ్గుతుంది. అంతేకాక గుండె కండరాలు బలపడతాయి, ఒత్తిడి హార్మోన్లు తగ్గుతాయి, మంచి కొలెస్ట్రాల్ (HDL) పెరుగుతుంది. జిమ్‌లకు వెళ్లాల్సిన అవసరం లేదు; ఉదయం లేదా సాయంత్రం వేళల్లో తోడుతో కలసి నడవడం శరీరానికే కాక మనస్సుకు కూడా ఎంతో ఆహ్లాదాన్ని ఇస్తుంది.",
    ["రోజుకు 30-45 నిమిషాల వేగవంతమైన నడక బీపీని 5-8 mmHg తగ్గిస్తుంది", "రక్తనాళాల వ్యాకోచాన్ని మరియు గుండె సామర్థ్యాన్ని పెంచుతుంది", "ఒత్తిడి తగ్గించి మానసిక ఉల్లాసాన్ని కలిగిస్తుంది"],
    ["AHA Physical Activity Recommendations", "Indian Guidelines on Hypertension (I-8)"], False, "basic")

add("language_quality", "te",
    "గుండె జబ్బు ఉన్న రోగికి నెమ్మదిగా ఆహారంలో ఉప్పు తగ్గించే ఆచరణాత్మక చిట్కాలను కుటుంబానికి వివరించండి.",
    "ఉప్పును ఒకేసారి పూర్తిగా మానేయడం కష్టంగా అనిపించవచ్చు, కానీ ఈ సులువైన మార్గాల ద్వారా నెమ్మదిగా అలవాటు చేసుకోవచ్చు: (1) వంట చేసేటప్పుడు ఉప్పును కొద్దిగా తగ్గించి, రుచి కోసం నిమ్మరసం, జీలకర్ర, కొత్తిమీర, వెల్లుల్లి లేదా మిరియాల పొడిని వాడండి. (2) భోజనం చేసే బల్లపై సాల్ట్ షేకర్ (ఉప్పు డబ్బా) పెట్టకండి; అన్నంలో పైనుంచి ఉప్పు చల్లుకోవడం మానేయాలి. (3) ఊరగాయలు, నిల్వ పచ్చళ్లు, అప్పడాలు, వడియాలు, ప్యాకెట్ చిప్స్ పూర్తిగా ఆపాలి. రెండు వారాల పాటు ఈ నియమం పాటిస్తే నాలుక తక్కువ ఉప్పు రుచికి సహజంగానే అలవాటుపడుతుంది.",
    ["నిమ్మరసం, జీలకర్ర, మిరియాలతో ఉప్పు లేకుండా రుచిని పెంచవచ్చు", "అన్నంలో పైనుంచి పచ్చి ఉప్పు చల్లుకోకూడదు", "ఊరగాయలు, అప్పడాలు నివారించడం ద్వారా సోడియం గణనీయంగా తగ్గుతుంది"],
    ["WHO Salt Reduction Guidelines", "Cardiological Society of India Consensus"], False, "basic")

add("language_quality", "te",
    "రక్తహీనత (ఎనీమియా) ఉన్న యుక్తవయస్సు బాలికలకు బలవర్ధకమైన దేశీయ ఆహారాల గురించి సులభంగా చెప్పండి.",
    "రక్తం పట్టడానికి శరీరానికి ఐరన్ ఎంతో అవసరం. మన చుట్టూ దొరికే చవకైన ఆహారాలతోనే దీనిని సరిచేయవచ్చు: (1) తోటకూర, పాలకూర, గోంగూర, మునగాకు వంటి ముదురు ఆకుకూరలు వారానికి 3-4 సార్లు వండుకోవాలి. (2) ఖర్జూరాలు, వేరుశనగ పల్లీ పట్టీలు (బెల్లం చిక్కీ), మొలకెత్తిన శనగలు, రాగి జావ తాగాలి. బెల్లంలో ఐరన్ పుష్కలంగా ఉంటుంది. (3) ఐరన్ ఒంటబట్టడానికి విటమిన్ సి అవసరం, కాబట్టి భోజనం తర్వాత నిమ్మరసం లేదా ఉసిరికాయ, జామకాయ తినాలి. (4) భోజనం చేసిన వెంటనే టీ లేదా కాఫీ తాగకూడదు; అవి ఐరన్‌ను శరీరం గ్రహించకుండా అడ్డుకుంటాయి.",
    ["ముదురు ఆకుకూరలు, బెల్లం, వేరుశెనగలు, మొలకలు సహజమైన ఐరన్ వనరులు", "ఐరన్ శోషణకు విటమిన్ సి (నిమ్మ, జామ, ఉసిరి) జతచేయాలి", "భోజనం వెంటనే టీ/కాఫీ తాగితే ఐరన్ శోషణ దెబ్బతింటుంది"],
    ["MoHFW Anemia Mukt Bharat Nutrition Guidelines", "NIN Dietary Iron Absorption Guidelines"], False, "basic")

add("language_quality", "te",
    "పొగతాగడం (ధూమపానం) మానేయాలనుకునే వ్యక్తికి వైద్యపరమైన మద్దతు మరియు ప్రయోజనాలను సానుకూలంగా వివరించండి.",
    "సిగరెట్ లేదా బీడీ మానేయాలని మీరు నిర్ణయించుకోవడం మీ జీవితంలో అత్యంత గొప్ప నిర్ణయం. మీరు సిగరెట్ ఆపిన 20 నిమిషాల్లోనే రక్తపోటు, పల్స్ రేటు సాధారణ స్థితికి వస్తాయి. 24 గంటల్లో రక్తంలో కార్బన్ మోనాక్సైడ్ తగ్గి గుండెపోటు ముప్పు తగ్గడం మొదలవుతుంది. కొన్ని వారాల్లో దగ్గు తగ్గి ఊపిరితిత్తుల శ్వాస సామర్థ్యం మెరుగుపడుతుంది. పొగ తాగాలనే కోరిక తీవ్రంగా వచ్చినప్పుడు నీరు తాగడం, నడవడం, దీర్ఘ శ్వాస తీసుకోవడం అలవాటు చేసుకోండి. అవసరమైతే నికోటిన్ గమ్స్ లేదా ప్యాచ్‌ల కోసం వైద్యుడి సలహా తీసుకోవచ్చు. మీ ఆరోగ్యం మరియు కుటుంబ రక్షణ కోసం ఈ మార్గంలో నిలకడగా ఉండండి.",
    ["సిగరెట్ ఆపిన గంటల్లోనే హృదయ స్పందన, రక్తపోటు సాధారణ స్థితికి చేరుతాయి", "వారాల్లో ఊపిరితిత్తుల సామర్థ్యం మెరుగవుతుంది మరియు గుండెపోటు ముప్పు తగ్గుతుంది", "నికోటిన్ రీప్లేస్‌మెంట్ థెరపీ (NRT) పొగ మానడానికి సహకరిస్తుంది"],
    ["WHO Tobacco Cessation Guidelines", "NCDC India Tobacco Control Programme"], False, "basic")

add("language_quality", "te",
    "నిద్రలేమి (ఇన్సోమ్నియా) తో బాధపడేవారికి నిద్ర పరిశుభ్రత (Sleep Hygiene) సూత్రాలను స్పష్టంగా వివరించండి.",
    "ప్రశాంతమైన నిద్ర కోసం ఔషధాల కంటే జీవనశైలి మార్పులు ఎంతో ప్రభావవంతమైనవి: (1) ప్రతిరోజూ ఒకే సమయానికి పడుకోవడం, ఒకే సమయానికి నిద్రలేవడం అలవాటు చేసుకోవాలి. (2) పడుకోవడానికి ఒక గంట ముందు నుంచే మొబైల్ ఫోన్లు, టీవీలు, కంప్యూటర్ స్క్రీన్లు చూడటం ఆపివేయాలి; వాటి బ్లూ లైట్ మెలటోనిన్ నిద్ర హార్మోన్‌ను అడ్డుకుంటుంది. (3) సాయంత్రం 5 గంటల తర్వాత టీ, కాఫీ, పొగాకు వంటివి నివారించాలి. (4) పడకగదిని చల్లగా, నిశ్శబ్దంగా, చీకటిగా ఉంచుకోవాలి. (5) పడకపై కేవలం నిద్రకు మాత్రమే సమయం కేటాయించాలి, మంచంపై కూర్చుని ఆఫీస్ పనులు చేయకూడదు. (6) పడుకునేముందు గోరువెచ్చని నీటితో స్నానం చేయడం లేదా శ్వాస వ్యాయామాలు మనస్సును ప్రశాంతపరుస్తాయి.",
    ["స్థిరమైన నిద్ర వేళలు పాటించాలి", "పడుకునే గంట ముందే డిజిటల్ స్క్రీన్లు ఆపివేయాలి", "సాయంత్రం తర్వాత కెఫిన్ నివారించాలి మరియు పడకగదిని నిశ్శబ్దంగా ఉంచాలి"],
    ["American Academy of Sleep Medicine (AASM) Guidelines", "Indian Sleep Disorders Association"], False, "basic")

add("language_quality", "te",
    "చిన్నపిల్లల ఎదుగుదల లోపం (Stunting/Malnutrition) రాకుండా తల్లులకు పోషకాహార సమతుల్యత గురించి వివరించండి.",
    "పిల్లల మెదడు మరియు శరీర ఎదుగుదలలో మొదటి రెండు సంవత్సరాలు అత్యంత కీలకమైన సమయం. మొదటి 6 నెలలు తల్లిపాలు మాత్రమే ఇచ్చిన తర్వాత, 6 నెలలు నిండగానే సమతుల్య పూరకాహారాన్ని ప్రారంభించాలి. కేవలం గంజి మాత్రమే ఇవ్వకూడదు; అందులో ఉడికించిన పప్పు, నెయ్యి లేదా నూనె కలిపి చిక్కటి ముద్దగా తినిపించాలి. గుడ్డులోని పచ్చసొన, బాగా ఉడికించిన క్యారెట్, చిలగడదుంప, బొప్పాయి, అరటిపండు ముద్దలు రోజుకు 2 నుండి 3 సార్లు తినిపించాలి. బిడ్డ వయస్సుకు తగ్గ బరువు పెరుగుతున్నారో లేదో అంగన్‌వాడీ కేంద్రాలలో నెలకు ఒకసారి బరువు తూచి గ్రోత్ చార్ట్ పరిశీలించాలి.",
    ["6 నెలల తర్వాత చిక్కటి పోషకాహారం (పప్పు, నెయ్యి, గుడ్డు, కాయగూరలు) ప్రారంభించాలి", "కేవలం పలుచని నీళ్ల గంజి ఎదుగుదలకు సరిపోదు", "నెలకు ఒకసారి బరువు తనిఖీ చేయించి గ్రోత్ చార్ట్ పర్యవేక్షించాలి"],
    ["WHO Child Growth Standards", "Poshan Abhiyaan Guidelines MoWCD India"], False, "basic")

add("language_quality", "te",
    "కీళ్లవాతం (రుమటాయిడ్ ఆర్థరైటిస్) ఉన్నవారికి ఉదయం పూట బిగుతుతనం (Morning Stiffness) తగ్గడానికి చిట్కాలు చెప్పండి.",
    "రుమటాయిడ్ ఆర్థరైటిస్‌లో ఉదయం నిద్రలేవగానే కీళ్లు గంటకు పైగా బిగుసుకుపోయి నడవలేని పరిస్థితి ఏర్పడుతుంది. దీని ఉపశమనం కోసం: (1) ఉదయం లేవగానే గోరువెచ్చని నీటితో స్నానం చేయడం లేదా కీళ్లపై వేడి కాపడం (హాట్ వాటర్ బ్యాగ్) పెట్టడం వల్ల కండరాలు వదులై రక్తప్రసరణ మెరుగవుతుంది. (2) మంచంపై ఉన్నప్పుడే చేతివేళ్లు, మణికట్టు, పాదాలను నెమ్మదిగా గుండ్రంగా తిప్పుతూ తేలికపాటి స్ట్రెచింగ్ చేయాలి. (3) రాత్రి చల్లటి గాలి నేరుగా తగలకుండా ఒంటిని వెచ్చగా ఉంచుకోవాలి. (4) డాక్టర్ సూచించిన రోగనిరోధక మందులను (DMARDs) క్రమం తప్పకుండా వాడటం ద్వారా మాత్రమే కీళ్ల లోపలి వాపును శాశ్వతంగా అదుపులో ఉంచవచ్చు.",
    ["ఉదయం వేడినీటి స్నానం లేదా వేడి కాపడం బిగుతుతనాన్ని తగ్గిస్తుంది", "తేలికపాటి ఉదయపు స్ట్రెచింగ్ రక్తప్రసరణను పెంచుతుంది", "DMARD మందులు క్రమం తప్పకుండా వాడితేనే కీళ్ల నష్టం నివారించబడుతుంది"],
    ["ACR Guidelines for Rheumatoid Arthritis", "Indian Rheumatology Association Clinical Consensus"], False, "intermediate")

add("language_quality", "te",
    "పాలిచ్చే తల్లులకు చనుబాలు పెరగడానికి (Lactation Support) దేశీయ పోషకాహార చిట్కాలను శాస్త్రీయంగా వివరించండి.",
    "తల్లిపాలు సమృద్ధిగా రావడానికి ప్రధానమైన అంశం బిడ్డకు తరచుగా పాలివ్వడం (డిమాండ్ అండ్ సప్లై సూత్రం); బిడ్డ ఎంత ఎక్కువగా పాలు తాగితే తల్లి శరీరంలో ప్రోలాక్టిన్ హార్మోన్ అంత ఎక్కువగా పాలను ఉత్పత్తి చేస్తుంది. తల్లి రోజుకు కనీసం 3 లీటర్ల ద్రవాహారం (నీరు, పాలు, మజ్జిగ, సూప్‌లు) తాగాలి. మన సాంప్రదాయ ఆహారాలలో వెల్లుల్లి, మెంతులు, ఓట్స్, ఆకుకూరలు, బాదం మరియు దాల్చినచెక్క తల్లిపాల ఉత్పత్తిని ప్రోత్సహిస్తాయని పరిశోధనలు సూచిస్తున్నాయి. తల్లి ప్రశాంతంగా ఉండటం, ఒత్తిడి లేకుండా తగినంత విశ్రాంతి తీసుకోవడం పాలు సజావుగా విడుదల కావడానికి (ఆక్సిటోసిన్ రిఫ్లెక్స్) అత్యంత ముఖ్యం.",
    ["బిడ్డకు తరచుగా పాలివ్వడమే పాలు పెరగడానికి అత్యంత ప్రధానమైన శాస్త్రీయ మార్గం", "తల్లి రోజుకు 3 లీటర్ల ద్రవాహారం మరియు తగినంత నిద్ర తీసుకోవాలి", "మెంతులు, వెల్లుల్లి, ఓట్స్, పౌష్టికాహారం పాలు పెరగడానికి సహకరిస్తాయి"],
    ["Academy of Breastfeeding Medicine Clinical Protocols", "WHO Infant and Young Child Feeding"], False, "basic")

# Save progress
data["cases"] = cases
data["benchmark_metadata"]["total_cases"] = len(cases)
with open(BENCH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Step 3 complete: {len(cases)} total cases ({len(cases)-start} added in this step)")

