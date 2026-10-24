from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class FoodItem(BaseModel):
    food_id: int
    food_name: str
    category: str
    calories: float
    protein: float
    carbohydrates: float
    fat: float
    fiber: float
    diet_type: str
    allergens: str
    sodium_mg: float
    sugar_g: float
    dietary_attributes: str
    description: str
    match_score: Optional[float] = None
    distance: Optional[float] = None
    protein_pct: Optional[float] = None
    carb_pct: Optional[float] = None
    fat_pct: Optional[float] = None
    ai_rationale: Optional[str] = None


class RecommendationQuery(BaseModel):
    category: Optional[str] = None
    top_n: int = 5


class MealPlanResponse(BaseModel):
    meals: Dict[str, Optional[FoodItem]]
    actual_totals: Dict[str, float]
    target_totals: Dict[str, float]
    adherence_pct: Dict[str, float]
    summary_message: str


class FoodCatalogResponse(BaseModel):
    total_count: int
    items: List[FoodItem]
