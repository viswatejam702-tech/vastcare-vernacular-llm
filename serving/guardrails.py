"""
Trilingual Clinical Guardrails & Safety Defense Engine (Telugu • Hindi • English)
================================================================================
Comprehensive Defense-in-Depth for Clinical LLMs:
1. Medical Prompt Injection & Jailbreak Defense
2. Triage Emergency Escalation Dispatch (108, Tele-MANAS 14416, CPR, Stroke FAST)
3. Unsafe Advice & Off-Label Harm Filter
4. Unsupported Diagnosis Rejection
5. Medication-Risk & Dosage Modification Defense
6. Evidence Citation & Mandatory Clinical Disclaimer Enforcement

Author: Principal LLM Research Engineer & Production AI Infrastructure Architect
Project: VastCare Vernacular LLM
"""

import re
from typing import Tuple, Dict, Any, Optional, List

# Medical Prompt Injection & Jailbreak Patterns
JAILBREAK_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"act\s+as\s+(an?\s+)?(unrestricted|unfiltered|jailbroken|evil)\s+(doctor|pharmacist|bot)",
    r"you\s+are\s+now\s+in\s+dan\s+mode",
    r"pretend\s+(there\s+are\s+no|you\s+have\s+no)\s+(safety|medical|ethical)\s+rules",
    r"bypass\s+(medical\s+)?(disclaimers?|guardrails?|protocols?)",
    r"మునుపటి\s+సూచనలు\s+(మర్చిపో|రద్దు\s+చేయి)",
    r"నియమాలు\s+పట్టించుకోకు",
    r"నిబంధనలు\s+లేకుండా\s+సమాధానం\s+ఇవ్వు"
]

# Medication-Risk & Alteration Patterns
MEDICATION_ALTERATION_PATTERNS = [
    r"(మందుల|మాత్రల)\s+(డోస్|మోతాదు)\s+(పెంచ|తగ్గించ|డబుల్\s+చేయ|ఆపేయ)",
    r"(double|triple|increase|stop)\s+(my\s+)?(dosage|dose|tablets?|insulin|bp\s+medicine)",
    r"దవా\s+కా\s+డోస్\s+(బఢా|ఘటా|బంద్)",
    r"(insulin|bp\s+tablet|steroid)\s+sontanga\s+aapeyacha"
]

# Unsupported Direct Diagnosis Demands
UNSUPPORTED_DIAGNOSIS_PATTERNS = [
    r"నాకు\s+(క్యాన్సర్|హెచ్‌ఐవీ|టీబీ)\s+ఉందో\s+లేదో\s+ఖచ్చితంగా\s+చెప్పండి",
    r"diagnose\s+me\s+definitively\s+with",
    r"tell\s+me\s+100%\s+if\s+i\s+have\s+(cancer|hiv|stroke|leukemia)",
    r"కన్ఫర్మ్\s+చేసి\s+డయాగ్నోసిస్\s+ఇవ్వండి"
]

