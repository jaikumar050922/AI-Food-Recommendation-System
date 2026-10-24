"use client";

import React, { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { User, CheckCircle2, AlertCircle, Save, Stethoscope, ShieldAlert } from "lucide-react";

const COMMON_ALLERGIES = [
  "Dairy",
  "Peanuts",
  "Nuts",
  "Eggs",
  "Seafood",
  "Gluten",
  "Soy",
];

const DOCTOR_RESTRICTIONS = [
  "Low Sodium / Hypertension Friendly",
  "Low Sugar / Diabetic Friendly",
  "Low Fat / Lipid Friendly",
  "Low Carb",
  "Gluten Free",
  "High Fiber",
  "Renal / Kidney Disease Friendly",
];

export function ProfileView() {
  const { user, updateProfile } = useAuth();

  const [name, setName] = useState("");
  const [age, setAge] = useState(28);
  const [gender, setGender] = useState("Male");
  const [heightCm, setHeightCm] = useState(172);
  const [weightKg, setWeightKg] = useState(70);
  const [targetWeight, setTargetWeight] = useState(70);
  const [activityLevel, setActivityLevel] = useState("Moderately Active (moderate exercise 3-5 days/wk)");
  const [foodPreference, setFoodPreference] = useState("Vegetarian");
  const [primaryGoal, setPrimaryGoal] = useState("Weight Loss");
  const [allergies, setAllergies] = useState<string[]>([]);
  const [customAllergies, setCustomAllergies] = useState("");
  const [foodsToAvoid, setFoodsToAvoid] = useState("");
  const [dietaryRestrictions, setDietaryRestrictions] = useState<string[]>([]);
  const [doctorCustomNotes, setDoctorCustomNotes] = useState("");

  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      setName(user.name || "");
      setAge(user.age || 28);
      setGender(user.gender || "Male");
      setHeightCm(user.height_cm || 172);
      setWeightKg(user.weight_kg || 70);
      setTargetWeight(user.target_weight || user.weight_kg || 70);
      setActivityLevel(user.activity_level || "Moderately Active (moderate exercise 3-5 days/wk)");
      setFoodPreference(user.food_preference || "Vegetarian");
      setPrimaryGoal(user.primary_goal || "Weight Loss");
      setAllergies(user.allergies || []);
      setCustomAllergies(user.custom_allergies || "");
      setFoodsToAvoid(user.foods_to_avoid || "");
      setDietaryRestrictions(user.dietary_restrictions || []);
      setDoctorCustomNotes(user.doctor_custom_notes || "");
    }
  }, [user]);

  const toggleAllergy = (item: string) => {
    setAllergies((prev) =>
      prev.includes(item) ? prev.filter((x) => x !== item) : [...prev, item]
    );
  };

  const toggleRestriction = (item: string) => {
    setDietaryRestrictions((prev) =>
      prev.includes(item) ? prev.filter((x) => x !== item) : [...prev, item]
    );
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    try {
      await updateProfile({
        name,
        age,
        gender,
        height_cm: heightCm,
        weight_kg: weightKg,
        target_weight: targetWeight,
        activity_level: activityLevel,
        food_preference: foodPreference,
        primary_goal: primaryGoal,
        allergies,
        custom_allergies: customAllergies,
        foods_to_avoid: foodsToAvoid,
        dietary_restrictions: dietaryRestrictions,
        doctor_custom_notes: doctorCustomNotes,
      });

      setSuccessMsg("Patient biometric profile and clinical restrictions updated successfully!");
      setTimeout(() => setSuccessMsg(null), 4000);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to update profile");
    } finally {
      setSaving(false);
    }
  };

  if (!user) return null;

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 bg-teal-100 text-teal-800 text-xs font-bold px-3 py-1 rounded-full mb-1">
          <User className="w-3.5 h-3.5 text-teal-700" />
          <span>Biometric & Clinical Profile</span>
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight">
          Patient Profile & Dietary Restrictions
        </h2>
        <p className="text-sm text-slate-600 mt-0.5">
          Modify biometrics, allergies, and physician instructions. Nutrition targets recalculate instantly.
        </p>
      </div>

      {successMsg && (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 p-3.5 rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {errorMsg && (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 p-3.5 rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: Physical Biometrics */}
        <div className="card-elevated p-6 space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-teal-800 border-b border-slate-100 pb-2 flex items-center gap-2">
            <span>👤</span>
            <span>Physical Biometrics & Activity</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Full Name *</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">Age (Years) *</label>
              <input
                type="number"
                min={10}
                max={120}
                required
                value={age}
                onChange={(e) => setAge(parseInt(e.target.value) || 28)}
                className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">Biological Gender *</label>
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
              >
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other / Non-Binary</option>
              </select>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">Height (cm) *</label>
              <input
                type="number"
                step="0.5"
                min={80}
                max={250}
                required
                value={heightCm}
                onChange={(e) => setHeightCm(parseFloat(e.target.value) || 170)}
                className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">Current Weight (kg) *</label>
              <input
                type="number"
                step="0.5"
                min={30}
                max={300}
                required
                value={weightKg}
                onChange={(e) => setWeightKg(parseFloat(e.target.value) || 70)}
                className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">Target Weight (kg) *</label>
              <input
                type="number"
                step="0.5"
                min={30}
                max={300}
                required
                value={targetWeight}
                onChange={(e) => setTargetWeight(parseFloat(e.target.value) || 70)}
                className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            <div className="sm:col-span-2">
              <label className="block font-bold text-slate-700 mb-1">Activity Level *</label>
              <select
                value={activityLevel}
                onChange={(e) => setActivityLevel(e.target.value)}
                className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
              >
                <option value="Sedentary (little to no exercise)">Sedentary (little to no exercise)</option>
                <option value="Lightly Active (light exercise 1-3 days/wk)">Lightly Active (light exercise 1-3 days/wk)</option>
                <option value="Moderately Active (moderate exercise 3-5 days/wk)">Moderately Active (moderate exercise 3-5 days/wk)</option>
                <option value="Very Active (hard exercise 6-7 days/wk)">Very Active (hard exercise 6-7 days/wk)</option>
              </select>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">Primary Nutritional Goal *</label>
              <select
                value={primaryGoal}
                onChange={(e) => setPrimaryGoal(e.target.value)}
                className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
              >
                <option value="Weight Loss">Weight Loss (-500 kcal deficit)</option>
                <option value="Weight Gain">Weight Gain (+400 kcal surplus)</option>
                <option value="Maintain Weight">Maintain Weight (Caloric equilibrium)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 2: Dietary Preferences & Allergies */}
        <div className="card-elevated p-6 space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-teal-800 border-b border-slate-100 pb-2 flex items-center gap-2">
            <span>🥗</span>
            <span>Dietary Preference & Food Allergies</span>
          </h3>

          <div className="space-y-4 text-xs">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Dietary Preference *</label>
              <div className="flex gap-4">
                <label className="inline-flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="preference"
                    value="Vegetarian"
                    checked={foodPreference.toLowerCase() === "vegetarian"}
                    onChange={() => setFoodPreference("Vegetarian")}
                    className="accent-teal-700"
                  />
                  <span className="font-semibold text-slate-800">Vegetarian</span>
                </label>
                <label className="inline-flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="preference"
                    value="Non-Vegetarian"
                    checked={foodPreference.toLowerCase() === "non-vegetarian"}
                    onChange={() => setFoodPreference("Non-Vegetarian")}
                    className="accent-teal-700"
                  />
                  <span className="font-semibold text-slate-800">Non-Vegetarian</span>
                </label>
              </div>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-2">
                Common Allergens (Strict Exclusion)
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {COMMON_ALLERGIES.map((allergy) => (
                  <label
                    key={allergy}
                    className={`flex items-center gap-2 p-2 rounded-lg border cursor-pointer transition-colors ${
                      allergies.includes(allergy)
                        ? "bg-rose-50 border-rose-300 text-rose-900 font-bold"
                        : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100 font-medium"
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={allergies.includes(allergy)}
                      onChange={() => toggleAllergy(allergy)}
                      className="accent-rose-700"
                    />
                    <span>{allergy}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block font-bold text-slate-700 mb-1">
                  Custom Allergies (Comma-separated)
                </label>
                <input
                  type="text"
                  placeholder="e.g. sesame, mustard"
                  value={customAllergies}
                  onChange={(e) => setCustomAllergies(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">
                  Foods to Avoid / Personal Dislikes
                </label>
                <input
                  type="text"
                  placeholder="e.g. mushroom, eggplant, pork"
                  value={foodsToAvoid}
                  onChange={(e) => setFoodsToAvoid(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Section 3: Physician & Clinical Prescriptions */}
        <div className="card-elevated p-6 space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-teal-800 border-b border-slate-100 pb-2 flex items-center gap-2">
            <Stethoscope className="w-4 h-4 text-teal-700" />
            <span>Physician Advice & Dietary Prescriptions</span>
          </h3>

          <div className="space-y-4 text-xs">
            <div>
              <label className="block font-bold text-slate-700 mb-2">
                Prescribed Dietary Restrictions
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {DOCTOR_RESTRICTIONS.map((res) => (
                  <label
                    key={res}
                    className={`flex items-center gap-2 p-2.5 rounded-lg border cursor-pointer transition-colors ${
                      dietaryRestrictions.includes(res)
                        ? "bg-purple-50 border-purple-300 text-purple-900 font-bold"
                        : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100 font-medium"
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={dietaryRestrictions.includes(res)}
                      onChange={() => toggleRestriction(res)}
                      className="accent-purple-700"
                    />
                    <span>{res}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">
                Doctor&apos;s Custom Notes / Clinical Instructions
              </label>
              <textarea
                rows={3}
                placeholder="e.g. Keep daily sodium under 2000mg. Focus on high biological value plant proteins."
                value={doctorCustomNotes}
                onChange={(e) => setDoctorCustomNotes(e.target.value)}
                className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="brand-gradient hover:opacity-95 text-white font-bold text-sm px-6 py-3 rounded-xl shadow-md transition-all flex items-center gap-2 disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? "Saving Biometrics..." : "Update Clinical Profile"}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
