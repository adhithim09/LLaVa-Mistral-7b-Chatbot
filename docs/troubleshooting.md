# Converso Troubleshooting Guide

This guide describes common installation and runtime errors encountered during local deployment of Converso, and how to resolve them.

---

## 1. Missing Model Weights
**Symptoms**:
* `Warning: Local model file not found at ...`
* Chat fails to initialize or responds with blank errors.

**Fix**:
Converso requires downloading GGUF models separately due to large file sizes. Run the following downloads:
- **Mistral 7B (small)**: Download [mistral-7b-instruct-v0.1.Q3_K_M.gguf](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF) and place it under `./models/`.
- **LLaVa 1.5 clip (visual)**: Download [Llama-3-Update-3.0-mmproj-model-f16.gguf](https://huggingface.co/mys/ggml_llava-v1.5-7b) and place it under `./models/llava/`.

---

## 2. PyAudio/Audio Recording Failure
**Symptoms**:
* Errors during `pip install -r requirements.txt` relating to `portaudio`.
* Speech recorder widget doesn't display or throws a compilation error.

**Fix**:
- **Windows**: Install the PyAudio wheel directly:
  ```bash
  pip install pipwin
  pipwin install pyaudio
  ```
- **macOS**: Install portaudio via Homebrew first:
  ```bash
  brew install portaudio
  pip install pyaudio
  ```
- **Linux (Debian/Ubuntu)**:
  ```bash
  sudo apt-get install portaudio19-dev python3-pyaudio
  pip install pyaudio
  ```

---

## 3. SQLite Database Locked
**Symptoms**:
* `sqlite3.OperationalError: database is locked`

**Fix**:
This occurs when multiple threads or processes access the database simultaneously without thread-safe handles.
Ensure the connection string is set up with `check_same_thread=False`:
```python
conn = sqlite3.connect("chat_sessions.db", check_same_thread=False)
```

---

## 4. CUDA Out of Memory (OOM)
**Symptoms**:
* Chat server crashes when loading visual models or PDF processing.

**Fix**:
Adjust the configurations in `core/config.yaml`:
* Set `gpu_layers` to `0` to run completely on CPU.
* Switch from `large` to `small` in your `ctransformers` model path config.
