import json
from fastapi import FastAPI, HTTPException, Cookie
from typing import Optional
from database.kidinteraction import KidInteraction
from fastapi import Depends
from database.session import Session

app = FastAPI()

def load_scenarios():
    with open('scenarios.json', 'r') as f:
        return json.load(f)

@app.get("/questions")
async def get_all_questions():
    try:
        scenarios = load_scenarios()
        return scenarios
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading scenarios")

@app.get("/question/{question_id}")
async def get_question(question_id: str):
    try:
        scenarios = load_scenarios()
        question_key = f"q{question_id}"
        
        if question_key not in scenarios:
            raise HTTPException(status_code=404, detail="Question not found")
            
        return scenarios[question_key]
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Scenarios file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving question")

@app.post("/answer/{question_id}")
async def submit_answer(
    question_id: str, 
    option_id: str, 
    kid_id: int = Cookie(None)
):
    try:
        if not kid_id:
            raise HTTPException(status_code=401, detail="Kid ID not found in session")

        scenarios = load_scenarios()
        question_key = f"q{question_id}"
        
        if question_key not in scenarios:
            raise HTTPException(status_code=404, detail="Question not found")
        
        question = scenarios[question_key]
        selected_option = None
        
        # Find the selected option
        for opt_key, option in question["options"].items():
            if option["id"] == option_id:
                selected_option = option
                break
        
        if not selected_option:
            raise HTTPException(status_code=404, detail="Option not found")
        
        # Log the interaction
        await KidInteraction.create_interaction(
            kid_id=kid_id,
            question_id=int(question_id),
            option_id=int(option_id[-1]),  # Assuming option_id format like "1a", "2b", etc.
            is_correct=selected_option["correct"]
        )
        
        return {
            "correct": selected_option["correct"],
            "message": "Answer recorded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progress/{kid_id}")
async def get_progress(kid_id: int):
    try:
        interactions = await KidInteraction.get_interactions_by_kid(kid_id)
        correct_answers = await KidInteraction.get_interactions_by_kid_and_correctness(kid_id, True)
        
        return {
            "total_questions_attempted": len(interactions),
            "correct_answers": len(correct_answers),
            "interactions": interactions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving progress")