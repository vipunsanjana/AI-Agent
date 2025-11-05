import json
import requests
from fastapi import APIRouter, HTTPException, Header

router = APIRouter(prefix="/auth/linkedin", tags=["LinkedIn OAuth"])

# === LinkedIn App Config ===
LINKEDIN_CLIENT_ID = ""
LINKEDIN_CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:5173/auth/callback"

TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"


# === Step 1: Exchange Code for Access Token ===
@router.post("/token")
def get_access_token(data: dict):
    code = data.get("code")
    redirect_uri = data.get("redirect_uri") or REDIRECT_URI

    print("\n=================== LINKEDIN TOKEN DEBUG ===================")
    print(f"Received code: {code}")
    print(f"Received redirect_uri: {redirect_uri}")
    print("============================================================\n")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,  # must EXACTLY match the one in LinkedIn settings
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    print("➡️ Sending POST to LinkedIn token endpoint:")
    print(json.dumps(payload, indent=2))
    print("============================================================\n")

    res = requests.post(TOKEN_URL, data=payload, headers=headers)
    print(f"⬅️ LinkedIn token response status: {res.status_code}")
    print(f"Response body:\n{res.text}\n")

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.text)

    token_data = res.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="No access token in response")

    print("✅ Access Token received successfully!")
    return token_data


# === Step 2: Retrieve LinkedIn User Info ===
@router.get("/me")
def get_user_info(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    access_token = authorization.replace("Bearer ", "")
    headers = {"Authorization": f"Bearer {access_token}"}

    print("\n=================== LINKEDIN USER DEBUG ===================")
    print(f"Authorization header: {authorization}")
    print("============================================================\n")

    res = requests.get(USERINFO_URL, headers=headers)
    print(f"⬅️ LinkedIn /userinfo status: {res.status_code}")
    print(f"Response:\n{res.text}\n")

    if res.status_code == 401:
        raise HTTPException(status_code=401, detail="Access token invalid or revoked")
    elif res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.text)

    data = res.json()

    # ✅ Extract and return essential user info
    return {
        "id": data.get("sub"),
        "name": data.get("name"),
        "email": data.get("email"),
        "picture": data.get("picture"),
        "locale": data.get("locale"),
    }
