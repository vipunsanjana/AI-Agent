from pymongo import MongoClient
from typing import Optional
from app.utils.config import MONGO_URI, DB_NAME, DB_COLLECTION_NAME
from app.models.post import Post
from app.utils.constants import POST_SAVE_ERROR
from app.utils.logger import get_logger
from langchain.tools import tool

logger = get_logger(__name__)

# ==============================================================
# 🔹 MongoDB Connection Helper
#    Returns a reference to the main collection
# ==============================================================

def get_collection():
    """
    Establish a MongoDB connection and return the main collection.
    """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[DB_COLLECTION_NAME]


# ==============================================================
# 🔹 Save Post Tool
#    Used by LangChain to persist posts (LinkedIn, etc.)
# ==============================================================

@tool("save_post")
def save_post(platform: str, content: str, image_data: Optional[bytes] = None) -> Optional[str]:
    """
    Save a post to MongoDB.

    Flow:
        1️⃣ Get MongoDB collection.
        2️⃣ Create a Post model instance with provided data.
        3️⃣ Insert the post document into MongoDB.
        4️⃣ Return the inserted document ID on success.

    Args:
        platform (str): Platform name (e.g., "LinkedIn").
        content (str): Post text.
        image_data (Optional[bytes]): Optional image binary data.

    Returns:
        Optional[str]: MongoDB inserted post ID if successful.
    """
    collection = get_collection()
    try:
        # Step 1: Build post model
        post = Post(platform=platform, content=content, image_data=image_data)

        # Step 2: Insert into collection
        result = collection.insert_one(post.model_dump())

        # Step 3: Log and return ID
        logger.info(f"Post saved successfully with ID: {result.inserted_id}")
        return str(result.inserted_id)

    # Step 4: Handle insertion failure
    except Exception as e:
        logger.error(POST_SAVE_ERROR.format(error=e))
        return None


# ==============================================================
# 🔹 Get Job Summary
#    Reads total completed and failed job counts
# ==============================================================

def get_job_summary_from_summary_collection() -> dict:
    """
    Fetch total completed and failed counts from the summary_collection.

    Flow:
        1️⃣ Connect to MongoDB.
        2️⃣ Access 'summary_collection'.
        3️⃣ Retrieve the summary document (first record).
        4️⃣ Extract total_completed and total_failed counts.
        5️⃣ Return as a dictionary.

    Returns:
        dict: { "total_completed": int, "total_failed": int }
    """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["summary_collection"]  # The summary collection name

    try:
        # Step 1: Get first summary document
        summary = collection.find_one()

        # Step 2: Extract values with defaults
        if summary:
            total_completed = summary.get("total_completed", 0)
            total_failed = summary.get("total_failed", 0)
        else:
            total_completed = 0
            total_failed = 0

        # Step 3: Log summary data
        logger.info("Fetched summary: completed=%d, failed=%d", total_completed, total_failed)
        return {"total_completed": total_completed, "total_failed": total_failed}

    # Step 4: Handle DB read errors
    except Exception as e:
        logger.error("Failed to fetch summary: %s", e)
        return {"total_completed": 0, "total_failed": 0}


# ==============================================================
# 🔹 Increment Total Completed
#    Updates 'total_completed' counter in MongoDB
# ==============================================================

def increment_total_completed() -> str:
    """
    Increment the 'total_completed' counter by 1 in MongoDB.

    Flow:
        1️⃣ Connect to MongoDB and get 'summary_collection'.
        2️⃣ Atomically increment 'total_completed' by +1.
        3️⃣ Retrieve the updated value.
        4️⃣ Log success or failure and return a message.

    Returns:
        str: Log message indicating success or failure.
    """
    try:
        # Step 1: Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db["summary_collection"]

        # Step 2: Increment the field atomically
        result = collection.find_one_and_update(
            {},
            {"$inc": {"total_completed": 1}},
            upsert=True,
            return_document=True
        )

        # Step 3: Extract updated value
        new_value = result.get("total_completed", 0)

        # Step 4: Log success
        msg = f"✅ Incremented 'total_completed'. New value: {new_value}."
        logger.info(msg)
        return msg

    except Exception as e:
        msg = f"❌ Failed to increment 'total_completed': {e}"
        logger.error(msg)
        return msg


# ==============================================================
# 🔹 Increment Total Failed
#    Updates 'total_failed' counter in MongoDB
# ==============================================================

def increment_total_failed() -> str:
    """
    Increment the 'total_failed' counter by 1 in MongoDB.

    Flow:
        1️⃣ Connect to MongoDB and get 'summary_collection'.
        2️⃣ Atomically increment 'total_failed' by +1.
        3️⃣ Retrieve the updated value.
        4️⃣ Log success or failure and return a message.

    Returns:
        str: Log message indicating success or failure.
    """
    try:
        # Step 1: Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db["summary_collection"]

        # Step 2: Increment the field atomically
        result = collection.find_one_and_update(
            {},
            {"$inc": {"total_failed": 1}},
            upsert=True,
            return_document=True
        )

        # Step 3: Extract updated value
        new_value = result.get("total_failed", 0)

        # Step 4: Log success
        msg = f"✅ Incremented 'total_failed'. New value: {new_value}."
        logger.info(msg)
        return msg

    except Exception as e:
        msg = f"❌ Failed to increment 'total_failed': {e}"
        logger.error(msg)
        return msg