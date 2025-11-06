from fastapi import APIRouter, HTTPException
from app.models.agent import AgentState
from app.models.post import NicheRequest
from app.services.mongodb_service import get_job_summary_from_summary_collection
from app.utils.logger import get_logger
from app.services.agent_graph import app

# ==============================================================
# 🔹 Setup: Logger and Router
# ==============================================================

logger = get_logger(__name__)
router = APIRouter(prefix="/agent", tags=["Agent Workflow"])

# ==============================================================
# 🔹 Endpoint: Run Agent Workflow
#    POST /agent/start
#    Starts and executes the AI agent pipeline
# ==============================================================

@router.post("/start")
def run_agent_workflow(req: NicheRequest):
    """
    🚀 Run the AI agent workflow for a given niche.

    Flow:
        1️⃣ Receive the niche input from the user.
        2️⃣ Initialize the AgentState with default values.
        3️⃣ Start the agent workflow using `app.stream()`.
        4️⃣ Log progress for each node executed in the graph.
        5️⃣ Return the final workflow state upon completion.
    """
    try:
        # Step 1: Initialize agent state with niche and default values
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

        # Step 2: Stream through agent workflow steps
        final_state = None
        for s in app.stream(state):
            node_name = list(s.keys())[0]
            logger.info("➡ Node executed: %s", node_name)
            final_state = s  # Capture latest state

        # Step 3: Workflow successfully completed
        logger.info("🎯 Workflow finished successfully for niche: %s", req.niche)
        return {"status": "success", "message": "Workflow completed", "final_state": final_state}

    # Step 4: Handle exceptions during workflow execution
    except Exception as e:
        logger.exception("❌ Workflow execution failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


# ==============================================================
# 🔹 Endpoint: Get Job Summary
#    GET /agent/summary
#    Retrieves job execution summary from MongoDB
# ==============================================================

@router.get("/summary")
def get_jobs_summary():
    """
    ✅ Returns total completed and failed jobs.

    Flow:
        1️⃣ Log start of summary retrieval.
        2️⃣ Fetch summary data from MongoDB via helper function.
        3️⃣ Log and return total completed and failed job counts.
        4️⃣ Handle exceptions with HTTP 500 response.
    """
    try:
        # Step 1: Log fetching action
        print("Fetching job summary from database...")

        # Step 2: Retrieve summary data from MongoDB
        job_summary = get_job_summary_from_summary_collection()  

        # Step 3: Log summary result
        logger.info(
            "Job summary fetched: completed=%d, failed=%d",
            job_summary["total_completed"],
            job_summary["total_failed"]
        )
        
        # Step 4: Return structured JSON response
        return {
            "total_completed": job_summary["total_completed"],
            "total_failed": job_summary["total_failed"]
        }

    # Step 5: Handle MongoDB or runtime errors
    except Exception as e:
        logger.exception("Failed to fetch job summary: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch job summary: {str(e)}")
