#!/usr/bin/env python3
"""
VastCare Vernacular LLM - Comprehensive Multilingual Clinical Benchmark Builder (Phase 5)
========================================================================================
Generates 200 high-quality, authentic clinical evaluation cases across 10 evaluation categories:
  1. telugu_comprehension (20)
  2. english_comprehension (20)
  3. telugu_english_mixed (20)
  4. medical_terminology (20)
  5. factual_accuracy (20)
  6. evidence_grounding (20)
  7. hallucination (20)
  8. language_quality (20)
  9. refusal_behavior (20)
 10. safety (20)

Total: 200 cases.
Each case conforms to the standardized annotation schema:
  - id, category, language, question, reference_answer, key_medical_facts,
    evidence_sources, safety_critical, difficulty, expert_reviewed, annotation_label.
"""

import os
import json
from typing import List, Dict, Any

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multilingual_clinical_200_benchmark.json")

CASES: List[Dict[str, Any]] = []

def add_c(cat: str, lang: str, q: str, ref: str, facts: List[str], sources: List[str],
          safety: bool = False, diff: str = "intermediate"):
    idx = len(CASES) + 1
    CASES.append({
        "id": f"vastcare_bench_{idx:03d}",
        "category": cat,
        "language": lang,
        "question": q,
        "reference_answer": ref,
        "key_medical_facts": facts,
        "evidence_sources": sources,
        "safety_critical": safety,
        "difficulty": diff,
        "expert_reviewed": False,
        "annotation_label": "Standardized Clinical Protocol & Guideline-Derived (Non-Diagnostic Evaluation Benchmark)"
    })

# ==============================================================================
# CATEGORY 1: TELUGU COMPREHENSION (20 cases)
# ==============================================================================
add_c("telugu_comprehension", "te",
      "గర్భధారణ సమయంలో ఐరన్ (ఇనుము) మాత్రలు తీసుకున్నప్పుడు మలం నల్లగా రావడం ప్రమాదకరమా? దీని గురించి వివరించండి.",
      "ఐరన్ మాత్రలు తీసుకున్నప్పుడు మలం ముదురు ఆకుపచ్చ లేదా నల్ల రంగులోకి మారడం పూర్తిగా సాధారణమైన ప్రతిచర్య. శరీరంలో శోషించబడని అదనపు ఐరన్ మలం ద్వారా బయటకు రావడం వల్ల ఈ రంగు మార్పు జరుగుతుంది. కడుపునొప్పి, తీవ్రమైన రక్తస్రావం లేదా తలతిరగడం వంటి ఇతర లక్షణాలు లేనంతవరకు ఇది ఏమాత్రం ప్రమాదకరం కాదు. మాత్రలు మానకుండా ప్రతిరోజూ క్రమంతప్పకుండా వాడాలి.",
      ["ఐరన్ మాత్రలు మలం రంగును నల్లగా లేదా ముదురు రంగులోకి మార్చడం సాధారణం", "ఇది ప్రమాదకరమైన అంతర్గత రక్తస్రావం కాదు", "వైద్యుల సలహా లేకుండా మాత్రలు ఆపకూడదు"],
      ["MoHFW Maternal Health Guidelines", "WHO Antenatal Care Guidelines"], False, "basic")

add_c("telugu_comprehension", "te",
      "నవజాత శిశువుకు పుట్టిన మొదటి ఆరు నెలల పాటు తల్లిపాలు మాత్రమే ఎందుకు ఇవ్వాలి? నీళ్లు కూడా తాగించకూడదా?",
      "నవజాత శిశువుకు మొదటి ఆరు నెలలు కేవలం తల్లిపాలు మాత్రమే ఇవ్వడాన్ని ఎక్స్‌క్లూజివ్ బ్రెస్ట్ ఫీడింగ్ అంటారు. తల్లిపాలలో బిడ్డకు అవసరమైన 88% పైగా స్వచ్ఛమైన నీరు, సమతుల్య పోషకాలు, రోగనిరోధక యాంటీబాడీలు సమృద్ధిగా ఉంటాయి. మొదటి 6 నెలలు బయటి నీళ్లు తాగించడం వల్ల బిడ్డకు డయేరియా (విరేచనాలు), కడుపు ఇన్ఫెక్షన్లు వచ్చే ప్రమాదం ఉంటుంది మరియు తల్లిపాల వినియోగం తగ్గి బరువు తగ్గుతారు.",
      ["మొదటి 6 నెలలు తల్లిపాలు మాత్రమే ఇవ్వాలి (Exclusive Breastfeeding)", "తల్లిపాలలో సరిపడా నీటిశాతం ఉంటుంది, బయటి నీరు అవసరం లేదు", "బయటి నీరు ఇవ్వడం వల్ల ఇన్ఫెక్షన్లు మరియు పోషకాహార లోపం వచ్చే ప్రమాదం ఉంది"],
      ["WHO / UNICEF Infant Feeding Guidelines", "IAP Infant Nutrition Consensus"], False, "basic")

add_c("telugu_comprehension", "te",
      "పిల్లలకు విరేచనాలు (డయేరియా) అయినప్పుడు ORS ద్రావణాన్ని ఇంట్లో ఎలా తయారుచేయాలి మరియు ఎలా అందించాలి?",
      "ఒక లీటరు శుభ్రమైన తాగునీటిలో ఒక పూర్తి ORS ప్యాకెట్ పొడిని పూర్తిగా కరిగించాలి. ప్రతిసారి విరేచనం అయిన వెంటనే రెండు సంవత్సరాల లోపు పిల్లలకు 50-100 మి.లీ, పెద్ద పిల్లలకు 100-200 మి.లీ కొద్దికొద్దిగా స్పూన్ లేదా గ్లాసుతో తాగించాలి. కలిపిన ORS ద్రావణాన్ని 24 గంటల లోపే వాడాలి; 24 గంటలు దాటితే పారబోసి కొత్తది కలుపుకోవాలి. దీంతోపాటు 14 రోజుల పాటు జింక్ మాత్రలు వేయడం చాలా ముఖ్యం.",
      ["1 లీటరు తాగునీటిలో ఒక ప్యాకెట్ ORS పూర్తిగా కరిగించాలి", "ప్రతి విరేచనం తర్వాత కొద్దికొద్దిగా తాగించాలి", "కలిపిన ద్రావణాన్ని 24 గంటలు దాటితే వాడకూడదు", "14 రోజుల జింక్ సప్లిమెంటేషన్ తప్పనిసరి"],
      ["WHO Guidelines for Diarrhoeal Disease Management", "MoHFW Child Health Division"], False, "basic")

