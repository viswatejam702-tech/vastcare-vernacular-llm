"""
Chat template formatters and conversation builders for Telugu Vernacular models.
"""

from typing import List, Dict, Optional, Any

DEFAULT_TELUGU_SYSTEM_PROMPT = (
    "మీరు వాస్ట్‌కేర్ (Vastcare) ఆధ్వర్యంలో పనిచేసే నిపుణులైన తెలుగు ఆరోగ్య మరియు సాధారణ AI సహాయకులు. "
    "వినియోగదారుల ప్రశ్నలకు స్పష్టమైన, ప్రామాణికమైన మరియు సులభంగా అర్థమయ్యే తెలుగులో మాత్రమే సమాధానాలు ఇవ్వండి."
)

CLINICAL_DISCLAIMER_TELUGU = (
    "\n\n*గమనిక*: ఈ సమాచారం కేవలం ప్రాథమిక అవగాహన మరియు ఆరోగ్య విద్యా ప్రయోజనాల కొరకు మాత్రమే. "
    "తీవ్రమైన అత్యవసర పరిస్థితుల్లో తక్షణమే సమీపంలోని అర్హత కలిగిన వైద్యుడిని లేదా 108 అత్యవసర సేవలను సంప్రదించండి."
)


def format_chatml_messages(
    messages: List[Dict[str, str]],
    system_prompt: Optional[str] = None
) -> str:
    """
    Formats a list of messages into Qwen/ChatML format:
    <|im_start|>system\n...<|im_end|>\n<|im_start|>user\n...<|im_end|>\n<|im_start|>assistant\n...<|im_end|>
    """
    formatted = []
    
    # Check if system message exists
    has_system = any(m.get("role") == "system" for m in messages)
    if not has_system:
        sys_text = system_prompt or DEFAULT_TELUGU_SYSTEM_PROMPT
        formatted.append(f"<|im_start|>system\n{sys_text}<|im_end|>")
    
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        formatted.append(f"<|im_start|>{role}\n{content}<|im_end|>")
        
    return "\n".join(formatted)


def format_instruction_sample(
    instruction: str,
    output: str,
    input_text: str = "",
    system_prompt: Optional[str] = None
) -> Dict[str, Any]:
    """
    Converts a single instruction sample into ChatML message structure.
    """
    sys_text = system_prompt or DEFAULT_TELUGU_SYSTEM_PROMPT
    user_content = instruction
    if input_text and input_text.strip():
        user_content = f"{instruction}\n\n[అదనపు వివరాలు / సందర్భం]: {input_text}"

    messages = [
        {"role": "system", "content": sys_text},
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": output}
    ]

    return {
        "messages": messages,
        "text": format_chatml_messages(messages, sys_text)
    }
