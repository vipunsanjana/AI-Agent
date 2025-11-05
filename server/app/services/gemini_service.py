from typing import Optional
from io import BytesIO
from PIL import Image
import os
import google.generativeai as genai
from langchain.tools import tool

from app.utils.config import GEMINI_API_KEY
from app.utils.logger import get_logger
from app.utils.constants import (
    GEMINI_CLIENT_INIT_FAIL,
    GEMINI_IMAGE_GEN_FAIL,
    GEMINI_NO_IMAGE_DATA,
    GEMINI_IMAGE_SAVE_FAIL,
    TEMP_FILE_REMOVED,
    GEMINI_MODEL,
    GEMINI_IMAGE_PROMPT_TEMPLATE,
)

logger = get_logger(__name__)


# def get_gemini_client() -> bool:
#     """Initialize Gemini with the API key."""
#     try:
#         genai.configure(api_key=GEMINI_API_KEY)
#         logger.info("✅ Gemini client configured successfully.")
#         return True
#     except Exception as e:
#         logger.error(GEMINI_CLIENT_INIT_FAIL.format(error=e))
#         return False


# @tool("generate_gemini_image")
# def generate_gemini_image(prompt: str, temp_path: str = "temp_gemini_image.png") -> Optional[bytes]:
#     """
#     Generate a professional AI image for a LinkedIn post using Gemini API.

#     Args:
#         prompt (str): The topic or description for the image.
#         temp_path (str, optional): Temporary file path to save the image. Defaults to "temp_gemini_image.png".

#     Returns:
#         Optional[bytes]: The image data in bytes, or None if generation failed.
#     """
#     if not get_gemini_client():
#         return None

#     full_prompt = GEMINI_IMAGE_PROMPT_TEMPLATE.format(topic=prompt)
#     logger.info(f"🎨 Generating Gemini image for prompt: '{prompt}'")

#     try:
#         model = genai.GenerativeModel(GEMINI_MODEL)
#         response = model.generate_content(full_prompt)

#         image_bytes: Optional[bytes] = None
#         # If Gemini returns inline data or media parts
#         if hasattr(response, "candidates") and response.candidates:
#             for part in response.candidates[0].content.parts:
#                 if hasattr(part, "inline_data") and part.inline_data:
#                     image_bytes = part.inline_data.data
#                     break

#         if not image_bytes:
#             logger.warning(GEMINI_NO_IMAGE_DATA)
#             return None

#         try:
#             image = Image.open(BytesIO(image_bytes))
#             image.save(temp_path)
#             logger.info(f"✅ Gemini image saved temporarily at {temp_path}")
#         except Exception as e:
#             logger.error(GEMINI_IMAGE_SAVE_FAIL.format(error=e))
#             return None

#         return image_bytes

#     except Exception as e:
#         logger.error(GEMINI_IMAGE_GEN_FAIL.format(error=e))
#         return None


@tool("generate_gemini_image")
def generate_gemini_image(prompt: str, temp_path: str = "generated_image.png") -> Optional[bytes]:
    """
    Temporary stub for Gemini image generation.
    Generates a dummy RGB image for testing workflows without a Gemini API key.

    Args:
        temp_path (str, optional): Path to save the dummy image. Defaults to "generated_image.png".

    Returns:
        Optional[bytes]: Image data in bytes.
    """
    temp_path = "dummy_image.png"  # Hardcoded path
    image = Image.new("RGB", (512, 512), color=(73, 109, 137))
    image.save(temp_path)
    logger.info(f"✅ Dummy image saved at {temp_path}")
     # Read image bytes
    with open(temp_path, "rb") as f:
        image_bytes = f.read()

    return image_bytes