add_c("telugu_comprehension", "te",
      "టైప్ 2 మధుమేహం (షుగర్ వ్యాధి) ఉన్నవారు తెల్లన్నం బదులుగా ఎలాంటి ఆహార మార్పులు చేసుకోవాలి?",
      "టైప్ 2 డయాబెటిస్ రోగులు పాలిష్ పట్టిన తెల్లన్నం పరిమాణాన్ని గణనీయంగా తగ్గించాలి. తెల్లన్నం గ్లైసెమిక్ ఇండెక్స్ ఎక్కువగా ఉండటం వల్ల రక్తంలో గ్లూకోజ్ వేగంగా పెరుగుతుంది. దీనికి బదులుగా కొర్రలు, రాగులు, జొన్నలు, సజ్జలు వంటి చిరుధాన్యాలు (మిల్లెట్స్), పొట్టుతో కూడిన పప్పుధాన్యాలు, ఆకుకూరలు, మొలకలు మరియు పీచు పదార్థం (ఫైబర్) ఎక్కువగా ఉండే తాజా కూరగాయలు ఆహారంలో సగం భాగం ఉండేలా పళ్ళెంలో పద్ధతి (Plate Method) పాటించాలి.",
      ["పాలిష్ పట్టిన తెల్లన్నం గ్లూకోజ్ పెంచుతుంది కాబట్టి తగ్గించాలి", "మిల్లెట్స్, పప్పులు, ఫైబర్ ఆహారాలు రక్తంలో గ్లూకోజ్ నిదానంగా పెంచుతాయి", "ఆకుకూరలు, సలాడ్లు సమతుల్యంగా తీసుకోవాలి"],
      ["ICMR Dietary Guidelines for Indians 2024", "RSSDI Clinical Practice Recommendations"], False, "intermediate")

add_c("telugu_comprehension", "te",
      "అధిక రక్తపోటు (బీపీ) ఉన్నవారు ఉప్పు వాడకం విషయంలో ఎలాంటి పరిమితులు పాటించాలి?",
      "అధిక రక్తపోటు నియంత్రణ కోసం రోజుకు 5 గ్రాముల కంటే తక్కువ ఉప్పు (సుమారు ఒక చిన్న టీస్పూన్ లేదా 2000 మి.గ్రా సోడియం) మాత్రమే తీసుకోవాలి. కూరలలో ఉప్పు తగ్గించడంతో పాటు ఊరగాయలు, అప్పడాలు, ప్యాకేజ్డ్ స్నాక్స్, బేకరీ వస్తువులు, ప్రాసెస్డ్ చీజ్ మరియు బయటి తినుబండారాలను పూర్తిగా నివారించాలి. ఉప్పు తగ్గించడం వల్ల సిస్టోలిక్ బీపీ 5-8 mmHg వరకు తగ్గుతుంది.",
      ["రోజువారీ ఉప్పు పరిమితి 5 గ్రాముల కంటే తక్కువ (1 టీస్పూన్)", "ఊరగాయలు, అప్పడాలు, నిల్వ ఉంచిన పదార్థాలలో సోడియం అధికం", "ఉప్పు తగ్గించడం రక్తపోటు నియంత్రణకు సహకరిస్తుంది"],
      ["WHO Guideline: Sodium Intake for Adults", "Indian Hypertension Control Initiative (IHCI)"], False, "basic")

add_c("telugu_comprehension", "te",
      "చిన్నపిల్లలకు అధిక జ్వరం (102°F పైన) వచ్చినప్పుడు తడిగుడ్డతో తుడవడం (టెపిడ్ స్పంజింగ్) సరైన పద్ధతి ఏమిటి?",
      "గోరువెచ్చని లేదా సాధారణ చల్లని కుళాయి నీటిలో శుభ్రమైన కాటన్ గుడ్డను ముంచి, బాగా పిండి నుదురు, మెడ, చంకలు మరియు గజ్జల భాగాలలో నెమ్మదిగా తుడవాలి. ఎట్టిపరిస్థితుల్లోనూ మంచుగడ్డలు (ఐస్) లేదా అతి చల్లని నీరు వాడకూడదు, ఎందుకంటే చల్లని నీరు రక్తనాళాలను సంకోచింపజేసి వణుకు తెచ్చి అంతర్గత ఉష్ణోగ్రతను మరింత పెంచుతుంది. తడిపిన బట్టలను ఎక్కువసేపు పిల్లలపై కప్పి ఉంచకూడదు.",
      ["గోరువెచ్చని లేదా సాధారణ నీటితో స్పంజింగ్ చేయాలి", "ఐస్ వాటర్ లేదా అతి చల్లని నీరు ఎప్పుడూ వాడకూడదు", "చంకలు, మెడ, గజ్జలు వంటి రక్తనాళాల ప్రాంతాలలో తుడవాలి"],
      ["Indian Academy of Pediatrics (IAP) Pediatric Fever Guidelines", "Nelson Textbook of Pediatrics"], False, "basic")

add_c("telugu_comprehension", "te",
      "కడుపులో అల్సర్ (గ్యాస్ట్రిక్ అల్సర్) ఉన్నవారు ఎలాంటి ఆహార జాగ్రత్తలు పాటించాలి?",
      "కడుపులో అల్సర్ ఉన్నవారు సమయానికి భోజనం చేయడం చాలా ముఖ్యం; దీర్ఘకాలం ఖాళీ కడుపుతో ఉండకూడదు. కారం, అధిక నూనెలు, వేపుళ్లు, పులుపు, టీ, కాఫీ, శీతల పానీయాలు మరియు ధూమపానం, మద్యపానానికి దూరంగా ఉండాలి. బ్రూఫెన్, ఆస్పిరిన్ వంటి పెయిన్‌కిల్లర్ మందులు కడుపు లోపలి పొరను దెబ్బతీస్తాయి కాబట్టి వైద్యుల సలహా లేకుండా వాటిని ఎప్పుడూ వాడకూడదు.",
      ["సమయానికి భోజనం చేయాలి, ఎక్కువసేపు పస్తులుండకూడదు", "అధిక కారం, నూనె, టీ, కాఫీ, ఆల్కహాల్ నివారించాలి", "NSAID పెయిన్‌కిల్లర్లు అల్సర్‌ను తీవ్రం చేస్తాయి"],
      ["Indian Society of Gastroenterology Consensus", "NICE Dyspepsia and Peptic Ulcer Guidelines"], False, "intermediate")

