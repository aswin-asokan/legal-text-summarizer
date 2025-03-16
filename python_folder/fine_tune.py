import torch
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
import evaluate
import numpy as np


# Load Pretrained Model & Tokenizer (InLegalBERT)
model_name = "law-ai/InLegalBERT"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Load Dataset (CSV with 'text' and 'label' columns)
df = pd.read_csv("/home/aswin/Documents/GitHub/legal-text-summarizer/python_folder/datasets/processed_dataset.csv")  # Change path accordingly

# Convert to Hugging Face Dataset
dataset = Dataset.from_pandas(df)

# Tokenization Function
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

# Tokenize the Dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Split Dataset (90% Train, 10% Validation)
split_dataset = tokenized_dataset.train_test_split(test_size=0.1)
train_dataset = split_dataset["train"]
eval_dataset = split_dataset["test"]

# Load BERTScore Metric
bertscore = evaluate.load("bertscore")

# Define BERTScore Evaluation Function
def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    # Convert logits to predicted token IDs
    predictions = np.argmax(predictions, axis=1)  # Get highest probability class

    # Convert labels to token IDs (if needed)
    labels = labels.astype(int)  # Ensure labels are integers

    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    results = bertscore.compute(predictions=decoded_preds, references=decoded_labels, lang="en")
    score = sum(results["f1"]) / len(results["f1"])
    return {"bert_score": score}

# Define Training Arguments
training_args = TrainingArguments(
    output_dir="./fine-tuned-inlegalbert",
    logging_strategy="steps",  # Log at step intervals
    logging_steps=100,  # Log loss every 50 steps
    eval_strategy="epoch",  # Evaluate only per epoch
    save_strategy="epoch",  # Save only per epoch
    learning_rate=4e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=8,
    gradient_accumulation_steps=1,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    max_grad_norm=1.0,
    load_best_model_at_end=True,
    metric_for_best_model="bert_score",
    greater_is_better=True,
    max_steps=7000
)



# Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    processing_class=tokenizer,
    compute_metrics=compute_metrics  # Use BERTScore for evaluation
)

# Start Training
trainer.train()

# Save Fine-Tuned Model
trainer.save_model("./fine-tuned-inlegalbert")
tokenizer.save_pretrained("./fine-tuned-inlegalbert")

print("Fine-Tuning Complete! Model Saved to './fine-tuned-inlegalbert'")