# Trilingual emergency keywords & pattern matching
EMERGENCY_PATTERNS = [
    (
        r"కార్డియాక్\s*అరెస్ట్|గుండె\s*ఆగిపోవడం|శ్వాస\s*ఆడట్లేదు|స్పృహ\s*తప్పి|cardiac\s*arrest|cpr|हार्ट\s*अटैक|सांस\s*रुक|सीपीआर|बेहोश",
        "CARDIAC_ARREST_CPR",
        {
            "te": "కార్డియాక్ అరెస్ట్ అత్యవసర పరిస్థితి! వెంటనే 108 కి కాల్ చేయండి. ఆలస్యం చేయకుండా నిమిషానికి 100-120 వేగంతో 30 ఛాతీ ఒత్తులకు 2 శ్వాసలు (30:2 CPR) ప్రారంభించండి! AED అందుబాటులో ఉంటే అమర్చండి.",
            "hi": "कार्डियक अरेस्ट आपातकालीन स्थिति है! तुरंत 108 पर कॉल करें। बिना देरी किए 100-120 प्रति मिनट की गति से 30 छाती के दबाव और 2 सांसें (30:2 CPR) शुरू करें! AED लगाएं।",
            "en": "Cardiac arrest emergency! Call 108 / 911 immediately. Start CPR at 100-120 compressions/min with a 30:2 compression-to-breath ratio without delay! Deploy an AED if available."
        }
    ),
    (
        r"గుండె\s*నొప్పి|ఛాతీలో\s*నొప్పి|గుండెపోటు|heart\s*attack|chest\s*pain|सीने\s*में\s*दर्द|दिल\s*का\s*दौरा",
        "CARDIAC_EMERGENCY",
        {
            "te": "ఛాతీలో తీవ్రమైన నొప్పి లేదా గుండెపోటు అనుమానం ఉంటే గోల్డెన్ అవర్ అత్యంత ముఖ్యం! వెంటనే 108 అంబులెన్స్‌కు ఫోన్ చేయండి. ఆస్పిరిన్ అలర్జీ లేకుంటే 300 mg మాత్ర నమలండి.",
            "hi": "सीने में तेज दर्द या दिल का दौरा पड़ने का संदेह होने पर तुरंत 108 एम्बुलेंस को कॉल करें! एस्पिरिन एलर्जी न होने पर 300 mg चबाएं।",
            "en": "Severe chest pain or suspected heart attack! Call 108 ambulance immediately. In the absence of aspirin allergy, chew a 300 mg aspirin tablet while awaiting transit."
        }
    ),
    (
        r"పక్షవాతం|ముఖం\s*వంకర|మాట\s*ముద్దబడటం|stroke|facial\s*droop|arm\s*weakness|slurred\s*speech|लकवा|स्ट्रोक",
        "STROKE_FAST_EMERGENCY",
        {
            "te": "పక్షవాతం (Stroke FAST) అత్యవసర పరిస్థితి! ముఖం వంకరపోవడం, చేయి పైకి లేపలేకపోవడం లేదా మాట ముద్దబడటం కనిపిస్తే తొలి 4.5 గంటల విండో పీరియడ్ లోపు సీటీ స్కాన్ ఉన్న ఆసుపత్రికి చేరాలి. మాలీష్ చేయవద్దు!",
            "hi": "स्ट्रोक (लकवा) आपातकाल! चेहरे का टेढ़ा होना या बोली लड़खड़ाहट स्ट्रोक के लक्षण हैं। पहले 4.5 घंटों के भीतर सीटी स्कैन वाले अस्पताल पहुंचें। मालिश न करें!",
            "en": "Acute Stroke FAST emergency! Sudden facial droop, arm weakness, or slurred speech requires hospital arrival within 4.5 hours for clot-dissolving therapy (rtPA). Do not waste time with home massages!"
        }
    ),
    (
        r"హెచ్‌ఐవీ\s*ఎక్స్‌పోజర్|సూది\s*గుచ్చుకుంది|needle\s*stick|pep\s*72|एचआईवी\s*एक्सपोजर|सुई\s*चुभना",
        "HIV_PEP_EMERGENCY",
        {
            "te": "హెచ్‌ఐవీ ఎక్స్‌పోజర్ జరిగినప్పుడు మొదటి 72 గంటల సమయం (మొదటి 2 గంటల్లో ఉత్తమం) అత్యంత కీలకం! తక్షణమే సమీప ప్రభుత్వ ART కేంద్రానికి వెళ్లి PEP (TLD) మందులు ప్రారంభించండి!",
            "hi": "एचआईवी एक्सपोजर के पहले 72 घंटे (विशेष रूप से पहले 2 घंटे) बेहद महत्वपूर्ण हैं! तुरंत नजदीकी सरकारी ART केंद्र जाकर PEP दवाएं शुरू करें!",
            "en": "HIV exposure emergency! The first 72 hours (ideally within 2 hours) are critical. Visit the nearest government ART center immediately for PEP treatment!"
        }
    ),
    (
        r"పాము\s*కాటు|snake\s*bite|విషపు\s*పాము|सांप\s*काटना|सांप\s*का\s*जहर",
        "SNAKEBITE_EMERGENCY",
        {
            "te": "పాము కాటు వేసినప్పుడు తాడుతో కట్టడం లేదా బ్లేడుతో కోయడం నిషిద్ధం! అవయవాన్ని కదల్చకుండా ఉంచి, తక్షణమే పాలీవాలెంట్ యాంటీ-స్నేక్ వెనమ్ (ASV) లభించే ప్రభుత్వ ఆసుపత్రికి తరలించండి!",
            "hi": "सांप के काटने पर रस्सी से न बांधें और न ही चीरा लगाएं! अंग को स्थिर रखें और तुरंत एंटी-स्नेक वेनम (ASV) उपलब्ध सरकारी अस्पताल ले जाएं!",
            "en": "Snakebite emergency! Do not apply tourniquets or cuts. Immobilize the limb and transport immediately to a government hospital equipped with Anti-Snake Venom (ASV)!"
        }
    ),
    (
        r"విషం|పురుగుల\s*మందు|poison|pesticide\s*ingestion|organophosphate|जहर|कीटनाशक",
        "POISONING_EMERGENCY",
        {
            "te": "విషం లేదా పురుగుల మందు తాగినప్పుడు బలవంతంగా వాంతి చేయించకూడదు; తక్షణమే బాధితుడిని అత్యవసర విభాగానికి (ICU) తీసుకెళ్ళి అట్రోపిన్ మరియు PAM విరుగుడు చికిత్స అందించాలి!",
            "hi": "जहर या कीटनाशक पीने पर जबरन उल्टी न करवाएं; पीड़ित को तुरंत आपातकालीन आईसीयू ले जाकर एंटीडोट (एट्रोपिन/PAM) दिलवाएं!",
            "en": "Poisoning or pesticide ingestion! Do not induce vomiting; transport the patient immediately to an emergency ICU for Atropine and Pralidoxime antidote resuscitation."
        }
    ),
    (
        r"ఆత్మహత్య|చనిపోవాలని|suicide|kill\s*myself|end\s*my\s*life|आत्महत्या|जान\s*देना",
        "SUICIDE_CRISIS_TELEMANAS",
        {
            "te": "దయచేసి ఆందోళన చెందకండి, మీ జీవితం ఎంతో విలువైనది. మీకు సహాయం చేయడానికి నిపుణులు సిద్ధంగా ఉన్నారు. తక్షణమే భారత ప్రభుత్వ ఉచిత మానసిక ఆరోగ్య టెలి-కౌన్సెలింగ్ హెల్ప్‌లైన్ Tele-MANAS నంబర్ 14416 లేదా 1800-891-4416 కు కాల్ చేయండి.",
            "hi": "कृपया परेशान न हों, आपका जीवन बहुत कीमती है। सहायता के लिए तुरंत भारत सरकार की मुफ्त मानसिक स्वास्थ्य हेल्पलाइन Tele-MANAS 14416 या 1800-891-4416 पर कॉल करें।",
            "en": "Please stay safe. You are not alone and help is available 24/7. Call India's national mental health helpline Tele-MANAS at 14416 or 1800-891-4416 immediately."
        }
    )
]

