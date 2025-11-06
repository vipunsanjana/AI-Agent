import json
import requests
from fastapi import APIRouter, HTTPException, Header
from app.utils.logger import get_logger
from app.utils.config import TOKEN_URL, USERINFO_URL, REDIRECT_URI

# === Initialize logger ===
logger = get_logger(__name__)

router = APIRouter(prefix="/auth/linkedin", tags=["LinkedIn OAuth"])

# === LinkedIn App Config ===
LINKEDIN_CLIENT_ID = ""
LINKEDIN_CLIENT_SECRET = ""

# ============================================================
# STEP 1: Exchange Authorization Code for Access Token
# ============================================================
@router.post("/token")
def get_access_token(data: dict):
    """
    Handles the LinkedIn OAuth 2.0 token exchange process.
    -------------------------------------------------------
    Flow:
    1️⃣ Receive the authorization code sent by the frontend after user login.
    2️⃣ Send a POST request to LinkedIn’s token endpoint with:
        - grant_type = authorization_code
        - code = the code received from LinkedIn
        - redirect_uri = must match the app settings
        - client_id, client_secret = from LinkedIn Developer Portal
    3️⃣ Receive and return the access token from LinkedIn.
    """

    # --- Extract data from frontend request ---
    code = data.get("code")
    # --- Validate required code parameter ---
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    # --- Prepare payload for token request ---
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # --- Exchange code for access token ---
    res = requests.post(TOKEN_URL, data=payload, headers=headers)

    # --- Handle LinkedIn API errors ---
    if res.status_code != 200:
        logger.error(f"LinkedIn token request failed: {res.text}")
        raise HTTPException(status_code=res.status_code, detail=res.text)

    # --- Parse token response ---
    token_data = res.json()
    access_token = token_data.get("access_token")

    if not access_token:
        logger.error("No access token in LinkedIn response.")
        raise HTTPException(status_code=400, detail="No access token in response")

    logger.info("✅ Access Token received successfully!")
    return token_data


# ============================================================
# STEP 2: Retrieve LinkedIn User Information
# ============================================================
@router.get("/me")
def get_user_info(authorization: str = Header(...)):
    """
    Retrieves the LinkedIn user profile using the access token.
    ----------------------------------------------------------
    Flow:
    1️⃣ Receive a Bearer token in the 'Authorization' header.
    2️⃣ Validate the header format (must start with 'Bearer ').
    3️⃣ Send a GET request to LinkedIn’s /userinfo endpoint.
    4️⃣ Parse and return essential user data (id, name, email, etc.).
    """

    # --- Validate Bearer token format ---
    if not authorization.startswith("Bearer "):
        logger.warning("Missing or invalid Bearer token.")
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    access_token = authorization.replace("Bearer ", "")
    headers = {"Authorization": f"Bearer {access_token}"}

    # --- Fetch user info from LinkedIn ---
    res = requests.get(USERINFO_URL, headers=headers)

    # --- Handle LinkedIn API response codes ---
    if res.status_code == 401:
        logger.error("Access token invalid or revoked.")
        raise HTTPException(status_code=401, detail="Access token invalid or revoked")
    elif res.status_code != 200:
        logger.error(f"LinkedIn userinfo request failed: {res.text}")
        raise HTTPException(status_code=res.status_code, detail=res.text)

    # --- Parse JSON response ---
    data = res.json()

    # ✅ Return only key user info for your app
    return {
        "id": data.get("sub"),
        "name": data.get("name"),
        "email": data.get("email"),
        "picture": data.get("picture"),
        "locale": data.get("locale"),
    }
