import os
import mimetypes
from PIL import Image
import io

ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP', 'GIF'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}

def validate_image_upload(file_bytes, filename=''):
    errors = []

    # Check file size
    if len(file_bytes) > MAX_FILE_SIZE:
        errors.append(f"File too large: {len(file_bytes)} bytes exceeds {MAX_FILE_SIZE}")

    # Verify file is valid image
    try:
        img = Image.open(io.BytesIO(file_bytes))
        if img.format not in ALLOWED_FORMATS:
            errors.append(f"Unsupported image format: {img.format}")
    except Exception as e:
        errors.append(f"Invalid image file: {str(e)}")
        return False, errors

    # Check MIME type if filename provided
    if filename:
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type and mime_type not in ALLOWED_MIME_TYPES:
            errors.append(f"Invalid MIME type: {mime_type}")

    # Check for XXE vulnerability (XML in image)
    if b'<?xml' in file_bytes[:1000]:
        errors.append("Potential XXE attack detected in file")

    return len(errors) == 0, errors

def is_valid_upload(file_bytes, filename=''):
    valid, _ = validate_image_upload(file_bytes, filename)
    return valid
