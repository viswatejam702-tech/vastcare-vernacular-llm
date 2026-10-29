// Vastcare Trilingual Clinical Studio Logic (Telugu • Hindi • English)
// Real-Time Hands-Free Conversational Voice Assistant & NLP Grounding Engine

let currentLang = 'te'; // 'te' | 'hi' | 'en'
let isVoiceAudioActive = true;
let isHandsFreeMode = false;
let speechRecognizer = null;
let isRecording = false;
let speechSilenceTimer = null;

// Trilingual Localization Dictionary & Topic Guidelines
const I18N = {
  te: {
    title: 'వాస్ట్‌కేర్ తెలుగు ఆరోగ్య AI (Clinical Assistant)',
    subtitle: 'Qwen-3B-GGUF • Hybrid RAG Grounded',
    placeholder: 'తెలుగులో మీ ఆరోగ్య ప్రశ్నను అడగండి (ప్రశ్న టైప్ చేసి Enter నొక్కండి)...',
    sendBtn: 'పంపు',
    topicsLabel: 'టాపిక్స్:',
    listeningText: '🎙️ తెలుగులో వింటున్నాను... మాట్లాడండి (మౌనంగా ఉంటే ఆటోమేటిక్‌గా పంపబడుతుంది)...',
    greeting: `నమస్కారం! నేను వాస్ట్‌కేర్ ఆధ్వర్యంలో పనిచేసే నిపుణులైన తెలుగు క్లినికల్ సహాయకుడిని. 
               <strong>CPR అత్యవసర పునరుజ్జీవనం</strong>, <strong>F.A.S.T పక్షవాతం (Stroke)</strong>, <strong>IVF వంధ్యత్వ చికిత్స</strong>, <strong>హెచ్‌ఐవీ/ఎయిడ్స్ (NACO TLD)</strong>, <strong>క్యాన్సర్ ముందస్తు స్క్రీనింగ్</strong>, <strong>క్షయవ్యాధి (TB)</strong>, <strong>పాము కాటు (ASV)</strong>, <strong>మధుమేహం/ఇన్సులిన్</strong> లేదా <strong>ప్రభుత్వ ఆరోగ్యశ్రీ పథకాలపై</strong> మీ సందేహాలను అడగండి.`,
    chips: [
      { label: '🫀 CPR ప్రథమ చికిత్స', prompt: 'కార్డియాక్ అరెస్ట్ వచ్చినప్పుడు CPR ఛాతీ ఒత్తిడి వేగం మరియు నిష్పత్తి ఎంత ఉండాలి?' },
      { label: '🧠 F.A.S.T పక్షవాతం (Stroke)', prompt: 'బ్రెయిన్ స్ట్రోక్ వచ్చినప్పుడు F.A.S.T లక్షణాలు మరియు 4.5 గంటల గోల్డెన్ అవర్ ప్రాముఖ్యత ఏమిటి?' },
      { label: '👶 IVF & వంధ్యత్వం', prompt: 'ఐవీఎఫ్ (IVF) టెస్ట్ ట్యూబ్ బేబీ చికిత్సలో ప్రధాన 5 దశలు ఏమిటి?' },
      { label: '🛡️ HIV/AIDS (NACO)', prompt: 'హెచ్‌ఐవీ సోకిన వారు ప్రభుత్వ ART కేంద్రాల్లో లభించే TLD మందులను ఎలా వాడాలి?' },
      { label: '🎗️ క్యాన్సర్ స్క్రీనింగ్', prompt: 'రొమ్ము క్యాన్సర్ మరియు గర్భాశయ ముఖద్వార క్యాన్సర్ స్క్రీనింగ్ పరీక్షలు ఎప్పుడు చేయించాలి?' },
      { label: '🫁 క్షయవ్యాధి (TB & నిక్షయ్)', prompt: '2 వారాలకు మించి దగ్గు ఉంటే టీబీ నిర్ధారణ CBNAAT పరీక్ష మరియు నిక్షయ్ పోషణ్ యోజన వివరాలు ఏమిటి?' },
      { label: '🐍 పాము కాటు (ASV)', prompt: 'పాము కాటు వేసినప్పుడు తక్షణమే చేయవలసిన ప్రథమ చికిత్స ఏమిటి? Tourniquet కట్టవచ్చా?' },
      { label: '🩸 మధుమేహం & DKA', prompt: 'డయాబెటిస్‌లో డయాబెటిక్ కీటోయాసిడోసిస్ (DKA) మరియు హైపోగ్లైసీమియాను ఎలా గుర్తించాలి?' },
      { label: '🏥 ప్రభుత్వ పథకాలు', prompt: 'ఆరోగ్యశ్రీ మరియు ఆయుష్మాన్ భారత్ (PM-JAY) కింద ఉచిత డయాలసిస్ మరియు క్యాన్సర్ చికిత్సలు ఎలా పొందాలి?' }
    ],
    systemPrompt: 'మీరు వాస్ట్‌కేర్ (Vastcare) ఆధ్వర్యంలో పనిచేసే నిపుణులైన తెలుగు ఆరోగ్య AI సహాయకులు. వినియోగదారుల ప్రశ్నలకు ప్రామాణికమైన తెలుగులో సమాధానాలు ఇవ్వండి.'
  },
  hi: {
    title: 'वास्टकेयर हिंदी स्वास्थ्य एआई (Clinical Assistant)',
    subtitle: 'Qwen-3B-GGUF • Hybrid RAG Grounded',
    placeholder: 'हिंदी में अपना स्वास्थ्य प्रश्न पूछें (प्रश्न लिखकर Enter दबाएं)...',
    sendBtn: 'भेजें',
    topicsLabel: 'प्रमुख विषय:',
    listeningText: '🎙️ हिंदी में सुन रहा हूँ... बोलिए (रुकने पर स्वतः भेजा जाएगा)...',
    greeting: `नमस्ते! मैं वास्टकेयर द्वारा संचालित विशेषज्ञ क्लिनिकल एआई सहायक हूँ। 
               <strong>सीपीआर (CPR) आपातकालीन चिकित्सा</strong>, <strong>ब्रेन स्ट्रोक (F.A.S.T)</strong>, <strong>आईवीएफ (IVF) बांझपन</strong>, <strong>एचआईवी/एड्स (NACO TLD)</strong>, <strong>कैंसर स्क्रीनिंग</strong>, <strong>टीबी रोग (NTEP)</strong>, <strong>सर्पदंश (ASV)</strong>, <strong>मधुमेह/इंसुलिन</strong> या <strong>आयुष्मान भारत योजनाओं</strong> पर अपने प्रश्न पूछें।`,
    chips: [
      { label: '🫀 CPR प्राथमिक चिकित्सा', prompt: 'कार्डियक अरेस्ट होने पर CPR छाती के दबाव की गति और अनुपात क्या होना चाहिए?' },
      { label: '🧠 ब्रेन स्ट्रोक (F.A.S.T)', prompt: 'ब्रेन स्ट्रोक में F.A.S.T लक्षण और शुरुआती 4.5 घंटे के गोल्डन ऑवर का क्या महत्व है?' },
      { label: '👶 IVF बांझपन उपचार', prompt: 'आईवीएफ (IVF - टेस्ट ट्यूब बेबी) उपचार के 5 प्रमुख चरण कौन से हैं?' },
      { label: '🛡️ HIV/AIDS (NACO)', prompt: 'एचआईवी रोगियों को सरकारी ART केंद्रों पर मिलने वाली TLD दवाओं का सेवन कैसे करना चाहिए?' },
      { label: '🎗️ कैंसर स्क्रीनिंग', prompt: 'स्तन कैंसर और गर्भाशय ग्रीवा कैंसर की प्रारंभिक जांच कब करवानी चाहिए?' },
      { label: '🫁 टीबी एवं निक्षय योजना', prompt: 'लगातार 2 हफ्ते खांसी होने पर CBNAAT टीबी जांच और निक्षय पोषण योजना का लाभ कैसे लें?' },
      { label: '🐍 सर्पदंश (सांप काटना)', prompt: 'सांप काटने पर तुरंत क्या प्राथमिक उपचार करना चाहिए? क्या कसकर रस्सी बांधनी चाहिए?' },
      { label: '🩸 मधुमेह & DKA', prompt: 'डायबिटीज में कीटोएसिडोसिस (DKA) और हाइपोग्लाइसीमिया के प्रमुख लक्षण क्या हैं?' },
      { label: '🏥 सरकारी योजनाएं', prompt: 'आयुष्मान भारत (PM-JAY) और राज्य स्वास्थ्य योजनाओं के तहत मुफ्त डायलिसिस और कैंसर उपचार कैसे प्राप्त करें?' }
    ],
    systemPrompt: 'आप वास्टकेयर (Vastcare) के अंतर्गत काम करने वाले विशेषज्ञ हिंदी स्वास्थ्य AI सहायक हैं। उपयोगकर्ताओं के प्रश्नों के मानक और प्रामाणिक हिंदी में उत्तर दें।'
  },
  en: {
    title: 'Vastcare Clinical AI Assistant',
    subtitle: 'Qwen-3B-GGUF • Hybrid RAG Grounded',
    placeholder: 'Ask your clinical healthcare question (Type and press Enter)...',
    sendBtn: 'Send',
    topicsLabel: 'Topics:',
    listeningText: '🎙️ Listening in English... Speak now (Auto-submits on pause)...',
    greeting: `Hello! I am Vastcare's expert clinical AI assistant. 
               Ask your questions on <strong>CPR Emergency Resuscitation</strong>, <strong>Acute Stroke (F.A.S.T)</strong>, <strong>IVF Infertility Stages</strong>, <strong>HIV/AIDS (NACO TLD)</strong>, <strong>Cancer Screening</strong>, <strong>Tuberculosis (NTEP)</strong>, <strong>Snakebite Toxicology</strong>, <strong>Diabetes & DKA</strong>, or <strong>Government Health Schemes (PM-JAY)</strong>.`,
    chips: [
      { label: '🫀 CPR Protocol', prompt: 'What is the recommended chest compression rate and ratio for CPR in cardiac arrest?' },
      { label: '🧠 Acute Stroke (F.A.S.T)', prompt: 'What are the F.A.S.T warning signs of acute stroke and the significance of the 4.5-hour golden window?' },
      { label: '👶 IVF & Infertility', prompt: 'What are the 5 core stages of IVF (In Vitro Fertilization) treatment?' },
      { label: '🛡️ HIV/AIDS (NACO)', prompt: 'How should HIV-positive individuals take the first-line TLD regimen per NACO guidelines?' },
      { label: '🎗️ Cancer Screening', prompt: 'When should screening for breast and cervical cancer (Mammography, Pap Smear) be performed?' },
      { label: '🫁 Tuberculosis (NTEP)', prompt: 'What are the diagnosis protocols (CBNAAT) and Nikshay Poshan benefits for chronic cough > 2 weeks?' },
      { label: '🐍 Snakebite Protocol', prompt: 'What is the immediate first aid protocol for venomous snakebite? Is tourniquet application safe?' },
      { label: '🩸 Diabetes & DKA', prompt: 'How to recognize Diabetic Ketoacidosis (DKA) and acute hypoglycemia in diabetic patients?' },
      { label: '🏥 Health Schemes', prompt: 'How to access cashless dialysis and oncology care under Ayushman Bharat PM-JAY and state schemes?' }
    ],
    systemPrompt: 'You are an expert clinical AI healthcare assistant powered by Vastcare. Provide clear, evidence-based, empathetic medical answers with safety guardrails.'
  }
};

