"use client";

import React from "react";
import { AlertCircle } from "lucide-react";

export function DisclaimerBanner() {
  return (
    <div className="disclaimer-card flex items-start gap-3 my-4">
      <AlertCircle className="w-5 h-5 text-teal-700 shrink-0 mt-0.5" />
      <div className="text-sm text-slate-700 leading-relaxed">
        <strong className="text-teal-900 font-bold">Clinical Safety Notice: </strong>
        NutriAI is an educational nutritional guidance platform and <strong>does not diagnose diseases or prescribe medical diets</strong>.
        For individuals receiving medical treatment or managing chronic conditions, the system strictly applies dietary restrictions
        <strong> explicitly entered by you or provided by your qualified healthcare professional</strong>.
      </div>
    </div>
  );
}
