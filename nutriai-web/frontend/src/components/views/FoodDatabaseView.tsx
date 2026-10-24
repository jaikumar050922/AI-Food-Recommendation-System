"use client";

import React, { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api";
import { FoodItem } from "@/lib/types";
import { FoodCard } from "@/components/FoodCard";
import { Search, Filter, RotateCcw } from "lucide-react";

interface FoodDatabaseViewProps {
  onLogMeal: (item: FoodItem) => void;
}

export function FoodDatabaseView({ onLogMeal }: FoodDatabaseViewProps) {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [dietType, setDietType] = useState("All");
  const [allergenFree, setAllergenFree] = useState("None");
  const [maxCalories, setMaxCalories] = useState<number>(600);

  const [foods, setFoods] = useState<FoodItem[]>([]);
  const [totalCount, setTotalCount] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);

  const loadFoods = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.foods.get({
        search,
        category,
        diet_type: dietType,
        allergen_free: allergenFree,
        max_calories: maxCalories,
        limit: 100,
      });
      setFoods(res.items || []);
      setTotalCount(res.total_count || 0);
    } catch (err) {
      console.error("Failed to load food database:", err);
    } finally {
      setLoading(false);
    }
  }, [search, category, dietType, allergenFree, maxCalories]);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadFoods();
    }, 250);
    return () => clearTimeout(timer);
  }, [loadFoods]);

  const resetFilters = () => {
    setSearch("");
    setCategory("All");
    setDietType("All");
    setAllergenFree("None");
    setMaxCalories(600);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 bg-teal-100 text-teal-800 text-xs font-bold px-3 py-1 rounded-full mb-1">
          <Search className="w-3.5 h-3.5 text-teal-700" />
          <span>Curated Clinical Database</span>
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight">
          Food Database & Nutritional Catalog
        </h2>
        <p className="text-sm text-slate-600 mt-0.5">
          Explore nutritional macros, glycemic density, and clinical allergy attributes across all 60 curated items.
        </p>
      </div>

      {/* Filter Toolbar */}
      <div className="card-elevated p-5 space-y-4">
        {/* Search Input */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            placeholder="Search by food name, description, or ingredient (e.g., salmon, quinoa, lentils)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 text-xs font-medium border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:outline-none bg-slate-50/50"
          />
        </div>

        {/* Dropdown Filters */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          <div>
            <label className="block font-bold text-slate-700 mb-1">Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
            >
              <option value="All">All Categories</option>
              <option value="Breakfast">Breakfast</option>
              <option value="Lunch">Lunch</option>
              <option value="Dinner">Dinner</option>
              <option value="Snack">Snack</option>
            </select>
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">Dietary Preference</label>
            <select
              value={dietType}
              onChange={(e) => setDietType(e.target.value)}
              className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
            >
              <option value="All">All Types</option>
              <option value="Vegetarian">Vegetarian</option>
              <option value="Non-Vegetarian">Non-Vegetarian</option>
            </select>
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">Exclude Allergen</label>
            <select
              value={allergenFree}
              onChange={(e) => setAllergenFree(e.target.value)}
              className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
            >
              <option value="None">None (Show All)</option>
              <option value="Dairy">Exclude Dairy</option>
              <option value="Gluten">Exclude Gluten</option>
              <option value="Nuts">Exclude Nuts</option>
              <option value="Eggs">Exclude Eggs</option>
              <option value="Seafood">Exclude Seafood</option>
              <option value="Soy">Exclude Soy</option>
            </select>
          </div>

          <div>
            <div className="flex justify-between font-bold text-slate-700 mb-1">
              <span>Max Calories</span>
              <span className="text-teal-700">{maxCalories} kcal</span>
            </div>
            <input
              type="range"
              min={150}
              max={650}
              step={25}
              value={maxCalories}
              onChange={(e) => setMaxCalories(parseInt(e.target.value))}
              className="w-full accent-teal-700 cursor-pointer"
            />
          </div>
        </div>

        <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
          <span className="font-semibold text-slate-600">
            Showing <strong className="text-slate-900">{foods.length}</strong> of {totalCount} matching foods
          </span>
          <button
            onClick={resetFilters}
            className="text-slate-500 hover:text-slate-800 font-bold flex items-center gap-1 transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset Filters
          </button>
        </div>
      </div>

      {/* Foods Grid */}
      {loading ? (
        <div className="py-16 text-center text-xs font-semibold text-slate-500">
          Querying food catalog...
        </div>
      ) : foods.length === 0 ? (
        <div className="card-elevated p-12 text-center text-xs text-slate-500">
          No food items matched your search and filter parameters. Try broadening your filter criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {foods.map((item) => (
            <FoodCard key={item.food_id} item={item} onLogMeal={onLogMeal} showMatchScore={false} />
          ))}
        </div>
      )}
    </div>
  );
}
