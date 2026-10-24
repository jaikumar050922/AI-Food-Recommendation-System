# NutriAI &mdash; Production Full-Stack Clinical Food Recommendation Platform

A production-ready full-stack web application converted from Streamlit into a modern **Next.js 16 (TypeScript + Tailwind CSS)** frontend and **Python FastAPI** serverless backend, deployable seamlessly on **Vercel**.

---

## 🌟 Key Features Preserved & Enhanced

- **Clinical Biometrics Engine**: Computes Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) via the validated **Mifflin-St Jeor equation**, establishing precise target calories and macronutrient splits (Protein, Carbohydrates, Healthy Fats, Dietary Fiber).
- **NearestNeighbors Recommendation Engine**: Employs Scikit-Learn `StandardScaler` and `NearestNeighbors` (Euclidean distance on 5D nutritional vectors) coupled with **Cosine Similarity & Calorie Proximity** match scoring.
- **Strict Multi-Layered Safety Filters**: Enforces dietary preferences (Vegetarian vs Non-Vegetarian), common allergen exclusion (Dairy, Gluten, Nuts, Eggs, Seafood, Soy), custom ingredient avoidance, and physician-prescribed dietary restrictions (Low Sodium &le; 320mg, Low Sugar &le; 8g, Low Fat &le; 15g, Low Carb &le; 35g, Gluten-Free, High Fiber &ge; 4g, Renal &le; 300mg sodium / &le; 25g protein).
- **Synchronized 4-Meal Daily Planner**: Auto-assembles Breakfast, Lunch, Dinner, and Snack plans with composite macronutrient adherence diagnostics.
- **Personal Progress & Weight Tracker**: Log daily weight and caloric intake with chronological history and trend visualization.
- **Curated 60-Item Clinical Food Database**: Real-time searchable and filterable database by category, diet type, and allergen thresholds.
- **Enterprise-Grade Security**: Passwords hashed with **PBKDF2-HMAC-SHA256** (100,000 iterations + random salt); stateless authentication using cryptographically signed **HMAC-SHA256 JSON Web Tokens (JWT)**.
- **Zero-Overwrite Coexistence**: The original Streamlit implementation (`app.py`, `recommender.py`, `db.py`) remains 100% intact and runnable in the root directory.

---

## 🏗️ Project Architecture

```
AI-Food-Recommendation-System/
├── app.py                      # Original Streamlit app (PRESERVED & INTACT)
├── recommender.py              # Original recommender (PRESERVED)
├── db.py                       # Original DB (PRESERVED)
├── data/                       # Original food dataset and sqlite db
│
└── nutriai-web/                # Modern Production Full-Stack Web Application
    ├── vercel.json             # Vercel deployment & routing configuration
    ├── .env.example            # Environment variables template
    ├── start_dev.bat           # Windows 1-click local development launcher
    ├── start_dev.ps1           # PowerShell local development launcher
    │
    ├── backend/                # Python FastAPI Backend API
    │   ├── api/
    │   │   └── index.py        # Vercel serverless entrypoint
    │   ├── core/
    │   │   ├── config.py       # Pydantic Settings & environment variables
    │   │   ├── database.py     # SQLite + PostgreSQL database manager
    │   │   ├── deps.py         # JWT authentication dependencies
    │   │   └── security.py     # PBKDF2 hashing & JWT issuance
    │   ├── data/
    │   │   └── foods.csv       # Preserved clinical foods dataset (60 items)
    │   ├── models/
    │   │   ├── food.py         # Pydantic food and recommendation schemas
    │   │   └── user.py         # Pydantic user, auth, and progress schemas
    │   ├── routers/
    │   │   ├── auth.py         # Login, register, demo account
    │   │   ├── profile.py      # Profile retrieval and biometrics updates
    │   │   ├── recommend.py    # Category recommendations & 4-meal planner
    │   │   ├── foods.py        # Catalog search & filtering
    │   │   ├── progress.py     # Daily weight/macro progress tracking
    │   │   └── guidelines.py   # Clinical reference thresholds
    │   ├── services/
    │   │   ├── nutrition.py    # BMR, TDEE, BMI, macro target math
    │   │   └── recommender.py  # Scikit-learn NearestNeighbors engine
    │   ├── main.py             # FastAPI app initialization & CORS
    │   ├── requirements.txt    # Python dependencies
    │   └── test_backend.py     # Automated backend unit test suite
    │
    └── frontend/               # Next.js 16 TypeScript Frontend
        ├── src/
        │   ├── app/
        │   │   ├── globals.css # Healthcare SaaS light-teal theme
        │   │   ├── layout.tsx  # AuthProvider wrapper & root metadata
        │   │   └── page.tsx    # Reactive single-page app router
        │   ├── components/
        │   │   ├── DisclaimerBanner.tsx  # Clinical safety banner
        │   │   ├── FoodCard.tsx          # Macro pills, allergens, quick log
        │   │   ├── Header.tsx            # Sticky header with status pills
        │   │   ├── KpiCard.tsx           # Metric cards
        │   │   ├── Sidebar.tsx           # Navigation & patient badge
        │   │   └── views/
        │   │       ├── AboutView.tsx           # Architecture & formulas
        │   │       ├── AnalyticsView.tsx       # Macro donut & BMR/TDEE
        │   │       ├── AuthView.tsx            # Login & registration portal
        │   │       ├── DashboardView.tsx       # 6 KPI cards & meal preview
        │   │       ├── FoodDatabaseView.tsx    # Searchable catalog
        │   │       ├── GuidelinesView.tsx      # Medical reference cards
        │   │       ├── MealPlannerView.tsx     # 4-meal plan & adherence
        │   │       ├── ProfileView.tsx         # Patient biometrics editor
        │   │       └── ProgressView.tsx        # Daily logger & trend graph
        │   ├── context/
        │   │   └── AuthContext.tsx # Reactive auth state & session storage
        │   └── lib/
        │       ├── api.ts          # Typed REST API client
        │       └── types.ts        # TypeScript interfaces
        ├── package.json
        ├── tsconfig.json
        └── next.config.ts          # Development proxy rewrites
```

