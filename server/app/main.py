from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.route import router as agent_router
from app.routes.authRoute import router as auth_router
import uvicorn

app = FastAPI(title="LinkedIn AI Posting Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(agent_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Welcome to the LinkedIn AI Agent API 🚀"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)




