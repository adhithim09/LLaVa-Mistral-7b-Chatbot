<div align="center">

<img src="https://img.shields.io/badge/LLaVA-Mistral_7B-6C63FF?style=for-the-badge&logo=openai&logoColor=white" alt="LLaVA Mistral 7B"/>

# 🤖 Converso — LLaVA · Mistral 7B Chatbot

**A fully local, multimodal AI chatbot powered by Mistral 7B & LLaVA.**  
Chat with text, images, audio, and PDFs — all running on your machine. No API keys. No cloud. Full privacy.

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=flat-square&logo=databricks&logoColor=white)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)

</div>

---

## ✨ Features

| Capability                 | Description                                                                               |
| :------------------------- | :---------------------------------------------------------------------------------------- |
| 💬 **Text Chat**           | Conversational AI with sliding window memory (configurable history)                       |
| 🖼️ **Image Understanding** | Upload images and ask questions — powered by LLaVA 1.5 + CLIP                             |
| 🎙️ **Voice Input**         | Record mic audio or upload audio files, transcribed via OpenAI Whisper                    |
| 📄 **PDF Chat**            | Upload PDFs and chat with their content using RAG + ChromaDB                              |
| 🗂️ **Session Management**  | Persistent SQLite-backed chat history across sessions                                     |
| ⚡ **Fully Local**         | All models run on-device via `ctransformers` & `llama-cpp-python` — zero cloud dependency |

---

## 🏗️ Architecture

```
converso/
├── app.py                   # Streamlit UI & entry point
├── llm_chains.py            # LLM chain builders (normal + PDF RAG)
├── prompt_templates.py      # Mistral instruction-tuned prompt templates
├── image_handler.py         # LLaVA multimodal image processing
├── audio_handler.py         # Whisper audio transcription
├── pdf_handler.py           # PDF parsing, chunking & vector DB ingestion
├── database_operations.py   # SQLite session persistence
├── html_templates.py        # Custom Streamlit HTML/CSS components
├── utils.py                 # Config loader & shared utilities
├── config.yaml              # 🔧 Central configuration file
└── models/                  # ← Place your .gguf models here
    ├── mistral-7b-instruct-v0.1.Q3_K_M.gguf  (or Q5)
    └── llava/
        ├── ggml-model-q5_k.gguf
        └── mmproj-model-f16.gguf
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

> **Note for GPU users:** Install `llama-cpp-python` with CUDA support for faster inference:
>
> ```bash
> CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall
> ```

### 4 · Download models

Place your GGUF model files in the `models/` directory (create it if needed):

| Model                                  | Purpose                     | Recommended                                                                 |
| :------------------------------------- | :-------------------------- | :-------------------------------------------------------------------------- |
| `mistral-7b-instruct-v0.1.Q3_K_M.gguf` | Text chat (smaller, faster) | [Download →](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF) |
| `mistral-7b-instruct-v0.1.Q5_K_M.gguf` | Text chat (better quality)  | [Download →](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF) |
| LLaVA GGUF + CLIP projection           | Image understanding         | [Download →](https://huggingface.co/mys/ggml_llava-v1.5-7b)                 |

### 5 · Configure

Edit `config.yaml` to set model paths and tune parameters:

```yaml
ctransformers:
  model_path:
    small: "./models/mistral-7b-instruct-v0.1.Q3_K_M.gguf"
    large: "./models/mistral-7b-instruct-v0.1.Q5_K_M.gguf"
  model_config:
    max_new_tokens: 100
    temperature: 0.1
    context_length: 2048
    gpu_layers: 0 # Set > 0 to offload layers to GPU
```

### 6 · Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ⚙️ Configuration Reference

All settings live in `config.yaml`:

| Key                             | Default                  | Description                                       |
| :------------------------------ | :----------------------- | :------------------------------------------------ |
| `model_path.small`              | Q3_K_M gguf              | Lighter model for faster responses                |
| `model_path.large`              | Q5_K_M gguf              | Higher quality responses                          |
| `max_new_tokens`                | `100`                    | Maximum tokens per response                       |
| `temperature`                   | `0.1`                    | Sampling temperature (lower = more deterministic) |
| `context_length`                | `2048`                   | Model context window                              |
| `gpu_layers`                    | `0`                      | Layers to offload to GPU (0 = CPU only)           |
| `chat_memory_length`            | `2`                      | Number of past exchanges kept in memory           |
| `number_of_retrieved_documents` | `3`                      | Chunks retrieved during PDF RAG                   |
| `chunk_size`                    | `1024`                   | PDF text chunk size (characters)                  |
| `whisper_model`                 | `openai/whisper-small`   | Whisper variant for transcription                 |
| `embeddings_path`               | `BAAI/bge-large-en-v1.5` | Embedding model for vector search                 |

---

## 🧠 How It Works

```
User Input
    │
    ├── Text  ──────────────────► Mistral 7B (CTransformers)
    │                                   │
    ├── Image ──► LLaVA 1.5 + CLIP ─────┤
    │                                   │
    ├── Audio ──► Whisper (ASR) ─────────┤──► Response
    │                                   │
    └── PDF ───► pypdfium2               │
                    └─► Text Chunks      │
                            └─► ChromaDB (RAG)
                                    └─► Mistral 7B
```

- **Normal chat** uses `ConversationBufferWindowMemory` for sliding-window context
- **PDF chat** uses a LangChain `LCEL` runnable with ChromaDB retrieval
- **Image chat** uses `llama-cpp-python` with `Llava15ChatHandler` and a CLIP projection model
- **Audio** is transcribed locally with HuggingFace `pipeline` using Whisper

---

## 📦 Dependencies

```
streamlit              # Web UI
streamlit-mic-recorder # Browser microphone recording
langchain              # LLM chains & memory
langchain-community    # CTransformers, ChromaDB, embeddings integrations
ctransformers          # GGUF model inference (CPU/GPU)
llama-cpp-python       # LLaVA multimodal inference
transformers           # Whisper audio transcription
librosa                # Audio processing
pypdfium2              # PDF text extraction
chromadb               # Local vector store
sentence-transformers  # Embedding support
InstructorEmbedding   # BAAI BGE embeddings
pyyaml                 # Config file parsing
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feat/your-feature`
3. **Commit** your changes: `git commit -m "feat: add your feature"`
4. **Push** and open a **Pull Request**

Please keep PRs focused — one feature or fix per PR.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

<div align="center">

Built with ❤️ using [Mistral 7B](https://mistral.ai/), [LLaVA](https://llava-vl.github.io/), [LangChain](https://www.langchain.com/), and [Streamlit](https://streamlit.io/)

</div>