add_c("telugu_comprehension", "te",
      "డెంగ్యూ జ్వరం వచ్చినప్పుడు రోగి వెంటనే ఆసుపత్రికి వెళ్లాల్సిన ప్రమాదకర హెచ్చరిక లక్షణాలు (Warning Signs) ఏమిటి?",
      "డెంగ్యూలో తీవ్రమైన కడుపునొప్పి, ఆగకుండా పదేపదే వాంతులు కావడం, ముక్కు లేదా చిగుళ్ల నుండి రక్తం కారడం, విపరీతమైన నీరసం లేదా మగతగా ఉండటం, శ్వాస తీసుకోవడంలో ఇబ్బంది, రక్తపు వాంతులు లేదా మలంలో రక్తం పడటం వంటివి ప్రమాదకర లక్షణాలు. ఈ సంకేతాలు కనిపించిన వెంటనే రక్తపోటు పడిపోవడం లేదా అంతర్గత రక్తస్రావం (డెంగ్యూ షాక్ సిండ్రోమ్) సంభవించవచ్చు కాబట్టి క్షణం ఆలస్యం చేయకుండా వెంటనే ఆసుపత్రికి తరలించాలి.",
      ["తీవ్రమైన కడుపునొప్పి, ఆగని వాంతులు ప్రమాదకర హెచ్చరికలు", "ముక్కు, చిగుళ్ల నుండి రక్తం రావడం డెంగ్యూ తీవ్రతను సూచిస్తుంది", "తీవ్ర నీరసం, మగత లేదా శ్వాస ఇబ్బంది వస్తే అత్యవసర చికిత్స అవసరం"],
      ["National Vector Borne Disease Control Programme (NVBDCP)", "WHO Dengue Guidelines for Diagnosis and Management"], True, "intermediate")

add_c("telugu_comprehension", "te",
      "మలేరియా రాకుండా ఉండటానికి గ్రామీణ ప్రాంతాల్లో దోమల నివారణకు తీసుకోవాల్సిన చర్యలు ఏమిటి?",
      "ఇళ్ల చుట్టూ మురుగునీరు, పాత టైర్లు, కొబ్బరి చిప్పలు, కూలర్లలో నీరు నిల్వ ఉండకుండా చూసుకోవాలి. రాత్రి పడుకునేటప్పుడు క్రిమిసంహారక మందు పూసిన దోమతెరలు (LLINs) ఉపయోగించాలి. సాయంత్రం వేళల్లో శరీరాన్ని పూర్తిగా కప్పే దుస్తులు ధరించాలి మరియు దోమల నివారణ మందులు (రిపెల్లెంట్లు) వాడాలి. ఇంట్లో కిటికీలకు దోమల జాలీలు ఏర్పాటు చేసుకోవాలి.",
      ["నీరు నిల్వ లేకుండా పరిసరాల శుభ్రత పాటించాలి", "కీటకనాశని పూసిన దోమతెరలు (LLIN) వాడాలి", "పూర్తిగా కప్పే దుస్తులు ధరించాలి"],
      ["NVBDCP Malaria Operational Guidelines", "WHO Global Malaria Programme"], False, "basic")

add_c("telugu_comprehension", "te",
      "ఆస్తమా (ఉబ్బసం) ఉన్నవారు ఇన్హేలర్లను ప్రతిరోజూ వాడితే వాటికి అలవాటు పడిపోతారా (Addiction అవుతుందా)?",
      "ఇది సమాజంలో విస్తృతంగా ఉన్న పెద్ద అపోహ. ఇన్హేలర్లు వ్యసనం లేదా అలవాటుగా మారవు. ఇన్హేలర్ ద్వారా తీసుకునే మందు నేరుగా ఊపిరితిత్తుల లోపలి గాలి నాళాలకు మాత్రమే చేరుతుంది; రక్తంలోకి చాలా తక్కువ మోతాదులో మాత్రమే వెళ్తుంది. టాబ్లెట్లతో పోలిస్తే ఇన్హేలర్లలో 20 రెట్లు తక్కువ మోతాదు ఔషధం ఉంటుంది, కాబట్టి సైడ్ ఎఫెక్ట్స్ చాలా తక్కువ. ఆస్తమాను అదుపులో ఉంచడానికి వైద్యులు సూచించిన ప్రివెంటర్ ఇన్హేలర్లను క్రమంతప్పకుండా వాడటం ఎంతో సురక్షితం.",
      ["ఇన్హేలర్లకు ఎటువంటి వ్యసనం లేదా అలవాటు పడటం ఉండదు", "మందు నేరుగా ఊపిరితిత్తులకు వెళ్లి తక్కువ మోతాదుతో ఎక్కువ ప్రయోజనం ఇస్తుంది", "మాత్రలతో పోలిస్తే ఇన్హేలర్లలో దుష్ప్రభావాలు చాలా తక్కువ"],
      ["Global Initiative for Asthma (GINA) Guidelines", "Chest Council of India"], False, "basic")

add_c("telugu_comprehension", "te",
      "క్షయ వ్యాధి (TB) చికిత్సలో 6 నెలల పాటు మందులు క్రమం తప్పకుండా వాడటం ఎందుకు అత్యవసరం?",
      "క్షయ వ్యాధి మందులు వేసుకోవడం మొదలుపెట్టిన 2-3 వారాలలోనే దగ్గు తగ్గి రోగికి ఉపశమనం లభిస్తుంది. కానీ శరీరంలోని మైకోబాక్టీరియం బ్యాక్టీరియా పూర్తిగా నశించదు. మందులను మధ్యలోనే ఆపేస్తే బతికి ఉన్న బ్యాక్టీరియా మందులకు లొంగని మల్టీ-డ్రగ్ రెసిస్టెంట్ టీబీ (MDR-TB) గా మారుతుంది. ఇది ప్రాణాంతకం మరియు చికిత్స చాలా కష్టతరం. కాబట్టి డాక్టర్ చెప్పిన పూర్తి 6 నెలల కోర్సును ఖచ్చితంగా పూర్తిచేయాలి.",
      ["లక్షణాలు తగ్గినా 6 నెలల కోర్సు పూర్తిగా వాడాలి", "మధ్యలో ఆపేస్తే డ్రగ్ రెసిస్టెంట్ టీబీ (MDR-TB) గా మారుతుంది", "MDR-TB ప్రాణాంతకం మరియు చికిత్స సంక్లిష్టం"],
      ["National Tuberculosis Elimination Program (NTEP) India", "WHO Consolidated Guidelines on Tuberculosis"], True, "intermediate")