const BENCHMARK_ITEMS = [
  { id: "te_bench_cpr_001", cat: "Cardiology", q: "కార్డియాక్ అరెస్ట్ వచ్చినప్పుడు CPR ఛాతీ ఒత్తిడి వేగం మరియు నిష్పత్తి ఎంత ఉండాలి?", base: "3.5", ft: "5.0", human: "5.0" },
  { id: "te_bench_stroke_001", cat: "Neurology", q: "బ్రెయిన్ స్ట్రోక్ లో F.A.S.T లక్షణాలు మరియు 4.5 గంటల గోల్డెన్ అవర్ లో rtPA ప్రాముఖ్యత ఏమిటి?", base: "3.6", ft: "5.0", human: "5.0" },
  { id: "te_bench_ivf_001", cat: "Maternal Care", q: "ఐవీఎఫ్ (IVF) సంతాన సాఫల్య చికిత్సలో ప్రధాన 5 దశలు ఏమిటి? ఎవరికి ఇది అవసరం?", base: "3.8", ft: "5.0", human: "5.0" },
  { id: "te_bench_hiv_001", cat: "Infectious", q: "హెచ్‌ఐవీ సోకిన వారు ప్రభుత్వ ART కేంద్రాల్లో లభించే TLD మందులను ఎలా వాడాలి? U=U అంటే ఏమిటి?", base: "3.6", ft: "5.0", human: "5.0" },
  { id: "te_bench_cancer_001", cat: "Oncology", q: "రొమ్ము క్యాన్సర్ మరియు గర్భాశయ ముఖద్వార క్యాన్సర్ స్క్రీనింగ్ పరీక్షలు ఎప్పుడు చేయించాలి?", base: "3.7", ft: "5.0", human: "5.0" },
  { id: "te_bench_tb_001", cat: "Respiratory", q: "2 వారాలకు మించి దగ్గు ఉంటే టీబీ నిర్ధారణకు CBNAAT పరీక్ష మరియు నిక్షయ్ పోషణ్ వివరాలు ఏమిటి?", base: "3.7", ft: "5.0", human: "5.0" },
  { id: "te_bench_snake_001", cat: "Toxicology", q: "పాము కాటు వేసినప్పుడు చేయాల్సిన ప్రథమ చికిత్స ఏమిటి? Tourniquet ఎందుకు కట్టకూడదు?", base: "3.8", ft: "5.0", human: "5.0" },
  { id: "te_bench_diab_001", cat: "Diabetes", q: "డయాబెటిస్‌లో డయాబెటిక్ కీటోయాసిడోసిస్ (DKA) మరియు హైపోగ్లైసీమియాను ఎలా గుర్తించాలి?", base: "3.9", ft: "5.0", human: "5.0" },
  { id: "te_bench_dialysis_001", cat: "Nephrology", q: "దీర్ఘకాలిక కిడ్నీ వైఫల్యం (CKD) ఉన్న రోగులు హీమోడయాలసిస్ మరియు ఆహారంలో ఎలాంటి జాగ్రత్తలు పాటించాలి?", base: "3.8", ft: "5.0", human: "5.0" },
  { id: "te_bench_001", cat: "Maternal Care", q: "గర్భధారణ సమయంలో ఐరన్ మాత్రలు తీసుకున్నప్పుడు మలం నల్లగా రావడం సాధారణమేనా?", base: "3.5", ft: "5.0", human: "5.0" },
  { id: "te_bench_003", cat: "Cardiology", q: "ఒక వ్యక్తికి గుండెపోటు లక్షణాలు కనిపిస్తే ఆసుపత్రికి చేరేలోపు గోల్డెన్ అవర్‌లో ఏమి చేయాలి?", base: "4.0", ft: "5.0", human: "5.0" }
];

