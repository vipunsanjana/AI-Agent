from __future__ import annotations
import os
from typing import Optional, Dict
from datetime import datetime, timezone

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END

from app.services.linkedin_service import post_to_linkedin, upload_media_to_linkedin
from app.services.gemini_service import generate_gemini_image
from app.services.mongodb_service import save_post
from app.services.mongodb_service import increment_total_completed, increment_total_failed
from app.utils.logger import get_logger
from app.utils.config import OPENAI_API_KEY
from app.models.agent import AgentState
from app.utils.constants import (
    TOPIC_GENERATOR_SYSTEM_PROMPT,
    TOPIC_GENERATOR_USER_PROMPT,
    CONTENT_CREATOR_SYSTEM_PROMPT,
    CONTENT_CREATOR_USER_PROMPT,
    REVIEWER_SYSTEM_PROMPT,
    POST_EXECUTOR_SUCCESS_MESSAGE,
    POST_EXECUTOR_FAILURE_MESSAGE,
)

# ============================================================
# 🔧 LOGGER & MODEL CONFIGURATION
# ============================================================
logger = get_logger(__name__)

MAX_ITERATIONS = 1
llm = ChatOpenAI(model="gpt-4o", temperature=0.7, openai_api_key=OPENAI_API_KEY)

# ============================================================
# ⚙️ DEFINE LANGGRAPH TOOLS & AGENT
# ============================================================
posting_tools = [post_to_linkedin, generate_gemini_image, save_post]
posting_agent = create_react_agent(model=llm, tools=posting_tools)

# ============================================================
# 🧩 NODE IMPLEMENTATIONS
# ============================================================

def topic_generator_node(state: AgentState) -> Dict[str, Optional[str]]:
    """Generate a relevant post topic based on the provided niche."""
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", TOPIC_GENERATOR_SYSTEM_PROMPT),
            ("user", TOPIC_GENERATOR_USER_PROMPT.format(niche=state.niche)),
        ])
        chain = prompt | llm
        result = chain.invoke({"niche": state.niche})
        topic = result.content.strip()

        logger.info("✅ Topic generated: %s", topic)
        return {"topic": topic, "current_node": "topic_generator"}
    except Exception as e:
        logger.exception("❌ Topic generation failed: %s", e)
        increment_total_failed()  # ✅ Record failure
        fallback = f"{state.niche} insight {datetime.utcnow().isoformat()}"
        return {"topic": fallback, "current_node": "topic_generator"}


def content_creator_node(state: AgentState) -> Dict[str, Optional[str]]:
    """Generate a professional LinkedIn post draft for the chosen topic."""
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", CONTENT_CREATOR_SYSTEM_PROMPT),
            ("user", CONTENT_CREATOR_USER_PROMPT.format(topic=state.topic)),
        ])
        chain = prompt | llm
        result = chain.invoke({"topic": state.topic})
        post_draft = result.content.strip()

        logger.info("✍️ Post draft created successfully.")
        return {"post_draft": post_draft, "current_node": "content_creator"}
    except Exception as e:
        logger.exception("❌ Content creation failed: %s", e)
        increment_total_failed()  # ✅ Record failure
        return {"post_draft": f"{state.topic} — quick insight", "current_node": "content_creator"}


def reviewer_node(state: AgentState) -> Dict[str, Optional[str]]:
    """Review and refine post drafts until approval or iteration limit reached."""
    current_iter = state.iteration_count + 1

    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", REVIEWER_SYSTEM_PROMPT),
            ("user", f"Critique this draft:\n\n{state.post_draft}"),
        ])
        chain = prompt | llm
        result = chain.invoke({"post_draft": state.post_draft})
        content = result.content.strip()
    except Exception as e:
        logger.exception("⚠️ Review step failed: %s", e)
        increment_total_failed()  # ✅ Record failure
        content = "APPROVED" if current_iter >= MAX_ITERATIONS else "Minor rewrite suggested."

    if "APPROVED" in content.upper() or current_iter >= MAX_ITERATIONS:
        if current_iter >= MAX_ITERATIONS and "APPROVED" not in content.upper():
            logger.warning("⚠️ Max iterations reached, forcing approval.")
        logger.info("✅ Post approved.")
        return {
            "is_approved": True,
            "final_post": state.post_draft,
            "current_node": "reviewer",
            "iteration_count": current_iter,
        }
    else:
        logger.info("🔁 Rework suggested (iteration %d): %s", current_iter, content[:80])
        return {
            "post_draft": content,
            "is_approved": False,
            "current_node": "reviewer",
            "iteration_count": current_iter,
        }


