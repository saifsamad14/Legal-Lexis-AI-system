# ⚖️ Legal Lexis

An AI-powered legal document question answering system that enables users to upload legal PDF documents and ask natural language questions. The application uses semantic search to retrieve the most relevant context from the document and Google Gemini to generate accurate, context-aware responses.

---

## 🚀 Features

- 📄 Upload legal PDF documents
- ❓ Ask questions in natural language
- 🔍 Semantic search using sentence embeddings
- 🤖 AI-generated answers powered by Google Gemini
- 📚 Context-aware document retrieval
- 🧠 Transformer-based embedding generation
- 💻 Simple and interactive user interface

---

## 🛠️ Technologies Used

- Python
- Google Gemini API
- Hugging Face Transformers
- Sentence Transformers
- PyMuPDF
- NumPy
- Gradio

---

## 📂 Project Structure

```
Legal-Lexis/
│
├── app.py
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── notebook/
│   └── legal_lexis_demo.ipynb
│
├── assets/
│   ├── homepage.png
│   ├── output.png
│   └── architecture.png
│
└── sample/
    └── sample_legal_document.pdf
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Legal-Lexis.git
```

Navigate to the project folder:

```bash
cd Legal-Lexis
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Configure your Google Gemini API key before running the application.

---

## ▶️ Running the Project

```bash
python app.py
```

---

## 🧠 How It Works

1. Upload a legal PDF document.
2. Extract text from the PDF using PyMuPDF.
3. Split the document into manageable chunks.
4. Generate embeddings using Sentence Transformers.
5. Compare the user's question with each chunk using cosine similarity.
6. Retrieve the most relevant section.
7. Send the retrieved context and question to Google Gemini.
8. Display the generated answer.

---

## 📸 Screenshots

### Home Page

> *(Add a screenshot here after testing the application.)*

![Home](https://github.com/saifsamad14/Legal-Lexis-AI-system/blob/main/assets/Hopepage.png)

---

### Example Output

> *(Add a screenshot of the generated answer.)*

![Output](https://github.com/saifsamad14/Legal-Lexis-AI-system/blob/main/assets/Result.png)

---

## 🔮 Future Improvements

- Support multiple PDF documents
- Chat history
- Citation highlighting
- Faster vector search using FAISS
- Flask/React web interface
- OCR support for scanned PDFs
- User authentication
- Cloud deployment

---

## 👨‍💻 Author

**Saif Samad**

- GitHub: https://github.com/saifsamad14

---

## 📄 License

This project is licensed under the MIT License.# Legal-Lexis-AI-system
Developed an AI-powered legal document assistant that enables users to upload PDF documents and ask natural language questions. Built using Python, PyMuPDF, Hugging Face Transformers, Google Gemini API, and Gradio, leveraging semantic search for context-aware question answering.
