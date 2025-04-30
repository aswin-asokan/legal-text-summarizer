import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from nltk.tokenize import sent_tokenize
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load classification model
# Change model path before running
model_path = "/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/bert_caselawbert"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

# Load paraphraser model
paraphrase_model_name = "humarin/chatgpt_paraphraser_on_T5_base"
paraphrase_tokenizer = T5Tokenizer.from_pretrained(paraphrase_model_name)
paraphrase_model = T5ForConditionalGeneration.from_pretrained(paraphrase_model_name)

# Label Mapping
label_map = {"FACTS": 0, "ARGUMENT": 1, "ANALYSIS": 2, "JUDGMENT": 3, "STATUTE": 4, "O": 5}
id_to_label = {v: k for k, v in label_map.items()}

def contains_legal_terms(text):
    legal_keywords = [
        "court", "judge", "plaintiff", "defendant", "judgment", "order",
        "bail", "ipc", "section", "act", "tribunal", "petition", "respondent",
        "writ", "appeal", "bench", "hearing", "case law", "legal"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in legal_keywords)

def custom_sent_tokenize(text):
    text = re.sub(r"\bNo\.\s*(\d+)", r"§No. \1§", text)
    text = re.sub(r"\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b", r"DATE_\1_\2_\3", text)
    text = re.sub(r"(^|\s)(\d+\.\s*){2,}", " ", text)
    text = re.sub(r"(Section\s\d+(\s*\(\w+\))?)", r"§\1§", text)
    text = re.sub(r"\b(N\.I\.|I\.P\.C\.|C\.R\.P\.C\.|Act\.)", r"§\1§", text)
    text = re.sub(r"\b(Dr|Mr|Mrs|Ms|Prof|Sr|Smt|Jr|Col|Gen|Lt|Maj|Hon|Rev|St)\.", r"§\1§", text)

    sentences = sent_tokenize(text)
    sentences = [s.replace("§", "").replace("Number_", "No. ").replace("DATE_", "") for s in sentences]
    return sentences

def extract_money(text):
    pattern = r"Rs\.?\s*\d+(?:,\d{3})*(?:\.\d+)?"
    return re.findall(pattern, text)

def rephrase_section_sentence_by_sentence(text):
    sentences = sent_tokenize(text)
    rephrased_sentences = []

    for sentence in sentences:
        prompt = f"paraphrase: {sentence}"
        input_ids = paraphrase_tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=128).input_ids
        output_ids = paraphrase_model.generate(input_ids, max_length=128, num_beams=4, early_stopping=True)
        rephrased = paraphrase_tokenizer.decode(output_ids[0], skip_special_tokens=True)
        rephrased_sentences.append(rephrased)

    return " ".join(rephrased_sentences)


def summarize_text(text):
    if not contains_legal_terms(text):
        return "⚠️ Not a legal document."

    sentences = custom_sent_tokenize(text)
    structured_summary = {label: [] for label in label_map.keys()}

    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)

        predicted_label = torch.argmax(outputs.logits, dim=1).item()
        label_name = id_to_label.get(predicted_label, "O")

        if label_name != "O":
            structured_summary[label_name].append(sentence)

    total_meaningful = sum(len(structured_summary[k]) for k in structured_summary if k not in ["O"])
    if total_meaningful < 3:
        return "⚠️ Not a legal document."

    summary_text = ""
    for label, sentence_list in structured_summary.items():
        if sentence_list:
            combined_section = " ".join(sentence_list)
            try:
                rephrased = rephrase_section_sentence_by_sentence(combined_section)
            except Exception:
                rephrased = combined_section  # fallback
            summary_text += f"➜ {label}:\n{rephrased}\n\n"


    return summary_text.strip()
