"use client";

import React, { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { MealPlan, FoodItem } from "@/lib/types";
import { FoodCard } from "@/components/FoodCard";
import {
  UtensilsCrossed,
  Printer,
  CheckCircle2,
  AlertCircle,
  PlusCircle,
  Sparkles
} from "lucide-react";

interface MealPlannerViewProps {
  onLogMeal: (item: FoodItem) => void;
}

export function MealPlannerView({ onLogMeal }: MealPlannerViewProps) {
  const { user } = useAuth();
  const [mealPlan, setMealPlan] = useState<MealPlan | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [loggedNotice, setLoggedNotice] = useState<string | null>(null);

  const fetchMealPlan = async () => {
    setLoading(true);
    setError(null);
    try {
      const plan = await api.recommend.getMealPlan();
      setMealPlan(plan);
    } catch (err: any) {
      console.error("Error loading meal plan:", err);
      setError(err.message || "Failed to load meal plan");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMealPlan();
  }, []);

  const handleLogFullDay = async () => {
    if (!mealPlan) return;
    try {
      const today = new Date().toISOString().split("T")[0];
      await api.progress.add({
        date: today,
        weight: user?.weight_kg || null,
        calories: mealPlan.actual_totals.calories,
        protein: mealPlan.actual_totals.protein,
        carbs: mealPlan.actual_totals.carbohydrates,
        fat: mealPlan.actual_totals.fat,
        notes: `Logged entire AI Meal Plan (${mealPlan.summary_message})`,
      });
      setLoggedNotice("Full day meal plan logged to your progress tracking history!");
      setTimeout(() => setLoggedNotice(null), 4000);
    } catch (err: any) {
      alert("Error logging full day: " + err.message);
    }
  };

  if (!user) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 bg-teal-100 text-teal-800 text-xs font-bold px-3 py-1 rounded-full mb-1">
            <UtensilsCrossed className="w-3.5 h-3.5 text-teal-700" />
            <span>Optimal Caloric & Macro Allocation</span>
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight">
            1-Day Balanced Clinical Meal Planner
          </h2>
          <p className="text-sm text-slate-600 mt-0.5">
            Synchronized 4-meal schedule tailored to your BMR/TDEE deficit targets.
          </p>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <button
            onClick={() => window.print()}
            className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-bold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg shadow-sm transition-colors"
          >
            <Printer className="w-4 h-4 text-slate-500" />
            <span>Print Plan</span>
          </button>
          <button
            onClick={handleLogFullDay}
            className="brand-gradient hover:opacity-95 text-white inline-flex items-center gap-1.5 px-4 py-2 text-xs font-bold rounded-lg shadow-sm transition-all"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Log Full Day to Progress</span>
          </button>
        </div>
      </div>

      {loggedNotice && (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 p-3 rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{loggedNotice}</span>
        </div>
      )}

      {error && (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded-xl text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {loading ? (
        <div className="py-20 text-center text-sm font-semibold text-slate-500">
          Assembling 4-meal clinical plan and computing macro adherence...
        </div>
      ) : mealPlan ? (
        <>
          {/* Adherence & Nutrition Comparison Banner */}
          <div className="card-elevated p-5">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4 pb-4 border-b border-slate-100">
              <div>
                <span className="text-xs font-extrabold uppercase tracking-wider text-teal-800">
                  Adherence Diagnostics
                </span>
                <h3 className="text-lg font-bold text-slate-900 mt-0.5">
                  Target vs. Actual Nutritional Intake
                </h3>
              </div>
              <div className="bg-teal-50 border border-teal-200 text-teal-900 px-3.5 py-1.5 rounded-xl text-xs font-bold flex items-center gap-2 self-start md:self-auto">
                <Sparkles className="w-4 h-4 text-teal-700" />
                <span>{mealPlan.summary_message}</span>
              </div>
            </div>

            {/* Macro Comparison Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {/* Calories */}
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                <div className="flex justify-between items-center text-xs font-bold mb-1">
                  <span className="text-slate-600">Calories</span>
                  <span className="text-teal-800 font-extrabold">
                    {mealPlan.adherence_pct.calories}%
                  </span>
                </div>
                <div className="text-lg font-black text-slate-900">
                  {mealPlan.actual_totals.calories}{" "}
                  <span className="text-xs font-medium text-slate-500">
                    / {mealPlan.target_totals.calories} kcal
                  </span>
                </div>
                <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden mt-2">
                  <div
                    className="bg-teal-600 h-full rounded-full transition-all"
                    style={{ width: `${Math.min(mealPlan.adherence_pct.calories, 100)}%` }}
                  />
                </div>
              </div>

              {/* Protein */}
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                <div className="flex justify-between items-center text-xs font-bold mb-1">
                  <span className="text-slate-600">Protein</span>
                  <span className="text-blue-800 font-extrabold">
                    {mealPlan.adherence_pct.protein}%
                  </span>
                </div>
                <div className="text-lg font-black text-slate-900">
                  {mealPlan.actual_totals.protein}g{" "}
                  <span className="text-xs font-medium text-slate-500">
                    / {mealPlan.target_totals.protein}g
                  </span>
                </div>
                <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden mt-2">
                  <div
                    className="bg-blue-600 h-full rounded-full transition-all"
                    style={{ width: `${Math.min(mealPlan.adherence_pct.protein, 100)}%` }}
                  />
                </div>
              </div>

              {/* Carbs */}
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                <div className="flex justify-between items-center text-xs font-bold mb-1">
                  <span className="text-slate-600">Carbohydrates</span>
                  <span className="text-sky-800 font-extrabold">
                    {mealPlan.adherence_pct.carbohydrates}%
                  </span>
                </div>
                <div className="text-lg font-black text-slate-900">
                  {mealPlan.actual_totals.carbohydrates}g{" "}
                  <span className="text-xs font-medium text-slate-500">
                    / {mealPlan.target_totals.carbohydrates}g
                  </span>
                </div>
                <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden mt-2">
                  <div
                    className="bg-sky-600 h-full rounded-full transition-all"
                    style={{ width: `${Math.min(mealPlan.adherence_pct.carbohydrates, 100)}%` }}
                  />
                </div>
              </div>

              {/* Fat */}
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                <div className="flex justify-between items-center text-xs font-bold mb-1">
                  <span className="text-slate-600">Healthy Fats</span>
                  <span className="text-amber-800 font-extrabold">
                    {mealPlan.adherence_pct.fat}%
                  </span>
                </div>
                <div className="text-lg font-black text-slate-900">
                  {mealPlan.actual_totals.fat}g{" "}
                  <span className="text-xs font-medium text-slate-500">
                    / {mealPlan.target_totals.fat}g
                  </span>
                </div>
                <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden mt-2">
                  <div
                    className="bg-amber-600 h-full rounded-full transition-all"
                    style={{ width: `${Math.min(mealPlan.adherence_pct.fat, 100)}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Micronutrients summary */}
            <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap gap-4 text-xs text-slate-600">
              <span>
                Total Dietary Fiber:{" "}
                <strong className="text-emerald-700">{mealPlan.actual_totals.fiber}g</strong>
              </span>
              <span>
                Total Sodium:{" "}
                <strong className="text-slate-800">{mealPlan.actual_totals.sodium_mg}mg</strong>
              </span>
              <span>
                Total Added Sugar:{" "}
                <strong className="text-slate-800">{mealPlan.actual_totals.sugar_g}g</strong>
              </span>
            </div>
          </div>

          {/* Meals Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {["Breakfast", "Lunch", "Dinner", "Snack"].map((cat) => {
              const item = mealPlan.meals[cat];
              const target = user.per_meal_targets?.[cat];

              return (
                <div key={cat} className="flex flex-col space-y-2">
                  <div className="flex items-center justify-between px-1">
                    <span className="text-xs font-black uppercase tracking-wider text-teal-800">
                      {cat}
                    </span>
                    <span className="text-[11px] text-slate-500 font-semibold">
                      Target: {target?.calories || 0} kcal
                    </span>
                  </div>

                  {item ? (
                    <FoodCard item={item} onLogMeal={onLogMeal} showMatchScore={true} />
                  ) : (
                    <div className="card-elevated p-6 text-center text-xs text-slate-500 border-dashed">
                      No matching recipe found for this meal category under current strict filters.
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </>
      ) : null}
    </div>
  );
}
