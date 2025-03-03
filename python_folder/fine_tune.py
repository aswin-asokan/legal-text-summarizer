from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TrainingArguments, Trainer
from datasets import load_dataset
import torch
import evaluate  

dataset = load_dataset("ninadn/indian-legal")

train_dataset = dataset["train"]
eval_dataset = dataset["test"]  

tokenizer = AutoTokenizer.from_pretrained("law-ai/InLegalBERT")  

def preprocess_function(examples):
    inputs = ["summarize: " + doc for doc in examples["Text"]]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True)

    model_output = tokenizer.batch_encode_plus(examples["Summary"], max_length=150, truncation=True)
    model_inputs["labels"] = model_output["input_ids"]
    return model_inputs

tokenized_train_dataset = train_dataset.map(preprocess_function, batched=True)
tokenized_eval_dataset = eval_dataset.map(preprocess_function, batched=True)

model = AutoModelForSeq2SeqLM.from_pretrained("t5-small") 

training_args = TrainingArguments(
    output_dir="./fine_tuned_inlegalbert",
    per_device_train_batch_size=4, 
    gradient_accumulation_steps=4, 
    num_train_epochs=3,  
    learning_rate=5e-5, 
    warmup_steps=500,
    weight_decay=0.01,
    per_device_eval_batch_size=4, 
    logging_strategy="steps",
    logging_steps=500,
    save_strategy="steps",
    save_steps=1000,
    evaluation_strategy="steps",
    eval_steps=500,
    load_best_model_at_end=True,
    metric_for_best_model="rouge1", 
    push_to_hub=False,  
)


rouge = evaluate.load("rouge")

def compute_metrics(eval_pred):
    predictions = eval_pred.predictions
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    labels = eval_pred.label_ids
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    
    decoded_preds = ["\n".join(sent) for sent in decoded_preds]
    decoded_labels = ["\n".join(sent) for sent in decoded_labels]

    result = rouge.compute(predictions=decoded_preds, references=decoded_labels)
    return result


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_eval_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,  
)


trainer.train()


trainer.save_model("./fine_tuned_inlegalbert")


test_dataset = dataset["test"]
tokenized_test_dataset = test_dataset.map(preprocess_function, batched=True)
trainer.eval_dataset = tokenized_test_dataset 
test_results = trainer.evaluate()
print(test_results)