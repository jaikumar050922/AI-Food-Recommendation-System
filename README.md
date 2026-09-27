# 🥗 NutriAI - Personalized Food Recommendation & Healthcare Platform

An intelligent, modern healthcare web application built with **Python**, **Pandas**, **Scikit-learn**, **Streamlit**, and **SQLite**.

The system features **persistent user authentication**, **patient profile management**, **dynamic metabolic target calculation**, **machine-learning meal recommendation**, **1-day meal planning**, and **personal progress tracking**.

---

## 🌟 Key Features

1. **Secure Authentication & Session Management**:
   - **Login & Registration** with secure PBKDF2-HMAC-SHA256 password hashing.
   - Persistent SQLite database (`data/nutriai.db`) with parameterized queries.
   - Strict **user data isolation**: each user only sees and modifies their own profile and progress records.
   - Pre-seeded **demo account** for 1-click evaluation.

2. **Personalized Health Profile**:
   - Stores Age, Gender, Height, Current Weight, Goal Weight, Activity Level, Diet Preference, Goal, Allergies, Dislikes, and Doctor Guidelines.
   - Dedicated **👤 My Profile** page to view and edit profile details, which dynamically updates the database and recalculates nutrition targets in real-time.

3. **Scientific Metabolic Calculations (Mifflin-St Jeor)**:
   - Basal Metabolic Rate (BMR) & Total Daily Energy Expenditure (TDEE).
   - Goal-directed caloric deficit (Weight Loss), surplus (Weight Gain), or maintenance.
   - Dynamic per-meal distribution: Breakfast (25%), Lunch (35%), Dinner (30%), Snack (10%).

4. **Multi-Stage Clinical & Safety Filtering**:
   - Vegetarian vs Non-Vegetarian enforcement.
   - Strict allergen shield (Dairy, Gluten, Nuts, Seafood, Eggs, Soy, etc.).
   - Ingredient dislike exclusion.
   - Doctor-prescribed clinical thresholds: Low Sodium (≤ 320mg), Low Sugar / Diabetic (≤ 8g), Low Fat, Low Carb, Gluten-Free, Renal Friendly.

5. **Scikit-Learn Machine Learning Recommender**:
   - 5D feature standardization using `StandardScaler`.
   - `NearestNeighbors` Euclidean distance matching in normalized nutritional space.
   - Cosine Similarity macronutrient alignment.
   - Transparent **AI Recommendation Reason** explaining why each item matches the patient's goal.

6. **1-Day Balanced Meal Planner**:
   - Assembles Breakfast, Lunch, Dinner, and Snack into an orchestrated daily menu.
   - Target vs Actual comparison table and interactive progress bars for calories, protein, carbs, fat, and fiber.
   - One-click Download Meal Plan (TXT).

7. **📈 My Progress Tracking**:
   - Daily logging form for Weight, Calories, Protein, Carbs, Fat, and workout notes.
   - Summary metrics: Starting Weight, Current Weight, Distance to Target Goal, Total Change.
   - Interactive Altair charts: **Weight Trajectory Over Time** and **Calorie Adherence vs Target**.
   - Complete historical log table.

8. **Food Database Explorer & Visual Analytics**:
   - Search dishes by keyword, ingredient, or clinical tag.
   - Filter by category and diet type.
   - Dual view: Interactive formatted data table and visual cards grid.
   - Altair donut chart for caloric macronutrient split and meal-by-meal calorie comparisons.

---

## ⚠️ Important Medical & Healthcare Disclaimer

> **PLEASE NOTE:**  
> This software is an educational and lifestyle tool and **does NOT diagnose diseases or prescribe medical diets**.  
> For individuals receiving medical treatment or managing chronic conditions, the application only applies restrictions **explicitly entered by the user or provided by their licensed physician, dietitian, or healthcare professional**.  
> Always consult a qualified medical professional before beginning any new diet or exercise regimen.

---

## 📁 Project Structure

```
AI-Food-Recommendation-System/
├── data/
│   ├── foods.csv              # Curated 58-item dataset with nutritional stats, allergens & tags
│   └── nutriai.db             # SQLite database (users, profiles, progress logs)
├── db.py                      # Database module: SQLite, PBKDF2 hashing, user CRUD, progress logs
├── create_dataset.py          # Script to generate/rebuild sample food dataset
├── recommender.py             # Machine learning recommendation engine (BMR, filters, Scikit-Learn)
├── test_system.py             # Full automated test suite (auth, profile, progress, data isolation)
├── app.py                     # Multi-page Streamlit web application
├── requirements.txt           # Project dependencies
└── README.md                  # Comprehensive setup & user documentation
```

---

## 🛠️ Installation & Setup Instructions

### 1. Prerequisites
- Python 3.9+
- `pip` package manager

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated System Tests
Verify that database operations, authentication, profile loading, recommendation algorithms, and data isolation pass all checks:
```bash
python test_system.py
```

---

## 🚀 Running the Web Application

Launch the application:

```bash
streamlit run app.py
```

Open your browser at:
```
http://localhost:8501
```

---

## 🔑 Demo Account Credentials

For quick evaluation without manual registration, you can use the pre-seeded demo account:

- **Email**: `demo@nutriai.com`
- **Password**: `Demo@1234`

*(Or click the **"Fill Demo Account Credentials & Log In"** button on the sign-in screen)*
