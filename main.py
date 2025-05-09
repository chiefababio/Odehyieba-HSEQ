from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

app = FastAPI()

# Load a pre-trained NLP model (zero-shot classification for simplicity)
classifier = pipeline("zero-shot-classification")

# Define possible root causes and contributing factors
ROOT_CAUSES = ["Human Error", "Equipment Failure", "Environmental Condition", "Lack of PPE", "Inadequate Training"]
CONTRIBUTING_FACTORS = ["Fatigue", "Poor Lighting", "Distraction", "Time Pressure", "Communication Breakdown"]

class IncidentReport(BaseModel):
    report: str

@app.post("/analyze-incident")
def analyze_incident(data: IncidentReport):
    try:
        result_root = classifier(data.report, ROOT_CAUSES)
        result_factors = classifier(data.report, CONTRIBUTING_FACTORS)

        top_root = result_root['labels'][0]
        top_factors = result_factors['labels'][:2]  # Top 2 contributing factors

        return {
            "root_cause": top_root,
            "contributing_factors": ", ".join(top_factors)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For local testing
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
