# Financial Document Q&A Assistant

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-brightgreen)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange)](https://ollama.com)
[![GitHub](https://img.shields.io/badge/Repository-Public-black)](https://github.com/rohitvmeshram/financial-qa-app)

A local web application built with Streamlit and Ollama for uploading and querying financial documents (PDF/Excel formats, e.g., income statements, balance sheets). Users can ask natural language questions about financial metrics (e.g., "What is the total operating expenses?") and receive accurate responses based on extracted content. The app supports conversational interactions, runs entirely offline after setup, and meets assignment requirements for document processing, Q&A functionality, and local deployment.

## Features
- **Document Upload:** Supports PDF and Excel files (e.g., income statements, balance sheets).
- **Text/Table Extraction:** Uses PyPDF2 for text and tabula-py for tables (requires Java).
- **Natural Language Q&A:** Powered by Ollama with lightweight models like `tinyllama` (~700 MB) or `qwen:0.5b` (~300 MB) for low-memory systems.
- **Interactive UI:** Streamlit-based chat interface with document preview and sidebar status (file name, model, JAVA_HOME).
- **Local Deployment:** Runs on localhost:8501 without cloud dependency.
- **Error Handling:** Manages timeouts, memory issues, and extraction failures with user-friendly messages.

## Example Usage
- Upload the [Sample Financial Statement](https://mbpc.tcnj.edu/wp-content/uploads/sites/148/2021/10/Sample-Financial-Statements-1.pdf).
- Ask: "What is the total operating expenses?" → Response: ~$1,805.
- Ask: "What is the net income?" → Response: ~$945.

## Prerequisites
Before installation, ensure the following are installed on your system (Windows 10/11 recommended):

1. **Python 3.10+:** Download from [python.org/downloads](https://www.python.org/downloads/). Check "Add Python to PATH" during installation.
   - Verify: `python --version` (expected: "Python 3.10.x").

2. **Git:** Download from [git-scm.com](https://git-scm.com/downloads). Choose "Use Git from the Windows Command Prompt".
   - Verify: `git --version` (expected: "git version 2.x").

3. **Ollama:** Download the Windows installer from [ollama.com/download](https://ollama.com/download). Run as administrator.
   - Verify: `ollama --version` (expected: "ollama version 0.11.11").

4. **Java JDK 17:** Download from [adoptium.net](https://adoptium.net/temurin/releases/?version=17) (Windows x64 MSI). Install to `C:\Program Files\Java\jdk-17`.
   - Required for tabula-py table extraction.
   - Verify: `java -version` (expected: "java version '17.0.12'").

5. **Visual Studio Code (VS Code):** Optional but recommended. Download from [code.visualstudio.com](https://code.visualstudio.com/). Install the Python extension.

**Hardware Requirements:**
- 8 GB+ RAM (minimum 4 GB for lightweight models like `qwen:0.5b`).
- ~1 GB disk space for dependencies and model (~700 MB for `tinyllama`, ~300 MB for `qwen:0.5b`).
- Internet connection for initial downloads (offline after setup).

## Installation
Follow these steps to set up the project in `C:\Users\Administrator\Downloads\Assingment Problem Statement Folder`.

### Step 1: Clone the Repository
1. Open Command Prompt or VS Code terminal (Ctrl+`).
2. Navigate to your project directory:
   ```
   cd C:\Users\Administrator\Downloads\Assingment Problem Statement Folder
   ```
3. Clone the repository:
   ```
   git clone https://github.com/rohitvmeshram/financial-qa-app.git
   cd financial-qa-app
   ```
4. Verify files: `app.py`, `requirements.txt`, `README.md`, `.gitignore`.

### Step 2: Set Up Environment Variables
1. **Set JAVA_HOME for tabula-py:**
   - Press Win+R, type `sysdm.cpl`, press Enter.
   - Go to "Advanced" tab > "Environment Variables".
   - Under "System variables", click "New":
     - Variable name: `JAVA_HOME`
     - Variable value: `C:\Program Files\Java\jdk-17` (adjust if installed elsewhere).
   - Edit "Path" under System variables:
     - Add: `C:\Program Files\Java\jdk-17\bin`.
   - Click OK to save.
   - Restart terminal and verify:
     ```
     echo %JAVA_HOME%
     dir "%JAVA_HOME%\bin\server\jvm.dll"
     ```
     - Expected: `C:\Program Files\Java\jdk-17` and `jvm.dll` file listed.

2. **Disable Anaconda Base (if `(venv) (base)` prompt appears):**
   - Run:
     ```
     conda deactivate
     conda config --set auto_activate_base false
     ```
   - Restart terminal to ensure `(venv)` only.

### Step 3: Create Virtual Environment and Install Dependencies
1. In the project folder (`financial-qa-app`):
   ```
   python -m venv venv
   ```
2. Activate the environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Prompt should show `(venv)`.

3. Install dependencies:
   ```
   pip install streamlit pypdf2 pandas openpyxl requests tabula-py jpype1
   pip freeze > requirements.txt
   ```
   - Installs libraries for Streamlit UI, PDF/Excel processing, and Ollama API.

4. Verify installation:
   ```
   pip list
   ```
   - Should include `streamlit`, `pypdf2`, `pandas`, `openpyxl`, `requests`, `tabula-py`, `jpype1`.

### Step 4: Download and Test Ollama Model
1. In a new terminal (keep open for `ollama serve`):
   ```
   ollama pull tinyllama
   ```
   - Downloads ~700 MB model for low memory.

2. Test the model:
   ```
   ollama run tinyllama "Test: What is 2+2?"
   ```
   - Expected: "4" (type `/bye` to exit).

3. For lighter memory usage (recommended for <1 GB RAM):
   ```
   ollama pull qwen:0.5b
   ```
   - Edit `app.py`: Change `MODEL = "tinyllama"` to `MODEL = "qwen:0.5b"`.

4. Start Ollama server:
   - In a separate terminal:
     ```
     ollama serve
     ```
   - Expected: "Listening on 127.0.0.1:11434" (as of 11:17 AM IST, September 17, 2025).

### Step 5: Test tabula-py for Table Extraction
1. Create `test_tabula.py` in the project folder:
   ```
   import tabula
   tables = tabula.read_pdf("sample.pdf", pages="all")
   print(tables)
   ```
2. Download [Sample Financial Statement](https://mbpc.tcnj.edu/wp-content/uploads/sites/148/2021/10/Sample-Financial-Statements-1.pdf) to the project folder as `sample.pdf`.
3. Run:
   ```
   python test_tabula.py
   ```
   - Expected: Prints table data (e.g., "Service revenue $2,750").
   - If error ("No JVM shared library file (jvm.dll) found"), verify `JAVA_HOME`.

## Running the App
### Step 1: Launch the App
1. Ensure `(venv)` is activated and Ollama server is running (`ollama serve` in a separate terminal).
2. In the project folder:
   ```
   streamlit run app.py
   ```
   - Expected output:
     ```
     You can now view your Streamlit app in your browser.
     Local URL: http://localhost:8501
     Network URL: http://<your-ip>:8501
     ```
3. Open `http://localhost:8501` in a browser (e.g., Chrome, Firefox).

### Step 2: Usage
1. **Upload Document:**
   - Click "Browse files" and select a PDF or Excel file (e.g., `sample.pdf`).
   - App processes: Shows "Processing document..." spinner, then "Document processed!" with a preview of extracted text (up to 1000 characters).

2. **Preview:**
   - Text area displays extracted content (e.g., "Service revenue $2,750", "Total operating expenses $1,805").
   - Sidebar shows:
     - Uploaded file name.
     - Ollama model (`tinyllama` or `qwen:0.5b`).
     - Ollama URL: `http://127.0.0.1:11434`.
     - JAVA_HOME: `C:\Program Files\Java\jdk-17` (or "Not set" if misconfigured).

3. **Ask Questions:**
   - In the chat input box, type: "What is the total operating expenses?" and press Enter.
   - Expected: Response like "The total operating expenses are $1,805" (based on sample PDF).
   - Additional queries: "What is the net income?" → ~$945.
   - Chat history persists for follow-up questions.

4. **Stop the App:**
   - Press Ctrl+C in the terminal to stop Streamlit.

### Step 3: Test with Sample PDF
1. Use the [Sample Financial Statement](https://mbpc.tcnj.edu/wp-content/uploads/sites/148/2021/10/Sample-Financial-Statements-1.pdf).
2. Upload `sample.pdf` via the app.
3. Verify preview contains:
   - Service revenue: $2,750
   - Total operating expenses: $1,805
   - Net income: $945
4. Ask:
   - "What is the total operating expenses?" → Expected: ~$1,805.
   - "What is the net income?" → Expected: ~$945.

## Making the App Live (Optional)
To share the app publicly on the web (not required for assignment, as it focuses on local deployment):

1. **Streamlit Community Cloud (Free):**
   - Ensure the repository is public.
   - Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
   - Click "New app", select `rohitvmeshram/financial-qa-app`, main branch, and `app.py` as the main file.
   - Deploy (~1-2 minutes).
   - Get a URL like `https://your-app-name.streamlit.app`.
   - **Note:** Ollama runs locally, so web deployment requires hosting Ollama on a server or using a cloud-based LLM API (beyond assignment scope).

2. **Render (Free Tier):**
   - Create a `Procfile` in the project root:
     ```
     web: streamlit run --server.port $PORT --server.address 0.0.0.0 app.py
     ```
   - Go to [render.com](https://render.com) and sign up with GitHub.
   - Click "New Web Service", connect `rohitvmeshram/financial-qa-app`.
   - Set:
     - Runtime: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `streamlit run --server.port $PORT --server.address 0.0.0.0 app.py`
   - Deploy (~2-5 minutes).
   - Get a URL like `https://your-app-name.onrender.com`.
   - **Note:** Free tier sleeps after inactivity; Ollama setup required.

## Troubleshooting
### Common Issues
1. **Ollama Timeout ("Error: Ollama server timed out after 60 seconds"):**
   - **Cause:** Memory overload with large document context (~910 MiB available).
   - **Fix:**
     - Edit `app.py`: Change `MODEL = "tinyllama"` to `MODEL = "qwen:0.5b"`.
     - Free >1.5 GiB RAM (Task Manager: Ctrl+Shift+Esc > Performance > Memory).
     - Restart Ollama: End `ollama.exe` in Task Manager, then run `ollama serve`.
     - Check logs: `C:\Users\Administrator\.ollama\logs\server.log` (since 11:17 AM IST, September 17, 2025).
     - Reduce context in `app.py`: Set `max_context = 500`, `"num_ctx": 256`.

2. **JAVA_HOME Error ("No JVM shared library file (jvm.dll) found"):**
   - **Cause:** `JAVA_HOME` unset or incorrect.
   - **Fix:**
     - Set `JAVA_HOME = C:\Program Files\Java\jdk-17` in Environment Variables.
     - Verify: `dir "%JAVA_HOME%\bin\server\jvm.dll"`.
     - Reinstall: `pip install jpype1 tabula-py`.

3. **Environment Conflict ("(venv) (base)"):**
   - **Cause:** Anaconda base environment interference.
   - **Fix:**
     ```
     conda deactivate
     venv\Scripts\activate
     conda config --set auto_activate_base false
     ```
     - Restart terminal.

4. **Git Push Rejection ("! [rejected] main -> main (fetch first)"):**
   - **Cause:** Remote repository has changes not in local.
   - **Fix:**
     ```
     git pull origin main --allow-unrelated-histories
     git add .
     git commit -m "Merge remote changes"
     git push
     ```
   - Use GitHub Personal Access Token if prompted: [github.com/settings/tokens](https://github.com/settings/tokens) (select "repo" scope).

5. **App Stuck at "Thinking...":**
   - **Cause:** Ollama processing delay due to memory or model issues.
   - **Fix:** Use `qwen:0.5b`, check `server.log`, ensure >1.5 GiB free RAM.

### Memory Optimization
- Close unnecessary apps to free RAM (Task Manager > Performance > Memory).
- Increase virtual memory:
  - Win+R > `sysdm.cpl` > Advanced > Performance > Settings > Advanced > Virtual Memory.
  - Set: Initial Size: 4096 MB, Maximum Size: 8192 MB.

### Debugging
- **Ollama Logs:** Check `C:\Users\Administrator\.ollama\logs\server.log` for errors (e.g., memory issues).
- **Streamlit Logs:** Terminal output during `streamlit run app.py` shows context size and connection attempts.
- **App Sidebar:** Displays file status, model, `JAVA_HOME`, and Ollama URL for debugging.

## Limitations
- **Performance:** CPU-only; slower on low-end hardware. Use `qwen:0.5b` for <1 GB RAM.
- **Table Extraction:** Requires Java; falls back to text-only if `JAVA_HOME` is unset.
- **Document Types:** Optimized for text-based PDFs; scanned documents need OCR (future enhancement).
- **Model Accuracy:** Lightweight models (`tinyllama`, `qwen:0.5b`) may hallucinate; best for basic financial queries.
- **Deployment:** Local only (localhost:8501); web deployment requires server-side Ollama setup.

## Contributing
1. Fork the repository: [github.com/rohitvmeshram/financial-qa-app](https://github.com/rohitvmeshram/financial-qa-app).
2. Clone: `git clone https://github.com/<your-username>/financial-qa-app.git`.
3. Create branch: `git checkout -b feature-branch`.
4. Commit changes: `git commit -m "Add feature"`.
5. Push: `git push origin feature-branch`.
6. Open a pull request on GitHub.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
- Open an issue on [GitHub](https://github.com/rohitvmeshram/financial-qa-app/issues).
- Contact: rohitvmeshram@gmail.com.
- Test with the sample PDF to verify functionality (e.g., $1,805 for total operating expenses).
