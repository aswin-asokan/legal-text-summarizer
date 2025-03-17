from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

model_name = "ajay-drew/midtral-7b-indian-law"
tokenizer = AutoTokenizer.from_pretrained(model_name)
base_model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-7B-v0.1")

# Load fine-tuned weights with PEFT
model = PeftModel.from_pretrained(base_model, model_name)

text = "What is the penalty for using forged document? " # Ask custom questions on Indian Law
inputs = tokenizer(text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
