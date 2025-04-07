# 🧾 Indian Legal Text Summarizer using BERT

## 📚 Table of Contents

- [📌 Description](#-description)
- [🏗️ Architecture](#-architecture)
- [📊 Test Evaluation](#-test-evaluation)
- [💬 Features](#-features)
- [📷 Screenshots](#-screenshots)
- [🚀 Installation & Usage](#-installation--usage)
- [📚 Citation](#-citation)
  - [🧠 Model: InCaseLawBERT](#-model-incaselawbert)
  - [📂 Dataset: Legal Case Document Summarization](#-dataset-legal-case-document-summarization)

---

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

![app_flow](https://github.com/user-attachments/assets/934b7815-3052-45a5-95a8-778b528a3993)

---

### 📊 Test Evaluation

| Epoch | Eval Loss | Accuracy | Precision | Recall | F1 Score | Runtime (s) | Samples/sec | Steps/sec |
| ----- | --------- | -------- | --------- | ------ | -------- | ----------- | ----------- | --------- |
| 1     | 0.5053    | 0.8206   | 0.8198    | 0.8206 | 0.8122   | 26.71       | 27.96       | 3.52      |
| 2     | 0.5862    | 0.8661   | 0.8670    | 0.8661 | 0.8621   | 26.65       | 28.03       | 3.53      |
| 3     | 0.6193    | 0.8929   | 0.8911    | 0.8929 | 0.8912   | 26.69       | 27.98       | 3.52      |
| 4     | 0.7844    | 0.8742   | 0.8753    | 0.8742 | 0.8697   | 26.76       | 27.91       | 3.51      |
| 5     | 0.8597    | 0.8755   | 0.8774    | 0.8755 | 0.8710   | 26.66       | 28.02       | 3.53      |

**Training Summary**

- 🏋️ Total Training Time: 4590.15 seconds
- 🚀 Samples/Second: 7.32
- 🔄 Steps/Second: 0.915
- 💡 Final Training Loss: 0.2268
- 📈 Total Epochs: 5
  
<img src="https://github.com/user-attachments/assets/33bea8b9-934a-4aad-b575-4b47443fbb28" height=350>

---

### 💬 Features

- ✅ Accurate summarization of legal documents
- ✅ Section-wise breakdown (Facts, Arguments, etc.)
- ✅ Grammar-corrected summaries
- ✅ Gemini-powered chatbot for interactive queries
- ✅ Designed for real-world legal use cases

---

### 📷 Screenshots

| 🏠 Home | 📄 Summary Page 1 |
|--------|-------------------|
| ![home](https://github.com/user-attachments/assets/4b84df81-3884-4bd2-94c7-4315f6d81b9f) | ![summary1](https://github.com/user-attachments/assets/c90abbb8-c5cf-415a-bfd8-68fc60fb0b1e) |

| 📄 Summary Page 2 | 💬 Chatbot |
|------------------|------------|
| ![summary2](https://github.com/user-attachments/assets/3447f53d-fa96-4de8-a256-35785c7950b4) | ![chatbot](https://github.com/user-attachments/assets/72d3cef5-b3f3-416b-85b0-fccaa0a95594) |

---

### 🚀 Installation & Usage

Follow these steps to set up and run the complete system, the project directory is as follows:

```bash
.
├── .gitignore
├── readme.md
├── requirements.txt
├── .venv/
├── legalhome/
│   ├── __pycache__/
│   ├── frontend/
│   ├── public/
│   ├── uploads/
│   ├── .env
│   ├── incaselaw.py
│   └── main.py
├── python_folder/
│   ├── bert_caselawbert/
│   ├── datasets/
│   ├── case_summary.py
│   ├── finetune_bert.py
│   └── process_data.py
├── sample_input/
```

**1. Create a virtual environment and install dependencies**

```bash
   python -m venv venv
   source venv/bin/activate     # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
```

**2. Preprocess the dataset**
Navigate to the <span style="color:green">python_folder</span> and run:

```bash
python process_data.py
```

**3. Fine-tune the InCaseLaw BERT model**

```bash
python finetune_bert.py
```

**4. Test summarization output**
Try out the model by running,

```bash
python case_summary.py
```

**5. Configure Gemini API for chatbot support**
Create a **.env** file inside the <span style="color:green">legalhome folder</span> and add your API key:

```bash
GENAI_API_KEY=your_api_key_here
```

**6. Run the backend API**
In the <span style="color:green">legalhome folder</span> directory, start the backend server:

```bash
uvicorn main:app --reload
```

**7. Run the frontend (in a split terminal)**
Navigate to the <span style="color:green">frontend</span> folder:

```bash
npm install
npm run dev
```

Your application should now be up and running with both frontend and backend connected!
Sample input files are provided on <span style="color:green">sample_input</span> folder, two of them are judgements from court and one is a non legal document.

---

## 📚 Citation

If you use this project, please cite the following works:

### 🧠 Model: InCaseLawBERT

Paul, Shounak, Mandal, Arpan, Goyal, Pawan, & Ghosh, Saptarshi. (2023).  
**Pre-trained Language Models for the Legal Domain: A Case Study on Indian Law**.  
_Proceedings of the 19th International Conference on Artificial Intelligence and Law (ICAIL 2023)._  
[📄 arXiv Paper](https://arxiv.org/abs/2209.06049) | [🤗 Hugging Face Model](https://huggingface.co/law-ai/InCaseLawBERT)

```bibtex
@inproceedings{paul-2022-pretraining,
  url = {https://arxiv.org/abs/2209.06049},
  author = {Paul, Shounak and Mandal, Arpan and Goyal, Pawan and Ghosh, Saptarshi},
  title = {Pre-trained Language Models for the Legal Domain: A Case Study on Indian Law},
  booktitle = {Proceedings of 19th International Conference on Artificial Intelligence and Law - ICAIL 2023},
  year = {2023},
}
```

### 📂 Dataset: Legal Case Document Summarization

**Citation:**

> Abhay Shukla, Paheli Bhattacharya, Soham Poddar, Rajdeep Mukherjee, Kripabandhu Ghosh, Pawan Goyal, & Saptarshi Ghosh. (2022).  
> _Legal Case Document Summarization: Extractive and Abstractive Methods and their Evaluation_ [Data set].  
> The 2nd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 12th International Joint Conference on Natural Language Processing (AACL-IJCNLP).  
> [🔗 Zenodo](https://zenodo.org/records/7152317)
