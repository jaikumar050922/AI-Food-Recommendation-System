import { UserProfile, FoodItem, MealPlan, ProgressEntry, ClinicalGuideline, AuthResponse } from "./types";

const BASE_URL = "/api";

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("nutriai_token");
}

export function setStoredToken(token: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem("nutriai_token", token);
  }
}

export function removeStoredToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("nutriai_token");
    localStorage.removeItem("nutriai_user");
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getStoredToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const url = `${BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorDetail = "An unexpected error occurred";
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || errJson.message || JSON.stringify(errJson);
    } catch {
      errorDetail = `HTTP ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export const api = {
  // Authentication
  auth: {
    login: (credentials: { email: string; password: string }) =>
      request<AuthResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify(credentials),
      }),

    register: (userData: any) =>
      request<AuthResponse>("/auth/register", {
        method: "POST",
        body: JSON.stringify(userData),
      }),

    demoLogin: () =>
      request<AuthResponse>("/auth/demo", {
        method: "POST",
      }),

    getMe: () => request<UserProfile>("/auth/me"),
  },

  // Profile Management
  profile: {
    get: () => request<UserProfile>("/profile"),
    update: (data: Partial<UserProfile>) =>
      request<UserProfile>("/profile", {
        method: "PUT",
        body: JSON.stringify(data),
      }),
  },

  // Recommendations & Meal Planner
  recommend: {
    get: (category?: string, top_n: number = 5) => {
      const params = new URLSearchParams();
      if (category && category !== "All") params.append("category", category);
      params.append("top_n", top_n.toString());
      return request<{
        filter_stats: Record<string, number>;
        category?: string;
        target?: Record<string, number>;
        recommendations?: FoodItem[];
        recommendations_by_category?: Record<string, FoodItem[]>;
      }>(`/recommend?${params.toString()}`);
    },

    getMealPlan: () => request<MealPlan>("/recommend/meal-plan"),
  },

  // Food Database
  foods: {
    get: (params: {
      search?: string;
      category?: string;
      diet_type?: string;
      allergen_free?: string;
      max_calories?: number;
      limit?: number;
    } = {}) => {
      const sp = new URLSearchParams();
      if (params.search) sp.append("search", params.search);
      if (params.category && params.category !== "All") sp.append("category", params.category);
      if (params.diet_type && params.diet_type !== "All") sp.append("diet_type", params.diet_type);
      if (params.allergen_free && params.allergen_free !== "None") sp.append("allergen_free", params.allergen_free);
      if (params.max_calories) sp.append("max_calories", params.max_calories.toString());
      if (params.limit) sp.append("limit", params.limit.toString());
      return request<{ total_count: number; items: FoodItem[] }>(`/foods?${sp.toString()}`);
    },

    getCategories: () => request<string[]>("/foods/categories"),
  },

  // Progress Tracking
  progress: {
    get: () => request<ProgressEntry[]>("/progress"),
    add: (entry: {
      date: string;
      weight?: number | null;
      calories?: number | null;
      protein?: number | null;
      carbs?: number | null;
      fat?: number | null;
      notes?: string;
    }) =>
      request<{ success: boolean; message: string }>("/progress", {
        method: "POST",
        body: JSON.stringify(entry),
      }),
  },

  // Guidelines
  guidelines: {
    get: () => request<ClinicalGuideline[]>("/guidelines"),
  },
};
