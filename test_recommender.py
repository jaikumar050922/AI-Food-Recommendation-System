from recommender import FoodRecommender, calculate_nutrition_targets

def test():
    print("Initializing FoodRecommender...")
    recommender = FoodRecommender()
    print(f"Loaded {len(recommender.df)} food items.")

    targets = calculate_nutrition_targets(
        age=28,
        gender="Male",
        height_cm=175.0,
        weight_kg=72.0,
        goal="Weight Loss",
        activity_level="Moderately Active (moderate exercise 3-5 days/wk)"
    )
    print("Calculated Targets:")
    print(f"  Calories: {targets['target_calories']} kcal (BMR: {targets['bmr']}, TDEE: {targets['tdee']})")
    print(f"  Protein: {targets['target_protein']}g | Carbs: {targets['target_carbs']}g | Fat: {targets['target_fat']}g | Fiber: {targets['target_fiber']}g")

    # Filter test
    filtered, stats = recommender.filter_foods(
        food_preference="Vegetarian",
        allergies=["Dairy"],
        foods_to_avoid="avocado",
        doctor_restrictions=["Low Sodium / Hypertension Friendly"],
        doctor_custom_notes=""
    )
    print(f"Filter stats: {stats}")

    # Category recommendations
    for cat in ["Breakfast", "Lunch", "Dinner", "Snack"]:
        cat_target = targets["per_meal_targets"][cat]
        recs = recommender.recommend_for_category(filtered, cat, cat_target, top_n=2)
        print(f"\nTop {cat} recommendations:")
        for _, row in recs.iterrows():
            print(f"  - {row['food_name']} ({row['calories']} kcal, P: {row['protein']}g, C: {row['carbohydrates']}g, F: {row['fat']}g) [Match: {row['match_score']}%]")

    # Full Day Plan test
    plan = recommender.build_full_day_plan(filtered, targets["per_meal_targets"])
    print("\nFull Day Plan Total Nutrition:")
    print(plan["actual_totals"])
    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    test()
