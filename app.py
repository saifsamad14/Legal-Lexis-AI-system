"""
=========================================================
Legal Lexis
AI-Powered Legal Document Question Answering System
---------------------------------------------------------
Author : Saif Samad
Description:
    Legal Lexis allows users to upload legal PDF documents
    and ask questions in natural language.

    The application:
    - Extracts text from PDFs
    - Splits the document into chunks
    - Generates sentence embeddings
    - Retrieves the most relevant section
    - Uses Google Gemini to answer questions
=========================================================
"""

# =========================================================
# Imports
# =========================================================

import os

import fitz
import gradio as gr
import numpy as np
import google.generativeai as genai

from transformers import pipeline


# =========================================================
# Configuration
# =========================================================
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

gemini_model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


# =========================================================
# Load Embedding Model
# =========================================================

print("Loading embedding model...")

embedding_model = pipeline(
    "feature-extraction",
    model="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully.")


# =========================================================
# PDF Processing
# =========================================================

def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract text from a PDF document.

    Parameters
    ----------
    pdf_path : str
        Path to the uploaded PDF.

    Returns
    -------
    str
        Complete extracted text.
    """

    text = ""

    with fitz.open(pdf_path) as document:
        for page in document:
            text += page.get_text()

    return text


# =========================================================
# Text Chunking
# =========================================================

def chunk_text(
    text: str,
    max_chunk_size: int = 1000
) -> list[str]:
    """
    Split large text into smaller chunks.

    Parameters
    ----------
    text : str
        Input document text.

    max_chunk_size : int
        Maximum chunk size.

    Returns
    -------
    list[str]
        List of text chunks.
    """

    words = text.split()

    chunks = []
    current_chunk = ""

    for word in words:

        if len(current_chunk) + len(word) + 1 <= max_chunk_size:
            current_chunk += " " + word

        else:
            chunks.append(current_chunk.strip())
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# =========================================================
# Embedding Generation
# =========================================================

def get_embedding(text: str) -> np.ndarray:
    """
    Generate a sentence embedding for the given text.

    Parameters
    ----------
    text : str
        Input text.

    Returns
    -------
    np.ndarray
        Embedding vector.
    """

    embedding = embedding_model(text)

    return np.mean(np.array(embedding[0]), axis=0)


# =========================================================
# Similarity Calculation
# =========================================================

def cosine_similarity(
    vector_a: np.ndarray,
    vector_b: np.ndarray
) -> float:
    """
    Compute cosine similarity between two vectors.
    """

    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )


# =========================================================
# Semantic Search
# =========================================================

def find_best_chunk(
    question: str,
    chunks: list[str]
) -> str:
    """
    Find the document chunk most relevant to the user's question.
    """

    question_embedding = get_embedding(question)

    best_chunk = ""
    highest_similarity = -1

    for chunk in chunks:

        chunk_embedding = get_embedding(chunk)

        similarity = cosine_similarity(
            question_embedding,
            chunk_embedding
        )

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_chunk = chunk

    return best_chunk


# =========================================================
# Gemini Response Generation
# =========================================================

def generate_answer(
    question: str,
    context: str
) -> str:
    """
    Generate an answer using Gemini based on the retrieved context.
    """

    prompt = f"""
You are an AI legal assistant.

Answer the user's question ONLY using the information provided in the document context.

If the answer cannot be found in the document, reply with:

"I couldn't find the answer in the uploaded document."

------------------------
Document Context:
{context}
------------------------

Question:
{question}

Answer:
"""

    response = gemini_model.generate_content(prompt)

    return response.text.strip()


# =========================================================
# Main Pipeline
# =========================================================

def answer_question_from_pdf(
    pdf_path: str,
    question: str
) -> str:
    """
    Complete pipeline for answering questions from a PDF.
    """

    text = extract_pdf_text(pdf_path)

    if not text.strip():
        return "No readable text found in the uploaded PDF."

    chunks = chunk_text(text)

    if not chunks:
        return "Unable to process the document."

    best_chunk = find_best_chunk(
        question,
        chunks
    )

    return generate_answer(
        question,
        best_chunk
    )

# =========================================================
# Gradio Interface
# =========================================================

def handle_query(pdf_file, question):
    """
    Handle Gradio interface inputs.

    Parameters
    ----------
    pdf_file
        Uploaded PDF file.

    question : str
        User's question.

    Returns
    -------
    str
        AI-generated answer.
    """

    if pdf_file is None:
        return "Please upload a PDF document."

    if not question.strip():
        return "Please enter a question."

    try:
        return answer_question_from_pdf(
            pdf_file.name,
            question
        )

    except Exception as error:
        return f"An error occurred:\n{error}"


# =========================================================
# Build Gradio Application
# =========================================================

# =========================================================
# Build Gradio Application
# =========================================================

app = gr.Interface(
    fn=handle_query,

    inputs=[
        gr.File(
            label="Upload Legal PDF",
            file_types=[".pdf"]
        ),
        gr.Textbox(
            label="Ask a Question",
            placeholder="Example: What is the termination clause?"
        )
    ],

    outputs=gr.Textbox(label="Answer"),

    title="⚖️ Legal Lexis",

    description=(
        "Upload a legal PDF document and ask questions in natural language. "
        "The application retrieves the most relevant section using semantic "
        "search and generates an answer using Google Gemini."
    )
)


# =========================================================
# Launch Application
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Legal Lexis")
    print("AI-Powered Legal Document Assistant")
    print("=" * 60)

app.launch(
    share=True,
    inbrowser=True
)