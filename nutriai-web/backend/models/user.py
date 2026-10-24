from typing import List, Optional
from pydantic import BaseModel, Field

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)
    age: int = Field(28, ge=10, le=120)
    gender: str = "Male"
    height_cm: float = Field(172.0, ge=80.0, le=250.0)
    weight_kg: float = Field(70.0, ge=30.0, le=300.0)
    target_weight: Optional[float] = None
    activity_level: str = "Moderately Active (moderate exercise 3-5 days/wk)"
    food_preference: str = "Vegetarian"
    primary_goal: str = "Weight Loss"
    allergies: List[str] = []
    custom_allergies: Optional[str] = ""
    foods_to_avoid: Optional[str] = ""
    dietary_restrictions: List[str] = []
    doctor_custom_notes: Optional[str] = ""


class UserLoginRequest(BaseModel):
    email: str = Field(..., min_length=5)
    password: str


class UserProfileResponse(BaseModel):
    user_id: int
    name: str
    email: str
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    target_weight: float
    activity_level: str
    food_preference: str
    primary_goal: str
    allergies: List[str] = []
    custom_allergies: str = ""
    foods_to_avoid: str = ""
    dietary_restrictions: List[str] = []
    doctor_custom_notes: str = ""
    # Calculated metrics
    bmi: float
    bmi_category: str
    bmr: float
    tdee: float
    target_calories: float
    target_protein: float
    target_carbs: float
    target_fat: float
    target_fiber: float


class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    age: int = Field(..., ge=10, le=120)
    gender: str
    height_cm: float = Field(..., ge=80.0, le=250.0)
    weight_kg: float = Field(..., ge=30.0, le=300.0)
    target_weight: float = Field(..., ge=30.0, le=300.0)
    activity_level: str
    food_preference: str
    primary_goal: str
    allergies: List[str] = []
    custom_allergies: Optional[str] = ""
    foods_to_avoid: Optional[str] = ""
    dietary_restrictions: List[str] = []
    doctor_custom_notes: Optional[str] = ""


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfileResponse


class ProgressEntryRequest(BaseModel):
    date: str
    weight: Optional[float] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    notes: Optional[str] = ""


class ProgressEntryResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    date: str
    weight: Optional[float] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    notes: Optional[str] = ""
    created_at: Optional[str] = None