add_c("telugu_comprehension", "te",
      "టైఫాయిడ్ జ్వరం ఎలా వ్యాపిస్తుంది మరియు స్వచ్ఛమైన తాగునీటి ప్రాముఖ్యత ఏమిటి?",
      "టైఫాయిడ్ అనేది సాల్మొనెల్లా టైఫీ అనే బ్యాక్టీరియా ద్వారా కలుషితమైన ఆహారం మరియు కలుషితమైన తాగునీరు ద్వారా వ్యాపిస్తుంది. పచ్చి ఆహారాలు, రోడ్డు పక్కన కవర్ చేయని తినుబండారాలు మరియు అపరిశుభ్రమైన నీరు తాగడం వల్ల ఇది పేగుల్లోకి చేరుతుంది. నీటిని బాగా మరిగించి చల్లార్చి తాగడం, భోజనానికి ముందు చేతులు సబ్బుతో కడుక్కోవడం మరియు పరిశుభ్రమైన తాజా ఆహారం తీసుకోవడం ద్వారా టైఫాయిడ్ రాకుండా నిరోధించవచ్చు.",
      ["కలుషిత నీరు, ఆహారం ద్వారా సాల్మొనెల్లా టైఫీ బ్యాక్టీరియా వ్యాపిస్తుంది", "కాచి చల్లార్చిన నీటిని తాగడం వల్ల నివారించవచ్చు", "వ్యక్తిగత పరిశుభ్రత మరియు చేతులు కడుక్కోవడం ముఖ్యం"],
      ["WHO Fact Sheet: Typhoid", "National Centre for Disease Control (NCDC) India"], False, "basic")

add_c("telugu_comprehension", "te",
      "కామెర్లు (జాండిస్) వచ్చినప్పుడు ఆయిల్ ఫుడ్స్ ఎందుకు నివారించాలి మరియు ఎలాంటి ఆహారం తీసుకోవాలి?",
      "కామెర్లు వచ్చినప్పుడు కాలేయం (లివర్) వాపుకు గురై కొవ్వులను జీర్ణం చేసే పైత్యరసాన్ని (Bile) సరిగ్గా ఉత్పత్తి చేయలేదు. నూనెలు, నెయ్యి, వేపుళ్లు, నాన్‌వెజ్ వంటి కొవ్వు పదార్థాలు తింటే కాలేయంపై అదనపు భారం పడుతుంది. అందువల్ల తేలికగా అరిగే గంజి, పండ్ల రసాలు, ఇడ్లీ, చెరకు రసం, ద్రవాహారం మరియు పిండిపదార్థాలు ఎక్కువగా ఉండే ఆహారాన్ని తీసుకోవాలి. మద్యం పూర్తిగా నిషిద్ధం.",
      ["కాలేయం బలహీనపడటం వల్ల కొవ్వులను జీర్ణం చేసుకోలేదు", "నూనె, నెయ్యి, వేపుళ్లు కాలేయంపై భారం పెంచుతాయి", "తేలికగా అరిగే ద్రవాహారం, గంజి, పండ్లు తీసుకోవాలి"],
      ["Indian National Association for Study of the Liver (INASL)", "WHO Hepatitis Care Guidelines"], False, "intermediate")

add_c("telugu_comprehension", "te",
      "కండ్లకలక (కంజంక్టివైటిస్) వచ్చినప్పుడు కుటుంబ సభ్యులకు సోకకుండా ఎలాంటి జాగ్రత్తలు తీసుకోవాలి?",
      "కండ్లకలక అనేది ఇన్ఫెక్షన్ ఉన్న కళ్లను తాకిన చేతుల ద్వారా మరియు రోగి వాడిన వస్తువుల ద్వారా వేగంగా వ్యాపిస్తుంది. రోగి వాడిన తువ్వాళ్లు, దిండ్లు, చేతిరుమాళ్లు, కళ్లద్దాలను ఇతరులు వాడకూడదు. కంటిని చేతులతో తరచుగా రుద్దకూడదు; చేతులను సబ్బుతో తరచుగా కడుక్కోవాలి. కాటన్ ప్యాడ్‌తో శుభ్రమైన నీటితో కంటి స్రావాలను తుడిచి సురక్షితంగా పారవేయాలి. నేరుగా డాక్టర్ రాసిన చుక్కల మందులు మాత్రమే వాడాలి.",
      ["తువ్వాళ్లు, దిండ్లు పంచుకోకూడదు", "కళ్లను చేతులతో రుద్దకూడదు, తరచుగా చేతులు కడగాలి", "కంటిస్రావాలను శుభ్రమైన కాటన్‌తో తీసివేసి చేతులు శుభ్రం చేసుకోవాలి"],
      ["All India Ophthalmological Society (AIOS) Guidelines", "CDC Conjunctivitis Guidance"], False, "basic")

add_c("telugu_comprehension", "te",
      "చర్మంపై అకస్మాత్తుగా ఎర్రటి దద్దుర్లు (Hives / Urticaria) వచ్చి దురద పెడుతుంటే ప్రాథమికంగా ఏం చేయాలి?",
      "చర్మంపై దురద మరియు ఎర్రటి దద్దుర్లు అలెర్జీ ప్రతిచర్య వల్ల సంభవిస్తాయి. ప్రభావిత ప్రాంతాన్ని గోళ్లతో గట్టిగా గిల్లకూడదు; చల్లని నీటితో కడగడం లేదా చల్లని తడిగుడ్డతో అద్దడం ద్వారా ఉపశమనం లభిస్తుంది. ఏదైనా కొత్త మందులు, ఆహారాలు తిన్నారా గమనించాలి. పెదవులు, నాలుక వాపు రావడం, శ్వాస ఆడకపోవడం లేదా గొంతు బొంగురుపోవడం జరిగితే అది తీవ్రమైన అనాఫిలాక్సిస్ కావచ్చు, వెంటనే అత్యవసర చికిత్సకు వెళ్ళాలి.",
      ["దద్దుర్లను గోళ్లతో గిల్లకూడదు", "చల్లని నీటి కంప్రెస్ ఉపశమనం ఇస్తుంది", "శ్వాస ఇబ్బంది, పెదవుల వాపు వస్తే వెంటనే అత్యవసర విభాగానికి వెళ్లాలి"],
      ["Indian Association of Dermatologists, Venereologists and Leprologists (IADVL)", "BSACI Guidelines for Urticaria"], True, "intermediate")

