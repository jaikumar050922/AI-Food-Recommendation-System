from typing import List, Dict, Any
from fastapi import APIRouter

router = APIRouter(prefix="/guidelines", tags=["Clinical Guidelines"])

CLINICAL_GUIDELINES = [
    {
        "id": "hypertension",
        "title": "Low Sodium / Hypertension Friendly",
        "threshold": "Sodium <= 320mg per serving",
        "clinical_rationale": "Excess dietary sodium elevates intravascular volume and systemic vascular resistance. Following DASH diet principles reduces systolic blood pressure by 8–14 mmHg.",
        "recommended_foods": "Fresh leafy greens, potassium-rich lentils, unsalted oatmeal, sweet potatoes, raw seeds.",
        "strictly_avoid": "Cured meats, canned soups, salted snacks, soy sauce, processed condiments."
    },
    {
        "id": "diabetic",
        "title": "Low Glycemic / Diabetic Friendly",
        "threshold": "Added Sugars <= 8.0g per serving, High Dietary Fiber",
        "clinical_rationale": "Prioritizes foods with low glycemic index (GI < 55) to mitigate postprandial glycemic excursions and improve HbA1c control without hyperinsulinemia.",
        "recommended_foods": "Moong dal cheela, wild salmon, chia seed porridge, firm tofu, cruciferous vegetables.",
        "strictly_avoid": "Refined sugars, white flour toast, fruit juices, sugary cereals, sweetened yogurts."
    },
    {
        "id": "renal",
        "title": "Renal / Kidney Disease Conscious",
        "threshold": "Sodium <= 300mg, Controlled Protein <= 25g per serving",
        "clinical_rationale": "Stages 3-4 Chronic Kidney Disease (CKD) require moderating protein nitrogenous waste burden and controlling sodium/phosphorus retention to slow GFR decline.",
        "recommended_foods": "Egg whites, white basmati rice, steamed cauliflower, light vegetable curries.",
        "strictly_avoid": "High-sodium processed meals, high-potassium salt substitutes, dark colas, heavy red meats."
    },
    {
        "id": "heart_healthy",
        "title": "Lipid Lowering / Cardiovascular Support",
        "threshold": "Total Fat <= 15.0g per serving, Zero Trans Fats, High Soluble Fiber",
        "clinical_rationale": "AHA/ACC guidelines recommend reducing saturated fatty acids to < 7% of total caloric intake to lower ApoB and LDL-cholesterol.",
        "recommended_foods": "Atlantic wild salmon (rich in EPA/DHA), walnuts, extra virgin olive oil, oats, avocados.",
        "strictly_avoid": "Deep-fried foods, hydrogenated oils, palm oil, processed sausages, commercial pastries."
    },
    {
        "id": "celiac",
        "title": "Gluten-Free / Celiac Protocol",
        "threshold": "Strict Exclusion of Wheat, Rye, Barley, Spelt, and Triticale",
        "clinical_rationale": "Protects small bowel mucosal villi from autoimmune T-cell atrophy in patients diagnosed with Celiac disease or Non-Celiac Gluten Sensitivity (NCGS).",
        "recommended_foods": "Quinoa, brown rice, certified GF oats, idli, lentil pancakes, fresh fish and poultry.",
        "strictly_avoid": "Wheat bread, regular sourdough, rye crackers, conventional pasta, beer, malt extract."
    }
]

@router.get("", response_model=List[Dict[str, Any]])
def get_guidelines():
    """Returns clinical nutrition guidelines and evidence-based safety thresholds."""
    return CLINICAL_GUIDELINES
