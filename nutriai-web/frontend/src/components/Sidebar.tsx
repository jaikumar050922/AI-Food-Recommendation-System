"use client";

import React from "react";
import { useAuth } from "@/context/AuthContext";
import {
  LayoutDashboard,
  Sparkles,
  UtensilsCrossed,
  LineChart,
  Search,
  PieChart,
  User,
  BookOpen,
  Info,
  LogOut,
  ShieldCheck
} from "lucide-react";

export type PageId =
  | "dashboard"
  | "recommendations"
  | "planner"
  | "progress"
  | "foods"
  | "analytics"
  | "profile"
  | "guidelines"
  | "about";

interface SidebarProps {
  activePage: PageId;
  onSelectPage: (page: PageId) => void;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
}

export function Sidebar({
  activePage,
  onSelectPage,
  isOpenMobile,
  onCloseMobile,
}: SidebarProps) {
  const { user, logout } = useAuth();

  if (!user) return null;

  const navItems: { id: PageId; label: string; icon: React.ReactNode }[] = [
    { id: "dashboard", label: "Dashboard", icon: <LayoutDashboard className="w-4 h-4" /> },
    { id: "recommendations", label: "AI Recommendations", icon: <Sparkles className="w-4 h-4" /> },
    { id: "planner", label: "Meal Planner", icon: <UtensilsCrossed className="w-4 h-4" /> },
    { id: "progress", label: "My Progress", icon: <LineChart className="w-4 h-4" /> },
    { id: "foods", label: "Food Database", icon: <Search className="w-4 h-4" /> },
    { id: "analytics", label: "Nutrition Analytics", icon: <PieChart className="w-4 h-4" /> },
    { id: "profile", label: "My Profile", icon: <User className="w-4 h-4" /> },
    { id: "guidelines", label: "Medical Guidelines", icon: <BookOpen className="w-4 h-4" /> },
    { id: "about", label: "About & Architecture", icon: <Info className="w-4 h-4" /> },
  ];

  // BMI badge color
  const bmiBadgeClass =
    user.bmi < 18.5
      ? "badge-blue"
      : user.bmi < 25.0
      ? "badge-emerald"
      : user.bmi < 30.0
      ? "badge-amber"
      : "badge-rose";

  return (
    <>
      {/* Mobile backdrop */}
      {isOpenMobile && (
        <div
          className="fixed inset-0 bg-slate-900/40 z-40 lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-white border-r border-slate-200 flex flex-col justify-between transition-transform duration-200 lg:translate-x-0 ${
          isOpenMobile ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="p-4 overflow-y-auto">
          {/* Brand Logo & Name */}
          <div className="flex items-center gap-2.5 px-2 py-3 mb-3 border-b border-slate-100">
            <div className="brand-gradient text-white font-extrabold w-9 h-9 rounded-xl flex items-center justify-center shadow-md">
              🩺
            </div>
            <div>
              <div className="font-extrabold text-lg text-slate-900 tracking-tight leading-none">
                Nutri<span className="text-teal-700">AI</span>
              </div>
              <div className="text-[10px] font-bold text-teal-800 uppercase tracking-wider mt-0.5">
                Clinical Nutrition
              </div>
            </div>
          </div>

          {/* User Profile Badge Card */}
          <div className="bg-teal-50/70 border border-teal-200 rounded-xl p-3 mb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full brand-gradient text-white font-bold flex items-center justify-center text-sm shadow-sm shrink-0">
                {user.name.slice(0, 1).toUpperCase()}
              </div>
              <div className="overflow-hidden">
                <div className="font-bold text-sm text-slate-900 truncate">
                  {user.name}
                </div>
                <div className="text-xs text-slate-500 truncate">{user.email}</div>
              </div>
            </div>

            <div className="flex flex-wrap gap-1 mt-2.5">
              <span
                className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${bmiBadgeClass}`}
              >
                ⚖️ BMI {user.bmi} ({user.bmi_category})
              </span>
              <span className="text-[11px] font-bold px-2 py-0.5 rounded-full badge-purple">
                🎯 {user.primary_goal}
              </span>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-2 mb-1.5">
            Menu Navigation
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const isActive = activePage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onSelectPage(item.id);
                    onCloseMobile();
                  }}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-all ${
                    isActive
                      ? "bg-teal-700 text-white shadow-sm"
                      : "text-slate-700 hover:bg-slate-100 hover:text-slate-900"
                  }`}
                >
                  <span className={isActive ? "text-white" : "text-teal-700"}>
                    {item.icon}
                  </span>
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Bottom user action */}
        <div className="p-4 border-t border-slate-100">
          <button
            onClick={logout}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 text-sm font-bold text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>
    </>
  );
}