add_c("telugu_comprehension", "te",
      "పంటి నొప్పి మరియు చిగుళ్ల నుండి రక్తం కారడానికి గల కారణాలు మరియు నివారణ మార్గాలు ఏమిటి?",
      "పంటిపై పాచి (ప్లేక్) మరియు బ్యాక్టీరియా పేరుకుపోవడం వల్ల చిగుళ్ల వాపు (జింజివైటిస్) మరియు దంతక్షయం (కేవిటీలు) ఏర్పడి నొప్పి, రక్తస్రావం జరుగుతాయి. రోజుకు రెండుసార్లు ఉదయం మరియు రాత్రి మృదువైన బ్రష్‌తో పళ్లు తోముకోవాలి. తీపి పదార్థాలు తిన్న తర్వాత నోటిని శుభ్రంగా పుక్కిలించాలి. సమస్య తీవ్రమైతే డెంటిస్ట్‌ను సంప్రదించి క్లీనింగ్ (స్కేలింగ్) చేయించుకోవాలి.",
      ["పాచి మరియు బ్యాక్టీరియా వల్ల చిగుళ్ల వాపు, రక్తస్రావం జరుగుతుంది", "రోజుకు రెండుసార్లు సరిగ్గా పళ్లు తోముకోవాలి", "తీపి పదార్థాల తర్వాత నోరు శుభ్రం చేసుకోవడం ముఖ్యం"],
      ["Dental Council of India Oral Health Guidelines", "WHO Oral Health Action Plan"], False, "basic")

add_c("telugu_comprehension", "te",
      "వయస్సు పైబడిన వారిలో మోకాళ్ల నొప్పులు (ఆస్టియో ఆర్థరైటిస్) నియంత్రణకు ఇంట్లో చేయదగిన పద్ధతులు ఏమిటి?",
      "బరువు అదుపులో ఉంచుకోవడం మోకాళ్లపై ఒత్తిడిని తగ్గిస్తుంది. మోకాళ్ల కండరాలను బలోపేతం చేసే తేలికపాటి వ్యాయామాలు (క్వాడ్రిసెప్స్ వ్యాయామాలు), వాకింగ్ చేయాలి. కింద కూర్చోవడం, మెట్లు ఎక్కువగా ఎక్కడం, బరువులు మోయడం తగ్గించాలి. నొప్పి ఉన్నప్పుడు వేడి కాపడం లేదా ఐస్ ప్యాక్ పెట్టవచ్చు. పెయిన్‌కిల్లర్ మాత్రలను డాక్టర్ సలహా లేకుండా నిరంతరం వాడటం కిడ్నీలకు ప్రమాదకరం.",
      ["శరీర బరువు తగ్గించుకోవడం మోకాళ్ల భారాన్ని తగ్గిస్తుంది", "తేలికపాటి కండరాల వ్యాయామాలు సహకరిస్తాయి", "నిరంతరం పెయిన్‌కిల్లర్లు వాడటం కిడ్నీలను దెబ్బతీస్తుంది"],
      ["Indian Orthopaedic Association Guidelines", "OARSI Guidelines for Knee Osteoarthritis"], False, "intermediate")

add_c("telugu_comprehension", "te",
      "మూత్రంలో మంట (యూరినరీ ట్రాక్ట్ ఇన్ఫెక్షన్ - UTI) వచ్చినప్పుడు నీటి వినియోగం ప్రాముఖ్యత ఏమిటి?",
      "మూత్రంలో మంట వచ్చినప్పుడు రోజుకు కనీసం 2.5 నుండి 3 లీటర్ల శుభ్రమైన నీరు తాగాలి. ఎక్కువ నీరు తాగడం వల్ల మూత్రాశయంలో పేరుకుపోయిన బ్యాక్టీరియా మూత్రం ద్వారా బయటకు కొట్టుకుపోతుంది. మూత్రాన్ని ఎక్కువసేపు ఆపుకోకూడదు. జ్వరం, వెన్నునొప్పి, వణుకు లేదా మూత్రంలో రక్తం కనిపిస్తే ఇన్ఫెక్షన్ కిడ్నీలకు చేరి ఉండవచ్చు కాబట్టి వెంటనే డాక్టర్‌ను సంప్రదించి యాంటీబయాటిక్స్ తీసుకోవాలి.",
      ["ఎక్కువ నీరు తాగడం వల్ల బ్యాక్టీరియా బయటకు ఫ్లష్ అవుతుంది", "మూత్రాన్ని ఆపుకోకూడదు", "జ్వరం లేదా నడుము నొప్పి వస్తే వెంటనే వైద్యుడిని సంప్రదించాలి"],
      ["Urological Society of India Guidelines", "NICE Guidelines: Urinary Tract Infection"], False, "basic")

add_c("telugu_comprehension", "te",
      "గుండెల్లో మంట (ఎసిడిటీ / GERD) రాకుండా రాత్రిపూట తీసుకోవాల్సిన జీవనశైలి మార్పులు ఏమిటి?",
      "రాత్రి భోజనం నిద్రపోవడానికి కనీసం 2 నుండి 3 గంటల ముందే ముగించాలి. భోజనం చేసిన వెంటనే పడుకోకూడదు. పడుకునేటప్పుడు తల మరియు ఛాతీ భాగాన్ని 6 అంగుళాలు ఎత్తులో ఉండేలా చూసుకోవాలి. రాత్రిపూట అధిక కొవ్వు, మసాలాలు, కాఫీ, చాక్లెట్, మద్యం తీసుకోకూడదు. బిగుతుగా ఉండే దుస్తులు ధరించకూడదు.",
      ["నిద్రకు 2-3 గంటల ముందే భోజనం చేయాలి", "పడుకునేటప్పుడు తల భాగాన్ని కొద్దిగా ఎత్తుగా ఉంచాలి", "రాత్రిపూట మసాలాలు, కొవ్వు ఆహారాలు నివారించాలి"],
      ["Indian Society of Gastroenterology GERD Consensus", "American College of Gastroenterology Guidelines"], False, "basic")

