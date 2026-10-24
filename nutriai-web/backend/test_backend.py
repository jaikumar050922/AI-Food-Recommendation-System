import sys
import os

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from core.database import init_db, seed_demo_user, get_user_by_email, get_user_progress
from core.security import verify_password, create_access_token, decode_access_token
from services.nutrition import calculate_bmi, calculate_nutrition_targets
from services.recommender import recommender

def run_tests():
    print("--- 1. Testing Database Initialization & Demo User ---")
    init_db()
    user_id = seed_demo_user()
    assert user_id is not None, "Demo user_id should not be None"
    demo_user = get_user_by_email("demo@nutriai.com")
    assert demo_user is not None, "Demo user should exist in DB"
    assert verify_password("Demo@1234", demo_user["password_hash"]), "Password verification should succeed"
    print("✅ Database & Demo User Seeded successfully! ID:", user_id)

    print("--- 2. Testing Security & JWT Token Generation ---")
    token = create_access_token({"sub": str(user_id), "email": "demo@nutriai.com"})
    payload = decode_access_token(token)
    assert payload is not None and payload.get("sub") == str(user_id), "JWT decoding failed"
    print("✅ JWT generated and verified successfully!")

    print("--- 3. Testing Nutrition Science Calculations ---")
    bmi, cat = calculate_bmi(175.0, 76.5)
    assert 24.5 <= bmi <= 25.5, f"Unexpected BMI: {bmi}"
    assert cat in ["Normal", "Overweight"], f"Unexpected BMI category: {cat}"
    targets = calculate_nutrition_targets(
        age=28,
        gender="Male",
        height_cm=175.0,
        weight_kg=76.5,
        goal="Weight Loss",
        activity_level="Moderately Active"
    )
    assert targets["target_calories"] > 1200, "Calories target should be safe floor"
    assert targets["target_protein"] > 50, "Protein target should be balanced"
    assert "Breakfast" in targets["per_meal_targets"], "Per-meal targets missing"
    print(f"✅ Nutrition targets calculated: {targets['target_calories']} kcal, {targets['target_protein']}g protein")

    print("--- 4. Testing Recommender Filtering & NearestNeighbors ---")
    filtered, stats = recommender.filter_foods(
        food_preference="Vegetarian",
        allergies=["Dairy"],
        foods_to_avoid="mushroom",
        doctor_restrictions=["Low Sodium / Hypertension Friendly"],
        doctor_custom_notes=""
    )
    assert len(filtered) > 0, "Filtered foods should not be empty"
    print(f"✅ Filters applied: {stats['initial']} total -> {stats['final_eligible']} eligible items")

    b_recs = recommender.recommend_for_category(
        filtered_df=filtered,
        category="Breakfast",
        target_macros=targets["per_meal_targets"]["Breakfast"],
        top_n=3
    )
    assert len(b_recs) > 0, "Breakfast recommendations should not be empty"
    print(f"✅ Top Breakfast Rec: {b_recs[0]['food_name']} (Match: {b_recs[0]['match_score']}%)")

    print("--- 5. Testing Full-Day Meal Plan ---")
    plan = recommender.build_full_day_plan(
        filtered_df=filtered,
        per_meal_targets=targets["per_meal_targets"],
        target_calories=targets["target_calories"],
        target_protein=targets["target_protein"],
        target_carbs=targets["target_carbs"],
        target_fat=targets["target_fat"]
    )
    assert "Breakfast" in plan["meals"], "Plan should have Breakfast"
    print(f"✅ Full Day Plan Built! Actual Calories: {plan['actual_totals']['calories']} kcal vs Target: {plan['target_totals']['calories']} kcal")

    print("--- 6. Testing Progress History ---")
    history = get_user_progress(user_id)
    assert len(history) >= 7, f"Expected at least 7 history items, got {len(history)}"
    print(f"✅ Progress entries found: {len(history)} records")

    print("\n🎉 ALL BACKEND LOGIC TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
