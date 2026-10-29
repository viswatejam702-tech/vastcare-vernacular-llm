"""
Trilingual Clinical Guardrails & Triage Safety System (Telugu • Hindi • English)
================================================================================
Detects medical emergencies across Telugu, Hindi, and English queries, enforcing
localized emergency escalation protocols and clinical disclaimers.
"""

import re
from typing import Tuple, Dict, Any

# Trilingual emergency keywords & pattern matching
EMERGENCY_PATTERNS = [
    (
        r"కార్డియాక్\s*అరెస్ట్|గుండె\s*ఆగిపోవడం|శ్వాస\s*ఆడట్లేదు|స్పృహ\s*తప్పి|cardiac\s*arrest|cpr|हार्ट\s*अटैक|सांस\s*रुक|सीपीआर|बेहोश",
        "CARDIAC_ARREST_CPR",
        {
            "te": "కార్డియాక్ అరెస్ట్ అత్యవసర పరిస్థితి! వెంటనే 108 కి కాల్ చేయండి. ఆలస్యం చేయకుండా నిమిషానికి 100-120 వేగంతో 30 ఛాతీ ఒత్తులకు 2 శ్వాసలు (30:2 CPR) ప్రారంభించండి!",
            "hi": "कार्डियक अरेस्ट आपातकालीन स्थिति है! तुरंत 108 पर कॉल करें। बिना देरी किए 100-120 प्रति मिनट की गति से 30 छाती के दबाव और 2 सांसें (30:2 CPR) शुरू करें!",
            "en": "Cardiac arrest emergency! Call 108 / 911 immediately. Start CPR at 100-120 compressions/min with 30:2 compression-to-breath ratio without delay!"
        }
    ),
    (
        r"గుండె\s*నొప్పి|ఛాతీలో\s*నొప్పి|గుండెపోటు|heart\s*attack|chest\s*pain|सीने\s*में\s*दर्द|दिल\s*का\s*दौरा",
        "CARDIAC_EMERGENCY",
        {
            "te": "ఛాతీలో తీవ్రమైన నొప్పి లేదా గుండెపోటు అనుమానం ఉంటే వెంటనే 108 అంబులెన్స్‌కు ఫోన్ చేయండి లేదా సమీప ఎమర్జెన్సీ ఆసుపత్రికి వెళ్లండి!",
            "hi": "सीने में तेज दर्द या दिल का दौरा पड़ने का संदेह होने पर तुरंत 108 एम्बुलेंस को कॉल करें या निकटतम आपातकालीन अस्पताल जाएं!",
            "en": "Severe chest pain or suspected heart attack! Call 108 ambulance immediately or reach the nearest emergency hospital."
        }
    ),
    (
        r"హెచ్‌ఐవీ\s*ఎక్స్‌పోజర్|సూది\s*గుచ్చుకుంది|needle\s*stick|pep\s*72|एचआईवी\s*एक्सपोजर|सुई\s*चुभना",
        "HIV_PEP_EMERGENCY",
        {
            "te": "హెచ్‌ఐవీ ఎక్స్‌పోజర్ జరిగినప్పుడు మొదటి 72 గంటల సమయం (మొదటి 2 గంటల్లో ఉత్తమం) అత్యంత కీలకం! తక్షణమే సమీప ప్రభుత్వ ART కేంద్రానికి వెళ్లి PEP మందులు ప్రారంభించండి!",
            "hi": "एचआईवी एक्सपोजर के पहले 72 घंटे (विशेष रूप से पहले 2 घंटे) बेहद महत्वपूर्ण हैं! तुरंत नजदीकी सरकारी ART केंद्र जाकर PEP दवाएं शुरू करें!",
            "en": "HIV exposure emergency! The first 72 hours (ideally within 2 hours) are critical. Visit the nearest government ART center immediately for PEP treatment!"
        }
    ),
    (
        r"కీటోయాసిడోసిస్|dka|ఫ్రూటీ\s*శ్వాస|diabetic\s*ketoacidosis|कीटोएसिडोसिस",
        "DIABETIC_DKA_EMERGENCY",
        {
            "te": "డయాబెటిక్ కీటోయాసిడోసిస్ (DKA) ప్రాణాంతక పరిస్థితి! తక్షణమే సమీప ఆసుపత్రి ఐసీయూలో చేరి ఐవీ ద్రవాలు మరియు ఇన్సులిన్ డ్రిప్ చికిత్స పొందండి!",
            "hi": "डायबिटिक कीटोएसिडोसिस (DKA) जानलेवा स्थिति है! तुरंत नजदीकी अस्पताल के ICU में भर्ती होकर IV तरल पदार्थ और इंसुलिन ड्रिप प्राप्त करें!",
            "en": "Diabetic Ketoacidosis (DKA) is a life-threatening emergency! Seek immediate hospital ICU admission for IV fluids and insulin infusion."
        }
    ),
    (
        r"పాము\s*కాటు|snake\s*bite|విషపు\s*పాము|सांप\s*काटना|सांप\s*का\s*जहर",
        "SNAKEBITE_EMERGENCY",
        {
            "te": "పాము కాటు వేసినప్పుడు అవయవాన్ని కదల్చకుండా ఉంచి, తక్షణమే యాంటీ-స్నేక్ వెనమ్ (ASV) లభించే ప్రభుత్వ ఆసుపత్రికి తరలించండి!",
            "hi": "सांप के काटने पर अंग को स्थिर रखें और तुरंत एंटी-स्नेक वेनम (ASV) उपलब्ध सरकारी अस्पताल ले जाएं!",
            "en": "Snakebite emergency! Immobilize the affected limb and transport immediately to a government hospital equipped with Anti-Snake Venom (ASV)!"
        }
    ),
    (
        r"విషం|పురుగుల\s*మందు|poison|pesticide\s*ingestion|जहर|कीटनाशक",
        "POISONING_EMERGENCY",
        {
            "te": "విషం లేదా పురుగుల మందు తాగినప్పుడు బలవంతంగా వాంతి చేయించకూడదు; తక్షణమే బాధితుడిని అత్యవసర చికిత్స విభాగానికి తీసుకెళ్లండి!",
            "hi": "जहर या कीटनाशक पीने पर जबरन उल्टी न करवाएं; पीड़ित को तुरंत आपातकालीन चिकित्सा केंद्र ले जाएं!",
            "en": "Poisoning or pesticide ingestion! Do not induce vomiting; transport the patient immediately to an emergency care department."
        }
    )
]

