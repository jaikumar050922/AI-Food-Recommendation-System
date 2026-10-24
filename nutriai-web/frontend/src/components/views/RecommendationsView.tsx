"use client";

import React, { useState, useEffect, useCallback } from "react";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { FoodItem } from "@/lib/types";
import { FoodCard } from "@/components/FoodCard";
import { Sparkles, Filter, ShieldCheck, AlertCircle } from "lucide-react";

interface RecommendationsViewProps {
  onLogMeal: (item: FoodItem) => void;
}

export function RecommendationsView({ onLogMeal }: RecommendationsViewProps) {
  const { user } = useAuth();
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [topN, setTopN] = useState<number>(5);
  const [loading, setLoading] = useState<boolean>(true);
  const [recs, setRecs] = useState<FoodItem[]>([]);
  const [recsByCategory, setRecsByCategory] = useState<Record<string, FoodItem[]>>({});
  const [filterStats, setFilterStats] = useState<Record<string, number>>({});
  const [error, setError] = useState<string | null>(null);

  const fetchRecommendations = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      if (selectedCategory === "All") {
        const res = await api.recommend.get(undefined, topN);
        setFilterStats(res.filter_stats || {});
        setRecsByCategory(res.recommendations_by_category || {});
        setRecs([]);
      } else {
        const res = await api.recommend.get(selectedCategory, topN);
        setFilterStats(res.filter_stats || {});
        setRecs(res.recommendations || []);
        setRecsByCategory({});
      }
    } catch (err: any) {
      console.error("Failed to fetch recommendations:", err);
      setError(err.message || "Failed to load recommendations");
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, topN]);

  useEffect(() => {
    fetchRecommendations();
  }, [fetchRecommendations]);

  if (!user) return null;

  const categories = ["All", "Breakfast", "Lunch", "Dinner", "Snack"];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 bg-teal-100 text-teal-800 text-xs font-bold px-3 py-1 rounded-full mb-1">
          <Sparkles className="w-3.5 h-3.5 text-teal-700" />
          <span>NearestNeighbors Multi-Vector Matching</span>
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight">
          AI-Based Personalized Meal Recommendations
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          Ranked by composite macro ratio cosine similarity and target calorie proximity.
        </p>
      </div>

      {/* Active Clinical Safety & Preference Summary */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
        <div className="flex items-center justify-between flex-wrap gap-2 mb-2 pb-2 border-b border-slate-100">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-700">
            <Filter className="w-4 h-4 text-teal-700" />
            <span>Active Safety & Clinical Filters</span>
          </div>
          <span className="text-xs font-bold text-teal-800 bg-teal-50 border border-teal-200 px-2.5 py-0.5 rounded-full flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            {filterStats.final_eligible !== undefined
              ? `${filterStats.final_eligible} of ${filterStats.initial || 58} Safe Recipes Active`
              : "Filters Active"}
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="bg-slate-100 text-slate-700 px-2.5 py-1 rounded-md font-semibold">
            🥗 Diet: <strong className="text-slate-900">{user.food_preference}</strong>
          </span>
          {user.allergies && user.allergies.length > 0 && (
            <span className="bg-rose-50 text-rose-700 border border-rose-200 px-2.5 py-1 rounded-md font-semibold">
              🚫 Allergies Filtered: <strong className="text-rose-900">{user.allergies.join(", ")}</strong>
            </span>
          )}
          {user.foods_to_avoid && (
            <span className="bg-amber-50 text-amber-800 border border-amber-200 px-2.5 py-1 rounded-md font-semibold">
              ⚠️ Avoided Ingredients: <strong className="text-amber-900">{user.foods_to_avoid}</strong>
            </span>
          )}
          {user.dietary_restrictions && user.dietary_restrictions.length > 0 && (
            <span className="bg-purple-50 text-purple-700 border border-purple-200 px-2.5 py-1 rounded-md font-semibold">
              🩺 Clinical Prescriptions: <strong className="text-purple-900">{user.dietary_restrictions.join("; ")}</strong>
            </span>
          )}
          {user.doctor_custom_notes && (
            <span className="bg-blue-50 text-blue-700 border border-blue-200 px-2.5 py-1 rounded-md font-semibold">
              📋 Clinical Notes: <strong className="text-blue-900">{user.doctor_custom_notes}</strong>
            </span>
          )}
        </div>
      </div>

      {/* Category Tabs & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-3">
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
          {categories.map((cat) => {
            const isSelected = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-lg text-xs font-bold whitespace-nowrap transition-all ${
                  isSelected
                    ? "brand-gradient text-white shadow-sm"
                    : "bg-white text-slate-700 hover:bg-slate-100 border border-slate-200"
                }`}
              >
                {cat === "All" ? "All Categories" : cat}
              </button>
            );
          })}
        </div>

        <div className="flex items-center gap-2 self-end sm:self-auto text-xs font-bold text-slate-600">
          <span>Show top:</span>
          {[3, 5, 8].map((n) => (
            <button
              key={n}
              onClick={() => setTopN(n)}
              className={`px-2.5 py-1 rounded-md border text-xs font-bold transition-all ${
                topN === n
                  ? "bg-teal-700 text-white border-teal-700"
                  : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
              }`}
            >
              {n}
            </button>
          ))}
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded-xl text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Loading state */}
      {loading ? (
        <div className="py-16 text-center text-sm font-semibold text-slate-500">
          Evaluating food vectors and calculating Euclidean distances...
        </div>
      ) : selectedCategory !== "All" ? (
        /* Single category display */
        recs.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recs.map((item) => (
              <FoodCard key={item.food_id} item={item} onLogMeal={onLogMeal} showMatchScore={true} />
            ))}
          </div>
        ) : (
          <div className="py-12 text-center text-sm text-slate-500 bg-white rounded-xl border border-dashed border-slate-200">
            No foods matched your criteria in {selectedCategory}. Try loosening avoidance keywords in My Profile.
          </div>
        )
      ) : (
        /* All categories display */
        <div className="space-y-8">
          {["Breakfast", "Lunch", "Dinner", "Snack"].map((cat) => {
            const catItems = recsByCategory[cat] || [];
            if (catItems.length === 0) return null;
            return (
              <div key={cat} className="space-y-3">
                <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                  <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-teal-600"></span>
                    <span>{cat} Recommendations</span>
                  </h3>
                  <span className="text-xs font-semibold text-slate-500">
                    Target: {user.per_meal_targets?.[cat]?.calories || 0} kcal
                  </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {catItems.map((item) => (
                    <FoodCard key={item.food_id} item={item} onLogMeal={onLogMeal} showMatchScore={true} />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
