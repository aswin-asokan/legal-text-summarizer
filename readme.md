# 🧾 Indian Legal Text Summarizer using BERT

### 📌 Description

Indian Legal Text Summarizer is a powerful tool designed to simplify and summarize long and complex Indian legal documents. It’s especially useful for:

- 🧑‍⚖️ Legal Advisors
- 👨‍💼 Lawyers
- 📚 Law Students
- 🧠 Curious Individuals interested in legal understanding

It also includes a chatbot powered by Gemini, allowing users to interact and query the summarized content or general legal knowledge in a conversational way.

---

### 🏗️ Architecture

**1. PDF Parsing**
Documents are uploaded and parsed using PyPDF2 to extract raw text.

**2. Content Labeling**
The extracted text is passed through a fine-tuned InCaseLaw BERT model, which labels the content into:

- FACTS
- ARGUMENTS
- JUDGMENTS
- ANALYSIS
- STATUTES

**3. Summarization & Grammar Correction**
Labeled content is summarized and passed to a T5 model to ensure grammatically correct output.

**4. Chatbot Integration**
A Gemini-powered chatbot allows users to:

- Ask questions about the summary.
- Query legal matters conversationally.

![App flow](https://aswin-asokan.github.io/legal-text-summarizer/images/app_flow.png)
