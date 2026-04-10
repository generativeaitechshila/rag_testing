# LLM & RAG Evaluation Framework

This repository provides a structured framework to evaluate **LLM and RAG (Retrieval-Augmented Generation)** pipelines using **DeepEval**.  
It is maintained by **Generative AI Techshila** and is intended for QA engineers, AI engineers, and developers working on GenAI systems.

---

## 📁 Project Structure

- **LLM_RAG_EVALUATION/**  
  Core directory containing evaluation scripts, test cases, and configuration.
- **test_rag_eval.py**  
  Main test file used to execute RAG evaluation.
- **requirements.txt**  
  List of Python dependencies required for the framework.

---

## 🛠️ Prerequisites

- Python 3.9 or above  
- Visual Studio Code (recommended)
- pip / pip3 installed
- Basic knowledge of virtual environments

---

## 🚀 Setup Instructions

Follow the steps below to set up and run the LLM & RAG evaluation framework.

### 1️⃣ Open the Framework
- Open the project in **Visual Studio Code**
- Navigate to the `LLM_RAG_EVALUATION` directory

---

### 2️⃣ Remove Existing Virtual Environment (If Any)
Delete the existing virtual environment folder:

```bash
llm_rag_eval_env

### 3️⃣ Create a New Virtual Environment
Open the VS Code terminal and run:

```bash
python3 -m venv llm_rag_eval_env

### 4️⃣ Activate the Virtual Environment

Navigate to the virtual environment scripts directory:

```bash
system_path\llm_rag_eval_env\Scripts


Activate the environment:

```bash
activate


✅ You should now see the virtual environment name in your terminal.


### 5️⃣ Install Dependencies

Install all required dependencies using the requirements.txt file:

```bash
pip3 install -r system_path\LLM_RAG_Evaluation\requirements.txt

### 6️⃣ Run RAG Evaluation Tests

Execute the DeepEval test runner:

```bash
deepeval test run test_rag_eval.py