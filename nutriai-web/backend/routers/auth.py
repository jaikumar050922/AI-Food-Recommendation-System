from fastapi import APIRouter, HTTPException, status, Depends
from core.database import register_user, get_user_by_email, get_user_profile, seed_demo_user
from core.security import verify_password, create_access_token
from core.deps import get_current_user_profile
from models.user import UserRegisterRequest, UserLoginRequest, AuthResponse, UserProfileResponse
from services.nutrition import calculate_bmi, calculate_nutrition_targets

router = APIRouter(prefix="/auth", tags=["Authentication"])

def build_profile_response(profile: dict) -> UserProfileResponse:
    bmi, bmi_category = calculate_bmi(profile["height_cm"], profile["weight_kg"])
    targets = calculate_nutrition_targets(
        age=profile["age"],
        gender=profile["gender"],
        height_cm=profile["height_cm"],
        weight_kg=profile["weight_kg"],
        goal=profile["primary_goal"],
        activity_level=profile["activity_level"]
    )
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


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(req: UserRegisterRequest):
    profile_data = {
        "age": req.age,
        "gender": req.gender,
        "height_cm": req.height_cm,
        "weight_kg": req.weight_kg,
        "target_weight": req.target_weight or req.weight_kg,
        "activity_level": req.activity_level,
        "food_preference": req.food_preference,
        "primary_goal": req.primary_goal,
        "allergies": req.allergies,
        "custom_allergies": req.custom_allergies or "",
        "foods_to_avoid": req.foods_to_avoid or "",
        "dietary_restrictions": req.dietary_restrictions,
        "doctor_custom_notes": req.doctor_custom_notes or ""
    }

    success, message, user_id = register_user(
        name=req.name,
        email=req.email,
        password=req.password,
        profile_data=profile_data
    )

    if not success or not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Profile creation failed")

    token = create_access_token({"sub": str(user_id), "email": req.email})
    return AuthResponse(access_token=token, user=build_profile_response(profile))


@router.post("/login", response_model=AuthResponse)
def login(req: UserLoginRequest):
    user = get_user_by_email(req.email)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please check your credentials or use the Demo login."
        )

    profile = get_user_profile(user["id"])
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    token = create_access_token({"sub": str(user["id"]), "email": user["email"]})
    return AuthResponse(access_token=token, user=build_profile_response(profile))


@router.post("/demo", response_model=AuthResponse)
def login_demo():
    """Instant 1-click access to pre-seeded demo user (demo@nutriai.com)."""
    user_id = seed_demo_user()
    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Demo user unavailable")

    token = create_access_token({"sub": str(user_id), "email": "demo@nutriai.com"})
    return AuthResponse(access_token=token, user=build_profile_response(profile))


@router.get("/me", response_model=UserProfileResponse)
def get_current_user(profile: dict = Depends(get_current_user_profile)):
    return build_profile_response(profile)
