from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from services.recommender import recommender
from models.food import FoodItem, FoodCatalogResponse

router = APIRouter(prefix="/foods", tags=["Food Database"])

@router.get("", response_model=FoodCatalogResponse)
def get_foods(
    search: Optional[str] = Query(None, description="Search query matching food name or description"),
    category: Optional[str] = Query(None, description="Category filter (Breakfast, Lunch, Dinner, Snack)"),
    diet_type: Optional[str] = Query(None, description="Vegetarian or Non-Vegetarian"),
    allergen_free: Optional[str] = Query(None, description="Exclude specific allergen"),
    max_calories: Optional[float] = Query(None, description="Maximum calorie threshold"),
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """Search and filter the curated clinical food database."""
    df = recommender.df.copy()

    if search and search.strip():
        q = search.strip().lower()
        df = df[df["food_name"].str.lower().str.contains(q) | df["description"].str.lower().str.contains(q) | df["dietary_attributes"].str.lower().str.contains(q)]

    if category and category.lower() != "all":
        df = df[df["category"].str.lower() == category.lower()]

    if diet_type and diet_type.lower() != "all":
        df = df[df["diet_type"].str.lower() == diet_type.lower()]

    if allergen_free and allergen_free.strip():
        a = allergen_free.strip().lower()
        df = df[~df["allergens"].str.lower().str.contains(a)]

    if max_calories is not None and max_calories > 0:
        df = df[df["calories"] <= max_calories]

    total_count = len(df)
    sliced = df.iloc[offset : offset + limit]

    items = []
    for _, row in sliced.iterrows():
        macro_cal = (row["protein"] * 4.0) + (row["carbohydrates"] * 4.0) + (row["fat"] * 9.0)
        p_pct = round((row["protein"] * 4.0 / macro_cal) * 100, 1) if macro_cal > 0 else 0.0
        c_pct = round((row["carbohydrates"] * 4.0 / macro_cal) * 100, 1) if macro_cal > 0 else 0.0
        f_pct = round((row["fat"] * 9.0 / macro_cal) * 100, 1) if macro_cal > 0 else 0.0
        
        d = row.to_dict()
        d["protein_pct"] = p_pct
        d["carb_pct"] = c_pct
        d["fat_pct"] = f_pct
        items.append(d)

    return FoodCatalogResponse(total_count=total_count, items=items)


@router.get("/categories", response_model=List[str])
def get_categories():
    """Returns unique food categories present in the dataset."""
    return sorted(recommender.df["category"].unique().tolist())


@router.get("/{food_id}", response_model=FoodItem)
def get_food_by_id(food_id: int):
    """Retrieve full nutritional profile for a specific food item."""
    df = recommender.df
    matched = df[df["food_id"] == food_id]
    if matched.empty:
        raise HTTPException(status_code=404, detail="Food item not found")
        
    row = matched.iloc[0]
    macro_cal = (row["protein"] * 4.0) + (row["carbohydrates"] * 4.0) + (row["fat"] * 9.0)
    d = row.to_dict()
    d["protein_pct"] = round((row["protein"] * 4.0 / macro_cal) * 100, 1) if macro_cal > 0 else 0.0
    d["carb_pct"] = round((row["carbohydrates"] * 4.0 / macro_cal) * 100, 1) if macro_cal > 0 else 0.0
    d["fat_pct"] = round((row["fat"] * 9.0 / macro_cal) * 100, 1) if macro_cal > 0 else 0.0
    return d
