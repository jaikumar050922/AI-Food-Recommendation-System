"use client";

import React from "react";

interface KpiCardProps {
  label: string;
  value: string | number;
  sub: string;
  valueColor?: string;
  subColor?: string;
  icon?: React.ReactNode;
}

export function KpiCard({
  label,
  value,
  sub,
  valueColor = "text-teal-800",
  subColor = "text-teal-600",
  icon,
}: KpiCardProps) {
  return (
    <div className="card-elevated p-4 text-center flex flex-col justify-center h-full">
      <div className="flex items-center justify-center gap-1.5 text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
        {icon}
        <span>{label}</span>
      </div>
      <div className={`text-2xl font-extrabold tracking-tight ${valueColor}`}>
        {value}
      </div>
      <div className={`text-xs font-semibold mt-1 ${subColor}`}>{sub}</div>
    </div>
  );
}
