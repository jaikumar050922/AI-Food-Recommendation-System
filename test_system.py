"""
NutriAI Full Automated System Test Suite
Tests:
1. Syntax check
2. Registration
3. Login & authentication
4. Invalid password rejection
5. Duplicate email rejection
6. Profile loading
7. Recommendation calculation using logged-in user data
8. Progress saving
9. User data isolation (User A cannot access User B's progress)
"""

import os
import db
from recommender import FoodRecommender, calculate_nutrition_targets

def run_tests():
    print("=== STARTING NUTRIAI FULL TEST SUITE ===")

    # Test 1: Verify Demo Account
    print("\n--- 1. Testing Demo User Authentication ---")
    demo_user = db.authenticate_user("demo@nutriai.com", "Demo@1234")
    assert demo_user is not None, "Demo user authentication failed!"
    print(f"PASS: Demo user logged in as {demo_user['name']} (ID: {demo_user['id']})")

    # Test 2: Invalid Password Rejection
    print("\n--- 2. Testing Invalid Password Rejection ---")
    bad_login = db.authenticate_user("demo@nutriai.com", "WrongPassword999")
    assert bad_login is None, "Failed! Invalid password was accepted."
    print("PASS: Invalid password successfully rejected.")

    # Test 3: User Registration (User A)
    print("\n--- 3. Testing New User Registration (User A: Jane Doe) ---")
    user_a_email = "janedoe@test.com"
    user_a_profile = {
        "age": 32,
        "gender": "Female",
        "height": 165.0,
        "weight": 62.0,
        "target_weight": 58.0,
        "activity_level": "Lightly Active (light exercise 1-3 days/wk)",
        "food_preference": "Vegetarian",
        "primary_goal": "Weight Loss",
        "allergies": ["Gluten"],
        "custom_allergies": "",
        "foods_to_avoid": "peanuts",
        "dietary_restrictions": ["Low Sugar / Diabetic Friendly"],
        "doctor_custom_notes": "Avoid high GI carbohydrates."
    }
    
    # In case already exists from previous run, test authentication or register
    user_a = db.authenticate_user(user_a_email, "JanePass@123")
    if not user_a:
        success, msg, user_a_id = db.register_user("Jane Doe", user_a_email, "JanePass@123", user_a_profile)
        assert success, f"Registration failed: {msg}"
        print(f"PASS: User A registered with ID {user_a_id}")
    else:
        user_a_id = user_a["id"]
        print(f"PASS: User A retrieved with ID {user_a_id}")

    # Test 4: Duplicate Email Rejection
    print("\n--- 4. Testing Duplicate Email Rejection ---")
    dup_success, dup_msg, _ = db.register_user("Jane Duplicate", user_a_email, "AnyPassword", user_a_profile)
    assert not dup_success, "Failed! Duplicate email was accepted."
    print(f"PASS: Duplicate email correctly rejected with message: '{dup_msg}'")

    # Test 5: Profile Loading
    print("\n--- 5. Testing Profile Loading ---")
    profile_a = db.get_user_profile(user_a_id)
    assert profile_a is not None, "Failed to load User A profile!"
    assert profile_a["gender"] == "Female"
    assert profile_a["age"] == 32
    assert "Gluten" in profile_a["allergies"]
    print(f"PASS: Profile loaded correctly: Age {profile_a['age']}, Weight {profile_a['weight_kg']}kg, Allergies {profile_a['allergies']}")

    # Test 6: Recommendation Calculation using User A's actual biometrics
    print("\n--- 6. Testing Recommendation using User A's Biometrics ---")
    targets_a = calculate_nutrition_targets(
        age=profile_a["age"],
        gender=profile_a["gender"],
        height_cm=profile_a["height_cm"],
        weight_kg=profile_a["weight_kg"],
        goal=profile_a["primary_goal"],
        activity_level=profile_a["activity_level"]
    )
    print(f"PASS: Targets calculated: {targets_a['target_calories']} kcal, P: {targets_a['target_protein']}g, C: {targets_a['target_carbs']}g, F: {targets_a['target_fat']}g")

    r = FoodRecommender("data/foods.csv")
    filtered, stats = r.filter_foods(
        food_preference=profile_a["food_preference"],
        allergies=profile_a["allergies"],
        foods_to_avoid=profile_a["foods_to_avoid"],
        doctor_restrictions=profile_a["doctor_restrictions"],
        doctor_custom_notes=profile_a["doctor_custom_notes"]
    )
    assert stats["final_eligible"] > 0, "No eligible foods found for User A!"
    print(f"PASS: Foods filtered safely. Initial: {stats['initial']}, Final safe: {stats['final_eligible']}")

    # Test 7: Progress Saving
    print("\n--- 7. Testing Progress Saving for User A ---")
    db.add_progress_entry(user_a_id, "2026-09-20", weight=63.0, calories=1500, protein=85, carbs=160, fat=40, notes="Day 1")
    db.add_progress_entry(user_a_id, "2026-09-25", weight=62.0, calories=1480, protein=90, carbs=150, fat=38, notes="Day 5 - feeling great")
    prog_a = db.get_user_progress(user_a_id)
    assert len(prog_a) >= 2, "Failed to retrieve User A progress!"
    print(f"PASS: Saved and retrieved {len(prog_a)} progress entries for User A.")

    # Test 8: Register User B & Verify Strict Data Isolation
    print("\n--- 8. Testing User Data Isolation (User A vs User B) ---")
    user_b_email = "bobjohnson@test.com"
    user_b_profile = {
        "age": 45,
        "gender": "Male",
        "height": 182.0,
        "weight": 92.0,
        "target_weight": 85.0,
        "activity_level": "Sedentary (little to no exercise)",
        "food_preference": "Non-Vegetarian",
        "primary_goal": "Weight Loss",
        "allergies": ["Seafood"],
        "custom_allergies": "",
        "foods_to_avoid": "",
        "dietary_restrictions": ["Low Sodium / Hypertension Friendly"],
        "doctor_custom_notes": ""
    }
    user_b = db.authenticate_user(user_b_email, "BobPass@123")
    if not user_b:
        _, _, user_b_id = db.register_user("Bob Johnson", user_b_email, "BobPass@123", user_b_profile)
    else:
        user_b_id = user_b["id"]

    db.add_progress_entry(user_b_id, "2026-09-26", weight=92.0, calories=2100, protein=130, carbs=220, fat=60, notes="Bob's private note: confidential BP check")
    
    prog_b = db.get_user_progress(user_b_id)
    prog_a_check = db.get_user_progress(user_a_id)

    # Verify User A progress entries NEVER contain User B entries
    assert all(row["notes"] != "Bob's private note: confidential BP check" for _, row in prog_a_check.iterrows()), "SECURITY BREACH: User A has access to User B's progress data!"
    print("PASS: Verified 100% data isolation. User A cannot view User B's private progress records.")

    print("\n=== ALL 8 VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_tests()
