"use client";

import React from "react";
import { useAuth } from "@/context/AuthContext";
import { Menu, ShieldCheck, Calendar } from "lucide-react";
import { PageId } from "./Sidebar";

interface HeaderProps {
  activePage: PageId;
  onOpenMobileMenu: () => void;
}

export function Header({ activePage, onOpenMobileMenu }: HeaderProps) {
  const { user } = useAuth();

  const pageTitles: Record<PageId, { title: string; subtitle: string }> = {
    dashboard: {
      title: "Patient Dashboard",
      subtitle: "Personalized metabolic energy targets & AI meal preview",
    },
    recommendations: {
      title: "AI Meal Recommendations",
      subtitle: "Scikit-Learn NearestNeighbors vector similarity matching",
    },
    planner: {
      title: "Clinical Meal Planner",
      subtitle: "1-day synchronized 4-meal plan with macro adherence diagnostics",
    },
    progress: {
      title: "Progress & Intake Tracking",
      subtitle: "Log weight and macronutrients with historical trend analytics",
    },
    foods: {
      title: "Nutritional Catalog & Food Database",
      subtitle: "Curated dataset with clinical allergen & glycemic attributes",
    },
    analytics: {
      title: "Metabolic Nutrition Analytics",
      subtitle: "Macronutrient caloric ratios and BMR/TDEE expenditure modeling",
    },
    profile: {
      title: "Patient Profile & Medical Constraints",
      subtitle: "Biometrics, allergen exclusions, and physician prescriptions",
    },
    guidelines: {
      title: "Medical Nutrition Guidelines",
      subtitle: "Evidence-based protocols for hypertension, diabetes, and CKD",
    },
    about: {
      title: "System Architecture & Mathematics",
      subtitle: "Machine learning algorithms, vector mechanics, and safety guarantees",
    },
  };

  const current = pageTitles[activePage] || {
    title: "NutriAI Portal",
    subtitle: "Clinical Nutrition Recommendation Platform",
  };

  const todayFormatted = new Intl.DateTimeFormat("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date());

  return (
    <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-slate-200 px-4 sm:px-8 py-3.5 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenMobileMenu}
          className="lg:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100 transition-colors"
          aria-label="Open navigation menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <h1 className="text-base sm:text-lg font-black text-slate-900 tracking-tight leading-tight">
            {current.title}
          </h1>
          <p className="text-[11px] text-slate-500 hidden sm:block">
            {current.subtitle}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Date Indicator */}
        <div className="hidden md:flex items-center gap-1.5 text-xs font-semibold text-slate-600 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
          <Calendar className="w-3.5 h-3.5 text-slate-500" />
          <span>{todayFormatted}</span>
        </div>

        {/* Clinical Engine Status */}
        <div className="hidden sm:inline-flex items-center gap-1.5 bg-teal-50 border border-teal-200 text-teal-800 text-xs font-bold px-3 py-1.5 rounded-lg">
          <span className="w-2 h-2 rounded-full bg-teal-600 animate-pulse"></span>
          <span>Engine Active</span>
        </div>

        {/* User initials */}
        {user && (
          <div className="w-8 h-8 rounded-full brand-gradient text-white font-bold text-xs flex items-center justify-center shadow-sm">
            {user.name.slice(0, 1).toUpperCase()}
          </div>
        )}
      </div>
    </header>
  );
}
