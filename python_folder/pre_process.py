import pandas as pd
import spacy
import re
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load SpaCy for sentence tokenization
nlp = spacy.load("en_core_web_sm")  

# Load NER model
model_name = "Amitava25/legal_ai_India_ner_results"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

# Define punishment-related keywords
punishment_keywords = {"fine", "imprisonment", "jail", "custody", "penalty", "bail", "sentence", "conviction"}

# Function to clean text
def clean_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Function to check if a sentence appears in the summary
def sentence_in_summary(sentence, summary):
    return sentence in summary

# Function to check if a sentence contains NER entities or punishment keywords
def contains_entities_or_punishment(sentence):
    ner_results = ner_pipeline(sentence)
    has_ner_entity = len(ner_results) > 0  # Check if any entity is found

    words = set(sentence.lower().split())  # Convert sentence to lowercase set of words
    has_punishment_word = any(word in punishment_keywords for word in words)

    return has_ner_entity or has_punishment_word

# Function to process each document
def process_document(text, summary):
    doc = nlp(clean_text(text))

    labeled_data = []
    for sent in doc.sents:
        sentence = sent.text.strip()
        label = 0  # Default label

        if sentence_in_summary(sentence, summary) or contains_entities_or_punishment(sentence):
            label = 1

        labeled_data.append({"text": sentence, "label": label})
    
    return labeled_data

# Load dataset (Assuming CSV with columns: 'text' and 'summary')
df = pd.read_csv("/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/test.csv")  
max_rows = 5
# Process all rows
dataset = []
for index, row in df.iterrows():
    print(f"Processing row {index}..")  # Print progress
    dataset.extend(process_document(row["Text"], row["Summary"]))
    if index >= max_rows:  # Stop after 1,000 rows
        print("Stopping after processing 1,000 rows.")
        break
# Convert to DataFrame
processed_df = pd.DataFrame(dataset)

# Save as CSV
processed_df.to_csv("/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/test_dataset.csv", index=False)

print("Dataset successfully processed and saved as 'processed_ner_dataset.csv'")
