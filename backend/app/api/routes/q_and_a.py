import random

from fastapi import APIRouter 


router = APIRouter()

@router.get("/question")
def get_question(document: str=""):
    # List of 5 random questions
    questions = [
        "What is the capital of France?",
        "Who wrote 'To Kill a Mockingbird'?",
        "What is the chemical symbol for water?",
        "What year was the Declaration of Independence signed?",
        "Who painted the Mona Lisa?",
    ]
    
    # Select a random question from the list
    random_question = random.choice(questions)
    
    return random_question