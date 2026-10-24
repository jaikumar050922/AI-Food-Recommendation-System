from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from core.deps import get_current_user_profile
from core.database import get_user_progress, add_progress_entry
from models.user import ProgressEntryRequest, ProgressEntryResponse

router = APIRouter(prefix="/progress", tags=["Progress Tracking"])

@router.get("", response_model=List[ProgressEntryResponse])
def get_progress(profile: dict = Depends(get_current_user_profile)):
    """Returns chronological patient progress entries."""
    entries = get_user_progress(profile["user_id"])
    return entries


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def log_progress(req: ProgressEntryRequest, profile: dict = Depends(get_current_user_profile)):
    """Adds a new daily tracking entry and updates current weight in profile."""
    success = add_progress_entry(
        user_id=profile["user_id"],
        date_str=req.date,
        weight=req.weight,
        calories=req.calories,
        protein=req.protein,
        carbs=req.carbs,
        fat=req.fat,
        notes=req.notes or ""
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record daily progress entry"
        )

    return {
        "success": True,
        "message": "Progress entry logged successfully."
    }
