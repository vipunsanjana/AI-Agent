from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.agent import AgentState
from app.services.mongodb_service import get_job_summary_from_summary_collection
from app.utils.logger import get_logger
from app.services.agent_graph import app

logger = get_logger(__name__)
router = APIRouter(prefix="/agent", tags=["Agent Workflow"])

# ✅ Define a request body model
class NicheRequest(BaseModel):
    niche: str

@router.post("/start")
def run_agent_workflow(req: NicheRequest):
    """
    🚀 Run the AI agent workflow for a given niche.
    """
    try:
        state = AgentState(
            niche=req.niche,
            topic=None,
            post_draft=None,
            final_post=None,
            image_asset_urn=None,
            is_approved=False,
            iteration_count=0,
        )

        logger.info("🚀 Starting workflow for niche: %s", req.niche)

        final_state = None
        for s in app.stream(state):
            node_name = list(s.keys())[0]
            logger.info("➡ Node executed: %s", node_name)
            final_state = s

        logger.info("🎯 Workflow finished successfully for niche: %s", req.niche)
        return {"status": "success", "message": "Workflow completed", "final_state": final_state}

    except Exception as e:
        logger.exception("❌ Workflow execution failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

@router.get("/summary")
def get_jobs_summary():
    """
    ✅ Returns total completed and failed jobs.
    """
    try:
        print("Fetching job summary from database...")

        job_summary =get_job_summary_from_summary_collection()  
        logger.info("Job summary fetched: completed=%d, failed=%d", job_summary["total_completed"], job_summary["total_failed"])
        
        return {
            "total_completed": job_summary["total_completed"],
            "total_failed": job_summary["total_failed"]
        }

    except Exception as e:
        logger.exception("Failed to fetch job summary: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch job summary: {str(e)}")