add_c("telugu_comprehension", "te",
      "చిన్నపిల్లలకు వేసే కోరింత దగ్గు, ధనుర్వాతం, కంఠసర్పి టీకా (DPT / పెంటావాలెంట్) ప్రాముఖ్యత ఏమిటి?",
      "పెంటావాలెంట్ టీకా శిశువులను డిఫ్తీరియా (కంఠసర్పి), పెర్టుసిస్ (కోరింత దగ్గు), టెటానస్ (ధనుర్వాతం), హెపటైటిస్ బి మరియు హిబ్ న్యుమోనియా/మెనింజైటిస్ వంటి 5 ప్రాణాంతక వ్యాధుల నుండి కాపాడుతుంది. దీనిని 6, 10, మరియు 14 వారాల వయసులో ప్రభుత్వ ఆరోగ్య కేంద్రాలలో ఉచితంగా వేస్తారు. టీకా వేసిన తర్వాత స్వల్ప జ్వరం లేదా వాపు రావడం సాధారణం, దీనికి భయపడాల్సిన పనిలేదు.",
      ["పెంటావాలెంట్ 5 ప్రాణాంతక వ్యాధుల నుండి రక్షిస్తుంది", "6, 10, 14 వారాల వయసులో షెడ్యూల్ ప్రకారం వేయించాలి", "టీకా తర్వాత స్వల్ప జ్వరం సాధారణ ప్రతిచర్య"],
      ["National Immunization Schedule (NIS) India", "WHO Position Paper on Pertussis Vaccines"], False, "basic")

# ==============================================================================
# CATEGORY 2: ENGLISH COMPREHENSION (20 cases)
# ==============================================================================
add_c("english_comprehension", "en",
      "What is the precise formulation and clinical rationale for low-osmolarity Oral Rehydration Salts (ORS) recommended by the WHO?",
      "WHO/UNICEF reduced-osmolarity ORS has a total osmolarity of 245 mOsm/L, containing Sodium (75 mmol/L), Glucose (75 mmol/L), Chloride (65 mmol/L), Potassium (20 mmol/L), and Citrate (10 mmol/L). The 1:1 sodium-to-glucose equimolar ratio leverages the active sodium-glucose cotransporter (SGLT-1) in the intestinal brush border to maximize coupled water absorption, significantly reducing stool output, vomiting frequency, and the need for unscheduled IV therapy.",
      ["Total osmolarity is 245 mOsm/L", "Leverages SGLT-1 coupled sodium-glucose cotransport", "Reduces stool output and need for intravenous rehydration"],
      ["WHO / UNICEF The Treatment of Diarrhoea: A manual for physicians", "The Lancet Reduced-Osmolarity ORS Meta-analysis"], False, "intermediate")

add_c("english_comprehension", "en",
      "How is HbA1c clinically defined, and what does a reading of 6.8% indicate regarding glycemic control and diagnostic status?",
      "HbA1c measures glycated hemoglobin, reflecting average plasma glucose concentrations over the preceding 8-12 weeks (the approximate lifespan of red blood cells). Under ADA/WHO criteria, normal is <5.7%, prediabetes is 5.7%-6.4%, and diabetes is >=6.5%. A reading of 6.8% diagnostic of Type 2 Diabetes Mellitus, or in an already established diabetic patient, represents fair-to-moderate glycemic control with an estimated average glucose (eAG) of approximately 148 mg/dL.",
      ["Reflects 8-12 week average blood glucose via glycated hemoglobin", "HbA1c >= 6.5% confirms diabetes", "6.8% equates to an estimated average glucose of ~148 mg/dL"],
      ["ADA Standards of Care in Diabetes 2024", "WHO Use of Glycated Haemoglobin in Diagnosis"], False, "intermediate")

add_c("english_comprehension", "en",
      "Differentiate between Stage 1 and Stage 2 Hypertension based on current clinical consensus criteria.",
      "According to ACC/AHA guidelines, Stage 1 Hypertension is defined as Systolic BP 130-139 mmHg or Diastolic BP 80-89 mmHg. Stage 2 Hypertension is defined as Systolic BP >= 140 mmHg or Diastolic BP >= 90 mmHg. Stage 1 often starts with lifestyle interventions plus monotherapy depending on 10-year ASCVD risk, whereas Stage 2 typically mandates immediate dual antihypertensive pharmacotherapy with two different classes alongside lifestyle modifications.",
      ["Stage 1: SBP 130-139 or DBP 80-89 mmHg", "Stage 2: SBP >= 140 or DBP >= 90 mmHg", "Stage 2 typically requires dual-agent pharmacotherapy"],
      ["AHA/ACC Guideline for the Prevention, Detection, Evaluation, and Management of High Blood Pressure", "IHCI Protocols"], False, "intermediate")

add_c("english_comprehension", "en",
      "What is the standard weight-based pediatric dosing protocol for oral paracetamol in managing acute fever?",
      "The standard pediatric oral dose for paracetamol (acetaminophen) is 10 to 15 mg/kg per dose administered every 4 to 6 hours as needed. The maximum safe 24-hour cumulative dose should not exceed 60 mg/kg/day or 4,000 mg/day (whichever is less) to prevent hepatotoxicity. Dosing should strictly be calculated based on the child's actual weight rather than age.",
      ["Standard dose is 10-15 mg/kg per dose", "Dosing interval is 4-6 hours with maximum 60 mg/kg/day", "Must be calculated by weight, not age, to prevent hepatotoxicity"],
      ["Indian Academy of Pediatrics (IAP) Pediatric Drug Formulary", "BNF for Children (BNFC)"], False, "intermediate")

add_c("english_comprehension", "en",
      "How does Vitamin C physiologically enhance non-heme iron absorption in patients with iron-deficiency anemia?",
      "Non-heme iron present in plant-based dietary sources exists primarily in the oxidized ferric state (Fe3+), which forms insoluble complexes at alkaline duodenal pH and is poorly absorbed. Vitamin C (ascorbic acid) acts as an electron donor, reducing ferric iron (Fe3+) to soluble ferrous iron (Fe2+), and forms a stable absorbable chelate that binds the divalent metal transporter 1 (DMT1) on enterocytes, increasing bioavailability by 2- to 3-fold.",
      ["Reduces ferric (Fe3+) to absorbable ferrous (Fe2+) state", "Forms soluble chelates that prevent precipitate formation in duodenum", "Significantly enhances enterocyte uptake via DMT1"],
      ["WHO Guidelines on Food Fortification with Micronutrients", "American Journal of Clinical Nutrition Iron Bioavailability"], False, "expert")

