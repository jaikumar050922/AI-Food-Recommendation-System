"""
AI-Based Personalized Food Recommendation Engine
Uses Scikit-Learn (NearestNeighbors & StandardScaler) + Nutrition Science (Mifflin-St Jeor)
to provide personalized meal recommendations based on user biometrics, goals, allergies,
and doctor's dietary restrictions.
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Any, Optional

DEFAULT_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "foods.csv")


def calculate_bmr(age: int, gender: str, height_cm: float, weight_kg: float) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation.
    """
    if gender.lower() == "male":
        bmr = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age + 5.0
    elif gender.lower() == "female":
        bmr = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age - 161.0
    else:  # Other / Non-binary average
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
      - Weight Loss: ~20% calorie deficit, high protein, moderate carbs, healthy fats
      - Weight Gain: ~15% calorie surplus, balanced protein, higher carbs, moderate fats
      - Maintain Weight: TDEE, balanced macros
    """
    bmr = calculate_bmr(age, gender, height_cm, weight_kg)

    # Activity multipliers
    activity_factors = {
        "Sedentary (little to no exercise)": 1.2,
        "Lightly Active (light exercise 1-3 days/wk)": 1.375,
        "Moderately Active (moderate exercise 3-5 days/wk)": 1.55,
        "Very Active (hard exercise 6-7 days/wk)": 1.725,
    }
    multiplier = activity_factors.get(activity_level, 1.4)
    tdee = bmr * multiplier

    # Adjust for goal
    goal_lower = goal.lower()
    if "loss" in goal_lower:
        target_calories = max(1200.0, tdee - 500.0)  # Safe floor
        protein_ratio = 0.32   # 32% protein (higher satiety & lean mass preservation)
        carb_ratio = 0.40      # 40% carbs
        fat_ratio = 0.28       # 28% fat
        fiber_target = 35.0
    elif "gain" in goal_lower:
        target_calories = tdee + 400.0
        protein_ratio = 0.25   # 25% protein
        carb_ratio = 0.50      # 50% carbs
        fat_ratio = 0.25       # 25% fat
        fiber_target = 30.0
    else:  # Maintain Weight
        target_calories = tdee
        protein_ratio = 0.25   # 25% protein
        carb_ratio = 0.50      # 50% carbs
        fat_ratio = 0.25       # 25% fat
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


class FoodRecommender:
    """
    Content-Based Food Recommendation System powered by Scikit-Learn NearestNeighbors.
    """

    def __init__(self, data_path: str = DEFAULT_DATA_PATH):
        self.data_path = data_path
        self.df = self.load_data()
        self.feature_cols = ["calories", "protein", "carbohydrates", "fat", "fiber"]

    def load_data(self) -> pd.DataFrame:
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}. Run create_dataset.py first.")
        df = pd.read_csv(self.data_path)
        # Ensure string columns are clean
        for col in ["food_name", "category", "diet_type", "allergens", "dietary_attributes", "description"]:
            if col in df.columns:
                df[col] = df[col].fillna("None").astype(str)
        return df

    def filter_foods(
        self,
        food_preference: str,
        allergies: List[str],
        foods_to_avoid: str,
        doctor_restrictions: List[str],
        doctor_custom_notes: str = ""
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """
        Apply rigorous safety, preference, allergy, and doctor-prescribed filters.
        """
        filtered = self.df.copy()
        initial_count = len(filtered)
        filter_stats = {"initial": initial_count}

        # 1. Food preference (Vegetarian vs Non-Vegetarian)
        if food_preference.lower() == "vegetarian":
            filtered = filtered[filtered["diet_type"].str.lower() == "vegetarian"]
        filter_stats["after_diet_pref"] = len(filtered)

        # 2. Allergy Filter
        if allergies:
            # Clean allergen input
            allergens_clean = [a.strip().lower() for a in allergies if a.strip() and a.lower() != "none"]
            if allergens_clean:
                def has_allergen(food_allergens_str: str) -> bool:
                    food_allergens = [x.strip().lower() for x in food_allergens_str.split(",")]
                    return any(user_allergen in food_allergens for user_allergen in allergens_clean)

                filtered = filtered[~filtered["allergens"].apply(has_allergen)]
        filter_stats["after_allergies"] = len(filtered)

        # 3. Foods to Avoid (user-entered keywords / ingredients)
        if foods_to_avoid and foods_to_avoid.strip():
            avoid_tokens = [t.strip().lower() for t in foods_to_avoid.replace(";", ",").split(",") if t.strip()]
            if avoid_tokens:
                def contains_avoided_item(row: pd.Series) -> bool:
                    searchable = f"{row['food_name']} {row['description']} {row['dietary_attributes']}".lower()
                    return any(token in searchable for token in avoid_tokens)

                filtered = filtered[~filtered.apply(contains_avoided_item, axis=1)]
        filter_stats["after_avoidance"] = len(filtered)

        # 4. Doctor's Advice & Prescribed Dietary Restrictions
        if doctor_restrictions:
            for restriction in doctor_restrictions:
                r_lower = restriction.lower()
                if "sodium" in r_lower:  # Low Sodium
                    filtered = filtered[filtered["sodium_mg"] <= 320]
                elif "sugar" in r_lower or "diabetic" in r_lower:  # Low Sugar / Diabetic
                    filtered = filtered[filtered["sugar_g"] <= 8.0]
                elif "fat" in r_lower:  # Low Fat
                    filtered = filtered[filtered["fat"] <= 15.0]
                elif "carb" in r_lower:  # Low Carb
                    filtered = filtered[filtered["carbohydrates"] <= 35.0]
                elif "gluten" in r_lower:  # Gluten Free
                    filtered = filtered[~filtered["allergens"].str.lower().str.contains("gluten")]
                elif "fiber" in r_lower:  # High Fiber
                    filtered = filtered[filtered["fiber"] >= 4.0]
                elif "renal" in r_lower or "kidney" in r_lower:
                    filtered = filtered[(filtered["sodium_mg"] <= 300) & (filtered["protein"] <= 25.0)]

        # 5. Doctor Custom Advice / Notes (Free Text keywords)
        if doctor_custom_notes and doctor_custom_notes.strip():
            doc_tokens = [t.strip().lower() for t in doctor_custom_notes.replace(";", ",").split(",") if t.strip()]
            if doc_tokens:
                def contains_doc_excluded(row: pd.Series) -> bool:
                    searchable = f"{row['food_name']} {row['description']} {row['dietary_attributes']}".lower()
                    return any(token in searchable for token in doc_tokens)

                filtered = filtered[~filtered.apply(contains_doc_excluded, axis=1)]

        filter_stats["final_eligible"] = len(filtered)
        return filtered, filter_stats

    def recommend_for_category(
        self,
        filtered_df: pd.DataFrame,
        category: str,
        target_macros: Dict[str, float],
        top_n: int = 5
    ) -> pd.DataFrame:
        """
        Uses Scikit-Learn NearestNeighbors to recommend top items in a category
        matching the target nutritional profile.
        """
        cat_df = filtered_df[filtered_df["category"].str.lower() == category.lower()].copy()
        if cat_df.empty:
            return pd.DataFrame()

        # Target vector for this meal category
        target_vector = np.array([[
            target_macros.get("calories", 300.0),
            target_macros.get("protein", 20.0),
            target_macros.get("carbohydrates", 40.0),
            target_macros.get("fat", 10.0),
            target_macros.get("fiber", 5.0)
        ]])

        feature_matrix = cat_df[self.feature_cols].values

        # Normalize features using StandardScaler to ensure balanced weighting across macro scales
        scaler = StandardScaler()
        # Combine to fit scaler across full range
        combined = np.vstack([feature_matrix, target_vector])
        scaled_combined = scaler.fit_transform(combined)

        scaled_candidates = scaled_combined[:-1]
        scaled_target = scaled_combined[-1:]

        # Nearest Neighbors with Euclidean metric on scaled features
        n_neighbors = min(top_n, len(cat_df))
        nn_model = NearestNeighbors(n_neighbors=n_neighbors, metric="euclidean")
        nn_model.fit(scaled_candidates)

        distances, indices = nn_model.kneighbors(scaled_target)

        raw_distances = distances[0]
        recommended = cat_df.iloc[indices[0]].copy()

        # Calculate Cosine Similarity on macronutrient distribution [protein, carbs, fat, fiber]
        cand_macros = recommended[["protein", "carbohydrates", "fat", "fiber"]].values
        target_macros_arr = target_vector[:, 1:]
        cos_sims = cosine_similarity(cand_macros, target_macros_arr).flatten()

        # Calculate Calorie Proximity (how close the item is to target meal calorie budget)
        target_cals = float(target_macros.get("calories", 300.0))
        cal_proximities = 1.0 - np.clip(np.abs(recommended["calories"].values - target_cals) / max(target_cals, 1.0), 0.0, 1.0)

        # Combined Match Score: 60% macro balance + 40% calorie proximity
        combined_scores = (0.60 * cos_sims + 0.40 * cal_proximities) * 100.0
        recommended["match_score"] = np.round(np.clip(combined_scores, 25.0, 99.5), 1)
        recommended["distance"] = np.round(raw_distances, 3)

        # Calculate macro percentages of total calories for visualization
        def calc_macro_pct(row):
            macro_cal = (row["protein"] * 4.0) + (row["carbohydrates"] * 4.0) + (row["fat"] * 9.0)
            if macro_cal <= 0:
                return 0.0, 0.0, 0.0
            p_pct = round((row["protein"] * 4.0 / macro_cal) * 100, 1)
            c_pct = round((row["carbohydrates"] * 4.0 / macro_cal) * 100, 1)
            f_pct = round((row["fat"] * 9.0 / macro_cal) * 100, 1)
            return p_pct, c_pct, f_pct

        pcts = recommended.apply(calc_macro_pct, axis=1)
        recommended["protein_pct"] = [p[0] for p in pcts]
        recommended["carb_pct"] = [p[1] for p in pcts]
        recommended["fat_pct"] = [p[2] for p in pcts]

        return recommended

    def build_full_day_plan(
        self,
        filtered_df: pd.DataFrame,
        per_meal_targets: Dict[str, Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Generates a balanced 1-day personalized meal plan across
        Breakfast, Lunch, Dinner, and Snack.
        """
        categories = ["Breakfast", "Lunch", "Dinner", "Snack"]
        plan = {}
        total_nutrition = {
            "calories": 0.0,
            "protein": 0.0,
            "carbohydrates": 0.0,
            "fat": 0.0,
            "fiber": 0.0,
            "sodium_mg": 0.0,
            "sugar_g": 0.0
        }

        for cat in categories:
            target = per_meal_targets.get(cat, {})
            cat_recs = self.recommend_for_category(filtered_df, cat, target, top_n=1)
            if not cat_recs.empty:
                top_item = cat_recs.iloc[0].to_dict()
                plan[cat] = top_item
                for key in total_nutrition.keys():
                    total_nutrition[key] += float(top_item.get(key, 0.0))
            else:
                plan[cat] = None

        # Round totals
        for key in total_nutrition:
            total_nutrition[key] = round(total_nutrition[key], 1)

        return {
            "meals": plan,
            "actual_totals": total_nutrition
        }
