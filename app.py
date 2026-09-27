"""
NutriAI | Modern Clinical Nutrition & AI-Based Personalized Food Recommendation Platform
Professional Healthcare SaaS UI with Persistent Authentication, Profile Management & Progress Tracking.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import date, datetime
import db
from recommender import FoodRecommender, calculate_nutrition_targets, calculate_bmr

# ---------------------------------------------------------
# Page Configuration & Global Theme Settings
# ---------------------------------------------------------
st.set_page_config(
    page_title="NutriAI | Clinical Nutrition & Food Recommender",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Ultra-Crisp Professional Healthcare CSS (Light SaaS Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Light Theme Force */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }

    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        max-width: 1280px;
    }

    /* Force high contrast text on all core elements */
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    p, span, div, li {
        color: #1E293B;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] * {
        color: #0F172A;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        color: #1E293B !important;
        padding: 0.4rem 0.6rem !important;
        border-radius: 8px !important;
        transition: background 0.15s ease;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
        background-color: #F1F5F9 !important;
    }

    /* Form Labels & Inputs */
    label[data-testid="stWidgetLabel"] p, .stWidgetLabel p, label p {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        margin-bottom: 0.2rem !important;
    }
    input, textarea, select {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
    }
    input:focus, textarea:focus {
        border-color: #0F766E !important;
        box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.15) !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #CBD5E1 !important;
        color: #0F172A !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] span {
        color: #0F172A !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 0.55rem 1.1rem !important;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"] {
        background: linear-gradient(135deg, #0F766E 0%, #0D9488 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25) !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #115E59 0%, #0F766E 100%) !important;
        box-shadow: 0 6px 16px rgba(15, 118, 110, 0.35) !important;
        transform: translateY(-1px);
    }
    button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
    }
    button[kind="secondary"]:hover {
        border-color: #0F766E !important;
        color: #0F766E !important;
    }

    /* Top Healthcare Hero Header */
    .brand-hero {
        background: linear-gradient(135deg, #0F766E 0%, #0369A1 100%);
        border-radius: 16px;
        padding: 1.6rem 2.2rem;
        color: #FFFFFF !important;
        box-shadow: 0 10px 25px -5px rgba(15, 118, 110, 0.25);
        margin-bottom: 1.2rem;
    }
    .brand-hero h1, .brand-hero h2, .brand-hero span {
        color: #FFFFFF !important;
    }
    .brand-hero p {
        color: #E0F2FE !important;
        font-size: 0.95rem;
        margin: 0.35rem 0 0 0;
    }

    /* Medical Disclaimer Banner */
    .disclaimer-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #0D9488;
        border-radius: 12px;
        padding: 0.9rem 1.25rem;
        margin-bottom: 1.2rem;
        color: #334155 !important;
        font-size: 0.86rem;
        line-height: 1.5;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    .disclaimer-card strong {
        color: #0F766E !important;
    }

    /* Status Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    .badge-teal { background: #CCFBF1 !important; color: #115E59 !important; border: 1px solid #99F6E4; }
    .badge-blue { background: #E0F2FE !important; color: #0369A1 !important; border: 1px solid #BAE6FD; }
    .badge-emerald { background: #D1FAE5 !important; color: #065F46 !important; border: 1px solid #A7F3D0; }
    .badge-amber { background: #FEF3C7 !important; color: #92400E !important; border: 1px solid #FDE68A; }
    .badge-rose { background: #FFE4E6 !important; color: #9F1239 !important; border: 1px solid #FECDD3; }
    .badge-purple { background: #EDE9FE !important; color: #5B21B6 !important; border: 1px solid #DDD6FE; }

    /* Modern KPI Metric Cards */
    .metric-card-modern {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.15rem 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-card-modern:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(15, 118, 110, 0.09);
        border-color: #0D9488;
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B !important;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #0F172A !important;
        line-height: 1.15;
    }
    .metric-sub {
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }

    /* Food Recommendation Cards */
    .food-card-modern {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        transition: all 0.2s ease;
    }
    .food-card-modern:hover {
        border-color: #0D9488;
        box-shadow: 0 8px 20px rgba(13, 148, 136, 0.1);
        transform: translateY(-2px);
    }
    .food-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.6rem;
    }
    .food-title {
        font-size: 1.12rem;
        font-weight: 800;
        color: #0F172A !important;
        margin: 0;
    }
    .food-desc {
        color: #475569 !important;
        font-size: 0.88rem;
        margin-top: 0.25rem;
        line-height: 1.45;
    }
    .ai-reason-pill {
        background: #F0FDFA !important;
        border: 1px solid #99F6E4;
        color: #0F766E !important;
        padding: 0.4rem 0.75rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 0.6rem;
        display: block;
    }
    .match-pill {
        background: linear-gradient(135deg, #0F766E 0%, #0D9488 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        box-shadow: 0 2px 6px rgba(15, 118, 110, 0.25);
        white-space: nowrap;
    }
    .macro-pill {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        background: #F1F5F9 !important;
        color: #1E293B !important;
        margin-right: 0.4rem;
        margin-top: 0.3rem;
    }
    .tag-chip {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.74rem;
        font-weight: 600;
        background: #EFF6FF !important;
        color: #1D4ED8 !important;
        margin-right: 0.3rem;
    }
    .allergen-chip {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.74rem;
        font-weight: 600;
        background: #FEE2E2 !important;
        color: #B91C1C !important;
        margin-right: 0.3rem;
    }

    /* Page Header Section */
    .page-header-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0.8rem;
        margin-bottom: 1.2rem;
    }
    .page-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0F172A !important;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .page-subtitle {
        font-size: 0.88rem;
        color: #64748B !important;
        margin-top: 0.2rem;
    }

    /* Clean Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0F766E 0%, #0284C7 100%) !important;
    }

    /* Clean Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px 8px 0 0;
        font-weight: 700;
        font-size: 0.9rem;
        color: #475569 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #0F766E !important;
        border-bottom: 2px solid #0F766E !important;
    }

    /* Footer */
    .nutri-footer {
        border-top: 1px solid #E2E8F0;
        margin-top: 3rem;
        padding: 1.5rem 0;
        text-align: center;
        color: #64748B !important;
        font-size: 0.84rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Dashboard"


# ---------------------------------------------------------
# Load Recommender Backend
# ---------------------------------------------------------
@st.cache_resource
def get_recommender():
    data_path = os.path.join(os.path.dirname(__file__), "data", "foods.csv")
    return FoodRecommender(data_path)

try:
    recommender = get_recommender()
except Exception as e:
    st.error(f"Error initializing recommender: {e}. Ensure data/foods.csv exists.")
    st.stop()


# =========================================================
# AUTHENTICATION GUARD: HIGH-CONTRAST LIGHT LOGIN PAGE
# =========================================================
if not st.session_state["authenticated"]:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem 0;">
        <div style="display:inline-flex; align-items:center; gap:0.6rem; background:#CCFBF1; padding:0.45rem 1.25rem; border-radius:9999px; border:1px solid #99F6E4; color:#0F766E; font-weight:700; font-size:0.85rem;">
            <span>🩺</span> Clinical Nutrition & Food Portal
        </div>
        <h1 style="font-size:2.5rem; font-weight:800; color:#0F172A; margin:0.8rem 0 0.3rem 0; letter-spacing:-0.03em;">Welcome to NutriAI</h1>
        <p style="color:#475569; font-size:1.05rem; max-width:620px; margin:0 auto; font-weight:500;">
            Your personalized clinical nutrition and health companion.
        </p>
    </div>
    """, unsafe_allow_html=True)

    auth_tab_login, auth_tab_register = st.tabs(["🔑 Sign In to Portal", "📝 Create New Account"])

    # ---------------- LOGIN TAB ----------------
    with auth_tab_login:
        col_space_l, col_auth, col_space_r = st.columns([1, 1.8, 1])
        with col_auth:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; padding:2rem 2.2rem; box-shadow:0 10px 25px -5px rgba(15, 23, 42, 0.06); margin-top:0.8rem;">
                <h3 style="margin-top:0; font-weight:800; color:#0F172A; font-size:1.4rem;">Sign In</h3>
                <p style="font-size:0.88rem; color:#475569; margin-bottom:1.4rem;">Enter your credentials to access your personalized nutritional dashboard.</p>
            """, unsafe_allow_html=True)

            with st.form("login_form"):
                login_email = st.text_input("Email Address", placeholder="e.g. demo@nutriai.com")
                login_password = st.text_input("Password", type="password", placeholder="Enter your password")
                remember_me = st.checkbox("Remember me on this device", value=True)
                login_submitted = st.form_submit_button("🚀 Sign In to Your Portal", use_container_width=True, type="primary")

                if login_submitted:
                    user_data = db.authenticate_user(login_email, login_password)
                    if user_data:
                        st.session_state["authenticated"] = True
                        st.session_state["user_id"] = user_data["id"]
                        st.session_state["user_name"] = user_data["name"]
                        st.session_state["user_email"] = user_data["email"]
                        st.session_state["current_page"] = "🏠 Dashboard"
                        st.success(f"Welcome back, {user_data['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password. Please verify your credentials or use the demo login below.")

            st.markdown("---")
            st.markdown("""
            <div style="background:#F0FDFA; border:1px solid #99F6E4; border-radius:10px; padding:0.85rem 1.1rem; font-size:0.86rem; color:#0F766E;">
                <strong>⚡ Instant Demo Access (Pre-Configured Profile):</strong><br>
                Email: <code>demo@nutriai.com</code><br>
                Password: <code>Demo@1234</code>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            if st.button("Fill Demo Account Credentials & Log In", use_container_width=True):
                user_data = db.authenticate_user("demo@nutriai.com", "Demo@1234")
                if user_data:
                    st.session_state["authenticated"] = True
                    st.session_state["user_id"] = user_data["id"]
                    st.session_state["user_name"] = user_data["name"]
                    st.session_state["user_email"] = user_data["email"]
                    st.session_state["current_page"] = "🏠 Dashboard"
                    st.rerun()

            with st.expander("Forgot Password?"):
                st.markdown("<span style='font-size:0.86rem; color:#475569;'>To reset clinical credentials, please contact your healthcare provider or register a new profile.</span>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- REGISTRATION TAB ----------------
    with auth_tab_register:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; padding:2rem 2.2rem; box-shadow:0 10px 25px -5px rgba(15, 23, 42, 0.06); margin-top:0.8rem; margin-bottom:1.5rem;">
            <h3 style="margin-top:0; font-weight:800; color:#0F172A; font-size:1.4rem;">Register New Patient Profile</h3>
            <p style="font-size:0.88rem; color:#475569; margin-bottom:1.2rem;">Provide your biometrics and dietary restrictions to build your personalized AI nutrition model.</p>
        """, unsafe_allow_html=True)

        with st.form("registration_form"):
            rc1, rc2 = st.columns(2)
            with rc1:
                reg_name = st.text_input("Full Name *", placeholder="e.g. Sarah Jenkins")
                reg_email = st.text_input("Email Address *", placeholder="e.g. sarah@example.com")
                reg_password = st.text_input("Password (min 6 characters) *", type="password")
                reg_confirm_password = st.text_input("Confirm Password *", type="password")

                st.markdown("##### 👤 Physical Biometrics")
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    reg_age = st.number_input("Age (Years) *", min_value=12, max_value=115, value=28, step=1)
                with b_col2:
                    reg_gender = st.selectbox("Gender *", ["Male", "Female", "Other"])

                h_col1, h_col2 = st.columns(2)
                with h_col1:
                    reg_height = st.number_input("Height (cm) *", min_value=90.0, max_value=240.0, value=170.0, step=0.5)
                with h_col2:
                    reg_weight = st.number_input("Current Weight (kg) *", min_value=30.0, max_value=250.0, value=68.0, step=0.5)

                reg_target_weight = st.number_input("Target Goal Weight (kg)", min_value=30.0, max_value=250.0, value=65.0, step=0.5)

            with rc2:
                reg_activity = st.selectbox(
                    "Physical Activity Level *",
                    [
                        "Sedentary (little to no exercise)",
                        "Lightly Active (light exercise 1-3 days/wk)",
                        "Moderately Active (moderate exercise 3-5 days/wk)",
                        "Very Active (hard exercise 6-7 days/wk)"
                    ],
                    index=2
                )

                reg_preference = st.radio(
                    "Dietary Preference *",
                    ["Vegetarian", "Non-Vegetarian"],
                    horizontal=True
                )

                reg_goal = st.selectbox(
                    "Primary Health Goal *",
                    ["Weight Loss", "Weight Gain", "Maintain Weight"]
                )

                st.markdown("##### 🛡️ Allergies & Disliked Ingredients")
                common_allergens = ["Dairy", "Gluten", "Nuts", "Peanuts", "Seafood", "Eggs", "Soy"]
                reg_allergies = st.multiselect("Known Food Allergies", options=common_allergens)
                reg_custom_allergies = st.text_input("Other Allergens (Optional)", placeholder="e.g. Sesame, Mustard")
                reg_foods_to_avoid = st.text_input("Foods or Ingredients to Avoid", placeholder="e.g. mushroom, pork, beef")

                st.markdown("##### 🩺 Doctor Guidelines & Clinical Restrictions")
                doc_preset_options = [
                    "Low Sodium / Hypertension Friendly",
                    "Low Sugar / Diabetic Friendly",
                    "Low Fat / Cholesterol Conscious",
                    "Low Carb / Metabolic Friendly",
                    "Gluten-Free (Celiac / Sensitivity)",
                    "High Fiber / Digestive Health",
                    "Renal Friendly (Kidney Care)"
                ]
                reg_doctor_restrictions = st.multiselect("Clinical Prescriptions", options=doc_preset_options)
                reg_doctor_notes = st.text_area("Specific Physician Notes", placeholder="e.g. Limit saturated fat, avoid high-oxalate foods")

            reg_submit = st.form_submit_button("✅ Create Account & Enter Portal", use_container_width=True, type="primary")

            if reg_submit:
                if reg_password != reg_confirm_password:
                    st.error("Passwords do not match. Please re-enter your password.")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif not reg_name.strip() or not reg_email.strip():
                    st.error("Please fill in your name and email address.")
                else:
                    new_profile = {
                        "age": reg_age,
                        "gender": reg_gender,
                        "height": reg_height,
                        "weight": reg_weight,
                        "target_weight": reg_target_weight,
                        "activity_level": reg_activity,
                        "food_preference": reg_preference,
                        "primary_goal": reg_goal,
                        "allergies": reg_allergies,
                        "custom_allergies": reg_custom_allergies,
                        "foods_to_avoid": reg_foods_to_avoid,
                        "dietary_restrictions": reg_doctor_restrictions,
                        "doctor_custom_notes": reg_doctor_notes
                    }
                    success, msg, new_uid = db.register_user(reg_name, reg_email, reg_password, new_profile)
                    if success:
                        st.success(f"{msg} Logging you in...")
                        st.session_state["authenticated"] = True
                        st.session_state["user_id"] = new_uid
                        st.session_state["user_name"] = reg_name
                        st.session_state["user_email"] = reg_email
                        st.session_state["current_page"] = "🏠 Dashboard"
                        st.rerun()
                    else:
                        st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    # Medical Disclaimer Banner on Auth page
    st.markdown("""
    <div class="disclaimer-card" style="margin-top:2rem;">
        <strong>⚠️ Healthcare Safety Policy:</strong>
        NutriAI is an educational nutritional guidance platform and <strong>does not diagnose diseases or prescribe medical diets</strong>.
        For individuals receiving medical treatment or managing chronic conditions, the system strictly applies dietary restrictions 
        <strong>explicitly entered by you or provided by your qualified healthcare professional</strong>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nutri-footer">
        <strong>NutriAI™ Healthcare & Clinical Nutrition Platform</strong> | Built with Python, Pandas, Scikit-learn, SQLite & Streamlit<br>
        Educational and academic demonstration platform. Always consult a licensed healthcare professional before making dietary changes.
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# =========================================================
# AUTHENTICATED SESSION: LOAD USER PROFILE FROM SQLITE
# =========================================================
user_id = st.session_state.get("user_id")
user_profile = db.get_user_profile(user_id) if user_id else None

if not user_profile:
    st.session_state["authenticated"] = False
    st.session_state["user_id"] = None
    st.session_state["user_name"] = ""
    st.session_state["user_email"] = ""
    st.rerun()

# Dynamic Nutrition Calculations from database user profile (NOT HARD-CODED!)
targets = calculate_nutrition_targets(
    age=int(user_profile["age"]),
    gender=user_profile["gender"],
    height_cm=float(user_profile["height_cm"]),
    weight_kg=float(user_profile["weight_kg"]),
    goal=user_profile["primary_goal"],
    activity_level=user_profile["activity_level"]
)

# Apply Safety, Allergy, Preference, and Doctor Restrictions Filters
all_user_allergies = list(user_profile["allergies"])
if user_profile["custom_allergies"].strip():
    for extra in user_profile["custom_allergies"].split(","):
        if extra.strip() and extra.strip() not in all_user_allergies:
            all_user_allergies.append(extra.strip())

filtered_df, filter_stats = recommender.filter_foods(
    food_preference=user_profile["food_preference"],
    allergies=all_user_allergies,
    foods_to_avoid=user_profile["foods_to_avoid"],
    doctor_restrictions=user_profile["doctor_restrictions"],
    doctor_custom_notes=user_profile["doctor_custom_notes"]
)

# BMI Calculation
height_m = user_profile["height_cm"] / 100.0
bmi = round(user_profile["weight_kg"] / (height_m ** 2), 1)

if bmi < 18.5:
    bmi_category = "Underweight"
    bmi_badge = "badge-blue"
    bmi_color = "#0284C7"
elif bmi < 25.0:
    bmi_category = "Normal Weight"
    bmi_badge = "badge-emerald"
    bmi_color = "#059669"
elif bmi < 30.0:
    bmi_category = "Overweight"
    bmi_badge = "badge-amber"
    bmi_color = "#D97706"
else:
    bmi_category = "Obese"
    bmi_badge = "badge-rose"
    bmi_color = "#DC2626"

# Goal badge info
if "Loss" in user_profile["primary_goal"]:
    goal_badge = "badge-purple"
    goal_desc = "-500 kcal Deficit (Lean Focus)"
elif "Gain" in user_profile["primary_goal"]:
    goal_badge = "badge-teal"
    goal_desc = "+400 kcal Surplus (Hypertrophy)"
else:
    goal_badge = "badge-blue"
    goal_desc = "Caloric Equilibrium"


# ---------------------------------------------------------
# SIDEBAR: Authenticated User Header & Navigation
# ---------------------------------------------------------
with st.sidebar:
    # Authenticated User Badge Card
    st.markdown(f"""
    <div style="background:#F0FDFA; border:1px solid #99F6E4; border-radius:14px; padding:1rem; margin-bottom:1.2rem;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
            <div style="background:#0F766E; color:white; border-radius:50%; width:42px; height:42px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.1rem; box-shadow:0 2px 6px rgba(15,118,110,0.3);">
                {user_profile['name'][:1].upper()}
            </div>
            <div style="overflow:hidden;">
                <div style="font-size:1rem; font-weight:800; color:#0F172A; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{user_profile['name']}</div>
                <div style="font-size:0.75rem; color:#475569; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{user_profile['email']}</div>
            </div>
        </div>
        <div style="margin-top:0.75rem; display:flex; gap:0.4rem; flex-wrap:wrap;">
            <span class="badge-pill {bmi_badge}" style="font-size:0.72rem; padding:0.2rem 0.55rem;">⚖️ BMI {bmi} ({bmi_category})</span>
            <span class="badge-pill {goal_badge}" style="font-size:0.72rem; padding:0.2rem 0.55rem;">🎯 {user_profile['primary_goal']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:#64748B; margin-bottom:0.4rem;'>Menu Navigation</div>", unsafe_allow_html=True)
    nav_pages = [
        "🏠 Dashboard",
        "🤖 AI Recommendations",
        "🍽️ Meal Planner",
        "📈 My Progress",
        "🔎 Food Database",
        "📊 Nutrition Analytics",
        "👤 My Profile",
        "🩺 Medical Guidelines",
        "ℹ️ About"
    ]

    selected_nav = st.radio(
        "Navigation",
        options=nav_pages,
        index=nav_pages.index(st.session_state["current_page"]) if st.session_state["current_page"] in nav_pages else 0,
        label_visibility="collapsed"
    )
    st.session_state["current_page"] = selected_nav

    st.markdown("---")

    # Logout Button at bottom of sidebar
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["user_id"] = None
        st.session_state["user_name"] = ""
        st.session_state["user_email"] = ""
        st.session_state["current_page"] = "🏠 Dashboard"
        st.rerun()


# =========================================================
# PAGE 1: 🏠 DASHBOARD
# =========================================================
if selected_nav == "🏠 Dashboard":
    st.markdown(f"""
    <div class="brand-hero">
        <h1><span>👋</span> Welcome back, {user_profile['name']}!</h1>
        <p>Your personalized healthcare & metabolic nutrition overview.</p>
    </div>
    """, unsafe_allow_html=True)

    # Medical Disclaimer Callout
    st.markdown("""
    <div class="disclaimer-card">
        <strong>⚠️ Clinical Safety Notice:</strong> 
        NutriAI is an educational nutritional guidance platform and <strong>does not diagnose diseases or prescribe medical diets</strong>. 
        For individuals receiving medical treatment or managing chronic conditions, the system strictly applies dietary restrictions 
        <strong>explicitly entered by you or provided by your qualified healthcare professional</strong>.
    </div>
    """, unsafe_allow_html=True)

    # Status Badges Row
    b1, b2, b3, b4 = st.columns([1.2, 1.4, 1.2, 2.0])
    with b1:
        st.markdown(f'<span class="badge-pill {bmi_badge}">⚖️ {bmi_category} (BMI {bmi})</span>', unsafe_allow_html=True)
    with b2:
        st.markdown(f'<span class="badge-pill {goal_badge}">🎯 {user_profile["primary_goal"]}</span>', unsafe_allow_html=True)
    with b3:
        st.markdown(f'<span class="badge-pill badge-emerald">🥗 {user_profile["food_preference"]}</span>', unsafe_allow_html=True)
    with b4:
        st.markdown(f'<span class="badge-pill badge-teal">🛡️ {filter_stats["final_eligible"]} Safe Recipes Active ({len(all_user_allergies)} Allergens Filtered)</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 6 Modern KPI Metric Cards
    st.markdown("#### 📊 Daily Metabolic & Macronutrient Targets")
    m1, m2, m3, m4, m5, m6 = st.columns(6)

    with m1:
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label">Daily Calories</div>
            <div class="metric-value" style="color:#0F766E !important;">{targets['target_calories']:,}</div>
            <div class="metric-sub" style="color:#0D9488 !important;">kcal / day</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        p_cal = targets['target_protein'] * 4.0
        p_pct = round((p_cal / targets['target_calories']) * 100)
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label">Protein Target</div>
            <div class="metric-value" style="color:#0369A1 !important;">{targets['target_protein']}g</div>
            <div class="metric-sub" style="color:#0284C7 !important;">{p_pct}% of calories</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        c_cal = targets['target_carbs'] * 4.0
        c_pct = round((c_cal / targets['target_calories']) * 100)
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label">Carbohydrates</div>
            <div class="metric-value" style="color:#0284C7 !important;">{targets['target_carbs']}g</div>
            <div class="metric-sub" style="color:#38BDF8 !important;">{c_pct}% of calories</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        f_cal = targets['target_fat'] * 9.0
        f_pct = round((f_cal / targets['target_calories']) * 100)
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label">Healthy Fats</div>
            <div class="metric-value" style="color:#D97706 !important;">{targets['target_fat']}g</div>
            <div class="metric-sub" style="color:#F59E0B !important;">{f_pct}% of calories</div>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label">Current Weight</div>
            <div class="metric-value" style="color:#059669 !important;">{user_profile['weight_kg']} kg</div>
            <div class="metric-sub" style="color:#10B981 !important;">Goal: {user_profile['target_weight']} kg</div>
        </div>
        """, unsafe_allow_html=True)

    with m6:
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label">BMR / TDEE</div>
            <div class="metric-value" style="color:#334155 !important; font-size:1.35rem;">{int(targets['bmr'])} / {int(targets['tdee'])}</div>
            <div class="metric-sub" style="color:#64748B !important;">kcal metabolic burn</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Health Progress & Quick Actions
    dash_col1, dash_col2 = st.columns([1.6, 1])

    with dash_col1:
        st.markdown("#### 📈 Your Health Progress")
        user_progress_df = db.get_user_progress(user_id)

        if not user_progress_df.empty:
            weights = user_progress_df["weight"].dropna()
            start_wt = weights.iloc[0] if len(weights) > 0 else user_profile["weight_kg"]
            curr_wt = weights.iloc[-1] if len(weights) > 0 else user_profile["weight_kg"]
            tgt_wt = user_profile.get("target_weight", start_wt)
            wt_diff = round(curr_wt - start_wt, 1)

            # Goal progress calculation
            total_needed = start_wt - tgt_wt
            if abs(total_needed) > 0.1:
                progress_pct = min(max(round(((start_wt - curr_wt) / total_needed) * 100), 0), 100)
            else:
                progress_pct = 100

            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.25rem 1.4rem; box-shadow:0 2px 8px rgba(15,23,42,0.04);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem; flex-wrap:wrap; gap:0.5rem;">
                    <div>
                        <span style="font-size:0.82rem; color:#64748B; font-weight:700; text-transform:uppercase;">Starting</span><br>
                        <b style="font-size:1.15rem; color:#0F172A;">{start_wt} kg</b>
                    </div>
                    <div>
                        <span style="font-size:0.82rem; color:#64748B; font-weight:700; text-transform:uppercase;">Current</span><br>
                        <b style="font-size:1.15rem; color:#0F766E;">{curr_wt} kg</b>
                    </div>
                    <div>
                        <span style="font-size:0.82rem; color:#64748B; font-weight:700; text-transform:uppercase;">Target</span><br>
                        <b style="font-size:1.15rem; color:#0369A1;">{tgt_wt} kg</b>
                    </div>
                    <div>
                        <span style="font-size:0.82rem; color:#64748B; font-weight:700; text-transform:uppercase;">Net Change</span><br>
                        <b style="font-size:1.15rem; color:{'#059669' if wt_diff <= 0 else '#D97706'};">{'+' if wt_diff > 0 else ''}{wt_diff} kg</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"**Goal Progress**: `{progress_pct}% completed`")
            st.progress(progress_pct / 100.0)

            st.markdown(f"""
                <div style="font-size:0.86rem; color:#475569; margin-top:0.8rem;">
                    Recorded <b>{len(user_progress_df)} daily logs</b> in NutriAI database.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No progress entries logged yet. Head to **📈 My Progress** to log your daily stats!")

    with dash_col2:
        st.markdown("#### ⚡ Quick Actions")
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.25rem 1.4rem; box-shadow:0 2px 8px rgba(15,23,42,0.04);">
        """, unsafe_allow_html=True)
        if st.button("🤖 Get AI Food Recommendations", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "🤖 AI Recommendations"
            st.rerun()
        if st.button("🍽️ Create / View Meal Plan", use_container_width=True):
            st.session_state["current_page"] = "🍽️ Meal Planner"
            st.rerun()
        if st.button("📈 Track Today's Meal & Weight", use_container_width=True):
            st.session_state["current_page"] = "📈 My Progress"
            st.rerun()
        if st.button("📊 Inspect Nutrition Analytics", use_container_width=True):
            st.session_state["current_page"] = "📊 Nutrition Analytics"
            st.rerun()
        if st.button("🔎 Explore Food Database", use_container_width=True):
            st.session_state["current_page"] = "🔎 Food Database"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# PAGE 2: 🤖 AI RECOMMENDATIONS
# =========================================================
elif selected_nav == "🤖 AI Recommendations":
    st.markdown(f"""
    <div class="page-header-box">
        <div>
            <h2 class="page-title">🤖 AI-Ranked Food Recommendations</h2>
            <div class="page-subtitle">Tailored for {user_profile['name']} ({user_profile['age']}y {user_profile['gender']}, {user_profile['food_preference']}, {user_profile['primary_goal']}).</div>
        </div>
        <div>
            <span class="badge-pill badge-teal">✅ {filter_stats['final_eligible']} Safe Options Filtered</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if filter_stats["final_eligible"] == 0:
        st.error("⚠️ No foods match your active combination of dietary restrictions and allergies. Please adjust your restrictions in **👤 My Profile**.")
    else:
        meal_tabs = st.tabs(["🍳 Breakfast", "🥗 Lunch", "🍲 Dinner", "🥜 Healthy Snacks"])
        categories = [("Breakfast", meal_tabs[0], "🍳"), ("Lunch", meal_tabs[1], "🥗"), ("Dinner", meal_tabs[2], "🍲"), ("Snack", meal_tabs[3], "🥜")]

        for cat_name, subtab, cat_icon in categories:
            with subtab:
                cat_target = targets["per_meal_targets"][cat_name]

                st.markdown(f"""
                <div style="background:#F0FDFA; border:1px solid #CCFBF1; border-radius:10px; padding:0.8rem 1.2rem; margin-bottom:1.2rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
                    <span style="font-weight:700; color:#0F766E;">🎯 Target for {cat_name}:</span>
                    <span style="font-size:0.88rem; color:#134E4A;">
                        Calories: <b>{cat_target['calories']} kcal</b> | 
                        Protein: <b>{cat_target['protein']}g</b> | 
                        Carbs: <b>{cat_target['carbohydrates']}g</b> | 
                        Fat: <b>{cat_target['fat']}g</b> | 
                        Fiber: <b>{cat_target['fiber']}g</b>
                    </span>
                </div>
                """, unsafe_allow_html=True)

                recs = recommender.recommend_for_category(filtered_df, cat_name, cat_target, top_n=5)

                if recs.empty:
                    st.warning(f"No {cat_name} items match current allergy or avoidance filters.")
                else:
                    for _, food in recs.iterrows():
                        match_score = food.get("match_score", 85.0)
                        allergens_list = [a.strip() for a in str(food['allergens']).split(',') if a.strip() and a.lower() != 'none']
                        attributes_list = [a.strip().replace('_', ' ') for a in str(food['dietary_attributes']).split(',') if a.strip()]

                        # Reason why recommended
                        reasons = []
                        if food['protein'] >= cat_target['protein'] * 0.8:
                            reasons.append(f"Provides {food['protein']}g high-quality protein for {user_profile['primary_goal'].lower()}")
                        if food['sodium_mg'] <= 250:
                            reasons.append(f"Low sodium ({food['sodium_mg']}mg)")
                        if food['fiber'] >= 5:
                            reasons.append(f"Rich in prebiotic fiber ({food['fiber']}g)")
                        if not reasons:
                            reasons.append(f"Matches {cat_name.lower()} energy budget ({food['calories']} kcal)")
                        ai_reason_text = " • ".join(reasons)

                        st.markdown(f"""
                        <div class="food-card-modern">
                            <div class="food-header">
                                <div>
                                    <h3 class="food-title">{cat_icon} {food['food_name']}</h3>
                                    <div class="food-desc">{food['description']}</div>
                                    <div class="ai-reason-pill">💡 <b>Why Recommended:</b> {ai_reason_text}</div>
                                </div>
                                <div style="text-align:right;">
                                    <span class="match-pill">🎯 {match_score}% Match</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        c1, c2, c3, c4, c5, c6 = st.columns(6)
                        c1.metric("Calories", f"{food['calories']} kcal")
                        c2.metric("Protein", f"{food['protein']}g", f"{food.get('protein_pct', 0)}% cal")
                        c3.metric("Carbs", f"{food['carbohydrates']}g", f"{food.get('carb_pct', 0)}% cal")
                        c4.metric("Fat", f"{food['fat']}g", f"{food.get('fat_pct', 0)}% cal")
                        c5.metric("Fiber", f"{food['fiber']}g")
                        c6.metric("Sodium", f"{food['sodium_mg']} mg")

                        chips_html = "<div style='margin-top:0.75rem; display:flex; flex-wrap:wrap; gap:0.3rem;'>"
                        chips_html += f"<span class='tag-chip' style='background:#DCFCE7 !important; color:#166534 !important;'>🥗 {food['diet_type']}</span>"
                        if allergens_list:
                            for alg in allergens_list:
                                chips_html += f"<span class='allergen-chip'>⚠️ Contains {alg}</span>"
                        else:
                            chips_html += "<span class='tag-chip' style='background:#F0FDF4 !important; color:#15803D !important;'>✅ Allergen-Free</span>"
                        for attr in attributes_list[:4]:
                            chips_html += f"<span class='tag-chip'>🏷️ {attr.title()}</span>"
                        chips_html += "</div></div>"
                        st.markdown(chips_html, unsafe_allow_html=True)


# =========================================================
# PAGE 3: 🍽️ MEAL PLANNER
# =========================================================
elif selected_nav == "🍽️ Meal Planner":
    st.markdown(f"""
    <div class="page-header-box">
        <div>
            <h2 class="page-title">🍽️ 1-Day Personalized Meal Plan</h2>
            <div class="page-subtitle">Harmonized breakfast, lunch, dinner, and snack schedule for {user_profile['name']}.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    daily_plan = recommender.build_full_day_plan(filtered_df, targets["per_meal_targets"])
    meals = daily_plan["meals"]
    actual_totals = daily_plan["actual_totals"]

    plan_col_left, plan_col_right = st.columns([3.2, 2.0])

    with plan_col_left:
        st.markdown("#### 🕒 Today's Recommended Meals")
        meal_order = [
            ("Breakfast", "🍳", "#0F766E"),
            ("Lunch", "🥗", "#0284C7"),
            ("Dinner", "🍲", "#0D9488"),
            ("Snack", "🥜", "#F59E0B")
        ]

        for meal_type, icon, accent in meal_order:
            item = meals.get(meal_type)
            if item:
                score = item.get('match_score', 85.0)
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:5px solid {accent}; border-radius:12px; padding:1.1rem 1.3rem; margin-bottom:0.9rem; box-shadow:0 2px 8px rgba(15,23,42,0.03);">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <span style="font-size:0.75rem; font-weight:800; text-transform:uppercase; color:{accent}; letter-spacing:0.04em;">
                                {icon} {meal_type}
                            </span>
                            <h4 style="margin: 0.2rem 0 0.2rem 0; color:#0F172A !important; font-size:1.1rem;">{item['food_name']}</h4>
                            <p style="margin:0; font-size:0.86rem; color:#475569 !important;">{item['description']}</p>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.25rem; font-weight:800; color:#0F172A !important;">{item['calories']} <span style="font-size:0.75rem; color:#64748B; font-weight:500;">kcal</span></div>
                            <span class="match-pill" style="font-size:0.72rem; padding:0.2rem 0.55rem;">{score}% Match</span>
                        </div>
                    </div>
                    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:0.6rem; padding-top:0.6rem; border-top:1px dashed #E2E8F0;">
                        <span class="macro-pill">🥩 Protein: <b>{item['protein']}g</b></span>
                        <span class="macro-pill">🍞 Carbs: <b>{item['carbohydrates']}g</b></span>
                        <span class="macro-pill">🥑 Fat: <b>{item['fat']}g</b></span>
                        <span class="macro-pill">🌾 Fiber: <b>{item['fiber']}g</b></span>
                        <span class="macro-pill">🧂 Sodium: <b>{item['sodium_mg']}mg</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"No safe {meal_type} dish found matching current filters.")

    with plan_col_right:
        st.markdown("#### 🎯 Daily Target Progress")

        cal_pct = min(actual_totals['calories'] / max(targets['target_calories'], 1.0), 1.0)
        prot_pct = min(actual_totals['protein'] / max(targets['target_protein'], 1.0), 1.0)
        carb_pct = min(actual_totals['carbohydrates'] / max(targets['target_carbs'], 1.0), 1.0)
        fat_pct = min(actual_totals['fat'] / max(targets['target_fat'], 1.0), 1.0)
        fiber_pct = min(actual_totals['fiber'] / max(targets['target_fiber'], 1.0), 1.0)

        st.markdown(f"**Calories**: `{actual_totals['calories']} / {targets['target_calories']} kcal` ({round(cal_pct*100)}%)")
        st.progress(cal_pct)

        st.markdown(f"**Protein**: `{actual_totals['protein']} / {targets['target_protein']} g` ({round(prot_pct*100)}%)")
        st.progress(prot_pct)

        st.markdown(f"**Carbohydrates**: `{actual_totals['carbohydrates']} / {targets['target_carbs']} g` ({round(carb_pct*100)}%)")
        st.progress(carb_pct)

        st.markdown(f"**Healthy Fats**: `{actual_totals['fat']} / {targets['target_fat']} g` ({round(fat_pct*100)}%)")
        st.progress(fat_pct)

        st.markdown(f"**Dietary Fiber**: `{actual_totals['fiber']} / {targets['target_fiber']} g` ({round(fiber_pct*100)}%)")
        st.progress(fiber_pct)

        st.markdown("<br>", unsafe_allow_html=True)

        meal_plan_text = f"""=====================================================
NutriAI - Personalized 1-Day Clinical Meal Plan
=====================================================
Patient: {user_profile['name']} | {user_profile['age']}y | {user_profile['gender']} | Height: {user_profile['height_cm']}cm | Weight: {user_profile['weight_kg']}kg
Goal: {user_profile['primary_goal']} ({goal_desc})
Diet: {user_profile['food_preference']}
Allergens Excluded: {', '.join(all_user_allergies) if all_user_allergies else 'None'}
Clinical Guidance: {', '.join(user_profile['doctor_restrictions']) if user_profile['doctor_restrictions'] else 'Standard Lifestyle'}

TODAY'S SCHEDULED MEALS:
1. BREAKFAST: {meals['Breakfast']['food_name'] if meals.get('Breakfast') else 'N/A'} ({meals['Breakfast']['calories'] if meals.get('Breakfast') else 0} kcal)
2. LUNCH:     {meals['Lunch']['food_name'] if meals.get('Lunch') else 'N/A'} ({meals['Lunch']['calories'] if meals.get('Lunch') else 0} kcal)
3. DINNER:    {meals['Dinner']['food_name'] if meals.get('Dinner') else 'N/A'} ({meals['Dinner']['calories'] if meals.get('Dinner') else 0} kcal)
4. SNACK:     {meals['Snack']['food_name'] if meals.get('Snack') else 'N/A'} ({meals['Snack']['calories'] if meals.get('Snack') else 0} kcal)

TOTAL DAILY NUTRITION ACHIEVED:
Calories:      {actual_totals['calories']} kcal (Target: {targets['target_calories']} kcal)
Protein:       {actual_totals['protein']}g (Target: {targets['target_protein']}g)
Carbohydrates: {actual_totals['carbohydrates']}g (Target: {targets['target_carbs']}g)
Fat:           {actual_totals['fat']}g (Target: {targets['target_fat']}g)
Dietary Fiber: {actual_totals['fiber']}g (Target: {targets['target_fiber']}g)

Notice: Educational nutritional platform. Consult licensed medical professionals.
"""
        st.download_button(
            label="📥 Download Daily Meal Plan (TXT)",
            data=meal_plan_text,
            file_name=f"NutriAI_Meal_Plan_{user_profile['name'].replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# PAGE 4: 📈 MY PROGRESS
# =========================================================
elif selected_nav == "📈 My Progress":
    st.markdown("""
    <div class="page-header-box">
        <div>
            <h2 class="page-title">📈 My Personal Progress Tracking</h2>
            <div class="page-subtitle">Track your weight trajectory, daily caloric intake, and macronutrient adherence over time.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    prog_df = db.get_user_progress(user_id)

    # Summary Metrics
    pm1, pm2, pm3, pm4, pm5 = st.columns(5)
    
    if not prog_df.empty:
        weights = prog_df["weight"].dropna()
        start_w = weights.iloc[0] if len(weights) > 0 else user_profile["weight_kg"]
        curr_w = weights.iloc[-1] if len(weights) > 0 else user_profile["weight_kg"]
        tgt_w = user_profile.get("target_weight", start_w)
        total_chg = round(curr_w - start_w, 1)
        rem_to_goal = round(curr_w - tgt_w, 1)
    else:
        start_w = user_profile["weight_kg"]
        curr_w = user_profile["weight_kg"]
        tgt_w = user_profile.get("target_weight", start_w)
        total_chg = 0.0
        rem_to_goal = round(curr_w - tgt_w, 1)

    with pm1:
        st.metric("Starting Weight", f"{start_w} kg")
    with pm2:
        st.metric("Current Weight", f"{curr_w} kg", f"{'+' if total_chg > 0 else ''}{total_chg} kg")
    with pm3:
        st.metric("Target Goal", f"{tgt_w} kg")
    with pm4:
        st.metric("Distance to Goal", f"{abs(rem_to_goal)} kg", "To target" if rem_to_goal > 0 else "Goal achieved!")
    with pm5:
        st.metric("Total Entries", f"{len(prog_df)}")

    st.markdown("<br>", unsafe_allow_html=True)

    tab_log, tab_history = st.tabs(["📝 Log Daily Intake & Weight", "📋 Progress History & Logs"])

    with tab_log:
        with st.form("progress_entry_form"):
            st.markdown("##### ✍️ Record Today's Health Log")
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                entry_date = st.date_input("Date", value=date.today())
                entry_weight = st.number_input("Weight Today (kg)", min_value=30.0, max_value=250.0, value=float(curr_w), step=0.1)
                entry_calories = st.number_input("Calories Consumed (kcal)", min_value=0.0, max_value=10000.0, value=float(targets["target_calories"]), step=50.0)
            with col_l2:
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    entry_protein = st.number_input("Protein (g)", min_value=0.0, max_value=500.0, value=float(targets["target_protein"]), step=5.0)
                with col_m2:
                    entry_carbs = st.number_input("Carbs (g)", min_value=0.0, max_value=800.0, value=float(targets["target_carbs"]), step=5.0)
                with col_m3:
                    entry_fat = st.number_input("Fat (g)", min_value=0.0, max_value=300.0, value=float(targets["target_fat"]), step=5.0)
                entry_notes = st.text_input("Daily Notes / Workout Summary", placeholder="e.g. Completed 45 min strength session, followed meal plan.")

            save_prog = st.form_submit_button("💾 Save Progress Entry", use_container_width=True, type="primary")
            if save_prog:
                db.add_progress_entry(
                    user_id=user_id,
                    date_str=entry_date.isoformat(),
                    weight=entry_weight,
                    calories=entry_calories,
                    protein=entry_protein,
                    carbs=entry_carbs,
                    fat=entry_fat,
                    notes=entry_notes
                )
                st.success("Daily progress entry recorded successfully!")
                st.rerun()

    with tab_history:
        if not prog_df.empty:
            st.dataframe(
                prog_df[["date", "weight", "calories", "protein", "carbs", "fat", "notes"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No entries logged yet. Submit the form to record your first entry!")

    st.markdown("<br>", unsafe_allow_html=True)

    if len(prog_df) >= 2:
        st.markdown("#### 📊 Progress Trends Over Time")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("##### ⚖️ Weight Trajectory (kg)")
            weight_chart = alt.Chart(prog_df).mark_line(point=True, color="#0F766E", strokeWidth=3).encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("weight:Q", scale=alt.Scale(zero=False), title="Weight (kg)"),
                tooltip=["date", "weight", "notes"]
            ).properties(height=300)
            st.altair_chart(weight_chart, use_container_width=True)

        with chart_col2:
            st.markdown("##### 🔥 Calorie Adherence vs Target")
            cal_chart = alt.Chart(prog_df).mark_bar(color="#0284C7", cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("calories:Q", title="Calories (kcal)"),
                tooltip=["date", "calories"]
            ).properties(height=300)
            st.altair_chart(cal_chart, use_container_width=True)
    elif len(prog_df) == 1:
        st.info("💡 You have 1 entry recorded. Add a second entry to visualize your trajectory chart!")


# =========================================================
# PAGE 5: 🔎 FOOD DATABASE
# =========================================================
elif selected_nav == "🔎 Food Database":
    st.markdown("""
    <div class="page-header-box">
        <div>
            <h2 class="page-title">🔎 Food Database Explorer</h2>
            <div class="page-subtitle">Search, filter, and inspect detailed nutritional facts, allergens, and clinical tags.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input("🔎 Search by Dish Name, Ingredient, or Tag", placeholder="e.g. Salmon, Oats, Tofu, Avocado, Chicken, Low Sodium")

    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        cat_filter = st.multiselect("Filter Category", options=["Breakfast", "Lunch", "Dinner", "Snack"], default=["Breakfast", "Lunch", "Dinner", "Snack"])
    with f_col2:
        diet_filter = st.multiselect("Filter Diet Type", options=["Vegetarian", "Non-Vegetarian"], default=["Vegetarian", "Non-Vegetarian"])
    with f_col3:
        display_layout = st.radio("Display View", ["📊 Interactive Table", "🃏 Visual Cards"], horizontal=True)

    # Added Calorie and Protein Sliders as requested!
    slider_c1, slider_c2 = st.columns(2)
    with slider_c1:
        cal_range = st.slider("Calorie Range (kcal)", min_value=50, max_value=800, value=(50, 800), step=25)
    with slider_c2:
        prot_range = st.slider("Protein Range (g)", min_value=0, max_value=60, value=(0, 60), step=5)

    df_view = recommender.df.copy()
    if cat_filter:
        df_view = df_view[df_view["category"].isin(cat_filter)]
    if diet_filter:
        df_view = df_view[df_view["diet_type"].isin(diet_filter)]
    
    # Filter by sliders
    df_view = df_view[(df_view["calories"] >= cal_range[0]) & (df_view["calories"] <= cal_range[1])]
    df_view = df_view[(df_view["protein"] >= prot_range[0]) & (df_view["protein"] <= prot_range[1])]

    if search_query.strip():
        sq = search_query.strip().lower()
        df_view = df_view[
            df_view["food_name"].str.lower().str.contains(sq) |
            df_view["description"].str.lower().str.contains(sq) |
            df_view["dietary_attributes"].str.lower().str.contains(sq)
        ]

    st.write(f"Showing **{len(df_view)}** matching dishes:")

    if display_layout == "📊 Interactive Table":
        table_cols = ["food_id", "food_name", "category", "diet_type", "calories", "protein", "carbohydrates", "fat", "fiber", "sodium_mg", "sugar_g", "allergens"]
        st.dataframe(df_view[table_cols], use_container_width=True, hide_index=True)
    else:
        for i in range(0, len(df_view), 2):
            g_cols = st.columns(2)
            for j in range(2):
                idx = i + j
                if idx < len(df_view):
                    row = df_view.iloc[idx]
                    with g_cols[j]:
                        st.markdown(f"""
                        <div class="food-card-modern" style="padding:1rem;">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                <h4 style="margin:0; font-size:1.05rem; color:#0F172A !important;">{row['food_name']}</h4>
                                <span class="tag-chip" style="background:#F0FDFA !important; color:#0F766E !important;">{row['category']}</span>
                            </div>
                            <p style="margin:0.25rem 0 0.5rem 0; font-size:0.84rem; color:#475569 !important;">{row['description']}</p>
                            <div style="display:flex; gap:0.35rem; flex-wrap:wrap; font-size:0.78rem;">
                                <span class="macro-pill">🔥 {row['calories']} kcal</span>
                                <span class="macro-pill">🥩 P: {row['protein']}g</span>
                                <span class="macro-pill">🍞 C: {row['carbohydrates']}g</span>
                                <span class="macro-pill">🥑 F: {row['fat']}g</span>
                                <span class="macro-pill">🌾 Fib: {row['fiber']}g</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


# =========================================================
# PAGE 6: 📊 NUTRITION ANALYTICS
# =========================================================
elif selected_nav == "📊 Nutrition Analytics":
    st.markdown(f"""
    <div class="page-header-box">
        <div>
            <h2 class="page-title">📊 Visual Nutrition Analytics</h2>
            <div class="page-subtitle">Macronutrient caloric energy split and meal caloric budget for {user_profile['name']}.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    daily_plan = recommender.build_full_day_plan(filtered_df, targets["per_meal_targets"])
    meals = daily_plan["meals"]
    actual_totals = daily_plan["actual_totals"]

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("##### 🍩 Macronutrient Caloric Energy Split")
        p_cal = targets["target_protein"] * 4.0
        c_cal = targets["target_carbs"] * 4.0
        f_cal = targets["target_fat"] * 9.0

        donut_df = pd.DataFrame({
            "Nutrient": ["Protein (4 kcal/g)", "Carbohydrates (4 kcal/g)", "Healthy Fats (9 kcal/g)"],
            "Grams": [targets["target_protein"], targets["target_carbs"], targets["target_fat"]],
            "Calories": [p_cal, c_cal, f_cal],
            "Share": [
                f"{round(p_cal / targets['target_calories'] * 100, 1)}%",
                f"{round(c_cal / targets['target_calories'] * 100, 1)}%",
                f"{round(f_cal / targets['target_calories'] * 100, 1)}%"
            ]
        })

        donut_chart = alt.Chart(donut_df).mark_arc(innerRadius=65, stroke="#FFFFFF", strokeWidth=2).encode(
            theta=alt.Theta(field="Calories", type="quantitative"),
            color=alt.Color(
                field="Nutrient",
                type="nominal",
                scale=alt.Scale(
                    domain=["Protein (4 kcal/g)", "Carbohydrates (4 kcal/g)", "Healthy Fats (9 kcal/g)"],
                    range=["#0F766E", "#0284C7", "#F59E0B"]
                ),
                legend=alt.Legend(orient="bottom", titleFontSize=12, labelFontSize=11)
            ),
            tooltip=["Nutrient", "Grams", "Calories", "Share"]
        ).properties(height=320)

        st.altair_chart(donut_chart, use_container_width=True)

    with c2:
        st.markdown("##### 📈 Meal Caloric Budget vs Recommended Plan")
        meal_chart_data = []
        for m in ["Breakfast", "Lunch", "Dinner", "Snack"]:
            target_c = targets["per_meal_targets"][m]["calories"]
            actual_c = meals[m]["calories"] if meals.get(m) else 0
            meal_chart_data.append({"Meal": m, "Type": "Target Budget", "Calories": target_c})
            meal_chart_data.append({"Meal": m, "Type": "Recommended Plan", "Calories": actual_c})

        meal_bar = alt.Chart(pd.DataFrame(meal_chart_data)).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X("Meal:N", title="Meal Category", sort=["Breakfast", "Lunch", "Dinner", "Snack"]),
            y=alt.Y("Calories:Q", title="Calories (kcal)"),
            color=alt.Color(
                "Type:N",
                scale=alt.Scale(domain=["Target Budget", "Recommended Plan"], range=["#94A3B8", "#0D9488"]),
                legend=alt.Legend(orient="bottom", title=None)
            ),
            xOffset="Type:N",
            tooltip=["Meal", "Type", "Calories"]
        ).properties(height=320)

        st.altair_chart(meal_bar, use_container_width=True)


# =========================================================
# PAGE 7: 👤 MY PROFILE
# =========================================================
elif selected_nav == "👤 My Profile":
    st.markdown(f"""
    <div class="page-header-box">
        <div>
            <h2 class="page-title">👤 Patient Profile & Settings</h2>
            <div class="page-subtitle">View and update your health biometrics, dietary restrictions, and clinical advice.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    prof_tab_view, prof_tab_edit = st.tabs(["📋 Current Profile Summary", "✏️ Edit Profile & Clinical Guidelines"])

    with prof_tab_view:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0F766E 0%, #0369A1 100%); border-radius: 14px; padding: 1.4rem 1.6rem; color: white; margin-bottom: 1.2rem;">
            <h3 style="margin:0; font-size:1.4rem; color:white !important;">{user_profile['name']}</h3>
            <p style="margin:0.2rem 0 0 0; opacity:0.9; font-size:0.9rem; color:#E0F2FE !important;">{user_profile['email']}</p>
        </div>
        """, unsafe_allow_html=True)

        pc1, pc2 = st.columns(2)
        with pc1:
            st.markdown("##### 👤 Physical Biometrics")
            st.markdown(f"""
            - **Age**: {user_profile['age']} years
            - **Gender**: {user_profile['gender']}
            - **Height**: {user_profile['height_cm']} cm
            - **Current Weight**: {user_profile['weight_kg']} kg
            - **Target Goal Weight**: {user_profile['target_weight']} kg
            - **Body Mass Index (BMI)**: {bmi} ({bmi_category})
            - **Activity Level**: {user_profile['activity_level']}
            """)

        with pc2:
            st.markdown("##### 🥗 Nutrition & Medical Constraints")
            st.markdown(f"""
            - **Dietary Preference**: {user_profile['food_preference']}
            - **Primary Health Goal**: {user_profile['primary_goal']}
            - **Allergies Excluded**: {', '.join(all_user_allergies) if all_user_allergies else 'None'}
            - **Foods to Avoid**: {user_profile['foods_to_avoid'] or 'None'}
            - **Doctor Restrictions**: {', '.join(user_profile['doctor_restrictions']) if user_profile['doctor_restrictions'] else 'None'}
            - **Doctor Custom Notes**: {user_profile['doctor_custom_notes'] or 'None'}
            """)

    with prof_tab_edit:
        st.markdown("##### ✏️ Update Your Biometrics & Clinical Guidelines")
        with st.form("edit_profile_form"):
            ep_col1, ep_col2 = st.columns(2)
            with ep_col1:
                edit_name = st.text_input("Full Name", value=user_profile["name"])
                edit_age = st.number_input("Age (Years)", min_value=12, max_value=115, value=user_profile["age"], step=1)
                gender_opts = ["Male", "Female", "Other"]
                edit_gender = st.selectbox("Gender", gender_opts, index=gender_opts.index(user_profile["gender"]))
                edit_height = st.number_input("Height (cm)", min_value=90.0, max_value=240.0, value=float(user_profile["height_cm"]), step=0.5)
                edit_weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=250.0, value=float(user_profile["weight_kg"]), step=0.5)
                edit_target_weight = st.number_input("Target Weight (kg)", min_value=30.0, max_value=250.0, value=float(user_profile["target_weight"]), step=0.5)

            with ep_col2:
                act_opts = [
                    "Sedentary (little to no exercise)",
                    "Lightly Active (light exercise 1-3 days/wk)",
                    "Moderately Active (moderate exercise 3-5 days/wk)",
                    "Very Active (hard exercise 6-7 days/wk)"
                ]
                edit_activity = st.selectbox("Activity Level", act_opts, index=act_opts.index(user_profile["activity_level"]))
                pref_opts = ["Vegetarian", "Non-Vegetarian"]
                edit_pref = st.radio("Food Preference", pref_opts, index=pref_opts.index(user_profile["food_preference"]), horizontal=True)
                goal_opts = ["Weight Loss", "Weight Gain", "Maintain Weight"]
                edit_goal = st.selectbox("Primary Goal", goal_opts, index=goal_opts.index(user_profile["primary_goal"]))

                all_allergens = ["Dairy", "Gluten", "Nuts", "Peanuts", "Seafood", "Eggs", "Soy"]
                edit_allergies = st.multiselect("Food Allergies", options=all_allergens, default=[a for a in user_profile["allergies"] if a in all_allergens])
                edit_custom_allergies = st.text_input("Other Allergens", value=user_profile["custom_allergies"])
                edit_foods_to_avoid = st.text_input("Foods or Ingredients to Avoid", value=user_profile["foods_to_avoid"])

                doc_preset_options = [
                    "Low Sodium / Hypertension Friendly",
                    "Low Sugar / Diabetic Friendly",
                    "Low Fat / Cholesterol Conscious",
                    "Low Carb / Metabolic Friendly",
                    "Gluten-Free (Celiac / Sensitivity)",
                    "High Fiber / Digestive Health",
                    "Renal Friendly (Kidney Care)"
                ]
                edit_doctor_restrictions = st.multiselect("Clinical Prescriptions", options=doc_preset_options, default=[d for d in user_profile["doctor_restrictions"] if d in doc_preset_options])
                edit_doctor_notes = st.text_area("Doctor Instructions", value=user_profile["doctor_custom_notes"])

            save_profile_submit = st.form_submit_button("💾 Save Changes & Recalculate Nutrition", use_container_width=True, type="primary")

            if save_profile_submit:
                updated_data = {
                    "name": edit_name,
                    "age": edit_age,
                    "gender": edit_gender,
                    "height": edit_height,
                    "weight": edit_weight,
                    "target_weight": edit_target_weight,
                    "activity_level": edit_activity,
                    "food_preference": edit_pref,
                    "primary_goal": edit_goal,
                    "allergies": edit_allergies,
                    "custom_allergies": edit_custom_allergies,
                    "foods_to_avoid": edit_foods_to_avoid,
                    "dietary_restrictions": edit_doctor_restrictions,
                    "doctor_custom_notes": edit_doctor_notes
                }
                success = db.update_user_profile(user_id, updated_data)
                if success:
                    st.session_state["user_name"] = edit_name
                    st.success("Profile and clinical parameters updated! Recalculating targets...")
                    st.rerun()
                else:
                    st.error("Failed to update profile.")


# =========================================================
# PAGE 8: 🩺 MEDICAL GUIDELINES
# =========================================================
elif selected_nav == "🩺 Medical Guidelines":
    st.markdown("""
    <div class="page-header-box">
        <div>
            <h2 class="page-title">🩺 Clinical Methodology & Medical Guidelines</h2>
            <div class="page-subtitle">Scientific foundations, ethical parameters, and safety guidelines.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-card" style="font-size:0.92rem; padding:1.25rem;">
        <h4 style="color:#0F766E !important; margin-top:0;">🛡️ Core Healthcare Disclaimer & Ethical Boundary:</h4>
        NutriAI is strictly an educational lifestyle planning application. <strong>It does NOT diagnose medical conditions, provide clinical diagnoses, or prescribe therapeutic diets.</strong><br>
        For individuals undergoing medical therapy (including hypertension, cardiovascular disease, diabetes, celiac disease, or renal conditions), the recommendation engine strictly applies dietary restrictions <strong>explicitly entered by the user or advised by a registered dietitian or licensed physician</strong>.
    </div>
    """, unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("""
        ### 1. Basal Metabolic Rate (Mifflin-St Jeor)
        The system relies on the clinically validated **Mifflin-St Jeor Equation** to calculate Basal Metabolic Rate (BMR):
        
        $$\\text{BMR}_{\\text{male}} = 10 \\times \\text{weight (kg)} + 6.25 \\times \\text{height (cm)} - 5 \\times \\text{age} + 5$$
        $$\\text{BMR}_{\\text{female}} = 10 \\times \\text{weight (kg)} + 6.25 \\times \\text{height (cm)} - 5 \\times \\text{age} - 161$$
        
        **Total Daily Energy Expenditure (TDEE):**
        - **Sedentary:** $1.20 \\times \\text{BMR}$
        - **Light Activity:** $1.375 \\times \\text{BMR}$
        - **Moderate Activity:** $1.55 \\times \\text{BMR}$
        - **Very Active:** $1.725 \\times \\text{BMR}$
        
        **Goal Calibration:**
        - *Weight Loss:* Safe $\\sim 20\\%$ caloric deficit ($-500$ kcal) with elevated protein ($32\\%$) for lean mass retention.
        - *Weight Gain:* $+400$ kcal surplus with balanced protein ($25\\%$) and complex carbs ($50\\%$).
        - *Maintenance:* Caloric equilibrium ($25\\%$ P, $50\\%$ C, $25\\%$ F).
        """)

    with g2:
        st.markdown("""
        ### 2. Clinical Restriction Thresholds
        When a user enters doctor-advised dietary guidance, the system applies strict clinical filtering rules:
        - **Low Sodium / Hypertension:** Excludes any food containing $> 320$ mg sodium per portion.
        - **Low Sugar / Diabetic Friendly:** Filters out dishes with $> 8$ g of simple sugars; favors low-glycemic, fiber-rich whole foods.
        - **Low Fat / Cholesterol Conscious:** Drops items with $> 15$ g fat per meal.
        - **Low Carb / Metabolic:** Excludes recipes with $> 35$ g carbohydrates.
        - **Gluten-Free:** Strictly purges wheat, barley, rye, and gluten-contaminated grains for Celiac safety.
        - **Renal Friendly:** Constrains both sodium ($< 300$ mg) and excessive protein burden ($< 25$ g) to minimize kidney filtration strain.
        """)

    st.markdown("---")
    st.markdown("""
    ### 3. Machine Learning Architecture (Scikit-Learn)
    - **Feature Scaling:** Uses Scikit-Learn's `StandardScaler` to normalize 5 dimensions: `[Calories, Protein, Carbohydrates, Fat, Fiber]`.
    - **K-Nearest Neighbors:** Identifies candidate dishes using Euclidean distance in normalized feature space matching the target meal profile.
    - **Cosine Similarity:** Evaluates the angle between the dish's macronutrient proportions and the user's ideal macro balance.
    - **Transparent Match Score:** Combines macro alignment ($60\\%$) with portion calorie proximity ($40\\%$) to yield an intuitive $0 - 100\\%$ match score.
    """)


# =========================================================
# PAGE 9: ℹ️ ABOUT
# =========================================================
elif selected_nav == "ℹ️ About":
    st.markdown("""
    <div class="page-header-box">
        <div>
            <h2 class="page-title">ℹ️ About NutriAI Project</h2>
            <div class="page-subtitle">Project overview, technology stack, and academic demonstration details.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    a1, a2 = st.columns([1.6, 1.0])

    with a1:
        st.markdown("""
        ### 🌟 Project Vision
        **NutriAI** is an AI-based Personalized Food Recommendation System engineered to bridge clinical nutrition science with modern machine learning. 
        Unlike generic recipe recommenders, NutriAI respects individual biometrics, metabolic expenditure, food allergies, ingredient dislikes, and physician-prescribed dietary restrictions.

        #### 💻 Technology Stack
        - **Language:** Python 3.9+
        - **Database:** SQLite (`data/nutriai.db`) with PBKDF2 password hashing
        - **Machine Learning:** Scikit-Learn (`NearestNeighbors`, `StandardScaler`, `cosine_similarity`)
        - **Data Processing:** Pandas, NumPy
        - **Web Application:** Streamlit (Custom Healthcare SaaS Light Theme)
        - **Data Visualization:** Altair Interactive Charts
        - **Metabolic Model:** Mifflin-St Jeor Energy Expenditure Algorithm

        #### 📚 Dataset Specifications
        - **Total Records:** 58 thoroughly vetted, nutrient-dense dishes across Breakfast, Lunch, Dinner, and Snacks.
        - **Attributes per dish:** Food Name, Meal Category, Calories, Protein, Carbohydrates, Fat, Fiber, Diet Type, Allergens, Sodium (mg), Sugar (g), Clinical Tags, Preparation Notes.
        """)

    with a2:
        st.markdown("""
        ### 🎓 Academic Project Info
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.4rem; box-shadow:0 2px 8px rgba(15,23,42,0.04);">
            <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase; color:#0F766E;">Project Title</div>
            <div style="font-size:1.1rem; font-weight:800; color:#0F172A; margin-bottom:0.8rem;">AI-Based Personalized Food Recommendation System</div>
            
            <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase; color:#0F766E;">Domain</div>
            <div style="font-size:0.92rem; color:#334155; margin-bottom:0.8rem;">Artificial Intelligence / Healthcare & Clinical Nutrition</div>
            
            <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase; color:#0F766E;">Key Algorithms</div>
            <div style="font-size:0.92rem; color:#334155; margin-bottom:0.8rem;">K-Nearest Neighbors, Content-Based Filtering, Cosine Similarity, Feature Normalization</div>

            <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase; color:#0F766E;">Authentication & Storage</div>
            <div style="font-size:0.92rem; color:#334155; margin-bottom:0.8rem;">SQLite, PBKDF2 Password Hashing, User Data Isolation</div>

            <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase; color:#0F766E;">Development Status</div>
            <div style="font-size:0.92rem; color:#059669; font-weight:700;">● Production Ready / SaaS Polished</div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# CONSISTENT FOOTER
# ---------------------------------------------------------
st.markdown("""
<div class="nutri-footer">
    <strong>NutriAI™ Healthcare & Clinical Nutrition Platform</strong> | Built with Python, Pandas, Scikit-learn, SQLite & Streamlit<br>
    Educational and academic demonstration platform. Always consult a licensed healthcare professional before making dietary changes.
</div>
""", unsafe_allow_html=True)