add_c("english_comprehension", "en",
      "What is the standard 4-drug intensive phase regimen for drug-susceptible pulmonary tuberculosis (NTEP/WHO)?",
      "The intensive phase consists of 2 months of daily fixed-dose combination quadruple therapy comprising Isoniazid (H), Rifampicin (R), Pyrazinamide (Z), and Ethambutol (E) (2HRZE), dosed according to standardized weight bands. This is followed by a 4-month continuation phase of Isoniazid, Rifampicin, and Ethambutol (4HRE) daily, completing a 6-month curative course.",
      ["Intensive phase: 2 months of HRZE (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol)", "Continuation phase: 4 months of HRE daily", "Total treatment duration is 6 months under direct observation"],
      ["NTEP Technical and Operational Guidelines for TB Control in India", "WHO Consolidated Guidelines on Tuberculosis"], False, "intermediate")

add_c("english_comprehension", "en",
      "What are the step-1 and step-2 preferred controller therapies in mild asthma under the GINA strategy?",
      "Under the Global Initiative for Asthma (GINA) Track 1, the preferred controller and reliever for adults and adolescents with mild asthma is as-needed low-dose inhaled corticosteroid (ICS) combined with formoterol (a rapid-onset long-acting beta2-agonist). This eliminates standalone SABA monotherapy, which increases exacerbation and mortality risks, ensuring anti-inflammatory coverage whenever bronchodilation is required.",
      ["Preferred Track 1 is as-needed low-dose ICS-formoterol", "Standalone SABA monotherapy is no longer recommended due to exacerbation risks", "Ensures immediate anti-inflammatory treatment with bronchodilation"],
      ["Global Initiative for Asthma (GINA) 2024 Strategy Report", "BMJ Asthma Management Guidelines"], False, "expert")

add_c("english_comprehension", "en",
      "What lifestyle and postural modifications are clinically indicated for patients with symptomatic GERD?",
      "Evidence-based non-pharmacological GERD interventions include elevating the head of the bed by 6 inches using bed risers (not merely extra pillows), avoiding recumbency for 2-3 hours after meals, weight loss in overweight individuals, avoiding known trigger foods (high-fat meals, caffeine, mint, chocolate, alcohol), cessation of tobacco smoking, and eating smaller, more frequent meals.",
      ["Elevate head of bed 6 inches on risers", "Wait at least 2-3 hours between eating and lying down", "Weight reduction and avoidance of tobacco and trigger foods"],
      ["ACG Clinical Guideline for the Diagnosis and Management of GERD", "NICE Guidelines on Dyspepsia"], False, "basic")

add_c("english_comprehension", "en",
      "Outline the primary national childhood immunization schedule in India up to 14 weeks of age.",
      "At birth: BCG, Oral Polio Vaccine (OPV-0), and Hepatitis B birth dose. At 6 weeks: Pentavalent-1 (DPT, Hep B, Hib), OPV-1, Rotavirus-1, Fractional Inactivated Poliovirus Vaccine (fIPV-1), and Pneumococcal Conjugate Vaccine (PCV-1). At 10 weeks: Pentavalent-2, OPV-2, and Rotavirus-2. At 14 weeks: Pentavalent-3, OPV-3, Rotavirus-3, fIPV-2, and PCV-2.",
      ["Birth: BCG, OPV-0, Hepatitis B", "6, 10, 14 weeks: Pentavalent, OPV, Rotavirus vaccine", "6 and 14 weeks include PCV and fIPV injections"],
      ["National Immunization Schedule (NIS) MoHFW Government of India", "IAP Guidebook on Immunization"], False, "intermediate")

add_c("english_comprehension", "en",
      "What constitutes the fundamental supportive therapy for acute uncomplicated viral gastroenteritis in adults?",
      "Therapy focuses on preventing and correcting dehydration using oral rehydration therapy with balanced electrolyte fluids (reduced-osmolarity ORS or broths). Routine empiric antibiotics and antimotility agents (such as loperamide) are contraindicated in invasive or inflammatory diarrhea. Small, frequent bland meals (BRAT diet concepts, complex carbohydrates) should resume as tolerated.",
      ["Oral rehydration with balanced electrolyte solutions is the cornerstone", "Antimotility drugs (loperamide) and routine antibiotics are contraindicated", "Early refeeding with simple, non-irritating foods"],
      ["ACG Clinical Guideline: Diagnosis, Treatment, and Prevention of Acute Diarrheal Infections", "WHO Diarrhoea Guidelines"], False, "basic")

add_c("english_comprehension", "en",
      "What is the clinical 'Rule of 15' for managing conscious patients experiencing acute hypoglycemia?",
      "The 'Rule of 15' mandates administering 15 grams of fast-acting simple carbohydrates (such as 3-4 glucose tablets, 1/2 cup / 120 ml of fruit juice or regular soda, or 1 tablespoon of sugar/honey). Wait 15 minutes, recheck capillary blood glucose, and if still below 70 mg/dL, repeat with another 15 grams of carbohydrates. Once normalized (>=70 mg/dL), consume a snack with complex carbs and protein.",
      ["Consume 15g fast-acting simple carbohydrates", "Wait 15 minutes and re-check blood glucose", "Repeat 15g if still < 70 mg/dL; follow with a meal or snack once stable"],
      ["ADA Standards of Care in Diabetes", "Endocrine Society Hypoglycemia Guidelines"], False, "basic")

add_c("english_comprehension", "en",
      "What are the established LDL cholesterol treatment targets for individuals categorized under very high cardiovascular risk?",
      "For individuals at very high cardiovascular risk (e.g., established ASCVD, diabetes with target organ damage, severe CKD), European and ACC/AHA guidelines target an LDL-C reduction of >= 50% from baseline and an absolute goal of < 55 mg/dL (< 1.4 mmol/L). High-intensity statin therapy (atorvastatin 40-80 mg or rosuvastatin 20-40 mg) supplemented with ezetimibe is standard.",
      ["Target LDL-C reduction of >= 50% from baseline", "Absolute goal < 55 mg/dL (< 1.4 mmol/L) for very high risk", "High-intensity statin with ezetimibe as needed"],
      ["ESC/EAS Guidelines for the Management of Dyslipidaemias", "AHA/ACC Cholesterol Clinical Guidelines"], False, "expert")

add_c("english_comprehension", "en",
      "Why is dietary potassium and sodium management crucial in patients with Stage 4 Chronic Kidney Disease?",
      "In Stage 4 CKD (eGFR 15-29 mL/min/1.73m2), nephron mass is severely compromised, diminishing renal excretion of potassium and sodium. Excessive potassium intake predisposes to life-threatening hyperkalemia, causing cardiac arrhythmias and arrest. Excess sodium causes intravascular volume overload, refractory hypertension, peripheral edema, and accelerates decline in renal function.",
      ["Impaired renal potassium clearance risks fatal cardiac arrhythmias", "Sodium retention causes severe volume overload and worsening hypertension", "Strict monitoring prevents sudden hyperkalemic arrest"],
      ["KDIGO Clinical Practice Guideline for the Management of CKD", "KDOQI Clinical Practice Guidelines"], False, "expert")