---

## 🗄️ Database Architecture: Production vs. Local

### The Serverless File System Constraint
On Vercel, serverless function instances are **stateless and ephemeral**:
- Filesystem writes outside `/tmp` are strictly read-only.
- The `/tmp` directory is wiped whenever a serverless container cold-starts, terminates, or scales across regions.
- Consequently, a local SQLite file in a serverless function cannot guarantee persistence across sessions.

### The Production Solution
`nutriai-web` implements a dual-mode database engine:
1. **Local Development (Default)**: Automatically uses a local SQLite file (`nutriai-web/backend/data/nutriai.db`). Zero cloud configuration needed to run locally.
2. **Production Vercel Deployment**: Connect a managed PostgreSQL database (e.g., free tier on **Neon**, **Supabase**, or **Vercel Postgres**) by setting the `DATABASE_URL` environment variable:
   ```bash
   DATABASE_URL=postgresql://username:password@ep-host.pooler.region.neon.tech/nutriaidb?sslmode=require
   ```
   When deployed on Vercel without an external database, the engine automatically falls back to `/tmp/nutriai.db` to prevent read-only filesystem errors and auto-seeds the demo account.

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- Node.js &ge; 18
- Python &ge; 3.10

### 1. Install Backend Dependencies
```bash
cd nutriai-web/backend
pip install -r requirements.txt
```

### 2. Verify Backend Tests
```bash
python test_backend.py
```
*(All 6 unit tests should output `ALL BACKEND LOGIC TESTS PASSED SUCCESSFULLY!`)*

### 3. Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### 4. Run Development Servers
You can launch both services using the provided launcher:

**Windows Command Prompt:**
```cmd
cd nutriai-web
start_dev.bat
```

**PowerShell:**
```powershell
cd nutriai-web
.\start_dev.ps1
```

**Or manually in two terminals:**
- **Terminal 1 (Backend):**
  ```bash
  cd nutriai-web/backend
  python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
  ```
- **Terminal 2 (Frontend):**
  ```bash
  cd nutriai-web/frontend
  npm run dev
  ```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🔑 Demo Account Credentials

A pre-configured clinical profile is automatically seeded for immediate presentation:
- **Email**: `demo@nutriai.com`
- **Password**: `Demo@1234`
- **1-Click Login**: Simply click the **"1-Click Demo Account Sign In"** button on the portal landing page.

---

## 🌐 Deploying to Vercel

### Step 1: Push Code to GitHub / GitLab
Ensure `nutriai-web/` is committed to your Git repository.

### Step 2: Import Project in Vercel
1. Navigate to [vercel.com/new](https://vercel.com/new) and select your repository.
2. Set the **Root Directory** to `nutriai-web` (or leave as root if deploying the entire repository).
3. Under **Framework Preset**, select **Next.js**.

### Step 3: Configure Environment Variables
In the Vercel project dashboard under **Settings &rarr; Environment Variables**, configure:

| Variable | Recommended Value | Purpose |
| :--- | :--- | :--- |
| `SECRET_KEY` | *(Generate a 64-char hex string)* | Signs and verifies user JWT session tokens |
| `DATABASE_URL` | `postgresql://...` (Neon/Supabase) | Persistent cloud database connection |
| `NEXT_PUBLIC_API_URL` | `/api` | Root for frontend API requests |

### Step 4: Deploy & Verify
1. Click **Deploy**.
2. Once the build completes, test:
   - `https://your-project.vercel.app/` &rarr; Next.js healthcare SaaS UI
   - `https://your-project.vercel.app/api/health` &rarr; `{"status":"healthy","database":"connected"}`
   - Click **1-Click Demo Account Sign In** to verify authentication and NearestNeighbors recommendations.

---

## 📡 API Reference

All endpoints are prefixed with `/api`.

### Authentication
- `POST /api/auth/register` &mdash; Registers user and physical biometrics profile.
- `POST /api/auth/login` &mdash; Validates credentials and returns JWT bearer token.
- `POST /api/auth/demo` &mdash; 1-click authentication as pre-seeded demo user.
- `GET /api/auth/me` &mdash; Returns current authenticated profile and metabolic metrics.

### Profile & Biometrics
- `GET /api/profile` &mdash; Retrieves user profile, BMI, BMR, TDEE, and macro targets.
- `PUT /api/profile` &mdash; Updates age, weight, target weight, allergies, and restrictions.

### Recommendations & Meal Planner
- `GET /api/recommend?category={Breakfast|Lunch|Dinner|Snack}&top_n=5` &mdash; AI NearestNeighbors matches.
- `GET /api/recommend/meal-plan` &mdash; 4-meal full-day plan with adherence diagnostics.

### Food Database
- `GET /api/foods?search={query}&category={cat}&diet_type={type}` &mdash; Searchable catalog.
- `GET /api/foods/categories` &mdash; List unique categories.
- `GET /api/foods/{food_id}` &mdash; Item nutritional breakdown.

### Progress Tracking
- `GET /api/progress` &mdash; Chronological check-in history.
- `POST /api/progress` &mdash; Logs daily weight, calories, and macros.

### Clinical Guidelines
- `GET /api/guidelines` &mdash; Evidence-based medical diet protocols and thresholds.
