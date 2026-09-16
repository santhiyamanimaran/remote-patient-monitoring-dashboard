from pydantic import BaseModel, Field
class VitalReadingCreate(BaseModel):
    patient_id: int = Field(gt=0)
    heart_rate: float = Field(ge=30, le=220)
    spo2: float = Field(ge=70, le=100)
    temperature: float = Field(ge=30, le=45)
    systolic_bp: float = Field(ge=60, le=250)
    diastolic_bp: float = Field(ge=30, le=150)
    sugar_level: float = Field(ge=40, le=500)