def image_generation_node(state: AgentState) -> Dict[str, Optional[str]]:
    """Generate an image using Gemini and upload it to LinkedIn."""
    if not state.final_post:
        logger.warning("⚠️ No final_post available, skipping image generation.")
        increment_total_failed()  # ✅ Record skipped/failure
        return {"image_asset_urn": None, "current_node": "image_generation"}

    TEMP_IMAGE_PATH = "temp_dummy_image.png"

    try:
        image_bytes = generate_gemini_image.invoke(state.final_post)

        if not image_bytes:
            logger.warning("⚠️ Image generation returned no data. Skipping image.")
            increment_total_failed()
            return {"image_asset_urn": None, "current_node": "image_generation"}

        with open(TEMP_IMAGE_PATH, "wb") as f:
            f.write(image_bytes)
        logger.info(f"✅ Dummy image saved at {TEMP_IMAGE_PATH}")

        asset_urn = upload_media_to_linkedin(TEMP_IMAGE_PATH)

        if os.path.exists(TEMP_IMAGE_PATH):
            os.remove(TEMP_IMAGE_PATH)
            logger.info("🧹 Temporary image file removed.")

        if asset_urn and asset_urn.startswith("urn:li:asset:"):
            logger.info("🖼️ Image asset URN generated: %s", asset_urn)
            return {"image_asset_urn": asset_urn, "current_node": "image_generation"}
        else:
            logger.warning("⚠️ Image upload failed, post will be text-only.")
            increment_total_failed()
            return {"image_asset_urn": None, "current_node": "image_generation"}

    except Exception as e:
        logger.exception("❌ Image generation error: %s", e)
        increment_total_failed()
        return {"image_asset_urn": None, "current_node": "image_generation"}


def post_executor_node(state: AgentState) -> Dict[str, Optional[str]]:
    """Publish final content to LinkedIn and store record in MongoDB."""
    if not state.final_post:
        logger.error("❌ No final_post to publish.")
        increment_total_failed()
        return {"messages": [{"role": "system", "content": "post_failed"}], "current_node": "post_executor"}

    try:
        linkedin_response = post_to_linkedin.invoke({
            "post_content": state.final_post,
            "image_urn": state.image_asset_urn
        })
        logger.info("✅ LinkedIn post successful: %s", linkedin_response)

        save_post.invoke({
            "platform": "LinkedIn",
            "niche": state.niche,
            "topic": state.topic,
            "content": state.final_post,
            "image_urn": state.image_asset_urn,
            "posted_at": datetime.now(timezone.utc).isoformat(),
            "linkedin_response": linkedin_response,
        })
        logger.info(POST_EXECUTOR_SUCCESS_MESSAGE)

        increment_total_completed()  # ✅ Mark as successful job
        return {"messages": [{"role": "system", "content": "post_success"}], "current_node": "post_executor"}

    except Exception as e:
        logger.exception(POST_EXECUTOR_FAILURE_MESSAGE.format(error=e))
        increment_total_failed()  # ✅ Record failure
        return {"messages": [{"role": "system", "content": "post_failed"}], "current_node": "post_executor"}


# ============================================================
# 🧭 DECISION FUNCTION
# ============================================================
def decide_to_rework(state: AgentState) -> str:
    """Determine whether to rework content or move to image generation."""
    return "image_generation" if state.is_approved else "content_creator"


# ============================================================
# ⚙️ GRAPH BUILDER CONFIGURATION
# ============================================================
builder = StateGraph(AgentState)
builder.add_node("topic_generator", topic_generator_node)
builder.add_node("content_creator", content_creator_node)
builder.add_node("reviewer", reviewer_node)
builder.add_node("image_generation", image_generation_node)
builder.add_node("post_executor", post_executor_node)

builder.set_entry_point("topic_generator")
builder.add_edge("topic_generator", "content_creator")
builder.add_edge("content_creator", "reviewer")
builder.add_conditional_edges("reviewer", decide_to_rework, {
    "image_generation": "image_generation",
    "content_creator": "content_creator",
})
builder.add_edge("image_generation", "post_executor")
builder.add_edge("post_executor", END)

app = builder.compile()
logger.info("✅ Agent graph compiled successfully.")
