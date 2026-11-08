# Limitations & Ethical Risk Mitigation

**Document Version:** 2.5.0-PROD  
**Principal Engineers:** Principal AI Safety Engineer & Medical Ethics Reviewer  

---

## 1. Technological & Model Limitations

1. **Non-Clinical Validation Notice:**  
   VastCare Vernacular LLM is an assistive research and health literacy platform. It has **NOT** undergone randomized controlled clinical trials (RCTs) or Central Drugs Standard Control Organisation (CDSCO) / FDA medical device certification. It must **never** be deployed as an autonomous medical diagnostic device.

2. **Severe Dialectal Variations:**  
   While the model supports standard Telugu, Rayalaseema, and Telangana regional vernaculars alongside Tanglish code-switching, isolated tribal dialects (e.g. Chenchu, Koya, Lambadi) are not yet represented in the training corpus and may exhibit degraded comprehension.

3. **Complex Polypharmacy Interactions:**  
   Multi-drug pharmacodynamic and pharmacokinetic interactions (e.g., Warfarin + Amiodarone, Methotrexate + NSAIDs) require exhaustive individualized lab panels (INR, LFT, Creatinine) and cannot be conclusively evaluated by conversational models.

4. **Speech-to-Text Acoustic Noise:**  
   In noisy rural primary health center environments (background traffic, rain, crowd ambient noise), simulated voice transcription may experience word error rate (WER) degradation unless high-quality directional microphone hardware is used.

---

## 2. Ethical Risk Boundaries & Refusal Protocols

- **Abortion Inquiries:** Under India's Medical Termination of Pregnancy (MTP) Amendment Act 2021, medical termination of pregnancy requires supervision by registered medical practitioners. The model strictly refuses to provide DIY abortion concoctions or unprescribed dosage schedules.
- **Pre-Natal Sex Determination:** Fully prohibited under the Pre-Conception and Pre-Natal Diagnostic Techniques (PCPNDT) Act 1994. The model categorically refuses inquiries probing fetal sex.
- **Substance Abuse & Prescription Narcotics:** Requests for scheduled opioids, sedatives, or illicit substances are immediately rejected and redirected to de-addiction helplines.

---

## 3. Human-in-the-Loop Safeguards

1. **Mandatory Physician Escalation:**  
   All advisory prompts instruct patients to bring the model's educational printout to their primary care physician (MBBS/MD) for formal clinical confirmation.
2. **Emergency Banners:**  
   Identified emergencies (cardiac arrest, snakebite, organophosphate poisoning, stroke) prioritize dialing **108** over LLM conversation.
3. **Tele-MANAS Integration:**  
   Mental health crises trigger national helpline **14416** immediately.

