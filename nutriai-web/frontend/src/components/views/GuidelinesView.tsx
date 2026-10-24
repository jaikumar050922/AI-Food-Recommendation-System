"use client";

import React, { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { ClinicalGuideline } from "@/lib/types";
import { BookOpen, AlertCircle, ShieldAlert, CheckCircle2 } from "lucide-react";

export function GuidelinesView() {
  const [guidelines, setGuidelines] = useState<ClinicalGuideline[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchGuidelines() {
      try {
        const data = await api.guidelines.get();
        setGuidelines(data);
      } catch (err) {
        console.error("Failed to load guidelines:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchGuidelines();
  }, []);

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 bg-teal-100 text-teal-800 text-xs font-bold px-3 py-1 rounded-full mb-1">
          <BookOpen className="w-3.5 h-3.5 text-teal-700" />
          <span>Evidence-Based Clinical Nutrition</span>
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight">
          Medical Guidelines & Prescribed Protocols
        </h2>
        <p className="text-sm text-slate-600 mt-0.5">
          Standardized nutritional thresholds applied across NutriAI algorithms for chronic metabolic management.
        </p>
      </div>

      {loading ? (
        <div className="py-16 text-center text-xs font-semibold text-slate-500">
          Loading clinical guidelines and reference values...
        </div>
      ) : (
        <div className="space-y-4">
          {guidelines.map((g) => (
            <div key={g.id} className="card-elevated p-6 space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-teal-600"></span>
                  <span>{g.title}</span>
                </h3>
                <span className="text-xs font-extrabold text-teal-800 bg-teal-50 border border-teal-200 px-3 py-1 rounded-full self-start sm:self-auto">
                  Threshold: {g.threshold}
                </span>
              </div>

              <div>
                <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-0.5">
                  Clinical Rationale
                </div>
                <p className="text-xs text-slate-700 leading-relaxed font-medium">
                  {g.clinical_rationale}
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
                <div className="p-3 rounded-xl bg-emerald-50/70 border border-emerald-100">
                  <div className="font-bold text-emerald-900 flex items-center gap-1.5 mb-1">
                    <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                    <span>Prioritized Therapeutic Foods</span>
                  </div>
                  <p className="text-emerald-800 font-medium leading-relaxed">
                    {g.recommended_foods}
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-rose-50/70 border border-rose-100">
                  <div className="font-bold text-rose-900 flex items-center gap-1.5 mb-1">
                    <AlertCircle className="w-4 h-4 text-rose-700" />
                    <span>Strict Clinical Contraindications</span>
                  </div>
                  <p className="text-rose-800 font-medium leading-relaxed">
                    {g.strictly_avoid}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
