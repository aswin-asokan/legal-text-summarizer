from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("law-ai/InLegalBERT")
text = '''
The court ruled that the accused must serve a five-year prison sentence.
The case was heard in the High Court, and the judge found the evidence sufficient.
However, the defense lawyer argued for leniency.
Ultimately, the decision was upheld, and the accused was sentenced.
'''
encoded_input = tokenizer(text, return_tensors="pt")

print(encoded_input)

model = AutoModel.from_pretrained("law-ai/InLegalBERT")
output = model(**encoded_input)
print(output.last_hidden_state)
last_hidden_state = output.last_hidden_state
print(last_hidden_state.shape)