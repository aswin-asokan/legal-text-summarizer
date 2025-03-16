from summarizer import Summarizer  # BERT Extractive Summarizer

# Load BERT for extractive summarization
bert_model = Summarizer()
input_text = """
The US has "passed the peak" on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month.
The US has over 637,000 confirmed Covid-19 cases and over 30,826 deaths, the highest for any country in the world.
At the daily White House coronavirus briefing on Wednesday, Trump said new guidelines to reopen the country would be announced on Thursday after he speaks to governors.
"We'll be the comeback kids, all of us," he said. "We want to get our country back."
The Trump administration has previously fixed May 1 as a possible date to reopen the world's largest economy, but the president said some states may be able to return to normalcy earlier than that.
"""

# Extractive summarization (top n sentences)
extracted_summary = bert_model(input_text, num_sentences=3)
print("Extracted Summary:", extracted_summary)


from transformers import BartForConditionalGeneration, BartTokenizer

# Load BART model & tokenizer
bart_model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(bart_model_name)
bart_model = BartForConditionalGeneration.from_pretrained(bart_model_name)

# Tokenize extracted summary
inputs = tokenizer(extracted_summary, return_tensors="pt", max_length=1024, truncation=True)

# Generate abstractive summary
summary_ids = bart_model.generate(inputs.input_ids, max_length=150, min_length=50, length_penalty=2.0, num_beams=4)
abstractive_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print("Final Abstractive Summary:", abstractive_summary)
