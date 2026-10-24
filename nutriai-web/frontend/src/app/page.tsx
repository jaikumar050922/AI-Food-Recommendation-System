"use client";

import React, { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { Sidebar, PageId } from "@/components/Sidebar";
import { Header } from "@/components/Header";
import { AuthView } from "@/components/views/AuthView";
import { DashboardView } from "@/components/views/DashboardView";
import { RecommendationsView } from "@/components/views/RecommendationsView";
import { MealPlannerView } from "@/components/views/MealPlannerView";
import { ProgressView } from "@/components/views/ProgressView";
import { FoodDatabaseView } from "@/components/views/FoodDatabaseView";
import { AnalyticsView } from "@/components/views/AnalyticsView";
import { ProfileView } from "@/components/views/ProfileView";
import { GuidelinesView } from "@/components/views/GuidelinesView";
import { AboutView } from "@/components/views/AboutView";
import { FoodItem } from "@/lib/types";
import { api } from "@/lib/api";
import { CheckCircle2, Stethoscope } from "lucide-react";

export default function Home() {
  const { user, loading } = useAuth();
  const [activePage, setActivePage] = useState<PageId>("dashboard");
  const [mobileOpen, setMobileOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const handleLogMeal = async (item: FoodItem) => {
    try {
      const today = new Date().toISOString().split("T")[0];
      await api.progress.add({
        date: today,
        calories: item.calories,
        protein: item.protein,
        carbs: item.carbohydrates,
        fat: item.fat,
        notes: `Logged meal: ${item.food_name} (${item.category})`,
      });
      setToastMessage(`Logged "${item.food_name}" (${item.calories} kcal) to today's progress!`);
      setTimeout(() => setToastMessage(null), 4000);
    } catch (err: any) {
      alert("Error logging meal: " + err.message);
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
        <div className="w-14 h-14 rounded-2xl brand-gradient text-white flex items-center justify-center shadow-lg animate-pulse mb-4">
          <Stethoscope className="w-8 h-8" />
        </div>
        <div className="text-base font-extrabold text-slate-800">
          Loading NutriAI Clinical Workspace...
        </div>
        <div className="text-xs text-slate-500 mt-1">
          Validating cryptographic session & biometric model...
        </div>
      </div>
    );
  }

  // Unauthenticated: render high-contrast light healthcare Auth portal
  if (!user) {
    return <AuthView />;
  }

  // Authenticated workspace
  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar navigation */}
      <Sidebar
        activePage={activePage}
        onSelectPage={setActivePage}
        isOpenMobile={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
      />

      {/* Main content area */}
      <div className="lg:pl-64 flex flex-col flex-1 min-w-0">
        <Header
          activePage={activePage}
          onOpenMobileMenu={() => setMobileOpen(true)}
        />

        {/* Global Toast Notification */}
        {toastMessage && (
          <div className="fixed bottom-6 right-6 z-50 bg-teal-800 text-white px-4 py-3 rounded-xl shadow-xl flex items-center gap-2.5 text-xs font-bold border border-teal-600 animate-bounce">
            <CheckCircle2 className="w-4 h-4 text-teal-300 shrink-0" />
            <span>{toastMessage}</span>
          </div>
        )}

        <main className="p-4 sm:p-8 flex-1 max-w-7xl w-full mx-auto">
          {activePage === "dashboard" && (
            <DashboardView onNavigate={setActivePage} onLogMeal={handleLogMeal} />
          )}
          {activePage === "recommendations" && (
            <RecommendationsView onLogMeal={handleLogMeal} />
          )}
          {activePage === "planner" && (
            <MealPlannerView onLogMeal={handleLogMeal} />
          )}
          {activePage === "progress" && <ProgressView />}
          {activePage === "foods" && (
            <FoodDatabaseView onLogMeal={handleLogMeal} />
          )}
          {activePage === "analytics" && <AnalyticsView />}
          {activePage === "profile" && <ProfileView />}
          {activePage === "guidelines" && <GuidelinesView />}
          {activePage === "about" && <AboutView />}
        </main>

        {/* Clinical SaaS Footer */}
        <footer className="border-t border-slate-200 bg-white py-5 px-6 text-center text-xs text-slate-500">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
            <div className="font-semibold text-slate-700">
              NutriAI &copy; {new Date().getFullYear()} &mdash; Clinical Nutrition & AI-Based Recommendation System
            </div>
            <div className="text-[11px] text-slate-400">
              Mifflin-St Jeor Engine &bull; Scikit-Learn Vector Architecture &bull; Vercel Serverless Ready
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
