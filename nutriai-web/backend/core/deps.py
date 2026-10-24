from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_access_token
from core.database import get_user_profile, get_user_by_id
from services.nutrition import calculate_bmi, calculate_nutrition_targets

security = HTTPBearer(auto_error=False)

def get_current_user_profile(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """Dependency that authenticates JWT token and loads full user profile."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_id = int(payload["sub"])
    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
        
    # Enrich with calculated metrics
    bmi, bmi_category = calculate_bmi(profile["height_cm"], profile["weight_kg"])
    targets = calculate_nutrition_targets(
        age=profile["age"],
        gender=profile["gender"],
        height_cm=profile["height_cm"],
        weight_kg=profile["weight_kg"],
        goal=profile["primary_goal"],
        activity_level=profile["activity_level"]
    )
    
    profile.update({
        "bmi": bmi,
        "bmi_category": bmi_category,
        "bmr": targets["bmr"],
        "tdee": targets["tdee"],
        "target_calories": targets["target_calories"],
        "target_protein": targets["target_protein"],
        "target_carbs": targets["target_carbs"],
        "target_fat": targets["target_fat"],
        "target_fiber": targets["target_fiber"],
        "per_meal_targets": targets["per_meal_targets"]
    })
    
    return profile
