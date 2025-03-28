import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import evaluate
from sklearn.model_selection import train_test_split
import numpy as np

# Define label mapping
label_map = {"FACTS": 0, "ARGUMENT": 1, "ANALYSIS": 2, "JUDGMENT": 3, "STATUTE": 4, "O": 5}
id_to_label = {v: k for k, v in label_map.items()} 

df = pd.read_csv("/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/balanced_data.csv")

# Convert text labels to numerical IDs
df["label"] = df["label"].map(label_map)

# Split dataset
train_texts, val_texts, train_labels, val_labels = train_test_split(df["sentence"].tolist(),
                                                                    df["label"].tolist(),
                                                                    test_size=0.1,
                                                                    random_state=42)

tokenizer = AutoTokenizer.from_pretrained("law-ai/InCaseLawBERT")

# Tokenize data
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)

# Create dataset class
class LegalDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

train_dataset = LegalDataset(train_encodings, train_labels)
val_dataset = LegalDataset(val_encodings, val_labels)

num_labels = len(label_map)  
model = AutoModelForSequenceClassification.from_pretrained("law-ai/InCaseLawBERT", num_labels=len(label_map))

accuracy = evaluate.load("accuracy")
precision = evaluate.load("precision")
recall = evaluate.load("recall")
f1 = evaluate.load("f1")

# Define compute_metrics function
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy_results = accuracy.compute(predictions=predictions, references=labels)
    precision_results = precision.compute(predictions=predictions, references=labels, average="weighted", zero_division=0)
    recall_results = recall.compute(predictions=predictions, references=labels, average="weighted")
    f1_results = f1.compute(predictions=predictions, references=labels, average="weighted")

    return {
        "accuracy": accuracy_results["accuracy"],
        "precision": precision_results["precision"],
        "recall": recall_results["recall"],
        "f1": f1_results["f1"],
    }

training_args = TrainingArguments(
    output_dir="./bert_caselawbert",
    eval_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    gradient_accumulation_steps=1,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=50,
    load_best_model_at_end=True,
    metric_for_best_model="f1", 
    greater_is_better=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()


model.save_pretrained("./bert_caselawbert")
tokenizer.save_pretrained("./bert_caselawbert")
