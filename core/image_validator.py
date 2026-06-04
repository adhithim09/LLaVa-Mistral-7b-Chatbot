"""
Image file validation to prevent XXE and arbitrary code execution attacks.

Validates file type through magic bytes (file signature) to prevent spoofed
images and ensures only safe image formats are processed.
"""

from typing import Tuple
import io
from PIL import Image


# Magic bytes for safe image formats
MAGIC_BYTES = {
    b"\xFF\xD8\xFF": "jpeg",  # JPEG
    b"\x89PNG\r\n\x1a\n": "png",  # PNG
    b"GIF87a": "gif87a",  # GIF87a
    b"GIF89a": "gif89a",  # GIF89a
    b"RIFF": "webp",  # WebP (needs further check for WEBP signature)
    b"BM": "bmp",  # BMP
}

ALLOWED_FORMATS = {"jpeg", "jpg", "png", "gif", "webp"}
MAX_FILE_SIZE_MB = 50


class ImageValidationError(Exception):
    """Raised when image validation fails."""
    pass


def validate_magic_bytes(image_bytes: bytes) -> str:
    """
    Validate image by checking magic bytes (file signature).

    Prevents XXE attacks and spoofed file uploads by verifying
    actual file format matches declared type.

    Args:
        image_bytes: Raw image data

    Returns:
        Detected image format (lowercase)

    Raises:
        ImageValidationError: If magic bytes don't match allowed formats
    """
    if not image_bytes:
        raise ImageValidationError("Image data is empty")

    # Check each magic byte pattern
    for magic_bytes, fmt in MAGIC_BYTES.items():
        if image_bytes.startswith(magic_bytes):
            # Special handling for WebP
            if fmt == "webp":
                if b"WEBP" in image_bytes[:20]:
                    return "webp"
            else:
                return fmt

    raise ImageValidationError(
        f"File does not have a valid image signature. Detected: {image_bytes[:8].hex()}"
    )


def validate_format(image_bytes: bytes) -> str:
    """
    Validate image format using PIL Image library.

    Args:
        image_bytes: Raw image data

    Returns:
        Image format

    Raises:
        ImageValidationError: If PIL cannot open image
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img_format = (img.format or "unknown").lower()

        if img_format not in ALLOWED_FORMATS:
            raise ImageValidationError(
                f"Format {img_format} not supported. Allowed: {', '.join(ALLOWED_FORMATS)}"
            )

        return img_format
    except Exception as e:
        raise ImageValidationError(f"Failed to open image: {str(e)}")


def validate_image_size(image_bytes: bytes, max_mb: int = MAX_FILE_SIZE_MB) -> int:
    """
    Validate image file size.

    Args:
        image_bytes: Raw image data
        max_mb: Maximum allowed size in megabytes

    Returns:
        File size in bytes

    Raises:
        ImageValidationError: If file exceeds maximum size
    """
    max_bytes = max_mb * 1024 * 1024
    file_size = len(image_bytes)

    if file_size > max_bytes:
        raise ImageValidationError(
            f"Image too large: {file_size / 1024 / 1024:.1f}MB exceeds limit of {max_mb}MB"
        )

    return file_size


def validate_image_bytes(image_bytes: bytes, max_mb: int = MAX_FILE_SIZE_MB) -> Tuple[bool, str]:
    """
    Comprehensive image validation.

    Checks:
    1. File size within limits
    2. Magic bytes match allowed formats
    3. PIL can open and identify format
    4. Format is in allowed list

    Args:
        image_bytes: Raw image data
        max_mb: Maximum file size in MB

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.

    Raises:
        ImageValidationError: With detailed error message
    """
    try:
        # Check file size first
        validate_image_size(image_bytes, max_mb)

        # Verify magic bytes
        validate_magic_bytes(image_bytes)

        # Verify format with PIL
        validate_format(image_bytes)

        return (True, "")
    except ImageValidationError as e:
        return (False, str(e))


def is_valid_image(image_bytes: bytes) -> bool:
    """Quick validation check returning boolean."""
    try:
        validate_image_size(image_bytes)
        validate_magic_bytes(image_bytes)
        validate_format(image_bytes)
        return True
    except ImageValidationError:
        return False
