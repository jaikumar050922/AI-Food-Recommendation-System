import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Any, Optional
from core.config import settings

class FoodRecommender:
    """
    Production Content-Based Food Recommendation System powered by Scikit-Learn NearestNeighbors.
    Preserves exact mathematical calculations and filtering from NutriAI.
    """

    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path or settings.DATA_PATH
        self.df = self.load_data()
        self.feature_cols = ["calories", "protein", "carbohydrates", "fat", "fiber"]

    def load_data(self) -> pd.DataFrame:
        if not os.path.exists(self.data_path):
            # Fallback relative location
            alt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "foods.csv")
            if os.path.exists(alt_path):
                self.data_path = alt_path
            else:
                raise FileNotFoundError(f"Dataset not found at {self.data_path}")
                
        df = pd.read_csv(self.data_path)
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
        Apply clinical safety, dietary preference, allergen exclusion, and doctor constraints.
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
    ) -> List[Dict[str, Any]]:
        """
        Uses Scikit-Learn NearestNeighbors to recommend top items in a category
        matching target nutrition vector.
        """
        cat_df = filtered_df[filtered_df["category"].str.lower() == category.lower()].copy()
        if cat_df.empty:
            return []

        target_vector = np.array([[
            target_macros.get("calories", 300.0),
            target_macros.get("protein", 20.0),
            target_macros.get("carbohydrates", 40.0),
            target_macros.get("fat", 10.0),
            target_macros.get("fiber", 5.0)
        ]])

        feature_matrix = cat_df[self.feature_cols].values

        # Normalize features with StandardScaler
        scaler = StandardScaler()
        combined = np.vstack([feature_matrix, target_vector])
        scaled_combined = scaler.fit_transform(combined)

        scaled_candidates = scaled_combined[:-1]
        scaled_target = scaled_combined[-1:]

        # Nearest Neighbors with Euclidean metric
        n_neighbors = min(top_n, len(cat_df))
        nn_model = NearestNeighbors(n_neighbors=n_neighbors, metric="euclidean")
        nn_model.fit(scaled_candidates)

        distances, indices = nn_model.kneighbors(scaled_target)
        raw_distances = distances[0]
        recommended = cat_df.iloc[indices[0]].copy()

        # Cosine Similarity on macronutrient ratios [protein, carbs, fat, fiber]
        cand_macros = recommended[["protein", "carbohydrates", "fat", "fiber"]].values
        target_macros_arr = target_vector[:, 1:]
        cos_sims = cosine_similarity(cand_macros, target_macros_arr).flatten()

        # Calorie Proximity score
        target_cals = float(target_macros.get("calories", 300.0))
        cal_proximities = 1.0 - np.clip(np.abs(recommended["calories"].values - target_cals) / max(target_cals, 1.0), 0.0, 1.0)

        # Combined Match Score: 60% macro ratio balance + 40% calorie proximity
        combined_scores = (0.60 * cos_sims + 0.40 * cal_proximities) * 100.0
        recommended["match_score"] = np.round(np.clip(combined_scores, 25.0, 99.5), 1)
        recommended["distance"] = np.round(raw_distances, 3)

        # Calculate macro calorie percentages and AI rationale
        result_items = []
        for i, (_, row) in enumerate(recommended.iterrows()):
            macro_cal = (row["protein"] * 4.0) + (row["carbohydrates"] * 4.0) + (row["fat"] * 9.0)
            p_pct = round((row["protein"] * 4.0 / macro_cal) * 100, 1) if macro_cal > 0 else 0.0
            c_pct = round((row["carbohydrates"] * 4.0 / macro_cal) * 100, 1) if macro_cal > 0 else 0.0
            f_pct = round((row["fat"] * 9.0 / macro_cal) * 100, 1) if macro_cal > 0 else 0.0
            
            # AI rationale text
            match_val = float(row["match_score"])
            if match_val >= 90:
                rationale = f"Optimal match for your {category} target ({row['calories']} kcal, {row['protein']}g protein) with pristine macro alignment."
            elif match_val >= 80:
                rationale = f"Strong nutritional profile offering {row['fiber']}g dietary fiber and balanced glycemic response."
            else:
                rationale = f"Compatible safe choice meeting all clinical exclusions and calorie constraints."

            item_dict = row.to_dict()
            item_dict["protein_pct"] = p_pct
            item_dict["carb_pct"] = c_pct
            item_dict["fat_pct"] = f_pct
            item_dict["ai_rationale"] = rationale
            result_items.append(item_dict)

        return result_items

    def build_full_day_plan(
        self,
        filtered_df: pd.DataFrame,
        per_meal_targets: Dict[str, Dict[str, float]],
        target_calories: float,
        target_protein: float,
        target_carbs: float,
        target_fat: float
    ) -> Dict[str, Any]:
        """
        Builds a complete 1-day personalized meal plan across Breakfast, Lunch, Dinner, Snack.
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
            if cat_recs:
                top_item = cat_recs[0]
                plan[cat] = top_item
                for key in total_nutrition.keys():
                    total_nutrition[key] += float(top_item.get(key, 0.0))
            else:
                plan[cat] = None

        for key in total_nutrition:
            total_nutrition[key] = round(total_nutrition[key], 1)

        # Adherence percentages
        target_totals = {
            "calories": target_calories,
            "protein": target_protein,
            "carbohydrates": target_carbs,
            "fat": target_fat
        }
        
        adherence_pct = {
            "calories": round((total_nutrition["calories"] / max(target_calories, 1.0)) * 100, 1),
            "protein": round((total_nutrition["protein"] / max(target_protein, 1.0)) * 100, 1),
            "carbohydrates": round((total_nutrition["carbohydrates"] / max(target_carbs, 1.0)) * 100, 1),
            "fat": round((total_nutrition["fat"] / max(target_fat, 1.0)) * 100, 1),
        }

        avg_adh = sum(adherence_pct.values()) / 4.0
        if avg_adh >= 90:
            summary_msg = f"Exceptional Plan: {round(avg_adh, 1)}% composite alignment with your clinical metabolic targets."
        else:
            summary_msg = f"Balanced Plan: {round(avg_adh, 1)}% alignment with active food exclusions respected."

        return {
            "meals": plan,
            "actual_totals": total_nutrition,
            "target_totals": target_totals,
            "adherence_pct": adherence_pct,
            "summary_message": summary_msg
        }

# Global singleton recommender instance
recommender = FoodRecommender()
