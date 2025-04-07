import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import nltk
from nltk.tokenize import sent_tokenize
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load models
model_path = "/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/bert_caselawbert"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

grammar_model_name = "vennify/t5-base-grammar-correction"
grammar_tokenizer = T5Tokenizer.from_pretrained(grammar_model_name, legacy=False)
grammar_model = T5ForConditionalGeneration.from_pretrained(grammar_model_name)

model.eval()

# Label Mapping
label_map = {"FACTS": 0, "ARGUMENT": 1, "ANALYSIS": 2, "JUDGMENT": 3, "STATUTE": 4, "O": 5}
id_to_label = {v: k for k, v in label_map.items()} 

# Add this function near the top
def contains_legal_terms(text):
    legal_keywords = [
        "court", "judge", "plaintiff", "defendant", "judgment", "order",
        "bail", "ipc", "section", "act", "tribunal", "petition", "respondent",
        "writ", "appeal", "bench", "hearing", "case law", "legal"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in legal_keywords)


# Custom Sentence Tokenization
def custom_sent_tokenize(text):
    # Preserve formatting for statutes, legal abbreviations, and honorifics
    text = re.sub(r"\bNo\.\s*(\d+)", r"Number_\1", text)  
    text = re.sub(r"\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b", r"DATE_\1_\2_\3", text)  
    text = re.sub(r"(^|\s)(\d+\.\s*){2,}", " ", text)  
    text = re.sub(r"(Section\s\d+(\s*\(\w+\))?)", r"§\1§", text)  
    text = re.sub(r"\b(N\.I\.|I\.P\.C\.|C\.R\.P\.C\.|Act\.)", r"§\1§", text)  
    text = re.sub(r"\b(Dr|Mr|Mrs|Ms|Prof|Sr|Smt|Jr|Col|Gen|Lt|Maj|Hon|Rev|St)\.", r"§\1§", text)  

    # Tokenization
    sentences = sent_tokenize(text)

    # Restore original format
    sentences = [s.replace("§", "").replace("Number_", "No. ").replace("DATE_", "") for s in sentences]  
    return sentences

# Function to extract Rs. values
def extract_money(text):
    pattern = r"Rs\.?\s*\d+(?:,\d{3})*(?:\.\d+)?" 
    return re.findall(pattern, text)

# Function to correct grammar and reduce redundancy
def correct_grammar(text):
    input_text = "grammar: " + text  # Use "grammar" prompt instead of "rephrase"
    input_ids = grammar_tokenizer(input_text, return_tensors="pt").input_ids

    outputs = grammar_model.generate(input_ids, max_length=512)
    corrected_text = grammar_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return corrected_text


# Function to summarize text and remove redundancy
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

        if label_name == "STATUTE":
            if not re.search(r"\b(Section|Article|Act)\s+\d+", sentence):
                continue

        if label_name != "O":
            corrected_sentence = correct_grammar(sentence)
            structured_summary[label_name].append(corrected_sentence)

    # 💡 NEW STRONGER HEURISTIC:
    total_meaningful = sum(len(structured_summary[k]) for k in structured_summary if k not in ["O"])
    if total_meaningful < 3:  # Change 3 to a number that works well with your dataset
        return "⚠️ Not a legal document."

    # Format final output
    summary_text = ""
    for label, sentences in structured_summary.items():
        if sentences:
            summary_text += f"➜ {label}:\n" + " ".join(sentences) + "\n\n"

    return summary_text.strip()

