"use client";

import React, { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { DisclaimerBanner } from "@/components/DisclaimerBanner";
import { KpiCard } from "@/components/KpiCard";
import { FoodCard } from "@/components/FoodCard";
import { api } from "@/lib/api";
import { FoodItem, MealPlan } from "@/lib/types";
import { PageId } from "@/components/Sidebar";
import {
  Flame,
  Dumbbell,
  Wheat,
  Droplet,
  Salad,
  Activity,
  ArrowRight,
  ShieldCheck,
  Calendar,
  Sparkles
} from "lucide-react";

interface DashboardViewProps {
  onNavigate: (page: PageId) => void;
  onLogMeal: (item: FoodItem) => void;
}

export function DashboardView({ onNavigate, onLogMeal }: DashboardViewProps) {
  const { user } = useAuth();
  const [mealPlan, setMealPlan] = useState<MealPlan | null>(null);
  const [loadingPlan, setLoadingPlan] = useState(true);

  useEffect(() => {
    async function loadPlan() {
      try {
        const plan = await api.recommend.getMealPlan();
        setMealPlan(plan);
      } catch (err) {
        console.error("Error loading meal plan:", err);
      } finally {
        setLoadingPlan(false);
      }
    }
    loadPlan();
  }, []);

  if (!user) return null;

  // BMI categorization
  const bmiBadgeClass =
    user.bmi < 18.5
      ? "badge-blue"
      : user.bmi < 25.0
      ? "badge-emerald"
      : user.bmi < 30.0
      ? "badge-amber"
      : "badge-rose";

  // Macro calorie percentages
  const proteinCals = user.target_protein * 4.0;
  const proteinPct = Math.round((proteinCals / Math.max(user.target_calories, 1)) * 100);

  const carbCals = user.target_carbs * 4.0;
  const carbPct = Math.round((carbCals / Math.max(user.target_calories, 1)) * 100);

  const fatCals = user.target_fat * 9.0;
  const fatPct = Math.round((fatCals / Math.max(user.target_calories, 1)) * 100);

  return (
    <div className="space-y-6">
      {/* Brand Hero Banner */}
      <div className="brand-gradient text-white rounded-2xl p-6 sm:p-8 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 bg-white/20 text-white text-xs font-bold px-3 py-1 rounded-full backdrop-blur-sm mb-2">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Personalized Clinical Nutrition</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Welcome back, {user.name}!
            </h1>
            <p className="text-teal-100 text-sm mt-1 max-w-xl">
              Your personalized metabolic nutrition targets and AI-curated meal recommendations.
            </p>
          </div>

          <div className="flex sm:flex-col items-center sm:items-end gap-2 text-right">
            <div className="bg-white/10 border border-white/20 rounded-xl px-4 py-2.5 backdrop-blur-sm">
              <div className="text-[11px] font-semibold text-teal-200">Daily Calorie Target</div>
              <div className="text-2xl font-black text-white">{user.target_calories.toLocaleString()} kcal</div>
            </div>
          </div>
        </div>
      </div>

      {/* Clinical Disclaimer */}
      <DisclaimerBanner />

      {/* Status Badges Row */}
      <div className="flex flex-wrap items-center gap-2">
        <span className={`text-xs font-bold px-3 py-1 rounded-full ${bmiBadgeClass}`}>
          ⚖️ {user.bmi_category} (BMI {user.bmi})
        </span>
        <span className="text-xs font-bold px-3 py-1 rounded-full badge-purple">
          🎯 {user.primary_goal}
        </span>
        <span className="text-xs font-bold px-3 py-1 rounded-full badge-emerald">
          🥗 {user.food_preference}
        </span>
        <span className="text-xs font-bold px-3 py-1 rounded-full badge-teal flex items-center gap-1">
          <ShieldCheck className="w-3.5 h-3.5" />
          {user.allergies.length > 0 ? `${user.allergies.length} Allergens Filtered` : "Zero Major Allergens"}
        </span>
      </div>

      {/* 6 KPI Metric Cards */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-base font-bold text-slate-900">
            Daily Metabolic & Macronutrient Targets
          </h3>
          <span className="text-xs font-semibold text-slate-500">
            Mifflin-St Jeor Clinical Standard
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
          <KpiCard
            label="Daily Calories"
            value={`${user.target_calories.toLocaleString()}`}
            sub="kcal / day"
            valueColor="text-teal-700"
            subColor="text-teal-600"
            icon={<Flame className="w-3.5 h-3.5 text-teal-700" />}
          />
          <KpiCard
            label="Protein Target"
            value={`${user.target_protein}g`}
            sub={`${proteinPct}% of calories`}
            valueColor="text-blue-700"
            subColor="text-blue-600"
            icon={<Dumbbell className="w-3.5 h-3.5 text-blue-700" />}
          />
          <KpiCard
            label="Carbohydrates"
            value={`${user.target_carbs}g`}
            sub={`${carbPct}% of calories`}
            valueColor="text-sky-700"
            subColor="text-sky-600"
            icon={<Wheat className="w-3.5 h-3.5 text-sky-700" />}
          />
          <KpiCard
            label="Healthy Fats"
            value={`${user.target_fat}g`}
            sub={`${fatPct}% of calories`}
            valueColor="text-amber-700"
            subColor="text-amber-600"
            icon={<Droplet className="w-3.5 h-3.5 text-amber-700" />}
          />
          <KpiCard
            label="Dietary Fiber"
            value={`${user.target_fiber}g`}
            sub="daily minimum"
            valueColor="text-emerald-700"
            subColor="text-emerald-600"
            icon={<Salad className="w-3.5 h-3.5 text-emerald-700" />}
          />
          <KpiCard
            label="BMR & TDEE"
            value={`${user.bmr} / ${user.tdee}`}
            sub="Basal / Total exp."
            valueColor="text-purple-700"
            subColor="text-purple-600"
            icon={<Activity className="w-3.5 h-3.5 text-purple-700" />}
          />
        </div>
      </div>

      {/* Today's Full Day Meal Plan Preview */}
      <div className="card-elevated p-5 sm:p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-teal-700" />
              <span>Today&apos;s Personalized AI Meal Plan</span>
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Balanced across Breakfast, Lunch, Dinner, and Snack using Scikit-Learn NearestNeighbors
            </p>
          </div>
          <button
            onClick={() => onNavigate("planner")}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-teal-800 hover:text-teal-900 bg-teal-50 hover:bg-teal-100 border border-teal-200 px-3 py-1.5 rounded-lg transition-colors shrink-0"
          >
            <span>Full Plan & Adherence</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {loadingPlan ? (
          <div className="py-8 text-center text-sm text-slate-500">
            Generating optimal nutritional alignment...
          </div>
        ) : mealPlan?.meals ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {["Breakfast", "Lunch", "Dinner", "Snack"].map((cat) => {
              const item = mealPlan.meals[cat];
              if (!item) {
                return (
                  <div key={cat} className="border border-dashed border-slate-200 rounded-xl p-4 text-center">
                    <div className="text-xs font-bold uppercase text-slate-400">{cat}</div>
                    <div className="text-xs text-slate-500 mt-2">No matching item found under current filters</div>
                  </div>
                );
              }
              return (
                <div key={cat} className="flex flex-col">
                  <div className="text-xs font-bold uppercase tracking-wider text-teal-800 mb-1.5 flex items-center justify-between">
                    <span>{cat}</span>
                    <span className="text-[11px] text-slate-500 font-normal">
                      Target: {user.per_meal_targets?.[cat]?.calories || 0} kcal
                    </span>
                  </div>
                  <FoodCard item={item} onLogMeal={onLogMeal} showMatchScore={true} />
                </div>
              );
            })}
          </div>
        ) : (
          <div className="py-6 text-center text-sm text-slate-500">
            Adjust your dietary restrictions or biometrics to generate recommendations.
          </div>
        )}
      </div>

      {/* Quick Action Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div
          onClick={() => onNavigate("recommendations")}
          className="card-elevated p-4 cursor-pointer hover:border-teal-600 transition-all"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-100 text-teal-800 flex items-center justify-center font-bold">
              🤖
            </div>
            <div>
              <div className="font-bold text-sm text-slate-900">Explore AI Recipes</div>
              <div className="text-xs text-slate-500">Filter by category & match score</div>
            </div>
          </div>
        </div>

        <div
          onClick={() => onNavigate("progress")}
          className="card-elevated p-4 cursor-pointer hover:border-teal-600 transition-all"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-800 flex items-center justify-center font-bold">
              📈
            </div>
            <div>
              <div className="font-bold text-sm text-slate-900">Log Daily Weight</div>
              <div className="text-xs text-slate-500">Track progress vs target weight</div>
            </div>
          </div>
        </div>

        <div
          onClick={() => onNavigate("profile")}
          className="card-elevated p-4 cursor-pointer hover:border-teal-600 transition-all"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-800 flex items-center justify-center font-bold">
              👤
            </div>
            <div>
              <div className="font-bold text-sm text-slate-900">Update Biometrics</div>
              <div className="text-xs text-slate-500">Adjust clinical goals & restrictions</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
