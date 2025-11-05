from pymongo import MongoClient
from typing import Optional
from app.utils.config import MONGO_URI, DB_NAME, DB_COLLECTION_NAME
from app.models.post import Post
from app.utils.constants import POST_SAVE_ERROR
from app.utils.logger import get_logger
from langchain.tools import tool

logger = get_logger(__name__)

# === MongoDB Connection ===
def get_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[DB_COLLECTION_NAME]

@tool("save_post")
def save_post(platform: str, content: str, image_data: Optional[bytes] = None) -> Optional[str]:
    """
    Save a post to MongoDB.

    Args:
        platform (str): Platform name (e.g., "LinkedIn").
        content (str): Post text.
        image_data (Optional[bytes]): Optional image binary data.

    Returns:
        Optional[str]: MongoDB inserted post ID if successful.
    """
    collection = get_collection()
    try:
        post = Post(platform=platform, content=content, image_data=image_data)
        result = collection.insert_one(post.model_dump())
        logger.info(f"Post saved successfully with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(POST_SAVE_ERROR.format(error=e))
        return None

def get_job_summary_from_summary_collection() -> dict:
    """
    Fetch total completed and failed counts from the summary_collection.

    Returns:
        dict: { "total_completed": int, "total_failed": int }
    """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["summary_collection"]  # your summary collection name

    try:
        summary = collection.find_one()  # get the first (and only) summary document
        if summary:
            total_completed = summary.get("total_completed", 0)
            total_failed = summary.get("total_failed", 0)
        else:
            total_completed = 0
            total_failed = 0

        logger.info("Fetched summary: completed=%d, failed=%d", total_completed, total_failed)
        return {"total_completed": total_completed, "total_failed": total_failed}

    except Exception as e:
        logger.error("Failed to fetch summary: %s", e)
        return {"total_completed": 0, "total_failed": 0}

def update_job_summary(field: str, increment: int = 1) -> str:
    """
    Increment or decrement 'total_completed' or 'total_failed' by 1 
    and return a log message.

    Args:
        field (str): Either 'total_completed' or 'total_failed'.
        increment (int): +1 to increase or -1 to decrease.

    Returns:
        str: Log message indicating success or failure.
    """
    if field not in ["total_completed", "total_failed"]:
        msg = f"❌ Invalid field name: {field}. Must be 'total_completed' or 'total_failed'."
        logger.error(msg)
        return msg

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["summary_collection"]

    try:
        result = collection.find_one_and_update(
            {},
            {"$inc": {field: increment}},
            upsert=True,
            return_document=True
        )

        new_value = result.get(field, 0)
        msg = f"✅ Successfully updated '{field}' by {increment}. New value: {new_value}."
        logger.info(msg)
        return msg

    except Exception as e:
        msg = f"❌ Failed to update '{field}': {e}"
        logger.error(msg)
        return msg
