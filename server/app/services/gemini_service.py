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

# ------------------------------------------------------------
# Initialize logger for this module
# ------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------
# 1️⃣ Gemini Client Initialization Function
# ------------------------------------------------------------
def get_gemini_client() -> bool:
    """
    Initialize the Gemini API client with the configured API key.

    Returns:
        bool: True if the client was configured successfully, False otherwise.
    """
    try:
        # Configure Gemini API with the provided key
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("✅ Gemini client configured successfully.")
        return True
    except Exception as e:
        # Log error if initialization fails
        logger.error(GEMINI_CLIENT_INIT_FAIL.format(error=e))
        return False


# ------------------------------------------------------------
# 2️⃣ Gemini Image Generation Tool
# ------------------------------------------------------------
@tool("generate_gemini_image")
def generate_gemini_image(prompt: str, temp_path: str = "temp_gemini_image.png") -> Optional[bytes]:
    """
    Generate a professional AI image for a LinkedIn post using the Gemini API.

    Args:
        prompt (str): The topic or description for the image.
        temp_path (str, optional): Temporary file path to save the image.
                                   Defaults to "temp_gemini_image.png".

    Returns:
        Optional[bytes]: The image data in bytes, or None if generation failed.
    """
    # --------------------------------------------------------
    # Step 1: Ensure Gemini client is properly initialized
    # --------------------------------------------------------
    if not get_gemini_client():
        return None

    # --------------------------------------------------------
    # Step 2: Prepare a descriptive image prompt
    # --------------------------------------------------------
    full_prompt = GEMINI_IMAGE_PROMPT_TEMPLATE.format(topic=prompt)
    logger.info(f"🎨 Generating Gemini image for prompt: '{prompt}'")

    try:
        # ----------------------------------------------------
        # Step 3: Create a Gemini model instance and request image generation
        # ----------------------------------------------------
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(full_prompt)

        image_bytes: Optional[bytes] = None

        # ----------------------------------------------------
        # Step 4: Extract image bytes from Gemini response
        # ----------------------------------------------------
        if hasattr(response, "candidates") and response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    image_bytes = part.inline_data.data
                    break

        # ----------------------------------------------------
        # Step 5: Check if image data exists
        # ----------------------------------------------------
        if not image_bytes:
            logger.warning(GEMINI_NO_IMAGE_DATA)
            return None

        # ----------------------------------------------------
        # Step 6: Save the image temporarily using Pillow
        # ----------------------------------------------------
        try:
            image = Image.open(BytesIO(image_bytes))
            image.save(temp_path)
            logger.info(f"✅ Gemini image saved temporarily at {temp_path}")
        except Exception as e:
            logger.error(GEMINI_IMAGE_SAVE_FAIL.format(error=e))
            return None

        # ----------------------------------------------------
        # Step 7: Return image bytes for further processing
        # ----------------------------------------------------
        return image_bytes

    except Exception as e:
        # ----------------------------------------------------
        # Step 8: Handle image generation or API errors
        # ----------------------------------------------------
        logger.error(GEMINI_IMAGE_GEN_FAIL.format(error=e))
        return None