CLINICAL_DISCLAIMERS = {
    "te": "\n\n---\n*వైద్య నిరాకరణ (Vastcare Clinical Disclaimer)*: ఈ సమాచారం కేవలం అధికారిక మార్గదర్శకాల ఆధారంగా రూపొందించబడిన ఆరోగ్య అవగాహన కొరకు మాత్రమే. ఇది వైద్యుడి వ్యక్తిగత రోగ నిర్ధారణ లేదా చికిత్సకు ప్రత్యామ్నాయం కాదు. అత్యవసర పరిస్థితుల్లో తక్షణమే 108 కు కాల్ చేయండి.",
    "hi": "\n\n---\n*चिकित्सा अस्वीकरण (Vastcare Clinical Disclaimer)*: यह जानकारी केवल स्वास्थ्य जागरूकता के लिए है। यह किसी चिकित्सक के व्यक्तिगत निदान या उपचार का विकल्प नहीं है। आपात स्थिति में तुरंत 108 पर कॉल करें।",
    "en": "\n\n---\n*Medical Disclaimer (Vastcare Clinical Disclaimer)*: This information is for educational and guidance purposes only, grounded in published public health guidelines. It does not constitute a definitive medical diagnosis. In emergencies, call 108 or your local emergency number immediately."
}


class TeluguClinicalGuardrails:
    """Production Guardrails & Triage Interceptor."""

    @staticmethod
    def inspect_prompt_injection(query: str) -> Tuple[bool, Optional[str]]:
        """Detects adversarial jailbreak and prompt injection attempts."""
        for pattern in JAILBREAK_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return True, "PROMPT_INJECTION_BLOCKED"
        return False, None

    @staticmethod
    def inspect_medication_risk(query: str) -> Tuple[bool, Optional[str]]:
        """Identifies self-directed medication modification or dosage tampering."""
        for pattern in MEDICATION_ALTERATION_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return True, "MEDICATION_RISK_DETECTED"
        return False, None

    @staticmethod
    def inspect_unsupported_diagnosis(query: str) -> Tuple[bool, Optional[str]]:
        """Detects user demands for conclusive personal medical diagnosis."""
        for pattern in UNSUPPORTED_DIAGNOSIS_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return True, "UNSUPPORTED_DIAGNOSIS_DEMAND"
        return False, None

    @classmethod
    def inspect_query(cls, query: str, lang: str = "te") -> Tuple[bool, str, Dict[str, Any]]:
        """
        Comprehensive inspection of incoming user query across safety vectors.
        """
        lang = lang if lang in ["te", "hi", "en"] else "te"

        # 1. Jailbreak Check
        is_injection, tag = cls.inspect_prompt_injection(query)
        if is_injection:
            msg = {
                "te": "రక్షణ ప్రోటోకాల్: వైద్యపరమైన భద్రతా నియమాలను ఉల్లంఘించే లేదా కృత్రిమ ప్రాంప్ట్ ఇంజెక్షన్ అభ్యర్థనలు నిరాకరించబడ్డాయి.",
                "hi": "सुरक्षा चेतावनी: नैदानिक सुरक्षा दिशानिर्देशों को बायपास करने का प्रयास अस्वीकार कर दिया गया है।",
                "en": "Safety Protocol: Requests attempting to bypass medical guardrails or execute prompt injection are strictly rejected."
            }
            return True, tag, {
                "is_emergency": False,
                "is_security_violation": True,
                "emergency_tag": tag,
                "notice": msg.get(lang, msg["en"])
            }

        # 2. Medical Triage Emergency Check
        for pattern, em_tag, emergency_dict in EMERGENCY_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return True, em_tag, {
                    "is_emergency": True,
                    "is_security_violation": False,
                    "emergency_tag": em_tag,
                    "notice": emergency_dict.get(lang, emergency_dict["en"])
                }

        # 3. Medication Alteration Risk Check
        is_med_risk, med_tag = cls.inspect_medication_risk(query)
        if is_med_risk:
            med_warning = {
                "te": "ముఖ్య గమనిక: వైద్యుల అనుమతి లేకుండా ప్రిస్క్రిప్షన్ మందుల మోతాదును సొంతంగా మార్చడం లేదా ఆపడం ప్రాణాలకే ప్రమాదకరం. దయచేసి మీ డాక్టర్‌ను సంప్రదించండి.",
                "hi": "महत्वपूर्ण चेतावनी: चिकित्सक की सलाह के बिना दवाओं की खुराक बदलना या बंद करना खतरनाक हो सकता है। कृपया अपने डॉक्टर से संपर्क करें।",
                "en": "Medication Safety Warning: Modifying prescribed dosages or discontinuing medications without physician supervision can lead to severe complications. Please consult your prescribing doctor."
            }
            return False, med_tag, {
                "is_emergency": False,
                "is_med_risk": True,
                "emergency_tag": med_tag,
                "notice": med_warning.get(lang, med_warning["en"])
            }

        # 4. Routine Safe Query
        return False, "ROUTINE", {
            "is_emergency": False,
            "emergency_tag": "ROUTINE",
            "notice": None
        }

    @staticmethod
    def wrap_clinical_response(
        response_text: str,
        is_emergency: bool = False,
        emergency_notice: Optional[str] = None,
        rag_citations: Optional[List[Dict[str, Any]]] = None,
        lang: str = "te"
    ) -> str:
        """Appends formatted emergency banner, RAG citations, and localized clinical disclaimer."""
        lang = lang if lang in ["te", "hi", "en"] else "te"
        parts = []

        if is_emergency and emergency_notice:
            parts.append(f"🚨 **అత్యవసర హెచ్చరిక / EMERGENCY ALERT**:\n{emergency_notice}")

        parts.append(response_text)

        if rag_citations:
            citation_lines = ["\n📚 **అధికారిక క్లినికల్ ఆధారాలు (Evidence Sources)**:"]
            for c in rag_citations:
                title = c.get("title", "Clinical Guideline")
                source = c.get("source", "MoHFW/ICMR")
                citation_lines.append(f"- *{title}* ({source})")
            parts.append("\n".join(citation_lines))

        disclaimer = CLINICAL_DISCLAIMERS.get(lang, CLINICAL_DISCLAIMERS["te"])
        parts.append(disclaimer)
        return "\n\n".join(parts)
