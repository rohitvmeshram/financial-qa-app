import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import io
import requests
import json
import tabula  # For PDF table extraction
import os  # For JAVA_HOME debug

# Ollama API endpoint
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "tinyllama"  # Use tinyllama for low memory

def extract_pdf_text(file):
    """Extract text and tables from PDF."""
    text = f"JAVA_HOME: {os.getenv('JAVA_HOME', 'Not set')}\n"
    try:
        reader = PdfReader(io.BytesIO(file.read()))
        file.seek(0)  # Reset file pointer
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        # Try extracting tables with tabula-py
        try:
            tables = tabula.read_pdf(io.BytesIO(file.read()), pages="all", multiple_tables=True)
            for table in tables:
                text += table.to_string() + "\n"
        except Exception as tabula_error:
            text += f"Warning: Table extraction failed: {str(tabula_error)}\n"
    except Exception as e:
        text += f"Error extracting PDF: {str(e)}\n"
    return text

def extract_excel_data(file):
    """Extract data from Excel as DataFrame and convert to text summary."""
    try:
        df = pd.read_excel(io.BytesIO(file.read()))
        text = df.to_string()
    except Exception as e:
        text = f"Error extracting Excel: {str(e)}"
    return text

def process_document(uploaded_file):
    """Process uploaded file based on type."""
    if uploaded_file.name.endswith('.pdf'):
        return extract_pdf_text(uploaded_file)
    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
        return extract_excel_data(uploaded_file)
    else:
        return None

def query_ollama(prompt, context):
    """Send query to Ollama with document context."""
    print(f"Connecting to {OLLAMA_URL} with model {MODEL} for prompt: {prompt[:50]}... Context size: {len(context)} chars")
    if not MODEL:
        return "Error: No model specified."
    # Further reduce context size to avoid timeouts
    max_context = 1000  # Reduced to 1k chars
    if len(context) > max_context:
        context = context[:max_context] + "\n[Context truncated]"
    full_prompt = f"Context from financial document:\n{context}\n\nUser question: {prompt}\nAnswer based only on the context, focusing on revenue, expenses, profits, or other metrics. Be concise."
    
    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {"num_ctx": 512}  # Further reduced context window
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)  # Increased to 60s
        if response.status_code == 200:
            return response.json().get("response", "No response from model")
        else:
            return f"Error: Could not query the model. Status: {response.status_code} - {response.text}"
    except requests.exceptions.Timeout:
        return "Error: Ollama server timed out after 60 seconds. Try restarting the server, reducing context size, or using a lighter model like qwen:0.5b."
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {str(e)}"

st.title("Financial Document Q&A Assistant")

# Sidebar for document status and debug info
with st.sidebar:
    st.header("Document Status")
    if 'uploaded_file' in st.session_state and st.session_state.uploaded_file:
        st.write(f"Uploaded: {st.session_state.uploaded_file.name}")
    else:
        st.write("No document uploaded.")
    st.write(f"Ollama Model: {MODEL}")
    st.write(f"Ollama URL: {OLLAMA_URL}")
    st.write(f"JAVA_HOME: {os.getenv('JAVA_HOME', 'Not set')}")

# File Upload
uploaded_file = st.file_uploader("Upload a PDF or Excel financial document", type=['pdf', 'xlsx', 'xls'])

if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file
    with st.spinner("Processing document..."):
        document_text = process_document(uploaded_file)
        if document_text:
            st.success("Document processed! Extracted content preview:")
            st.text_area("Preview", document_text[:1000], height=200)
            st.session_state.doc_context = document_text
        else:
            st.error("Unsupported file type or extraction failed.")

# Chat Interface
if 'doc_context' in st.session_state:
    st.subheader("Ask questions about the financial data:")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know? (e.g., What is the revenue?)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = query_ollama(prompt, st.session_state.doc_context)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Please upload a document to start.")