from llama_cpp import Llama # pyrefly: ignore [missing-import]
from llama_cpp.llama_chat_format import Llava15ChatHandler # pyrefly: ignore [missing-import]
import base64
from core.utils import load_config
from PIL import Image # pyrefly: ignore [missing-import]
import io
from handler.image_cache import image_cache

config = load_config()

def convert_bytes_to_base64(image_bytes):
    encoded_string = base64.b64encode(image_bytes).decode("utf-8")
    return encoded_string

def resize_image_if_large(image_bytes, max_dim=800):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        width, height = img.size
        if width > max_dim or height > max_dim:
            if width > height:
                new_width = max_dim
                new_height = int(height * (max_dim / width))
            else:
                new_height = max_dim
                new_width = int(width * (max_dim / height))
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            out_bytes = io.BytesIO()
            img.save(out_bytes, format=img.format or "JPEG")
            return out_bytes.getvalue()
    except Exception as e:
        print(f"Warning: Image resize failed: {e}")
    return image_bytes

def handle_image(image_bytes, user_input):
    max_dim = config.get("system_config", {}).get("max_image_dimension", 800)

    # CRITICAL: Check cache before processing
    cached_result = image_cache.get(image_bytes, max_dim=max_dim)
    if cached_result is not None:
        print(f"[Cache HIT] Using cached image processing result")
        return cached_result

    # Retrieve configuration with fallback support to prevent KeyErrors
    moondream_config = config.get("moondream", {})
    clip_model_path = moondream_config.get("clip_model_path") or config.get("llava_model", {}).get("clip_model_path")
    model_path = moondream_config.get("model_path") or config.get("llava_model", {}).get("llava_model_path")

    if not clip_model_path or not model_path:
        raise ValueError("Model paths for LLavA/Moondream model or CLIP vision model are not configured.")

    # Using moondream/llava model for image description via llama-cpp-python
    chat_handler = Llava15ChatHandler(
        clip_model_path=clip_model_path
    )

    llm = Llama(
        model_path=model_path,
        chat_handler=chat_handler,
        n_ctx=2048,  # n_ctx should be sufficient for the image and text
    )

    # Resize large images to optimize local performance
    resized_bytes = resize_image_if_large(image_bytes, max_dim=max_dim)
    image_base64 = convert_bytes_to_base64(resized_bytes)

    response = llm.create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                ],
            }
        ]
    )

    result = response["choices"][0]["message"]["content"]

    # Cache the processing result
    image_cache.set(image_bytes, result, max_dim=max_dim)
    print(f"[Cache MISS] Processed image and cached result")

    return result