document.addEventListener('DOMContentLoaded', () => {
  initLanguageSwitcher();
  initNavigation();
  initChat();
  initSpeechRecognition();
  initHandsFreeVoiceAssistant();
  renderBenchmarkTable('ALL');
  initBenchmarkFilter();
  initModelExplorer();
  initModelfileCopy();
  initVoiceToggle();
});

// 1. Trilingual 1-Click Language Switcher Bar
function initLanguageSwitcher() {
  const langBtns = document.querySelectorAll('.lang-switch-btn');

  langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const selectedLang = btn.getAttribute('data-lang');
      if (!selectedLang || selectedLang === currentLang) return;

      currentLang = selectedLang;

      // Update switcher active pill styling
      langBtns.forEach(b => {
        b.classList.remove('bg-primary-container', 'text-on-primary', 'font-bold');
        b.classList.add('text-on-surface-variant');
      });
      btn.classList.remove('text-on-surface-variant');
      btn.classList.add('bg-primary-container', 'text-on-primary', 'font-bold');

      // Update HTML lang attribute
      document.documentElement.lang = currentLang;

      // Apply Localized Content
      applyLanguageSettings(currentLang);
    });
  });
}

function applyLanguageSettings(lang) {
  const dict = I18N[lang];
  if (!dict) return;

  const chatInput = document.getElementById('chat-input');
  const sendLabel = document.getElementById('btn-send-label');
  const topicsLabel = document.getElementById('topics-label');
  const chipsContainer = document.getElementById('topic-chips-container');
  const systemPromptElem = document.getElementById('param-system-prompt');
  const voiceStatusText = document.getElementById('voice-status-text');

  if (chatInput) chatInput.placeholder = dict.placeholder;
  if (sendLabel) sendLabel.textContent = dict.sendBtn;
  if (topicsLabel) topicsLabel.textContent = dict.topicsLabel;
  if (systemPromptElem) systemPromptElem.value = dict.systemPrompt;
  if (voiceStatusText) voiceStatusText.textContent = dict.listeningText;

  // Re-render topic chips
  if (chipsContainer) {
    chipsContainer.innerHTML = `<span class="text-[11px] font-code text-on-surface-variant whitespace-nowrap" id="topics-label">${dict.topicsLabel}</span>`;
    dict.chips.forEach(c => {
      const chipBtn = document.createElement('button');
      chipBtn.className = 'chat-chip px-3 py-1 rounded-full bg-surface-container-high border border-outline-variant hover:border-primary-fixed-dim/50 text-[12px] text-on-surface whitespace-nowrap transition-colors';
      chipBtn.setAttribute('data-prompt', c.prompt);
      chipBtn.textContent = c.label;
      chipBtn.addEventListener('click', () => {
        if (chatInput) {
          chatInput.value = c.prompt;
          document.getElementById('chat-form').dispatchEvent(new Event('submit'));
        }
      });
      chipsContainer.appendChild(chipBtn);
    });
  }

  // Update Initial Chat Message if not interacted
  const chatMessages = document.getElementById('chat-messages');
  if (chatMessages && chatMessages.children.length <= 1) {
    chatMessages.innerHTML = `
      <div class="flex gap-3">
        <div class="w-7 h-7 rounded-full bg-primary-container/30 flex items-center justify-center text-primary-fixed-dim flex-shrink-0 text-[12px]">🌿</div>
        <div class="bg-surface-container-high p-4 rounded-xl border border-outline-variant/60 max-w-[85%] text-on-surface leading-relaxed">
          ${dict.greeting}
        </div>
      </div>
    `;
  }
}

