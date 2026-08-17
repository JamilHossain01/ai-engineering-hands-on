# 🧠 LLM Engineering Hands-On

A hands-on, notebook-driven playground for learning practical **LLM Engineering**:
running frontier open-weight models locally with **Ollama**, calling them through
the **OpenAI SDK** and **LiteLLM**, and building multi-agent conversational systems.

This repo is designed as a portfolio project demonstrating:

- Local-first LLM development (no cloud API keys required)
- OpenAI-compatible client usage against self-hosted models
- Multi-agent orchestration patterns (adversarial / collaborative dialogue)
- Clean, reproducible Python + Jupyter project structure

---

## 📁 Project Structure

```
llm-engineering-hands-on/
├── .gitignore
├── README.md
├── requirements.txt
└── week01-frontier-models/
    ├── 01_frontier_models_ollama.ipynb
    └── 02_adversarial_3way_chat.ipynb
```

---

## 🛠️ Tech Stack

| Component        | Purpose                                          |
|-------------------|--------------------------------------------------|
| Python 3.10+      | Core language                                    |
| Jupyter Notebook  | Interactive experimentation                      |
| OpenAI SDK        | Unified client for chat completions              |
| LiteLLM           | Model-agnostic routing layer                     |
| Ollama            | Local inference server for open-weight models    |

---

## 🚀 Setup

### 1. Prerequisites (macOS)

- Python 3.10+ installed (`python3 --version`)
- [Ollama](https://ollama.com/download) installed and running
- VS Code with the **Python** and **Jupyter** extensions

### 2. Install Ollama models used in this repo

```bash
ollama pull qwen3:8b
ollama pull deepseek-coder:6.7b
```

Make sure the Ollama server is running (it starts automatically on macOS after install,
or launch it manually):

```bash
ollama serve
```

### 3. Clone / unzip and enter the project

```bash
cd llm-engineering-hands-on
```

### 4. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Register the Jupyter kernel (recommended)

```bash
python -m ipykernel install --user --name=llm-engineering-hands-on
```

### 7. Open in VS Code

```bash
code .
```

Open any notebook in `week01-frontier-models/`, select the
`llm-engineering-hands-on` kernel, and run the cells top to bottom.

---

## 📓 Notebooks — Week 01: Frontier Models

| Notebook | Description |
|---|---|
| `01_frontier_models_ollama.ipynb` | Connects to a local Ollama server through the OpenAI SDK and benchmarks `qwen3:8b` and `deepseek-coder:6.7b` on reasoning puzzles. |
| `02_adversarial_3way_chat.ipynb` | A 3-agent multi-persona conversation (Alex, Blake, Charlie) running entirely on local Ollama models — no external API calls. |

---

## 🔒 Notes

- No API keys are required — everything runs against `http://localhost:11434/v1`.
- If you want to swap in a real OpenAI/Anthropic key later, copy `.env.example` to
  `.env` and set `OPENAI_API_KEY` (never commit `.env`, it's already gitignored).

---

## 📄 License

MIT — feel free to fork and use this as a starting point for your own LLM engineering journey.
# ai-engineering-hands-on
