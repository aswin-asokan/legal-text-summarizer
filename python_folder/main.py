import torch
from transformers import BertTokenizer, BertForMaskedLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Indian Legal-BERT or generic BERT model
model_name = "law-ai/InLegalBERT"  # Can change to "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name).to(device)

# Load the dataset
dataset = load_dataset("ninadn/indian-legal")

# Tokenization function
def tokenize_function(examples):
    return tokenizer(examples["Text"], truncation=True, padding="max_length", max_length=512)

# Apply tokenization
tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["Text"])

# Set format for PyTorch
tokenized_dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])

# Define data collator (for Masked Language Model training)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True,  # Enable masked language modeling
    mlm_probability=0.15,  # 15% of tokens will be masked
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./indian-legal-bert",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,  # Can adjust
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=100,
    save_total_limit=2,
    push_to_hub=False,
)

# Trainer initialization
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],  # If available
    data_collator=data_collator,
)

# Train the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./indian-legal-bert")
tokenizer.save_pretrained("./indian-legal-bert")

print("Model training completed and saved successfully!")