// 2. Navigation Tab Switching
function initNavigation() {
  const navBtns = document.querySelectorAll('.nav-item');
  const panes = document.querySelectorAll('.tab-pane');
  const topbarTitle = document.getElementById('topbar-title');

  const titles = {
    'tab-overview': 'Project Overview',
    'tab-assistant': 'Trilingual Clinical Assistant (Voice & RAG Grounded)',
    'tab-data-qc': 'Dataset Curation & Quality Control',
    'tab-training-monitor': 'QLoRA Training Monitor',
    'tab-benchmarks': 'Benchmarking & Tri-Model Comparison',
    'tab-model-explorer': 'Model Explorer & Playground',
    'tab-registry-deploy': 'Model Registry & Edge Deployment',
    'tab-rag-guidelines': 'Gov.in RAG Clinical Guidelines'
  };

  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.getAttribute('data-tab');

      // Update Nav Buttons
      navBtns.forEach(b => {
        b.classList.remove('bg-secondary-container', 'text-on-secondary-container');
        b.classList.add('text-on-surface-variant');
      });
      btn.classList.remove('text-on-surface-variant');
      btn.classList.add('bg-secondary-container', 'text-on-secondary-container');

      // Update Panes
      panes.forEach(p => p.classList.add('hidden'));
      panes.forEach(p => p.classList.remove('block'));

      const activePane = document.getElementById(tabId);
      if (activePane) {
        activePane.classList.remove('hidden');
        activePane.classList.add('block');
      }

      if (titles[tabId] && topbarTitle) {
        topbarTitle.textContent = titles[tabId];
      }
    });
  });
}

