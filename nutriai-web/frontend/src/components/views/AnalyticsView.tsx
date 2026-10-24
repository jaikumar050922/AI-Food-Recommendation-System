"use client";

import React from "react";
import { useAuth } from "@/context/AuthContext";
import { PieChart, Activity, Target, Flame, ShieldAlert, Heart } from "lucide-react";

export function AnalyticsView() {
  const { user } = useAuth();

  if (!user) return null;

  // Macro calorie ratios
  const proteinCals = user.target_protein * 4.0;
  const carbCals = user.target_carbs * 4.0;
  const fatCals = user.target_fat * 9.0;
  const totalMacroCals = Math.max(proteinCals + carbCals + fatCals, 1);

  const proteinPct = Math.round((proteinCals / totalMacroCals) * 100);
  const carbPct = Math.round((carbCals / totalMacroCals) * 100);
  const fatPct = Math.round((fatCals / totalMacroCals) * 100);

  // Deficit / Surplus calculation
  const calDifference = Math.round(user.target_calories - user.tdee);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 bg-teal-100 text-teal-800 text-xs font-bold px-3 py-1 rounded-full mb-1">
          <PieChart className="w-3.5 h-3.5 text-teal-700" />
          <span>Biometric & Metabolic Science</span>
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight">
          Clinical Nutrition Analytics
        </h2>
        <p className="text-sm text-slate-600 mt-0.5">
          Detailed breakdown of your metabolic energy expenditure and macronutrient caloric proportions.
        </p>
      </div>

      {/* Top Analytics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Macronutrient Calorie Breakdown */}
        <div className="card-elevated p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700">
              Macronutrient Calorie Ratio
            </h3>
            <span className="text-xs font-bold text-teal-700">100% Macro Split</span>
          </div>

          {/* Visual Bar Split */}
          <div className="w-full h-4 rounded-full flex overflow-hidden shadow-inner">
            <div
              style={{ width: `${proteinPct}%` }}
              className="bg-blue-600 h-full transition-all"
              title={`Protein: ${proteinPct}%`}
            />
            <div
              style={{ width: `${carbPct}%` }}
              className="bg-sky-400 h-full transition-all"
              title={`Carbs: ${carbPct}%`}
            />
            <div
              style={{ width: `${fatPct}%` }}
              className="bg-amber-400 h-full transition-all"
              title={`Fat: ${fatPct}%`}
            />
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex justify-between items-center p-2 rounded-lg bg-blue-50/70 border border-blue-100">
              <span className="font-bold text-blue-900 flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
                Protein ({user.target_protein}g)
              </span>
              <span className="font-extrabold text-blue-800">{proteinPct}% ({Math.round(proteinCals)} kcal)</span>
            </div>

            <div className="flex justify-between items-center p-2 rounded-lg bg-sky-50/70 border border-sky-100">
              <span className="font-bold text-sky-900 flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-sky-400"></span>
                Carbohydrates ({user.target_carbs}g)
              </span>
              <span className="font-extrabold text-sky-800">{carbPct}% ({Math.round(carbCals)} kcal)</span>
            </div>

            <div className="flex justify-between items-center p-2 rounded-lg bg-amber-50/70 border border-amber-100">
              <span className="font-bold text-amber-900 flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                Healthy Fats ({user.target_fat}g)
              </span>
              <span className="font-extrabold text-amber-800">{fatPct}% ({Math.round(fatCals)} kcal)</span>
            </div>
          </div>
        </div>

        {/* Energy Expenditure Diagnostics */}
        <div className="card-elevated p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700">
              Metabolic Expenditure
            </h3>
            <span className="text-xs font-bold text-purple-700">Mifflin-St Jeor</span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-xl bg-purple-50/70 border border-purple-100">
              <div className="text-[11px] font-bold text-purple-900 uppercase">Basal Metabolic Rate (BMR)</div>
              <div className="text-2xl font-black text-purple-900 mt-0.5">{user.bmr} kcal</div>
              <div className="text-[11px] text-purple-700 mt-1">
                Resting energy burned at complete physical rest.
              </div>
            </div>

            <div className="p-3 rounded-xl bg-teal-50/70 border border-teal-100">
              <div className="text-[11px] font-bold text-teal-900 uppercase">
                Total Daily Energy Expenditure (TDEE)
              </div>
              <div className="text-2xl font-black text-teal-900 mt-0.5">{user.tdee} kcal</div>
              <div className="text-[11px] text-teal-700 mt-1">
                Factor: {user.activity_level.split("(")[0]}
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <div className="flex justify-between items-center font-bold">
                <span className="text-slate-700">Goal Caloric Delta:</span>
                <span className={calDifference < 0 ? "text-purple-700" : calDifference > 0 ? "text-teal-700" : "text-blue-700"}>
                  {calDifference > 0 ? `+${calDifference} kcal (Surplus)` : `${calDifference} kcal (Deficit)`}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Clinical Micronutrient Thresholds */}
        <div className="card-elevated p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700">
              Clinical Guardrails
            </h3>
            <span className="text-xs font-bold text-emerald-700">AHA / WHO Target</span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-xl bg-emerald-50/70 border border-emerald-100">
              <div className="text-[11px] font-bold text-emerald-900 uppercase">Minimum Dietary Fiber</div>
              <div className="text-2xl font-black text-emerald-900 mt-0.5">{user.target_fiber}g / day</div>
              <div className="text-[11px] text-emerald-700 mt-1">
                Optimizes glycemic curve and gastrointestinal microbiome motility.
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <div className="text-[11px] font-bold text-slate-700 uppercase">Sodium Ceiling</div>
              <div className="text-xl font-black text-slate-900 mt-0.5">&le; 2,300 mg / day</div>
              <div className="text-[11px] text-slate-500 mt-1">
                DASH diet limit for arterial pressure regulation.
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <div className="text-[11px] font-bold text-slate-700 uppercase">Free Sugar Ceiling</div>
              <div className="text-xl font-black text-slate-900 mt-0.5">&le; 25 g / day</div>
              <div className="text-[11px] text-slate-500 mt-1">
                WHO guideline to prevent insulin resistance and steatohepatitis.
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Per Meal Energy Distribution */}
      <div className="card-elevated p-5">
        <h3 className="text-base font-bold text-slate-900 mb-2">
          Recommended Per-Meal Caloric Split
        </h3>
        <p className="text-xs text-slate-500 mb-4">
          Standard circadian chrononutrition distribution for sustained glucose control.
        </p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Breakfast", pct: "25%", kcal: Math.round(user.target_calories * 0.25), icon: "🌅" },
            { label: "Lunch", pct: "35%", kcal: Math.round(user.target_calories * 0.35), icon: "☀️" },
            { label: "Dinner", pct: "30%", kcal: Math.round(user.target_calories * 0.30), icon: "🌙" },
            { label: "Snack", pct: "10%", kcal: Math.round(user.target_calories * 0.10), icon: "🍎" },
          ].map((meal) => (
            <div key={meal.label} className="p-4 rounded-xl bg-slate-50 border border-slate-100 text-center">
              <div className="text-2xl mb-1">{meal.icon}</div>
              <div className="text-xs font-bold uppercase text-slate-500">{meal.label}</div>
              <div className="text-lg font-black text-slate-900 mt-0.5">{meal.kcal} kcal</div>
              <div className="text-xs font-semibold text-teal-700 mt-0.5">{meal.pct} of daily energy</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
