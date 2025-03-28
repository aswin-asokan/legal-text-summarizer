import os
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
import re
nltk.download("punkt")  

CATEGORY_FOLDERS = {
    "FACTS": "/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/facts",
    "ARGUMENT": "/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/argument",
    "ANALYSIS": "/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/analysis",
    "JUDGMENT": "/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/judgement",
    "STATUTE": "/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/statute",
}
import os

JUDGMENT_PATH = "/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/judgements"
judgment_files = os.listdir(JUDGMENT_PATH)


dataset = []
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  
    text = text.strip()  
    return text

for filename in judgment_files:
    case_id = filename.replace(".txt", "")

    with open(os.path.join(JUDGMENT_PATH, filename), "r", encoding="utf-8", errors="ignore") as f:
        full_text = f.read()

    sentences = sent_tokenize(full_text)

    for sentence in sentences:
        sentence = clean_text(sentence)  
        label = "O"  

        for category, folder in CATEGORY_FOLDERS.items():
            file_path = os.path.join(folder, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    category_text = clean_text(f.read()) 
                if sentence in category_text:
                    label = category
                    break

        dataset.append({"case_id": case_id, "sentence": sentence, "label": label})

df = pd.DataFrame(dataset)
df.to_csv("/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/structured_data.csv", index=False)

df = pd.read_csv("/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/structured_data.csv")

df_O = df[df["label"] == "O"].sample(n=2000, random_state=42)


df_balanced = df[df["label"] != "O"]
oversampled_dfs = [df_balanced]  

for label in ["FACTS", "JUDGMENT", "ARGUMENT", "STATUTE", "ANALYSIS"]:  
    oversampled_dfs.append(df[df["label"] == label].sample(n=800, replace=True))

df_final = pd.concat([df_O] + oversampled_dfs, ignore_index=True)

df_final.to_csv("/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/balanced_data.csv", index=False)

print(df_final["label"].value_counts()) 
print("Preprocessed dataset saved as structured_data.csv!")