CLINICAL_DISCLAIMERS = {
    "te": "\n\n---\n*వైద్య నిరాకరణ (Vastcare Clinical Disclaimer)*: ఈ సమాచారం కేవలం అవగాహన కొరకు మాత్రమే. ఖచ్చితమైన రోగ నిర్ధారణ మరియు చికిత్స కొరకు అర్హత కలిగిన వైద్యుడిని లేదా 108 అత్యవసర సేవలను సంప్రదించండి.",
    "hi": "\n\n---\n*चिकित्सा अस्वीकरण (Vastcare Clinical Disclaimer)*: यह जानकारी केवल जागरूकता के लिए है। सटीक निदान और उपचार के लिए योग्य चिकित्सक या 108 आपातकालीन सेवाओं से संपर्क करें।",
    "en": "\n\n---\n*Medical Disclaimer (Vastcare Clinical Disclaimer)*: This information is for educational purposes only. For accurate diagnosis and treatment, please consult a qualified physician or contact 108 emergency services."
}


class TeluguClinicalGuardrails:
    @staticmethod
    def inspect_query(query: str, lang: str = "te") -> Tuple[bool, str, Dict[str, Any]]:
        """
        Inspects incoming user prompt across Telugu, Hindi, and English.
        """
        lang = lang if lang in ["te", "hi", "en"] else "te"
        for pattern, tag, emergency_dict in EMERGENCY_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return True, tag, {
                    "is_emergency": True,
                    "emergency_tag": tag,
                    "notice": emergency_dict.get(lang, emergency_dict["en"])
                }

        return False, "ROUTINE", {
            "is_emergency": False,
            "emergency_tag": "ROUTINE",
            "notice": None
        }

    @staticmethod
    def wrap_clinical_response(
        response_text: str,
        is_emergency: bool = False,
        emergency_notice: str = None,
        rag_citations: list = None,
        lang: str = "te"
    ) -> str:
        """
        Wraps model response with emergency warnings, RAG source citations, and localized disclaimer.
        """
        lang = lang if lang in ["te", "hi", "en"] else "te"
        final_text = response_text

        if is_emergency and emergency_notice:
            alert_header = {
                "te": "🚨 **అత్యవసర వైద్య హెచ్చరిక (CLINICAL EMERGENCY ALERT)**:\n",
                "hi": "🚨 **आपातकालीन चिकित्सा चेतावनी (CLINICAL EMERGENCY ALERT)**:\n",
                "en": "🚨 **CLINICAL EMERGENCY ALERT**:\n"
            }[lang]
            final_text = alert_header + emergency_notice + "\n\n" + final_text

        if rag_citations:
            citation_header = {
                "te": "\n\n📚 **ధృవీకరించబడిన వైద్య ఆధారాలు (Verified Guidelines)**:\n",
                "hi": "\n\n📚 **प्रमाणित चिकित्सा दिशानिर्देश (Verified Guidelines)**:\n",
                "en": "\n\n📚 **Verified Clinical Guidelines (Evidence-Based Grounding)**:\n"
            }[lang]
            citation_lines = citation_header
            for c in rag_citations:
                citation_lines += f"- *{c['title']}* (`{c['source']}`)\n"
            final_text += citation_lines

        final_text += CLINICAL_DISCLAIMERS.get(lang, CLINICAL_DISCLAIMERS["en"])
        return final_text
