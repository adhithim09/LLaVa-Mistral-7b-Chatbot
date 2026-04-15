<div align="center">

# 🤖 Converso — LLaVA · Mistral 7B Chatbot

**A fully local, multimodal AI chatbot powered by Mistral 7B & LLaVA.**  
Chat with text, images, audio, and PDFs — all running on your machine.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=flat-square&logo=databricks&logoColor=white)](https://www.trychroma.com/)

</div>

---

## ✨ Features

| Capability                 | Description                                                     |
| :------------------------- | :-------------------------------------------------------------- |
| 💬 **Text Chat**           | Conversational AI with sliding window memory                    |
| 🖼️ **Image Understanding** | Upload images and ask questions — powered by LLaVA 1.5 + CLIP   |
| 🎙️ **Voice Input**         | Record mic audio or upload audio files, transcribed via Whisper |
| 📄 **PDF Chat**            | Upload PDFs and chat with their content using RAG + ChromaDB    |
| 🗂️ **Session Management**  | Persistent SQLite-backed chat history with delete support       |

---

## 🗂️ Project Structure

```
LLaVa-Mistral-7b-Chatbot/
├── app.py                    # Streamlit UI & entry point
├── llm_chains.py             # LLM chain builders (normal + PDF RAG)
├── prompt_templates.py       # Mistral instruction-tuned prompt templates
├── image_handler.py          # LLaVA multimodal image processing
├── audio_handler.py          # Whisper audio transcription
├── pdf_handler.py            # PDF parsing, chunking & vector DB ingestion
├── database_operations.py    # SQLite session persistence
├── html_templates.py         # Custom Streamlit HTML/CSS components
├── utils.py                  # Config loader & shared utilities
├── config.yaml               # Central configuration file
└── requirements.txt
```

---

## 🚀 Getting Started

### 1 · Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/LLaVa-Mistral-7b-Chatbot.git
cd LLaVa-Mistral-7b-Chatbot
```

### 2 · Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3 · Install dependencies

```bash
pip install -r requirements.txt
```

### 4 · Download models

The project expects GGUF model files at the paths defined in `config.yaml`:

```yaml
ctransformers:
  model_path:
    small: "./models/mistral-7b-instruct-v0.1.Q3_K_M.gguf"
    large: "./models/mistral-7b-instruct-v0.1.Q5_K_M.gguf"

llava_model:
  llava_model_path: "./models/llava/ggml-model-q5_k.gguf"
  clip_model_path: "./models/llava/Llama-3-Update-3.0-mmproj-model-f16.gguf"
```

Create a `models/` directory and place the files there, or update the paths in `config.yaml` to match where your models are stored.

### 5 · Run

```bash
streamlit run app.py
```

---

## ⚙️ Configuration Reference

All settings are in `config.yaml`:

| Key                             | Default                            | Description                            |
| :------------------------------ | :--------------------------------- | :------------------------------------- |
| `model_path.small`              | Q3_K_M gguf                        | Lighter Mistral model                  |
| `model_path.large`              | Q5_K_M gguf                        | Higher quality Mistral model           |
| `max_new_tokens`                | `100`                              | Max tokens per response                |
| `temperature`                   | `0.1`                              | Sampling temperature                   |
| `context_length`                | `2048`                             | Model context window                   |
| `gpu_layers`                    | `0`                                | Layers offloaded to GPU (0 = CPU only) |
| `threads`                       | `-1`                               | CPU threads (-1 = auto)                |
| `chat_memory_length`            | `2`                                | Past exchanges kept in memory          |
| `number_of_retrieved_documents` | `3`                                | Chunks retrieved during PDF RAG        |
| `chunk_size`                    | `1024`                             | PDF text chunk size (characters)       |
| `overlap`                       | `50`                               | Chunk overlap                          |
| `whisper_model`                 | `openai/whisper-small`             | Whisper variant for transcription      |
| `embeddings_path`               | `BAAI/bge-large-en-v1.5`           | Embedding model for vector search      |
| `chromadb_path`                 | `chroma_db`                        | Local ChromaDB storage path            |
| `chat_sessions_database_path`   | `./chat_sessions/chat_sessions.db` | SQLite DB path                         |

---

## 📦 Dependencies

```
streamlit
streamlit-mic-recorder
langchain
langchain-community
ctransformers
llama-cpp-python
transformers
librosa
pypdfium2
chromadb
sentence-transformers
InstructorEmbedding
pyyaml
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push and open a Pull Request
