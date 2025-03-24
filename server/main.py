from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Dict, Any
import json
from pydantic import BaseModel

app = FastAPI(
    title="Autistic Kids App API",
    description="API for serving scenario-based questions for autistic children",
    version="1.0.0"
)

# Load scenarios from the JSON file
try:
    with open("scenarios.json", "r") as file:
        scenarios_data = json.load(file)
except FileNotFoundError:
    scenarios_data = {}
    print("Warning: scenarios.json file not found. Starting with empty data.")
except json.JSONDecodeError:
    scenarios_data = {}
    print("Warning: Invalid JSON in scenarios.json. Starting with empty data.")

# Define response models
class Option(BaseModel):
    id: str
    title: str
    correct: bool

class OptionDict(Dict[str, Option]):
    pass

class Scenario(BaseModel):
    id: str
    title: str
    description: str
    options: Dict[str, Option]

@app.get("/")
async def root():
    """Root endpoint providing basic information about the API"""
    return {
        "message": "Welcome to the Autistic Kids App API",
        "endpoints": {
            "/scenario/all": "Get all scenario IDs or a batch of them",
            "/scenario/{question_id}": "Get a specific scenario by ID"
        }
    }

@app.get("/scenario/all", response_model=List[str])
async def get_all_scenario_ids(batchsize: Optional[int] = Query(-1, description="Number of scenarios to return. -1 for all.")):
    """
    Get all scenario IDs or a batch of them based on the batchsize parameter.
    
    - If batchsize is -1 or not specified, return all question IDs
    - If batchsize is positive, return that number of question IDs
    """
    if not scenarios_data:
        return []
    
    # Extract all question IDs
    all_ids = [scenarios_data[q]["id"] for q in scenarios_data]
    
    # Return all IDs or a batch based on batchsize
    if batchsize == -1:
        return all_ids
    else:
        return all_ids[:batchsize]

@app.get("/scenario/{question_id}", response_model=Scenario)
async def get_scenario(question_id: str):
    """
    Get a specific scenario by its ID.
    
    Returns the full scenario data including title, description, and options.
    """
    # Find the scenario with the matching ID
    scenario = scenarios_data.get(question_id)
    if scenario:
        return scenario
    raise HTTPException(status_code=404, detail=f"Scenario with ID {question_id} not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)