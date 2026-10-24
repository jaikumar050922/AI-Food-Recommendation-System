from fastapi import APIRouter, HTTPException, status, Depends
from core.deps import get_current_user_profile
from core.database import update_user_profile, get_user_profile
from models.user import UserProfileResponse, UserProfileUpdateRequest
from services.nutrition import calculate_bmi, calculate_nutrition_targets

router = APIRouter(prefix="/profile", tags=["Profile Management"])

@router.get("", response_model=UserProfileResponse)
def get_profile(profile: dict = Depends(get_current_user_profile)):
    """Returns the authenticated user's profile and metabolic targets."""
    return UserProfileResponse(
        user_id=profile["user_id"],
        name=profile["name"],
        email=profile["email"],
        age=profile["age"],
        gender=profile["gender"],
        height_cm=profile["height_cm"],
        weight_kg=profile["weight_kg"],
        target_weight=profile["target_weight"],
        activity_level=profile["activity_level"],
        food_preference=profile["food_preference"],
        primary_goal=profile["primary_goal"],
        allergies=profile.get("allergies", []),
        custom_allergies=profile.get("custom_allergies", "") or "",
        foods_to_avoid=profile.get("foods_to_avoid", "") or "",
        dietary_restrictions=profile.get("dietary_restrictions", []),
        doctor_custom_notes=profile.get("doctor_custom_notes", "") or "",
        bmi=profile["bmi"],
        bmi_category=profile["bmi_category"],
        bmr=profile["bmr"],
        tdee=profile["tdee"],
        target_calories=profile["target_calories"],
        target_protein=profile["target_protein"],
        target_carbs=profile["target_carbs"],
        target_fat=profile["target_fat"],
        target_fiber=profile["target_fiber"]
    )


@router.put("", response_model=UserProfileResponse)
def update_profile(req: UserProfileUpdateRequest, profile: dict = Depends(get_current_user_profile)):
    """Updates user biometrics and dietary restrictions."""
    update_data = {
        "name": req.name or profile["name"],
        "age": req.age,
        "gender": req.gender,
        "height_cm": req.height_cm,
        "weight_kg": req.weight_kg,
        "target_weight": req.target_weight,
        "activity_level": req.activity_level,
        "food_preference": req.food_preference,
        "primary_goal": req.primary_goal,
        "allergies": req.allergies,
        "custom_allergies": req.custom_allergies or "",
        "foods_to_avoid": req.foods_to_avoid or "",
        "dietary_restrictions": req.dietary_restrictions,
        "doctor_custom_notes": req.doctor_custom_notes or ""
    }

    success = update_user_profile(profile["user_id"], update_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )

    updated_raw = get_user_profile(profile["user_id"])
    if not updated_raw:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found after update")

    bmi, bmi_category = calculate_bmi(updated_raw["height_cm"], updated_raw["weight_kg"])
    targets = calculate_nutrition_targets(
        age=updated_raw["age"],
        gender=updated_raw["gender"],
        height_cm=updated_raw["height_cm"],
        weight_kg=updated_raw["weight_kg"],
        goal=updated_raw["primary_goal"],
        activity_level=updated_raw["activity_level"]
    )

    return UserProfileResponse(
        user_id=updated_raw["user_id"],
        name=updated_raw["name"],
        email=updated_raw["email"],
        age=updated_raw["age"],
        gender=updated_raw["gender"],
        height_cm=updated_raw["height_cm"],
        weight_kg=updated_raw["weight_kg"],
        target_weight=updated_raw["target_weight"],
        activity_level=updated_raw["activity_level"],
        food_preference=updated_raw["food_preference"],
        primary_goal=updated_raw["primary_goal"],
        allergies=updated_raw.get("allergies", []),
        custom_allergies=updated_raw.get("custom_allergies", "") or "",
        foods_to_avoid=updated_raw.get("foods_to_avoid", "") or "",
        dietary_restrictions=updated_raw.get("dietary_restrictions", []),
        doctor_custom_notes=updated_raw.get("doctor_custom_notes", "") or "",
        bmi=bmi,
        bmi_category=bmi_category,
        bmr=targets["bmr"],
        tdee=targets["tdee"],
        target_calories=targets["target_calories"],
        target_protein=targets["target_protein"],
        target_carbs=targets["target_carbs"],
        target_fat=targets["target_fat"],
        target_fiber=targets["target_fiber"]
    )
