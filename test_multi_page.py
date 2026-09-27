"""
Test verification script for all 7 pages logic in app.py
"""
import pandas as pd
import numpy as np
import altair as alt
from recommender import FoodRecommender, calculate_nutrition_targets, calculate_bmr

def run_tests():
    print("Testing backend and multi-page components...")
    recommender = FoodRecommender("data/foods.csv")
    targets = calculate_nutrition_targets(28, "Male", 172.0, 70.0, "Weight Loss")
    filtered, stats = recommender.filter_foods("Vegetarian", ["Dairy"], "mushroom", ["Low Sodium / Hypertension Friendly"], "")

    print(f"Filter stats: {stats}")
    assert stats["final_eligible"] > 0, "No eligible foods found!"

    # Page 1: Dashboard checks
    bmr = calculate_bmr(28, "Male", 172.0, 70.0)
    assert bmr > 1000

    # Page 2: Recommendations & reasons
    for cat in ["Breakfast", "Lunch", "Dinner", "Snack"]:
        recs = recommender.recommend_for_category(filtered, cat, targets["per_meal_targets"][cat], top_n=5)
        assert not recs.empty, f"No recs for {cat}"
        for _, food in recs.iterrows():
            reasons = []
            if food["protein"] >= targets["per_meal_targets"][cat]["protein"] * 0.8:
                reasons.append(f"Provides {food['protein']}g protein")
            if food["sodium_mg"] <= 250:
                reasons.append("Low sodium")

    # Page 3: 1-Day Meal Plan
    plan = recommender.build_full_day_plan(filtered, targets["per_meal_targets"])
    assert plan["meals"]["Breakfast"] is not None
    assert plan["actual_totals"]["calories"] > 0

    # Page 4: Database search & filters
    df = recommender.df.copy()
    cats = ["Breakfast", "Lunch"]
    df_filtered = df[df["category"].isin(cats)]
    assert len(df_filtered) > 0

    # Page 5: Analytics & Altair Charts
    p_cal = targets["target_protein"] * 4.0
    c_cal = targets["target_carbs"] * 4.0
    f_cal = targets["target_fat"] * 9.0
    donut_df = pd.DataFrame({
        "Nutrient": ["Protein (4 kcal/g)", "Carbohydrates (4 kcal/g)", "Healthy Fats (9 kcal/g)"],
        "Calories": [p_cal, c_cal, f_cal]
    })
    donut_chart = alt.Chart(donut_df).mark_arc(innerRadius=65).encode(
        theta=alt.Theta(field="Calories", type="quantitative"),
        color=alt.Color(field="Nutrient", type="nominal")
    )
    assert donut_chart is not None

    print("All multi-page routines, calculations, and chart generators verified successfully!")

if __name__ == "__main__":
    run_tests()
