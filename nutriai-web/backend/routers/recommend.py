from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException
from core.deps import get_current_user_profile
from services.recommender import recommender
from services.nutrition import calculate_nutrition_targets
from models.food import FoodItem, MealPlanResponse

router = APIRouter(prefix="/recommend", tags=["AI Recommendations"])

@router.get("", response_model=Dict[str, Any])
def get_recommendations(
    category: Optional[str] = Query(None, description="Meal category: Breakfast, Lunch, Dinner, Snack"),
    top_n: int = Query(5, ge=1, le=20),
    profile: dict = Depends(get_current_user_profile)
):
    """
    Returns AI-personalized meal recommendations using NearestNeighbors on nutritional vectors,
    filtered by user allergies, dietary restrictions, and food preferences.
    """
    filtered_df, filter_stats = recommender.filter_foods(
        food_preference=profile["food_preference"],
        allergies=profile["allergies"],
        foods_to_avoid=profile["foods_to_avoid"],
        doctor_restrictions=profile["dietary_restrictions"],
        doctor_custom_notes=profile["doctor_custom_notes"]
    )

    per_meal_targets = profile["per_meal_targets"]

    if category:
        target = per_meal_targets.get(category.capitalize(), {
            "calories": profile["target_calories"] * 0.25,
            "protein": profile["target_protein"] * 0.25,
            "carbohydrates": profile["target_carbs"] * 0.25,
            "fat": profile["target_fat"] * 0.25,
            "fiber": profile["target_fiber"] * 0.25,
        })
        recs = recommender.recommend_for_category(filtered_df, category.capitalize(), target, top_n=top_n)
        return {
            "filter_stats": filter_stats,
            "category": category.capitalize(),
            "target": target,
            "recommendations": recs
        }
    else:
        # Return top N for each of the 4 categories
        all_recs = {}
        for cat in ["Breakfast", "Lunch", "Dinner", "Snack"]:
            cat_target = per_meal_targets.get(cat, {})
            all_recs[cat] = recommender.recommend_for_category(filtered_df, cat, cat_target, top_n=top_n)

        return {
            "filter_stats": filter_stats,
            "recommendations_by_category": all_recs
        }


@router.get("/meal-plan", response_model=MealPlanResponse)
def get_meal_plan(profile: dict = Depends(get_current_user_profile)):
    """
    Generates a full-day balanced 4-meal plan matching patient metabolic targets
    and respecting all clinical exclusions.
    """
    filtered_df, filter_stats = recommender.filter_foods(
        food_preference=profile["food_preference"],
        allergies=profile["allergies"],
        foods_to_avoid=profile["foods_to_avoid"],
        doctor_restrictions=profile["dietary_restrictions"],
        doctor_custom_notes=profile["doctor_custom_notes"]
    )

    plan_result = recommender.build_full_day_plan(
        filtered_df=filtered_df,
        per_meal_targets=profile["per_meal_targets"],
        target_calories=profile["target_calories"],
        target_protein=profile["target_protein"],
        target_carbs=profile["target_carbs"],
        target_fat=profile["target_fat"]
    )

    return MealPlanResponse(
        meals=plan_result["meals"],
        actual_totals=plan_result["actual_totals"],
        target_totals=plan_result["target_totals"],
        adherence_pct=plan_result["adherence_pct"],
        summary_message=plan_result["summary_message"]
    )