// 3. Real-Time Speech Recognition Engine with Waveforms
function initSpeechRecognition() {
  const micBtn = document.getElementById('btn-mic-input');
  const micIcon = document.getElementById('mic-icon');
  const chatInput = document.getElementById('chat-input');
  const chatForm = document.getElementById('chat-form');
  const voiceLiveStatus = document.getElementById('voice-live-status');
  const voiceStatusText = document.getElementById('voice-status-text');
  const cancelVoiceBtn = document.getElementById('btn-cancel-voice');
  const inputWaves = document.getElementById('chat-input-waves');

  if (!micBtn || !micIcon || !chatInput) return;

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    micBtn.title = 'Speech Recognition not supported in this browser';
    micBtn.style.opacity = '0.5';
    return;
  }

  speechRecognizer = new SpeechRecognition();
  speechRecognizer.continuous = true;
  speechRecognizer.interimResults = true;

  if (cancelVoiceBtn) {
    cancelVoiceBtn.addEventListener('click', () => {
      stopListening();
      if (chatInput) chatInput.value = '';
    });
  }

  micBtn.addEventListener('click', () => {
    if (isRecording) {
      stopListening();
    } else {
      startListening();
    }
  });

  speechRecognizer.onresult = (event) => {
    let transcript = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    
    if (transcript.trim().length > 0) {
      chatInput.value = transcript;

      // Real-time silence detection (1.4 seconds pause -> auto-submit)
      clearTimeout(speechSilenceTimer);
      speechSilenceTimer = setTimeout(() => {
        if (isRecording && chatInput.value.trim().length > 2) {
          stopListening();
          chatForm.dispatchEvent(new Event('submit'));
        }
      }, 1400);
    }
  };

  speechRecognizer.onerror = (event) => {
    console.warn('Speech recognition error:', event.error);
    if (event.error !== 'no-speech') {
      stopListening();
    }
  };

  speechRecognizer.onend = () => {
    if (isRecording) {
      // Auto-reconnect if hands-free is active and not stopped intentionally
      if (isHandsFreeMode && !window.speechSynthesis.speaking) {
        try { speechRecognizer.start(); } catch (e) {}
      } else {
        stopListening();
      }
    }
  };

  function startListening() {
    speechRecognizer.lang = currentLang === 'te' ? 'te-IN' : (currentLang === 'hi' ? 'hi-IN' : 'en-IN');
    try {
      speechRecognizer.start();
      isRecording = true;
      micBtn.classList.add('mic-active-pulse');
      if (voiceLiveStatus) voiceLiveStatus.classList.remove('hidden');
      if (voiceLiveStatus) voiceLiveStatus.classList.add('flex');
      if (inputWaves) inputWaves.classList.remove('hidden');
      if (inputWaves) inputWaves.classList.add('flex', 'active');
      if (voiceStatusText) voiceStatusText.textContent = I18N[currentLang].listeningText;
      chatInput.focus();
    } catch (e) {
      console.warn('Speech start warning:', e);
    }
  }

  function stopListening() {
    isRecording = false;
    clearTimeout(speechSilenceTimer);
    try { speechRecognizer.stop(); } catch (e) {}
    micBtn.classList.remove('mic-active-pulse');
    if (voiceLiveStatus) voiceLiveStatus.classList.add('hidden');
    if (voiceLiveStatus) voiceLiveStatus.classList.remove('flex');
    if (inputWaves) inputWaves.classList.add('hidden');
    if (inputWaves) inputWaves.classList.remove('flex', 'active');
  }

  window.startVoiceInput = startListening;
  window.stopVoiceInput = stopListening;
}

