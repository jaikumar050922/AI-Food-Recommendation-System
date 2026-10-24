from typing import Dict, Any, Tuple

def calculate_bmi(height_cm: float, weight_kg: float) -> Tuple[float, str]:
    """Calculate Body Mass Index (BMI) and WHO classification."""
    if height_cm <= 0:
        return 0.0, "Unknown"
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 1)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25.0:
        category = "Normal"
    elif bmi < 30.0:
        category = "Overweight"
    else:
        category = "Obese"
        
    return bmi, category


def calculate_bmr(age: int, gender: str, height_cm: float, weight_kg: float) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation.
    """
    if gender.lower() == "male":
        bmr = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age + 5.0
    elif gender.lower() == "female":
        bmr = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age - 161.0
    else:
        bmr = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age - 78.0
    return round(bmr, 1)


def calculate_nutrition_targets(
    age: int,
    gender: str,
    height_cm: float,
    weight_kg: float,
    goal: str,
    activity_level: str = "Moderately Active"
) -> Dict[str, Any]:
    """
    Calculate TDEE and target Calories and Macronutrients based on biometrics and goal.
    Goals:
      - Weight Loss: ~20% calorie deficit (-500 kcal), 32% protein, 40% carbs, 28% fat
      - Weight Gain: ~15% calorie surplus (+400 kcal), 25% protein, 50% carbs, 25% fat
      - Maintain Weight: TDEE, 25% protein, 50% carbs, 25% fat
    """
    bmr = calculate_bmr(age, gender, height_cm, weight_kg)

    # Activity multipliers
    activity_factors = {
        "Sedentary (little to no exercise)": 1.2,
        "Lightly Active (light exercise 1-3 days/wk)": 1.375,
        "Moderately Active (moderate exercise 3-5 days/wk)": 1.55,
        "Very Active (hard exercise 6-7 days/wk)": 1.725,
    }
    
    # Fuzzy match activity level
    multiplier = 1.4
    for key, val in activity_factors.items():
        if key.lower().split()[0] in activity_level.lower():
            multiplier = val
            break
            
    tdee = bmr * multiplier

    # Adjust for goal
    goal_lower = goal.lower()
    if "loss" in goal_lower:
        target_calories = max(1200.0, tdee - 500.0)
        protein_ratio = 0.32
        carb_ratio = 0.40
        fat_ratio = 0.28
        fiber_target = 35.0
    elif "gain" in goal_lower:
        target_calories = tdee + 400.0
        protein_ratio = 0.25
        carb_ratio = 0.50
        fat_ratio = 0.25
        fiber_target = 30.0
    else:
        target_calories = tdee
        protein_ratio = 0.25
        carb_ratio = 0.50
        fat_ratio = 0.25
        fiber_target = 28.0

    target_calories = round(target_calories)
    # 1g Protein = 4 kcal, 1g Carb = 4 kcal, 1g Fat = 9 kcal
    target_protein = round((target_calories * protein_ratio) / 4.0, 1)
    target_carbs = round((target_calories * carb_ratio) / 4.0, 1)
    target_fat = round((target_calories * fat_ratio) / 9.0, 1)

    # Meal distribution (Breakfast: 25%, Lunch: 35%, Dinner: 30%, Snack: 10%)
    meal_splits = {
        "Breakfast": 0.25,
        "Lunch": 0.35,
        "Dinner": 0.30,
        "Snack": 0.10,
    }

    per_meal_targets = {}
    for meal, split in meal_splits.items():
        per_meal_targets[meal] = {
            "calories": round(target_calories * split, 1),
            "protein": round(target_protein * split, 1),
            "carbohydrates": round(target_carbs * split, 1),
            "fat": round(target_fat * split, 1),
            "fiber": round(fiber_target * split, 1),
        }

    return {
        "bmr": bmr,
        "tdee": round(tdee, 1),
        "target_calories": target_calories,
        "target_protein": target_protein,
        "target_carbs": target_carbs,
        "target_fat": target_fat,
        "target_fiber": fiber_target,
        "per_meal_targets": per_meal_targets,
    }
