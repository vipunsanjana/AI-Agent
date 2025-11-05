from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional
from typing import List
from langchain_core.messages import BaseMessage

class AgentState(BaseModel):
    """Typed, validated state for LinkedIn content creation workflow."""
    messages: List[BaseMessage] = Field(default_factory=list)
    niche: str
    topic: Optional[str] = None
    post_draft: Optional[str] = None
    is_approved: bool = False
    final_post: Optional[str] = None
    current_node: str = "topic_generator"
    iteration_count: int = 0
    image_asset_urn: Optional[str] = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: Optional[datetime] = None

    @field_validator("niche")
    @classmethod
    def niche_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("niche must not be empty")
        return v