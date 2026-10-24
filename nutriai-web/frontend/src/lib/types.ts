export interface UserProfile {
  user_id: number;
  name: string;
  email: string;
  age: number;
  gender: string;
  height_cm: number;
  weight_kg: number;
  target_weight: number;
  activity_level: string;
  food_preference: string;
  primary_goal: string;
  allergies: string[];
  custom_allergies: string;
  foods_to_avoid: string;
  dietary_restrictions: string[];
  doctor_custom_notes: string;
  bmi: number;
  bmi_category: string;
  bmr: number;
  tdee: number;
  target_calories: number;
  target_protein: number;
  target_carbs: number;
  target_fat: number;
  target_fiber: number;
  per_meal_targets?: Record<string, {
    calories: number;
    protein: number;
    carbohydrates: number;
    fat: number;
    fiber: number;
  }>;
}

export interface FoodItem {
  food_id: number;
  food_name: string;
  category: string;
  calories: number;
  protein: number;
  carbohydrates: number;
  fat: number;
  fiber: number;
  diet_type: string;
  allergens: string;
  sodium_mg: number;
  sugar_g: number;
  dietary_attributes: string;
  description: string;
  match_score?: number;
  distance?: number;
  protein_pct?: number;
  carb_pct?: number;
  fat_pct?: number;
  ai_rationale?: string;
}

export interface MealPlan {
  meals: Record<string, FoodItem | null>;
  actual_totals: {
    calories: number;
    protein: number;
    carbohydrates: number;
    fat: number;
    fiber: number;
    sodium_mg: number;
    sugar_g: number;
  };
  target_totals: {
    calories: number;
    protein: number;
    carbohydrates: number;
    fat: number;
  };
  adherence_pct: {
    calories: number;
    protein: number;
    carbohydrates: number;
    fat: number;
  };
  summary_message: string;
}

export interface ProgressEntry {
  id: number;
  user_id: number;
  date: string;
  weight: number | null;
  calories: number | null;
  protein: number | null;
  carbs: number | null;
  fat: number | null;
  notes: string | null;
  created_at?: string;
}

export interface ClinicalGuideline {
  id: string;
  title: string;
  threshold: string;
  clinical_rationale: string;
  recommended_foods: string;
  strictly_avoid: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: UserProfile;
}
