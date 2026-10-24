"use client";

import React, { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { ProgressEntry } from "@/lib/types";
import {
  LineChart,
  PlusCircle,
  TrendingDown,
  TrendingUp,
  Target,
  CheckCircle2,
  AlertCircle
} from "lucide-react";

export function ProgressView() {
  const { user, refreshProfile } = useAuth();
  const [history, setHistory] = useState<ProgressEntry[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Form fields
  const [dateStr, setDateStr] = useState<string>(new Date().toISOString().split("T")[0]);
  const [weight, setWeight] = useState<string>("");
  const [calories, setCalories] = useState<string>("");
  const [protein, setProtein] = useState<string>("");
  const [carbs, setCarbs] = useState<string>("");
  const [fat, setFat] = useState<string>("");
  const [notes, setNotes] = useState<string>("");

  const loadHistory = async () => {
    try {
      const data = await api.progress.get();
      setHistory(data);
    } catch (err: any) {
      console.error("Failed to load progress:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    try {
      await api.progress.add({
        date: dateStr,
        weight: weight ? parseFloat(weight) : null,
        calories: calories ? parseFloat(calories) : null,
        protein: protein ? parseFloat(protein) : null,
        carbs: carbs ? parseFloat(carbs) : null,
        fat: fat ? parseFloat(fat) : null,
        notes,
      });

      setSuccessMsg("Daily progress successfully recorded!");
      // Reset form
      setWeight("");
      setCalories("");
      setProtein("");
      setCarbs("");
      setFat("");
      setNotes("");

      // Refresh data
      await loadHistory();
      await refreshProfile();
      setTimeout(() => setSuccessMsg(null), 4000);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to log progress");
    } finally {
      setSubmitting(false);
    }
  };

  if (!user) return null;

  // Weight analytics
  const firstEntry = history.length > 0 ? history[0] : null;
  const latestEntry = history.length > 0 ? history[history.length - 1] : null;
  const startingWeight = firstEntry?.weight || user.weight_kg;
  const currentWeight = latestEntry?.weight || user.weight_kg;
  const targetWeight = user.target_weight || user.weight_kg;
  const weightDiff = Math.round((currentWeight - startingWeight) * 10) / 10;
  const toGoal = Math.round((currentWeight - targetWeight) * 10) / 10;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 bg-teal-100 text-teal-800 text-xs font-bold px-3 py-1 rounded-full mb-1">
          <LineChart className="w-3.5 h-3.5 text-teal-700" />
          <span>Biometric & Intake Tracking</span>
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight">
          Personal Progress & Clinical Analytics
        </h2>
        <p className="text-sm text-slate-600 mt-0.5">
          Log daily weight and macronutrients to observe adherence trends over time.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="card-elevated p-4">
          <div className="text-xs font-bold uppercase text-slate-500 mb-1">Starting Weight</div>
          <div className="text-2xl font-black text-slate-900">{startingWeight} kg</div>
          <div className="text-xs text-slate-500 mt-1">Recorded on registration</div>
        </div>

        <div className="card-elevated p-4">
          <div className="text-xs font-bold uppercase text-slate-500 mb-1">Current Weight</div>
          <div className="text-2xl font-black text-teal-700">{currentWeight} kg</div>
          <div className="text-xs font-bold text-teal-600 mt-1 flex items-center gap-1">
            {weightDiff < 0 ? <TrendingDown className="w-3.5 h-3.5" /> : <TrendingUp className="w-3.5 h-3.5" />}
            {weightDiff > 0 ? `+${weightDiff} kg` : `${weightDiff} kg`} from start
          </div>
        </div>

        <div className="card-elevated p-4">
          <div className="text-xs font-bold uppercase text-slate-500 mb-1">Target Weight</div>
          <div className="text-2xl font-black text-blue-700">{targetWeight} kg</div>
          <div className="text-xs font-semibold text-blue-600 mt-1 flex items-center gap-1">
            <Target className="w-3.5 h-3.5" />
            {toGoal > 0 ? `${toGoal} kg remaining` : "Goal achieved!"}
          </div>
        </div>

        <div className="card-elevated p-4">
          <div className="text-xs font-bold uppercase text-slate-500 mb-1">Logged Days</div>
          <div className="text-2xl font-black text-purple-700">{history.length}</div>
          <div className="text-xs text-purple-600 font-semibold mt-1">Active tracking sessions</div>
        </div>
      </div>

      {/* Trend Visualizer (Simple SVG Line Graph) */}
      {history.length > 1 && (
        <div className="card-elevated p-5">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700 mb-3">
            Weight Trajectory Over Time (kg)
          </h3>
          <div className="h-40 w-full flex items-end gap-2 pt-6 pb-2 border-b border-slate-200">
            {history.map((h, i) => {
              const w = h.weight || user.weight_kg;
              // Normalize height between 20px and 120px
              const minW = Math.min(...history.map((x) => x.weight || user.weight_kg)) - 1;
              const maxW = Math.max(...history.map((x) => x.weight || user.weight_kg)) + 1;
              const pct = maxW === minW ? 50 : ((w - minW) / (maxW - minW)) * 100;

              return (
                <div key={h.id || i} className="flex-1 flex flex-col items-center gap-1 h-full justify-end group">
                  <span className="text-[10px] font-bold text-teal-800 opacity-0 group-hover:opacity-100 transition-opacity">
                    {w}kg
                  </span>
                  <div
                    style={{ height: `${Math.max(pct, 15)}%` }}
                    className="w-full bg-teal-600 rounded-t-md hover:bg-teal-500 transition-all cursor-pointer shadow-sm"
                  />
                  <span className="text-[9px] text-slate-500 whitespace-nowrap overflow-hidden text-ellipsis max-w-full">
                    {h.date.slice(5)}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Form & Table Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Progress Logging Form */}
        <div className="card-elevated p-5 lg:col-span-1">
          <h3 className="text-base font-bold text-slate-900 mb-1 flex items-center gap-2">
            <PlusCircle className="w-4 h-4 text-teal-700" />
            <span>Log Daily Health Metrics</span>
          </h3>
          <p className="text-xs text-slate-500 mb-4">
            Record weight and intake for today or any past date.
          </p>

          {successMsg && (
            <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 p-2.5 rounded-lg text-xs font-bold flex items-center gap-2 mb-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>{successMsg}</span>
            </div>
          )}

          {errorMsg && (
            <div className="bg-rose-50 border border-rose-200 text-rose-700 p-2.5 rounded-lg text-xs font-bold flex items-center gap-2 mb-3">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Date *</label>
              <input
                type="date"
                required
                value={dateStr}
                onChange={(e) => setDateStr(e.target.value)}
                className="w-full text-xs font-medium border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Weight (kg)</label>
                <input
                  type="number"
                  step="0.1"
                  placeholder="e.g. 76.5"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  className="w-full text-xs font-medium border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Calories (kcal)</label>
                <input
                  type="number"
                  step="1"
                  placeholder="e.g. 1950"
                  value={calories}
                  onChange={(e) => setCalories(e.target.value)}
                  className="w-full text-xs font-medium border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Protein (g)</label>
                <input
                  type="number"
                  step="0.5"
                  placeholder="e.g. 140"
                  value={protein}
                  onChange={(e) => setProtein(e.target.value)}
                  className="w-full text-xs font-medium border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Carbs (g)</label>
                <input
                  type="number"
                  step="0.5"
                  placeholder="e.g. 180"
                  value={carbs}
                  onChange={(e) => setCarbs(e.target.value)}
                  className="w-full text-xs font-medium border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Fat (g)</label>
                <input
                  type="number"
                  step="0.5"
                  placeholder="e.g. 55"
                  value={fat}
                  onChange={(e) => setFat(e.target.value)}
                  className="w-full text-xs font-medium border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Clinical / Workout Notes</label>
              <textarea
                rows={2}
                placeholder="e.g. Felt high energy, completed 45m strength training."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="w-full text-xs font-medium border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full brand-gradient text-white text-xs font-bold py-2.5 rounded-lg shadow-sm hover:opacity-95 transition-all disabled:opacity-50"
            >
              {submitting ? "Saving..." : "Save Daily Entry"}
            </button>
          </form>
        </div>

        {/* History Table */}
        <div className="card-elevated p-5 lg:col-span-2 overflow-hidden flex flex-col">
          <h3 className="text-base font-bold text-slate-900 mb-1">Historical Log Records</h3>
          <p className="text-xs text-slate-500 mb-4">
            Chronological audit of all user check-ins.
          </p>

          {loading ? (
            <div className="py-12 text-center text-xs text-slate-500">Loading progress data...</div>
          ) : history.length === 0 ? (
            <div className="py-12 text-center text-xs text-slate-500 border border-dashed border-slate-200 rounded-lg">
              No progress entries recorded yet. Add your first entry on the left!
            </div>
          ) : (
            <div className="overflow-x-auto flex-1">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-400 font-bold uppercase tracking-wider">
                    <th className="py-2 px-3">Date</th>
                    <th className="py-2 px-3">Weight</th>
                    <th className="py-2 px-3">Calories</th>
                    <th className="py-2 px-3">Macros (P/C/F)</th>
                    <th className="py-2 px-3">Notes</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {history.map((row) => (
                    <tr key={row.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-2.5 px-3 font-bold text-slate-900">{row.date}</td>
                      <td className="py-2.5 px-3 font-semibold text-teal-800">
                        {row.weight ? `${row.weight} kg` : "—"}
                      </td>
                      <td className="py-2.5 px-3 font-semibold text-slate-800">
                        {row.calories ? `${row.calories} kcal` : "—"}
                      </td>
                      <td className="py-2.5 px-3 text-slate-600">
                        {row.protein || row.carbs || row.fat
                          ? `${row.protein || 0}g / ${row.carbs || 0}g / ${row.fat || 0}g`
                          : "—"}
                      </td>
                      <td className="py-2.5 px-3 text-slate-500 max-w-xs truncate">
                        {row.notes || "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
