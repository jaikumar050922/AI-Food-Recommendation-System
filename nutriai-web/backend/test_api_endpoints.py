import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from fastapi.testclient import TestClient
from main import app
from core.database import init_db, seed_demo_user

def run_api_integration_tests():
    init_db()
    seed_demo_user()
    client = TestClient(app)

    print("--- 1. Testing Health Endpoint ---")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert res.json()["status"] == "healthy"
    print("✅ Health endpoint passed!")

    print("--- 2. Testing Demo Authentication ---")
    res = client.post("/api/auth/demo")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert "access_token" in data
    token = data["access_token"]
    user = data["user"]
    assert user["email"] == "demo@nutriai.com"
    assert user["target_calories"] > 1000
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Demo authentication passed!")

    print("--- 3. Testing Profile Retrieval & Update ---")
    res = client.get("/api/profile", headers=headers)
    assert res.status_code == 200
    profile = res.json()
    assert profile["user_id"] == user["user_id"]

    update_payload = {
        "name": "Alex Morgan Updated",
        "age": profile["age"],
        "gender": profile["gender"],
        "height_cm": profile["height_cm"],
        "weight_kg": profile["weight_kg"],
        "target_weight": 69.5,
        "activity_level": profile["activity_level"],
        "food_preference": profile["food_preference"],
        "primary_goal": profile["primary_goal"],
        "allergies": profile["allergies"],
        "custom_allergies": profile["custom_allergies"],
        "foods_to_avoid": profile["foods_to_avoid"],
        "dietary_restrictions": profile["dietary_restrictions"],
        "doctor_custom_notes": profile["doctor_custom_notes"]
    }
    res = client.put("/api/profile", json=update_payload, headers=headers)
    assert res.status_code == 200
    assert res.json()["target_weight"] == 69.5
    print("✅ Profile retrieval and update passed!")

    print("--- 4. Testing AI Recommendations ---")
    res = client.get("/api/recommend?category=Breakfast&top_n=3", headers=headers)
    assert res.status_code == 200
    rec_data = res.json()
    assert "recommendations" in rec_data
    assert len(rec_data["recommendations"]) > 0
    top_item = rec_data["recommendations"][0]
    assert "match_score" in top_item
    print(f"✅ AI recommendations passed! Top: {top_item['food_name']} ({top_item['match_score']}%)")

    print("--- 5. Testing 1-Day Clinical Meal Plan ---")
    res = client.get("/api/recommend/meal-plan", headers=headers)
    assert res.status_code == 200
    plan_data = res.json()
    assert "meals" in plan_data
    assert "Breakfast" in plan_data["meals"]
    assert "adherence_pct" in plan_data
    print(f"✅ Meal plan passed! Adherence: {plan_data['adherence_pct']['calories']}%")

    print("--- 6. Testing Food Database Catalog ---")
    res = client.get("/api/foods?search=quinoa&limit=5")
    assert res.status_code == 200
    catalog = res.json()
    assert catalog["total_count"] > 0
    print(f"✅ Food catalog search passed! Found {catalog['total_count']} matching items")

    print("--- 7. Testing Progress Tracking ---")
    progress_payload = {
        "date": "2026-10-24",
        "weight": 76.2,
        "calories": 1850,
        "protein": 150,
        "carbs": 165,
        "fat": 50,
        "notes": "Automated API integration test entry"
    }
    res = client.post("/api/progress", json=progress_payload, headers=headers)
    assert res.status_code == 201
    res = client.get("/api/progress", headers=headers)
    assert res.status_code == 200
    entries = res.json()
    assert len(entries) >= 8
    print(f"✅ Progress tracking passed! Total entries: {len(entries)}")

    print("--- 8. Testing Clinical Guidelines ---")
    res = client.get("/api/guidelines")
    assert res.status_code == 200
    guidelines = res.json()
    assert len(guidelines) >= 5
    print(f"✅ Clinical guidelines passed! {len(guidelines)} medical protocols verified")

    print("\n🎉 ALL 8 API INTEGRATION TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    run_api_integration_tests()
