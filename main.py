
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import openai
import json
from datetime import datetime
from typing import List

app = FastAPI()

# Allow CORS for local development and frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API key
openai.api_key = "your-openai-api-key"

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./incidents.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DB Models
class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    location = Column(String)
    description = Column(Text)
    people_involved = Column(String)
    immediate_causes = Column(Text)
    contributing_factors = Column(Text)
    root_cause = Column(Text)
    underlying_causes = Column(Text)
    corrective_actions = Column(Text)
    analyzed_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Model
class IncidentData(BaseModel):
    date: str
    location: str
    description: str
    peopleInvolved: str
    immediateCauses: str
    contributingFactors: str

# Response Model
class IncidentAnalysis(BaseModel):
    rootCause: str
    underlyingCauses: str
    correctiveActions: str
    analyzedAt: str

# Retrieval Model
class IncidentRecord(BaseModel):
    id: int
    date: str
    location: str
    description: str
    peopleInvolved: str
    immediateCauses: str
    contributingFactors: str
    rootCause: str
    underlyingCauses: str
    correctiveActions: str
    analyzedAt: str

    class Config:
        orm_mode = True

@app.post("/api/analyze")
async def analyze_incident(data: IncidentData, db: Session = Depends(get_db)):
    prompt = f"""
    Analyze this safety incident and respond strictly in this JSON format:
    {{
      "rootCause": "...",
      "underlyingCauses": "...",
      "correctiveActions": "..."
    }}

    Description: {data.description}
    Immediate Causes: {data.immediateCauses}
    Contributing Factors: {data.contributingFactors}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )

        output = response.choices[0].message.content.strip()
        result = json.loads(output)

        analyzed_at = datetime.utcnow()

        # Save to DB
        incident = Incident(
            date=data.date,
            location=data.location,
            description=data.description,
            people_involved=data.peopleInvolved,
            immediate_causes=data.immediateCauses,
            contributing_factors=data.contributingFactors,
            root_cause=result["rootCause"],
            underlying_causes=result["underlyingCauses"],
            corrective_actions=result["correctiveActions"],
            analyzed_at=analyzed_at
        )

        db.add(incident)
        db.commit()
        db.refresh(incident)

        return IncidentAnalysis(
            rootCause=incident.root_cause,
            underlyingCauses=incident.underlying_causes,
            correctiveActions=incident.corrective_actions,
            analyzedAt=incident.analyzed_at.isoformat()
        )

    except Exception as e:
        return {"error": str(e)}

@app.get("/api/incidents", response_model=List[IncidentRecord])
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).order_by(Incident.analyzed_at.desc()).all()
    return incidents
