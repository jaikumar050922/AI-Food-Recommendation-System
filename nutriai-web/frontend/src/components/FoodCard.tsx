"use client";

import React from "react";
import { FoodItem } from "@/lib/types";
import { PlusCircle, Sparkles, AlertTriangle, ShieldCheck } from "lucide-react";

interface FoodCardProps {
  item: FoodItem;
  onLogMeal?: (item: FoodItem) => void;
  showMatchScore?: boolean;
}

export function FoodCard({ item, onLogMeal, showMatchScore = true }: FoodCardProps) {
  const isVeg = item.diet_type.toLowerCase() === "vegetarian";
  const hasAllergens = item.allergens && item.allergens.toLowerCase() !== "none";

  return (
    <div className="card-elevated p-5 flex flex-col justify-between">
      <div>
        {/* Card Header */}
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${
                isVeg ? "bg-emerald-100 text-emerald-800 border border-emerald-200" : "bg-amber-100 text-amber-800 border border-amber-200"
              }`}>
                {item.diet_type}
              </span>
              <span className="text-[11px] font-semibold bg-slate-100 text-slate-700 px-2 py-0.5 rounded-full border border-slate-200">
                {item.category}
              </span>
            </div>
            <h4 className="text-base font-bold text-slate-900 leading-snug">{item.food_name}</h4>
          </div>

          {showMatchScore && item.match_score !== undefined && (
            <div className="brand-gradient text-white font-extrabold text-xs px-2.5 py-1 rounded-full shadow-sm whitespace-nowrap shrink-0">
              {item.match_score}% Match
            </div>
          )}
        </div>

        {/* Description */}
        <p className="text-xs text-slate-600 mt-2 leading-relaxed">{item.description}</p>

        {/* AI Rationale */}
        {item.ai_rationale && (
          <div className="bg-teal-50/80 border border-teal-200 text-teal-800 rounded-lg p-2.5 text-xs font-medium mt-3 flex items-start gap-2">
            <Sparkles className="w-3.5 h-3.5 text-teal-600 shrink-0 mt-0.5" />
            <span>{item.ai_rationale}</span>
          </div>
        )}

        {/* Macro Pills */}
        <div className="flex flex-wrap gap-1.5 mt-3 text-xs font-semibold">
          <span className="bg-slate-100 text-slate-800 px-2.5 py-1 rounded-md border border-slate-200">
            🔥 {item.calories} kcal
          </span>
          <span className="bg-blue-50 text-blue-800 px-2 py-1 rounded-md border border-blue-200">
            🥩 {item.protein}g P {item.protein_pct ? `(${item.protein_pct}%)` : ""}
          </span>
          <span className="bg-sky-50 text-sky-800 px-2 py-1 rounded-md border border-sky-200">
            🌾 {item.carbohydrates}g C {item.carb_pct ? `(${item.carb_pct}%)` : ""}
          </span>
          <span className="bg-amber-50 text-amber-800 px-2 py-1 rounded-md border border-amber-200">
            🥑 {item.fat}g F {item.fat_pct ? `(${item.fat_pct}%)` : ""}
          </span>
          <span className="bg-emerald-50 text-emerald-800 px-2 py-1 rounded-md border border-emerald-200">
            🥗 {item.fiber}g Fiber
          </span>
        </div>

        {/* Micronutrients & Allergens */}
        <div className="mt-3 flex items-center justify-between text-[11px] text-slate-500 border-t border-slate-100 pt-2.5">
          <div>
            Sodium: <strong className="text-slate-700">{item.sodium_mg}mg</strong> | Sugar: <strong className="text-slate-700">{item.sugar_g}g</strong>
          </div>
          {hasAllergens ? (
            <span className="text-rose-600 font-semibold flex items-center gap-1">
              <AlertTriangle className="w-3 h-3" />
              {item.allergens}
            </span>
          ) : (
            <span className="text-emerald-700 font-semibold flex items-center gap-1">
              <ShieldCheck className="w-3 h-3" />
              No Major Allergens
            </span>
          )}
        </div>
      </div>

      {/* Action footer */}
      {onLogMeal && (
        <div className="mt-4 pt-3 border-t border-slate-100">
          <button
            onClick={() => onLogMeal(item)}
            className="w-full text-xs font-bold text-teal-800 hover:text-teal-900 bg-teal-50 hover:bg-teal-100 border border-teal-200 py-2 px-3 rounded-lg flex items-center justify-center gap-1.5 transition-colors"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            Quick-Log to Today&apos;s Nutrition
          </button>
        </div>
      )}
    </div>
  );
}