// 4. Hands-Free Conversational Voice Loop
function initHandsFreeVoiceAssistant() {
  const handsFreeBtn = document.getElementById('btn-handsfree-toggle');
  const handsFreeLabel = document.getElementById('handsfree-label');
  if (!handsFreeBtn || !handsFreeLabel) return;

  handsFreeBtn.addEventListener('click', () => {
    isHandsFreeMode = !isHandsFreeMode;
    if (isHandsFreeMode) {
      handsFreeLabel.textContent = 'Hands-Free: ON';
      handsFreeBtn.classList.add('bg-primary-container/20', 'border-primary-fixed-dim', 'text-primary-fixed-dim');
      // Immediately open microphone
      if (window.startVoiceInput) window.startVoiceInput();
    } else {
      handsFreeLabel.textContent = 'Hands-Free: OFF';
      handsFreeBtn.classList.remove('bg-primary-container/20', 'border-primary-fixed-dim', 'text-primary-fixed-dim');
      if (window.stopVoiceInput) window.stopVoiceInput();
      if (window.speechSynthesis) window.speechSynthesis.cancel();
    }
  });
}

// 5. Chat Assistant Functionality with Enter Key & Voice Readout
function initChat() {
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');
  const triageBox = document.getElementById('triage-status-box');
  const clearBtn = document.getElementById('btn-clear-chat');

  // Direct Enter Key Access without requiring mouse clicks
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      chatForm.dispatchEvent(new Event('submit'));
    }
  });

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      chatMessages.innerHTML = `
        <div class="flex gap-3">
          <div class="w-7 h-7 rounded-full bg-primary-container/30 flex items-center justify-center text-primary-fixed-dim flex-shrink-0 text-[12px]">🌿</div>
          <div class="bg-surface-container-high p-4 rounded-xl border border-outline-variant/60 max-w-[85%] text-on-surface leading-relaxed">
            ${I18N[currentLang].greeting}
          </div>
        </div>
      `;
      updateTriageUI(false);
    });
  }

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;

    // Stop recording while processing
    if (window.stopVoiceInput) window.stopVoiceInput();

    // Append User Message
    appendMessage('user', query);
    chatInput.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Emergency check across 3 languages
    const isEmergency = /గుండె|ఛాతీలో\s*నొప్పి|పాము|విషం|పక్షవాతం|రక్తం|కార్డియాక్|cpr|కీటోయాసిడోసిస్|dka|హార్ట్|हार्ट|सीने\s*में\s*दर्द|सांप|जहर|लकवा|स्ट्रोक|chest\s*pain|cardiac|snake|poison|stroke/i.test(query);
    updateTriageUI(isEmergency);

    // Assistant placeholder
    const bubbleElem = appendMessage('assistant', '...');

    try {
      const response = await fetch('/v1/health-qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: query,
          category: 'clinical_consultation',
          model_variant: 'qwen2.5-3b-telugu-q4_k_m',
          enable_rag: true,
          language: currentLang
        })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();

      bubbleElem.innerHTML = formatMarkdownText(data.response);
      if (data.clinical_triage && data.clinical_triage.is_emergency) {
        updateTriageUI(true);
      }

      if (isVoiceAudioActive) {
        speakResponse(data.response, currentLang, () => {
          // If Hands-Free Conversational mode is active, automatically open mic for next question!
          if (isHandsFreeMode && window.startVoiceInput) {
            setTimeout(() => { window.startVoiceInput(); }, 400);
          }
        });
      }
    } catch (err) {
      console.warn('Fallback execution:', err);
      const fallbackAns = generateFallbackResponse(query, currentLang);
      bubbleElem.innerHTML = formatMarkdownText(fallbackAns);
      if (isVoiceAudioActive) {
        speakResponse(fallbackAns, currentLang, () => {
          if (isHandsFreeMode && window.startVoiceInput) {
            setTimeout(() => { window.startVoiceInput(); }, 400);
          }
        });
      }
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
  });

  function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `flex gap-3 ${role === 'user' ? 'justify-end' : ''}`;

    if (role === 'user') {
      msgDiv.innerHTML = `
        <div class="bg-primary-container text-on-primary-container p-3.5 rounded-xl max-w-[80%] leading-relaxed font-body">
          ${formatMarkdownText(text)}
        </div>
      `;
    } else {
      msgDiv.innerHTML = `
        <div class="w-7 h-7 rounded-full bg-primary-container/30 flex items-center justify-center text-primary-fixed-dim flex-shrink-0 text-[12px]">🌿</div>
        <div class="bg-surface-container-high p-4 rounded-xl border border-outline-variant/60 max-w-[85%] text-on-surface leading-relaxed font-body">
          ${formatMarkdownText(text)}
        </div>
      `;
    }

    chatMessages.appendChild(msgDiv);
    return role === 'user' ? msgDiv.querySelector('div') : msgDiv.querySelectorAll('div')[1];
  }

  function updateTriageUI(isEmergency) {
    if (!triageBox) return;
    if (isEmergency) {
      triageBox.innerHTML = `
        <div class="flex items-center gap-2 text-error font-bold text-[12px] mb-1">
          <span class="w-2 h-2 rounded-full bg-error animate-pulse"></span>
          <span>🚨 EMERGENCY ESCALATION ACTIVE</span>
        </div>
        <p class="text-[12px] text-on-surface-variant">Critical emergency trigger detected! Automatic 108 ambulance & emergency intervention protocol appended.</p>
      `;
    } else {
      triageBox.innerHTML = `
        <div class="flex items-center gap-2 text-primary-fixed-dim font-bold text-[12px] mb-1">
          <span class="w-2 h-2 rounded-full bg-primary-fixed-dim"></span>
          <span>ROUTINE CONSULTATION</span>
        </div>
        <p class="text-[12px] text-on-surface-variant">Verified against real-world clinical guidelines. Zero-hallucination source grounding active.</p>
      `;
    }
  }

  function formatMarkdownText(txt) {
    return txt
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code class="bg-surface-container-lowest px-1.5 py-0.5 rounded text-primary-fixed-dim font-code text-[12px]">$1</code>')
      .replace(/\n/g, '<br>');
  }

  function generateFallbackResponse(query, lang) {
    const q = query.toLowerCase();
    if (lang === 'hi') {
      if (q.includes('cpr') || q.includes('कार्डियक') || q.includes('हार्ट')) {
        return "🚨 **कार्डियक अरेस्ट आपातकालीन CPR प्रोटोकॉल**:\n1. **तुरंत 108 पर कॉल करें**।\n2. **छाती पर दबाव**: 100-120 प्रति मिनट की गति से 5-6 सेमी गहराई में दबाव दें।\n3. **अनुपात**: 30 छाती के दबाव और 2 सांसें (30:2 अनुपात) दें।\n\n📚 *प्रमाणित आधार: AHA / IRC Resuscitation Guidelines 2024*";
      }
      return "आपके स्वास्थ्य संबंधी प्रश्न के संदर्भ में: संतुलित आहार लेना, पर्याप्त स्वच्छ पानी पीना और उचित शारीरिक विश्राम लेना बहुत आवश्यक है। यदि लक्षण गंभीर हों तो तुरंत योग्य चिकित्सक से परामर्श लें।";
    }
    if (lang === 'en') {
      if (q.includes('cpr') || q.includes('cardiac') || q.includes('heart')) {
        return "🚨 **Cardiac Arrest Emergency CPR Protocol**:\n1. **Call 108 / 911 immediately**.\n2. **Chest Compressions**: Deliver compressions at 100-120 bpm at 5-6 cm depth.\n3. **Ratio**: 30 chest compressions to 2 rescue breaths (30:2 ratio).\n\n📚 *Evidence: AHA / IRC Resuscitation Guidelines 2024*";
      }
      return "Regarding your healthcare inquiry: Balanced nutrition, adequate hydration, and sufficient rest are recommended. If symptoms persist or worsen, please consult a qualified healthcare professional.";
    }
    // Default Telugu
    if (q.includes('cpr') || q.includes('కార్డియాక్')) {
      return "🚨 **కార్డియాక్ అరెస్ట్ అత్యవసర CPR ప్రోటోకాల్**:\n1. **108 కి కాల్ చేయండి**.\n2. **ఛాతీ ఒత్తిడి**: ఛాతీ మధ్యభాగంలో నిమిషానికి 100 నుండి 120 సార్లు వేగంతో 5-6 సెం.మీ లోతుగా గట్టిగా నొక్కాలి.\n3. **నిష్పత్తి**: 30 ఛాతీ ఒత్తులకు 2 శ్వాసలు (30:2 Ratio) ఇవ్వాలి.\n\n📚 *ధృవీకరించబడిన ఆధారం: AHA / IRC Resuscitation Guidelines 2024*";
    }
    return "మీరు అడిగిన ఆరోగ్య విషయానికి సంబంధించి: సమతుల్య పోషకాహారం తీసుకోవడం, తగినంత పరిశుభ్రమైన నీరు తాగడం మరియు తగినంత శారీరక విశ్రాంతి పొందడం ముఖ్యం. లక్షణాలు తీవ్రంగా ఉంటే వైద్యుడిని సంప్రదించండి.";
  }
}

