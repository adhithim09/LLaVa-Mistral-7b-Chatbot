import logging
from core.utils import load_config

logger = logging.getLogger(__name__)

class ModelLoadError(Exception):
    pass

def load_model_with_error_handling(model_path, timeout=300):
    """Load LLM model with comprehensive error handling"""
    if not model_path:
        raise ModelLoadError("Model path not configured")

    import os
    if not os.path.exists(model_path):
        raise ModelLoadError(f"Model file not found: {model_path}")

    try:
        from llama_cpp import Llama
        logger.info(f"Loading model from {model_path}")

        llm = Llama(model_path=model_path, n_ctx=2048)
        logger.info("Model loaded successfully")
        return llm

    except Exception as e:
        error_msg = f"Failed to load model: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise ModelLoadError(error_msg)

def verify_clip_model(clip_model_path):
    """Verify CLIP vision model exists and is loadable"""
    if not clip_model_path:
        raise ModelLoadError("CLIP model path not configured")

    import os
    if not os.path.exists(clip_model_path):
        raise ModelLoadError(f"CLIP model not found: {clip_model_path}")

    try:
        from llama_cpp.llama_chat_format import Llava15ChatHandler
        handler = Llava15ChatHandler(clip_model_path=clip_model_path)
        logger.info("CLIP model verified")
        return handler
    except Exception as e:
        error_msg = f"CLIP model verification failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise ModelLoadError(error_msg)
