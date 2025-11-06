import json
import requests
from langchain.tools import tool
from app.utils.logger import get_logger
from app.utils.constants import (
    LINKEDIN_MISSING_CREDENTIALS,
    LINKEDIN_ASSET_REGISTER_FAIL,
    LINKEDIN_ASSET_UPLOAD_FAIL,
    LINKEDIN_POST_SUCCESS,
    LINKEDIN_POST_FAIL,
    LINKEDIN_NETWORK_ERROR,
    REGISTER_UPLOAD_URL,
    LINKEDIN_POST_API_URL,
)

# ==============================================================
# 🔹 Global LinkedIn Credentials Storage
#    Keeps access token & person URN in backend memory
# ==============================================================

linkedin_credentials = {
    "access_token": None,
    "person_urn": None
}

# --------------------------------------------------------------
# ✅ Function: set_credentials
# Purpose: Store LinkedIn access token & person URN globally
# --------------------------------------------------------------
def set_credentials(access_token: str, person_urn: str):
    linkedin_credentials["access_token"] = access_token
    linkedin_credentials["person_urn"] = person_urn

# --------------------------------------------------------------
# ✅ Function: get_credentials
# Purpose: Retrieve stored LinkedIn credentials (token & person URN)
# --------------------------------------------------------------
def get_credentials():
    print("access_token:", linkedin_credentials["access_token"])
    print("person_urn:", linkedin_credentials["person_urn"])
    return linkedin_credentials["access_token"], linkedin_credentials["person_urn"]

logger = get_logger(__name__)

# --------------------------------------------------------------
# ✅ Function: upload_media_to_linkedin
# Purpose: Upload an image to LinkedIn and return the asset URN
#
# Flow:
#   1️⃣ Get LinkedIn credentials
#   2️⃣ Register upload request (LinkedIn API)
#   3️⃣ Extract upload URL & asset URN
#   4️⃣ Upload the actual image file
#   5️⃣ Return LinkedIn asset URN on success
# --------------------------------------------------------------
def upload_media_to_linkedin(file_path: str) -> str | None:
    """
    Upload an image to LinkedIn and return the asset URN.

    Args:
        file_path (str): Local path to the image file.

    Returns:
        str | None: LinkedIn asset URN if successful, else None.
    """
    # Step 1: Get stored credentials
    access_token, person_urn = get_credentials()
    if not access_token or not person_urn:
        logger.error("❌ LinkedIn credentials not set!")
        return None
    
    # Step 2: Prepare headers and request payload for upload registration
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": person_urn,
            "serviceProvider": "LBA"
        }
    }

    try:
        # Step 3: Register upload with LinkedIn
        reg_response = requests.post(REGISTER_UPLOAD_URL, headers=headers, json=payload)
        reg_response.raise_for_status()
        reg_data = reg_response.json()

        # Step 4: Extract asset URN & upload URL
        asset_urn = reg_data["value"]["asset"]
        upload_url = reg_data["value"]["uploadMechanism"][
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
        ]["uploadUrl"]

        # Step 5: Upload image bytes to LinkedIn upload URL
        with open(file_path, "rb") as f:
            upload_response = requests.post(upload_url, data=f, headers={
                "Authorization": f"Bearer {access_token}"
            })
            upload_response.raise_for_status()

        # Step 6: Success log and return asset URN
        logger.info(f"✅ Image uploaded successfully to LinkedIn Asset API. URN: {asset_urn}")
        return asset_urn

    # Step 7: Handle request/connection errors
    except requests.exceptions.RequestException as e:
        logger.error(LINKEDIN_ASSET_REGISTER_FAIL.format(error=e))
        return None
    except Exception as e:
        logger.error(LINKEDIN_ASSET_UPLOAD_FAIL.format(error=e))
        return None


# ==============================================================
# 🔹 LinkedIn Post Tool (Text/Image)
#    Uses the uploaded asset (if any) to publish posts
# ==============================================================

@tool("post_to_linkedin")
def post_to_linkedin(post_content: str, image_asset_urn: str | None = None) -> str:
    """
    💬 Publish a text or image post to LinkedIn.

    Args:
        post_content (str): The text content to publish.
        image_asset_urn (str | None): Optional LinkedIn asset URN for image.

    Returns:
        str: Status message of the operation.
    """
    # Step 1: Retrieve credentials
    access_token, person_urn = get_credentials()
    if not access_token or not person_urn:
        return "Missing LinkedIn credentials"       

    # Step 2: Prepare headers for API request
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Step 3: Construct post payload
    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_content},
                "shareMediaCategory": "IMAGE" if image_asset_urn else "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    # Step 4: Attach image URN if available
    if image_asset_urn:
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
            {"status": "READY", "media": image_asset_urn}
        ]

    # Step 5: Make LinkedIn API POST request
    try:
        response = requests.post(LINKEDIN_POST_API_URL, headers=headers, data=json.dumps(payload))
        
        # Step 6: Handle success or failure
        if response.status_code == 201:
            logger.info(LINKEDIN_POST_SUCCESS)
            return LINKEDIN_POST_SUCCESS
        else:
            logger.error(LINKEDIN_POST_FAIL.format(status=response.status_code, error=response.text))
            return LINKEDIN_POST_FAIL.format(status=response.status_code, error=response.text)
    
    # Step 7: Handle network issues
    except requests.exceptions.RequestException as e:
        logger.error(LINKEDIN_NETWORK_ERROR.format(error=e))
        return LINKEDIN_NETWORK_ERROR.format(error=e)
