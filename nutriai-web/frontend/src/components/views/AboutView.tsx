"use client";

import React from "react";
import { Info, Cpu, Database, Stethoscope, Lock, Server } from "lucide-react";

export function AboutView() {
  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 bg-teal-100 text-teal-800 text-xs font-bold px-3 py-1 rounded-full mb-1">
          <Info className="w-3.5 h-3.5 text-teal-700" />
          <span>System Architecture & Mathematical Principles</span>
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight">
          About NutriAI Platform
        </h2>
        <p className="text-sm text-slate-600 mt-0.5">
          Production-grade clinical nutrition intelligence combining deterministic metabolic equations with scikit-learn nearest neighbors.
        </p>
      </div>

      {/* Architecture Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* ML Engine */}
        <div className="card-elevated p-5 space-y-2">
          <div className="flex items-center gap-2 text-teal-800 font-bold text-sm">
            <Cpu className="w-5 h-5 text-teal-700" />
            <span>Scikit-Learn NearestNeighbors Engine</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Foods are embedded in a 5-dimensional nutritional vector space comprising <em>Calories</em>, <em>Protein</em>, <em>Carbohydrates</em>, <em>Fat</em>, and <em>Fiber</em>. Features are normalized via <code>StandardScaler</code> to ensure scale-invariance across grams and kilocalories. Unsupervised <code>NearestNeighbors</code> with Euclidean metric retrieves candidate matches for per-meal targets.
          </p>
        </div>

        {/* Cosine Similarity & Match Scoring */}
        <div className="card-elevated p-5 space-y-2">
          <div className="flex items-center gap-2 text-teal-800 font-bold text-sm">
            <Cpu className="w-5 h-5 text-teal-700" />
            <span>Cosine Similarity & Match Scoring</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            To reward harmonious macronutrient proportions, candidate items undergo cosine similarity analysis on their macro ratios:
            <br />
            <code>Match Score = (0.60 &times; CosineSimilarity + 0.40 &times; CalorieProximity) &times; 100%</code>
          </p>
        </div>

        {/* Mifflin-St Jeor Metabolic Formula */}
        <div className="card-elevated p-5 space-y-2">
          <div className="flex items-center gap-2 text-teal-800 font-bold text-sm">
            <Stethoscope className="w-5 h-5 text-teal-700" />
            <span>Mifflin-St Jeor Clinical Equation</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Basal Metabolic Rate is determined via the clinically validated Mifflin-St Jeor formula:
            <br />
            <code>BMR (Men) = 10 &times; Weight(kg) + 6.25 &times; Height(cm) - 5 &times; Age + 5</code>
            <br />
            <code>BMR (Women) = 10 &times; Weight(kg) + 6.25 &times; Height(cm) - 5 &times; Age - 161</code>
          </p>
        </div>

        {/* Full-Stack Architecture */}
        <div className="card-elevated p-5 space-y-2">
          <div className="flex items-center gap-2 text-teal-800 font-bold text-sm">
            <Server className="w-5 h-5 text-teal-700" />
            <span>Production Vercel Cloud Stack</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Frontend is architected in <strong>Next.js 14/15 with TypeScript</strong> and Tailwind CSS. The backend runs <strong>Python FastAPI</strong> serverless functions natively supported on Vercel. Database layer abstracts both <strong>PostgreSQL</strong> (Neon/Supabase) via <code>DATABASE_URL</code> and local development <strong>SQLite</strong>.
          </p>
        </div>
      </div>

      {/* Security & Authentication */}
      <div className="card-elevated p-5 space-y-3">
        <div className="flex items-center gap-2 text-slate-900 font-bold text-sm">
          <Lock className="w-5 h-5 text-teal-700" />
          <span>Security & Credential Integrity</span>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          Passwords are encrypted using <strong>PBKDF2-HMAC-SHA256</strong> with a cryptographically secure random 16-byte salt and 100,000 hashing iterations, strictly preventing plaintext credential exposure. Client sessions communicate using cryptographically signed <strong>HMAC-SHA256 JSON Web Tokens (JWT)</strong> transmitted via standard Authorization Bearer headers.
        </p>
      </div>
    </div>
  );
}