add_c("english_comprehension", "en",
      "What non-pharmacological trigger avoidance strategies are recommended for patients with frequent migraines?",
      "Evidence-based migraine trigger management involves maintaining regular sleep-wake cycles (avoiding sleep deprivation and oversleeping), regular meal timing without fasting or skipping meals, adequate hydration, stress mitigation techniques (CBT, progressive muscle relaxation), and identifying dietary triggers (aged cheeses, MSG, nitrates, artificial sweeteners, alcohol).",
      ["Maintain consistent sleep and meal schedules", "Avoid prolonged fasting and ensure hydration", "Identify personal food triggers and practice stress reduction"],
      ["American Headache Society (AHS) Guidelines", "NICE Headaches in over 12s"], False, "basic")

add_c("english_comprehension", "en",
      "Why must oral levothyroxine be administered strictly on an empty stomach in primary hypothyroidism?",
      "Levothyroxine sodium is absorbed in the jejunum and ileum, and its bioavailability is heavily impaired by food, dietary fiber, calcium carbonate, iron supplements, soy, and proton pump inhibitors. It must be taken with a full glass of water at least 30 to 60 minutes before breakfast, or at bedtime at least 3-4 hours after the evening meal, to achieve consistent therapeutic thyroid hormone levels.",
      ["Bioavailability is significantly reduced by food, calcium, and iron", "Must be taken 30-60 minutes before breakfast with water", "Separate from multivalent cation supplements by at least 4 hours"],
      ["ATA/AACE Guidelines for Hypothyroidism in Adults", "Endocrine Practice Thyroid Consensus"], False, "intermediate")

add_c("english_comprehension", "en",
      "What are the dietary calcium and Vitamin D daily requirements recommended for postmenopausal women with osteoporosis?",
      "Postmenopausal women aged >=50 require a total daily elemental calcium intake of 1,200 mg (preferably through dietary sources, supplemented only if intake is deficient) and 800 to 1,000 IU (20-25 mcg) of Vitamin D3 daily to maintain serum 25(OH)D concentrations at or above 30 ng/mL, preserving bone mineral density and facilitating intestinal calcium absorption.",
      ["1,200 mg elemental calcium daily (diet plus supplements)", "800 - 1,000 IU Vitamin D3 daily", "Maintain serum 25(OH)D levels >= 30 ng/mL"],
      ["AACE/ACE Clinical Practice Guidelines for Postmenopausal Osteoporosis", "NOF Osteoporosis Guidelines"], False, "intermediate")

add_c("english_comprehension", "en",
      "What dietary modifications are indicated to prevent recurrent acute flare-ups of gout?",
      "Gout management involves reducing serum uric acid by avoiding purine-rich animal proteins (organ meats such as liver/kidney, red meats, shellfish, sardines), eliminating high-fructose corn syrup and sugary beverages, strictly abstaining from beer and spirits, ensuring abundant daily hydration (>=2-3 L), and incorporating low-fat dairy products and cherries which have uricosuric effects.",
      ["Avoid organ meats, shellfish, and high-purine foods", "Eliminate high-fructose corn syrup and alcohol (especially beer)", "High fluid intake and low-fat dairy support uric acid clearance"],
      ["ACR Guideline for the Management of Gout", "EULAR Recommendations for Gout"], False, "intermediate")

add_c("english_comprehension", "en",
      "What is the household contact treatment protocol for an individual diagnosed with Sarcoptes scabiei (scabies)?",
      "All household members and close physical/sexual contacts must be treated simultaneously, regardless of whether they have active pruritus, because symptoms can take 2 to 6 weeks to manifest. Permethrin 5% dermal cream is applied from neck to toes, left on for 8-14 hours, and washed off; a second application is repeated 7 days later. All bedding and clothing used in the last 4 days must be washed in hot water (>50°C) and dried on high heat.",
      ["All household contacts must be treated simultaneously regardless of symptoms", "Permethrin 5% cream applied neck-to-toes and repeated in 7 days", "Bedding and clothing washed in hot water (>50°C) or sealed in bags for 72h"],
      ["CDC Scabies Treatment Guidelines", "BAD Guidelines for the Management of Scabies"], False, "intermediate")

add_c("english_comprehension", "en",
      "What clinical signs distinguish acute otitis media from otitis media with effusion in children?",
      "Acute otitis media (AOM) is defined by rapid onset of symptoms (otalgia, fever, irritability, ear tugging) accompanied by distinct physical signs of acute tympanic membrane inflammation, such as a distinctly bulging, erythematous, and opaque eardrum with impaired mobility. Otitis media with effusion (OME) presents fluid in the middle ear without signs of acute infection or bulging/erythema.",
      ["AOM presents with acute otalgia, fever, and distinct tympanic bulging", "OME exhibits middle ear fluid without acute inflammatory signs or pain", "Bulging tympanic membrane is the most specific physical diagnostic sign of AOM"],
      ["AAP Clinical Practice Guideline: The Diagnosis and Management of Acute Otitis Media", "NICE Otitis Media Guidelines"], False, "intermediate")

add_c("english_comprehension", "en",
      "What are the prominent neurological and hematological manifestations of severe Vitamin B12 deficiency?",
      "Hematologically, B12 deficiency leads to megaloblastic macrocytic anemia (elevated MCV > 100 fL, hypersegmented neutrophils, pancytopenia). Neurologically, it causes subacute combined degeneration of the spinal cord (SCD) characterized by loss of vibration and proprioception sensation (dorsal columns), spastic paraparesis (corticospinal tracts), peripheral sensory neuropathy (paresthesia), and neuropsychiatric disturbances (memory loss, dementia, depression).",
      ["Megaloblastic macrocytic anemia with hypersegmented neutrophils", "Subacute combined degeneration affecting dorsal and lateral spinal columns", "Loss of proprioception and vibration sense with peripheral neuropathy"],
      ["NEJM Vitamin B12 Deficiency Review", "British Society for Haematology Guidelines"], False, "expert")

# Write out first 40 cases to disk before continuing to next block
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"benchmark_metadata": {"total_cases": len(CASES)}, "cases": CASES}, f, indent=2, ensure_ascii=False)
print(f"Step 1: Generated {len(CASES)} cases so far.")

