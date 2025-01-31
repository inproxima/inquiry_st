from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime, timezone


class UnitPlan(BaseModel):
    unit_plan_id: int = 1
    grade: int = 1
    temperature: str
    outcomes: str
    user_context: str
    unit_plan: str = ""
    guiding_question: str = ""
    essential_knowledge: str = ""
    teacher_knowledge: str = ""
    assessment_plan: str = ""
    inquiry_impact: str = ""
    differentiation: str = ""
    ipad: str = ""
    western_views: str = ""
    user_id: str = "0"
    is_favorite: bool = False
    is_generated: bool = False
    progress_percentage: int = 0
    created_at: str = datetime.now(timezone.utc).isoformat()
    title: str = (created_at,)
    tags: Optional[List[str]] = None
    migrated_id: Optional[str] = None


def to_primary(self) -> "PrimaryUnitPlan":
    return PrimaryUnitPlan(
        unit_plan_id=self.unit_plan_id,
        grade=self.grade,
        temperature=self.temperature,
        outcomes=self.outcomes,
        user_id=self.user_id,
        user_context=self.user_context,
        unit_plan=self.unit_plan,
    )


class PrimaryUnitPlan(BaseModel):
    unit_plan_id: int = 1
    grade: int = 1
    temperature: str
    outcomes: str
    user_id: str = "0"
    user_context: str = ""
    unit_plan: str = ""


def to_progress(unit_plan: UnitPlan) -> "ProgressUnitPlan":
    return ProgressUnitPlan(
        unit_plan_id=unit_plan.unit_plan_id,
        is_generated=unit_plan.is_generated,
        progress_percentage=unit_plan.progress_percentage,
    )


class ProgressUnitPlan(BaseModel):
    unit_plan_id: int = 1
    is_generated: bool = False
    progress_percentage: int = 0