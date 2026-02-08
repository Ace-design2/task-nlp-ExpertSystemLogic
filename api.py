from fastapi import FastAPI, HTTPException
from src.study_planner import CourseDataLoader, StudyPlanner
import os

app = FastAPI(title="AI Study Planner API")

# Path to data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "courses.json")

# Initialize loader and planner (could successfully load once or per request depending on requirements.
# For simplicity and to ensure up-to-date data, we'll keep it simple, but robust apps might load once at startup)
# Checking if file exists at startup is good practice though.
if not os.path.exists(DATA_PATH):
    print(f"WARNING: Data file not found at {DATA_PATH}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Study Planner API. Use /schedule to generate a study plan."}

@app.get("/schedule")
def get_schedule(query: str, days: int):
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Course data file not found.")
    
    try:
        loader = CourseDataLoader(DATA_PATH)
        planner = StudyPlanner(loader)
        result = planner.generate_schedule(query, days)
        
        if "error" in result:
             raise HTTPException(status_code=400, detail=result["error"])
             
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
