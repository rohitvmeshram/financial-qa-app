# Financial Document Q&A Assistant
A Streamlit app for querying financial PDFs/Excel files using Ollama.

## Setup
1. Install Python 3.10+, VS Code, Ollama [](https://adoptium.net/).
2. Set JAVA_HOME to C:\Program Files\Java\jdk-17.
3. Run `ollama pull tinyllama` or `ollama pull qwen:0.5b` and `ollama serve`.
4. Clone repo: `git https://github.com/rohitvmeshram/financial-qa-app`
5. Navigate: `cd financial-qa-app`
6. Create venv: `python -m venv venv`
7. Activate: `venv\Scripts\activate` (Windows)
8. Install dependencies: `pip install -r requirements.txt`
9. Run: `streamlit run app.py`

## Usage
- Upload a financial PDF/Excel.
- Ask questions like “What is the total operating expenses?”

## Limitations
- CPU mode (slower) without NVIDIA GPU.
- Low-memory systems use `tinyllama` or `qwen:0.5b`.
- Table extraction requires `tabula-py`, `jpype1`, and JAVA_HOME.