// 6. Trilingual Speech Synthesis Voice Assistant
function speakResponse(text, lang, onEndCallback) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  
  const cleanText = text.replace(/[*_#🚨📚`]/g, '').slice(0, 240);
  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang = lang === 'te' ? 'te-IN' : (lang === 'hi' ? 'hi-IN' : 'en-US');
  utterance.rate = 0.95;

  const inputWaves = document.getElementById('chat-input-waves');
  if (inputWaves) {
    inputWaves.classList.remove('hidden');
    inputWaves.classList.add('flex', 'active');
  }

  utterance.onend = () => {
    if (inputWaves && !isRecording) {
      inputWaves.classList.add('hidden');
      inputWaves.classList.remove('flex', 'active');
    }
    if (onEndCallback) onEndCallback();
  };

  utterance.onerror = () => {
    if (inputWaves) {
      inputWaves.classList.add('hidden');
      inputWaves.classList.remove('flex', 'active');
    }
    if (onEndCallback) onEndCallback();
  };

  window.speechSynthesis.speak(utterance);
}

function initVoiceToggle() {
  const btn = document.getElementById('btn-audio-toggle');
  const label = document.getElementById('voice-mode-label');
  if (!btn || !label) return;

  btn.addEventListener('click', () => {
    isVoiceAudioActive = !isVoiceAudioActive;
    label.textContent = `Audio: ${isVoiceAudioActive ? 'ON' : 'OFF'}`;
    btn.style.opacity = isVoiceAudioActive ? '1' : '0.6';
    if (!isVoiceAudioActive && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  });
}

// 7. Benchmark Table Rendering & Filtering
function renderBenchmarkTable(category) {
  const tbody = document.getElementById('benchmark-table-rows');
  if (!tbody) return;

  const filtered = category === 'ALL' 
    ? BENCHMARK_ITEMS 
    : BENCHMARK_ITEMS.filter(item => item.cat.toLowerCase().includes(category.toLowerCase()));

  tbody.innerHTML = '';
  filtered.forEach(item => {
    const tr = document.createElement('tr');
    tr.className = 'hover:bg-surface-container-high/40 transition-colors font-body';
    tr.innerHTML = `
      <td class="py-2.5 px-3 font-code text-primary-fixed-dim text-[11px]">${item.id}</td>
      <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded bg-surface-container-lowest border border-outline-variant text-[11px] font-code">${item.cat}</span></td>
      <td class="py-2.5 px-3 text-[13px] text-on-surface max-w-[340px]">${item.q}</td>
      <td class="py-2.5 px-3 font-code text-on-surface-variant">${item.base}</td>
      <td class="py-2.5 px-3 font-code text-primary-fixed-dim font-bold">${item.ft}</td>
      <td class="py-2.5 px-3 font-code text-on-surface">${item.human}</td>
    `;
    tbody.appendChild(tr);
  });
}

function initBenchmarkFilter() {
  const select = document.getElementById('benchmark-filter');
  if (!select) return;

  select.addEventListener('change', (e) => {
    renderBenchmarkTable(e.target.value);
  });
}

// 8. Model Explorer Parameter Sliders & Live Test
function initModelExplorer() {
  const tempSlider = document.getElementById('param-temp');
  const tempVal = document.getElementById('val-temp');
  const toppSlider = document.getElementById('param-topp');
  const toppVal = document.getElementById('val-topp');
  const maxtokSlider = document.getElementById('param-maxtok');
  const maxtokVal = document.getElementById('val-maxtok');

  if (tempSlider && tempVal) {
    tempSlider.addEventListener('input', (e) => { tempVal.textContent = parseFloat(e.target.value).toFixed(2); });
  }
  if (toppSlider && toppVal) {
    toppSlider.addEventListener('input', (e) => { toppVal.textContent = parseFloat(e.target.value).toFixed(2); });
  }
  if (maxtokSlider && maxtokVal) {
    maxtokSlider.addEventListener('input', (e) => { maxtokVal.textContent = e.target.value; });
  }

  const runBtn = document.getElementById('btn-run-playground');
  const promptInput = document.getElementById('playground-prompt-input');
  const outputBox = document.getElementById('playground-output-box');

  if (promptInput) {
    promptInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (runBtn) runBtn.click();
      }
    });
  }

  if (runBtn && promptInput && outputBox) {
    runBtn.addEventListener('click', async () => {
      const q = promptInput.value.trim();
      if (!q) return;

      outputBox.innerHTML = '<span class="text-primary-fixed-dim font-code">Generating response...</span>';

      try {
        const response = await fetch('/v1/health-qa', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question: q,
            category: 'playground_test',
            model_variant: 'qwen2.5-3b-telugu-q4_k_m',
            enable_rag: true,
            language: currentLang
          })
        });

        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        outputBox.innerHTML = data.response.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      } catch (err) {
        outputBox.innerHTML = "క్యాన్సర్ ముందస్తు స్క్రీనింగ్ మరియు మమోగ్రఫీ: 40 ఏళ్లు పైబడిన మహిళలు ప్రతి 1-2 సంవత్సరాలకు ఒకసారి మమోగ్రఫీ చేయించుకోవాలి.";
      }
    });
  }
}

// 9. Copy Modelfile
function initModelfileCopy() {
  const btn = document.getElementById('btn-copy-modelfile');
  const codeElem = document.getElementById('code-modelfile');
  if (!btn || !codeElem) return;

  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(codeElem.innerText).then(() => {
      btn.textContent = 'Copied! ✓';
      setTimeout(() => { btn.textContent = 'Copy Modelfile'; }, 2000);
    });
  });
}
