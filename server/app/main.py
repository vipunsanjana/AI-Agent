from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.route import router as agent_router
from app.routes.authRoute import router as auth_router
import uvicorn

# ------------------------------------------------------------
# 1️⃣ Initialize FastAPI application
# ------------------------------------------------------------
app = FastAPI(title="LinkedIn AI Posting Agent")

# ------------------------------------------------------------
# 2️⃣ Configure CORS middleware
#    - Allows cross-origin requests from frontend or other services
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins (can be restricted later)
    allow_credentials=True,       # Allow cookies and credentials
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers
)

# ------------------------------------------------------------
# 3️⃣ Include route modules
#    - agent_router: Handles AI agent related routes
#    - auth_router: Handles authentication routes
# ------------------------------------------------------------
app.include_router(agent_router)
app.include_router(auth_router)

# ------------------------------------------------------------
# 4️⃣ Root endpoint
#    - Verifies that the API is running
# ------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the LinkedIn AI Agent API 🚀"}

# ------------------------------------------------------------
# 5️⃣ Application entry point
#    - Starts the FastAPI app using Uvicorn server
# ------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
