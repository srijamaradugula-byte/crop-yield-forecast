"""REST API consumed by the mobile app to fetch forecast + advisory alert.

Run: uvicorn app.api:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel
from src.alerts import build_alert
from src.predict import predict_yield

app = FastAPI(title="Crop Yield Forecast API")

class Field(BaseModel):
    district: str
    crop: str
    season: str
    soil_type: str
    irrigation: str
    area_acres: float
    rainfall_mm: float
    avg_temp_c: float
    humidity_pct: float
    fertilizer_kg_per_acre: float
    sowing_month: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(field: Field):
    data = field.model_dump()
    y = predict_yield(data)
    alert = build_alert(field.crop, field.district, y, field.area_acres)
    return {"predicted_yield_per_acre": round(y, 2), "alert": alert}
