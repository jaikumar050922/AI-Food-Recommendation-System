"use client";

import React, { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { Stethoscope, Sparkles, CheckCircle2, AlertCircle, ArrowRight, ShieldCheck } from "lucide-react";

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

export function AuthView() {
  const { login, register, demoLogin } = useAuth();
  const [tab, setTab] = useState<"login" | "register">("login");

  // Login states
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);

  // Register states
  const [regName, setRegName] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regConfirmPassword, setRegConfirmPassword] = useState("");
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

  const [regLoading, setRegLoading] = useState(false);
  const [regError, setRegError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginLoading(true);
    setLoginError(null);
    try {
      await login({ email: loginEmail, password: loginPassword });
    } catch (err: any) {
      setLoginError(err.message || "Invalid credentials. Please verify your email and password.");
    } finally {
      setLoginLoading(false);
    }
  };

  const handleDemoClick = async () => {
    setLoginLoading(true);
    setLoginError(null);
    try {
      await demoLogin();
    } catch (err: any) {
      setLoginError(err.message || "Failed to log in with demo account.");
    } finally {
      setLoginLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (regPassword !== regConfirmPassword) {
      setRegError("Passwords do not match. Please ensure both passwords match.");
      return;
    }

    setRegLoading(true);
    setRegError(null);
    try {
      await register({
        name: regName,
        email: regEmail,
        password: regPassword,
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
    } catch (err: any) {
      setRegError(err.message || "Registration failed. An account with this email may already exist.");
    } finally {
      setRegLoading(false);
    }
  };

  const toggleAllergy = (a: string) => {
    setAllergies((prev) =>
      prev.includes(a) ? prev.filter((x) => x !== a) : [...prev, a]
    );
  };

  const toggleRestriction = (r: string) => {
    setDietaryRestrictions((prev) =>
      prev.includes(r) ? prev.filter((x) => x !== r) : [...prev, r]
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8">
      {/* Top Brand Banner */}
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="inline-flex items-center gap-2 bg-teal-100 text-teal-800 text-xs font-bold px-3 py-1.5 rounded-full border border-teal-200 mb-3 shadow-sm">
          <Stethoscope className="w-4 h-4 text-teal-700" />
          <span>Clinical Nutrition & Food Portal</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
          Welcome to Nutri<span className="text-teal-700">AI</span>
        </h1>
        <p className="mt-2 text-sm text-slate-600 font-medium">
          Personalized clinical nutrition and metabolic health companion.
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-xl">
        {/* Tab switcher */}
        <div className="flex border-b border-slate-200 bg-white rounded-t-2xl px-6 pt-4 gap-6">
          <button
            onClick={() => setTab("login")}
            className={`pb-3 text-sm font-bold border-b-2 transition-all ${
              tab === "login"
                ? "border-teal-700 text-teal-800"
                : "border-transparent text-slate-500 hover:text-slate-700"
            }`}
          >
            🔑 Sign In to Portal
          </button>
          <button
            onClick={() => setTab("register")}
            className={`pb-3 text-sm font-bold border-b-2 transition-all ${
              tab === "register"
                ? "border-teal-700 text-teal-800"
                : "border-transparent text-slate-500 hover:text-slate-700"
            }`}
          >
            📝 Create New Account
          </button>
        </div>

        {/* Tab 1: Login */}
        {tab === "login" && (
          <div className="bg-white py-8 px-6 sm:px-10 shadow-lg rounded-b-2xl border-x border-b border-slate-200 space-y-6">
            <div>
              <h2 className="text-xl font-black text-slate-900">Sign In</h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Enter your credentials to access your personalized nutritional dashboard.
              </p>
            </div>

            {loginError && (
              <div className="bg-rose-50 border border-rose-200 text-rose-700 p-3 rounded-xl text-xs font-bold flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{loginError}</span>
              </div>
            )}

            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
                <input
                  type="email"
                  required
                  placeholder="e.g. demo@nutriai.com"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  className="w-full text-xs font-medium border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Password</label>
                <input
                  type="password"
                  required
                  placeholder="Enter your password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  className="w-full text-xs font-medium border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>

              <button
                type="submit"
                disabled={loginLoading}
                className="w-full brand-gradient text-white text-xs font-bold py-3 rounded-xl shadow-md hover:opacity-95 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <span>{loginLoading ? "Authenticating..." : "Sign In to Your Portal"}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>

            <div className="relative border-t border-slate-200 pt-5">
              <div className="bg-teal-50 border border-teal-200 rounded-xl p-3.5 text-xs text-teal-900 space-y-1">
                <div className="font-extrabold flex items-center gap-1.5 text-teal-800">
                  <Sparkles className="w-4 h-4 text-teal-600" />
                  <span>Instant Demo Access (Pre-Configured Profile):</span>
                </div>
                <div>Email: <code className="bg-teal-100 px-1 py-0.5 rounded font-mono font-bold">demo@nutriai.com</code></div>
                <div>Password: <code className="bg-teal-100 px-1 py-0.5 rounded font-mono font-bold">Demo@1234</code></div>
              </div>

              <button
                type="button"
                onClick={handleDemoClick}
                disabled={loginLoading}
                className="w-full mt-3 bg-white hover:bg-slate-50 text-teal-800 font-extrabold text-xs py-2.5 px-4 rounded-xl border border-teal-300 shadow-sm transition-colors flex items-center justify-center gap-2"
              >
                <span>1-Click Demo Account Sign In</span>
                <Sparkles className="w-3.5 h-3.5 text-teal-600" />
              </button>
            </div>
          </div>
        )}

        {/* Tab 2: Register */}
        {tab === "register" && (
          <div className="bg-white py-8 px-6 sm:px-10 shadow-lg rounded-b-2xl border-x border-b border-slate-200 space-y-6">
            <div>
              <h2 className="text-xl font-black text-slate-900">Register New Patient Profile</h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Provide biometrics and dietary restrictions to build your personalized AI nutrition model.
              </p>
            </div>

            {regError && (
              <div className="bg-rose-50 border border-rose-200 text-rose-700 p-3 rounded-xl text-xs font-bold flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{regError}</span>
              </div>
            )}

            <form onSubmit={handleRegister} className="space-y-5 text-xs">
              {/* Account Credentials */}
              <div className="space-y-3">
                <h3 className="font-extrabold text-slate-900 uppercase tracking-wider text-[11px] border-b border-slate-100 pb-1">
                  1. Account Credentials
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Full Name *</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. Alex Morgan"
                      value={regName}
                      onChange={(e) => setRegName(e.target.value)}
                      className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Email Address *</label>
                    <input
                      type="email"
                      required
                      placeholder="e.g. alex@example.com"
                      value={regEmail}
                      onChange={(e) => setRegEmail(e.target.value)}
                      className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Password (min 6 chars) *</label>
                    <input
                      type="password"
                      required
                      minLength={6}
                      value={regPassword}
                      onChange={(e) => setRegPassword(e.target.value)}
                      className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Confirm Password *</label>
                    <input
                      type="password"
                      required
                      minLength={6}
                      value={regConfirmPassword}
                      onChange={(e) => setRegConfirmPassword(e.target.value)}
                      className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    />
                  </div>
                </div>
              </div>

              {/* Physical Biometrics */}
              <div className="space-y-3">
                <h3 className="font-extrabold text-slate-900 uppercase tracking-wider text-[11px] border-b border-slate-100 pb-1">
                  2. Physical Biometrics
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Age (Years) *</label>
                    <input
                      type="number"
                      min={10}
                      max={120}
                      value={age}
                      onChange={(e) => setAge(parseInt(e.target.value) || 28)}
                      className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Gender *</label>
                    <select
                      value={gender}
                      onChange={(e) => setGender(e.target.value)}
                      className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    >
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Height (cm) *</label>
                    <input
                      type="number"
                      step="0.5"
                      value={heightCm}
                      onChange={(e) => setHeightCm(parseFloat(e.target.value) || 172)}
                      className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Weight (kg) *</label>
                    <input
                      type="number"
                      step="0.5"
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
                      value={targetWeight}
                      onChange={(e) => setTargetWeight(parseFloat(e.target.value) || 70)}
                      className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Goal *</label>
                    <select
                      value={primaryGoal}
                      onChange={(e) => setPrimaryGoal(e.target.value)}
                      className="w-full border border-slate-300 rounded-lg p-2 font-medium focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    >
                      <option value="Weight Loss">Weight Loss (-500 kcal)</option>
                      <option value="Weight Gain">Weight Gain (+400 kcal)</option>
                      <option value="Maintain Weight">Maintain Weight</option>
                    </select>
                  </div>
                </div>

                <div>
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
              </div>

              {/* Preferences & Allergies */}
              <div className="space-y-3">
                <h3 className="font-extrabold text-slate-900 uppercase tracking-wider text-[11px] border-b border-slate-100 pb-1">
                  3. Preferences & Medical Filters
                </h3>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Dietary Preference *</label>
                  <div className="flex gap-4">
                    <label className="inline-flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="reg_preference"
                        value="Vegetarian"
                        checked={foodPreference === "Vegetarian"}
                        onChange={() => setFoodPreference("Vegetarian")}
                        className="accent-teal-700"
                      />
                      <span className="font-semibold text-slate-800">Vegetarian</span>
                    </label>
                    <label className="inline-flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="reg_preference"
                        value="Non-Vegetarian"
                        checked={foodPreference === "Non-Vegetarian"}
                        onChange={() => setFoodPreference("Non-Vegetarian")}
                        className="accent-teal-700"
                      />
                      <span className="font-semibold text-slate-800">Non-Vegetarian</span>
                    </label>
                  </div>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Common Allergens (Strict Exclusion)</label>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5">
                    {COMMON_ALLERGIES.map((a) => (
                      <label
                        key={a}
                        className={`flex items-center gap-1.5 p-2 rounded-lg border cursor-pointer text-[11px] ${
                          allergies.includes(a)
                            ? "bg-rose-50 border-rose-300 text-rose-900 font-bold"
                            : "bg-slate-50 border-slate-200 text-slate-700"
                        }`}
                      >
                        <input
                          type="checkbox"
                          checked={allergies.includes(a)}
                          onChange={() => toggleAllergy(a)}
                          className="accent-rose-700"
                        />
                        <span>{a}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Prescribed Medical Restrictions</label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                    {DOCTOR_RESTRICTIONS.map((r) => (
                      <label
                        key={r}
                        className={`flex items-center gap-1.5 p-2 rounded-lg border cursor-pointer text-[11px] ${
                          dietaryRestrictions.includes(r)
                            ? "bg-purple-50 border-purple-300 text-purple-900 font-bold"
                            : "bg-slate-50 border-slate-200 text-slate-700"
                        }`}
                      >
                        <input
                          type="checkbox"
                          checked={dietaryRestrictions.includes(r)}
                          onChange={() => toggleRestriction(r)}
                          className="accent-purple-700"
                        />
                        <span>{r}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>

              <button
                type="submit"
                disabled={regLoading}
                className="w-full brand-gradient text-white text-xs font-bold py-3.5 rounded-xl shadow-md hover:opacity-95 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <span>{regLoading ? "Building Nutrition Model..." : "Register & Build AI Nutrition Model"}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
