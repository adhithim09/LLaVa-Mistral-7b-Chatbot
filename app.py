from flask import Flask, render_template, request, jsonify, session
import uuid

from llm_chains import load_normal_chain, load_pdf_chat_chain
from utils import load_config
from image_handler import handle_image
from audio_handler import transcribe_audio
from pdf_handler import add_documents_to_db
from database_operations import (
    init_db,
    load_last_k_text_messages,
    save_text_message,
    save_image_message,
    save_audio_message
)

app = Flask(__name__)
app.secret_key = "super_secret_key"  

config = load_config()

init_db()

def load_chain():
    if session.get("pdf_chat"):
        return load_pdf_chat_chain()
    return load_normal_chain()

def get_session_id():
    if "chat_id" not in session:
        session["chat_id"] = str(uuid.uuid4())
    return session["chat_id"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")

    session_id = get_session_id()

    llm_chain = load_chain()

    chat_history = load_last_k_text_messages(
        session_id,
        config["chat_config"]["chat_memory_length"]
    )

    llm_answer = llm_chain.run(
        user_input=user_input,
        chat_history=chat_history
    )

    # Save messages
    save_text_message(session_id, "human", user_input)
    save_text_message(session_id, "ai", llm_answer)

    return jsonify({"response": llm_answer})


@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    file = request.files["audio"]
    audio_bytes = file.read()

    session_id = get_session_id()

    transcribed_text = transcribe_audio(audio_bytes)

    llm_chain = load_chain()

    llm_answer = llm_chain.run(
        user_input="Summarize this text: " + transcribed_text,
        chat_history=[]
    )

    save_audio_message(session_id, "human", audio_bytes)
    save_text_message(session_id, "ai", llm_answer)

    return jsonify({
        "transcription": transcribed_text,
        "response": llm_answer
    })


@app.route("/upload_image", methods=["POST"])
def upload_image():
    file = request.files["image"]
    user_input = request.form.get("message")

    image_bytes = file.read()

    session_id = get_session_id()

    llm_answer = handle_image(image_bytes, user_input)

    save_text_message(session_id, "human", user_input)
    save_image_message(session_id, "human", image_bytes)
    save_text_message(session_id, "ai", llm_answer)

    return jsonify({"response": llm_answer})


@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    files = request.files.getlist("pdfs")

    add_documents_to_db(files)
    session["pdf_chat"] = True

    return jsonify({"status": "PDF processed"})
@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    session.pop("chat_id", None)
    session.pop("pdf_chat", None)
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)