"""
Authors: Temiloluwa Adeoti
Date: March 13, 2024

This module contains the frontend code of personal learning assistant
"""

import streamlit as st
import random

## dummy functions to be replace and imported from src folder
def get_value_at_index(index):
    return st.session_state["all_questions_info"].get(index, {"question": None, "answer": None, "feedback": None, "is_correct_answer": None})
      
def check_valid_ques_dict(current_question_info: dict):
    for k, v in current_question_info.items():
        # exclude is_correct_answer
        if k != "is_correct_answer" and v is None:
            return False
    return True

def ingest_document(document: str=""):
    pass

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

def get_answer(answer=""):
    answer = st.text_input('Your Answer:')

    return answer


def post_question_response_feedback(
    document="",
    question_info=""):
    pass


def get_feedback(question: str="", answer: str=""):
    is_correct_answer = random.choice([True, False])
    feedback =  "Your answer is correct!" if is_correct_answer else "Your answer is incorrect. Here is an explanation"

    return feedback, is_correct_answer

def get_summary(document: str=""):
    summary = """
                The document provides an overview of recent advancements in renewable energy technologies. 
                It explores innovative approaches to solar, wind, and hydroelectric power generation, 
                highlighting their potential to mitigate climate change and meet growing energy demands sustainably. 
                Case studies illustrate successful implementation strategies and future prospects for renewable energy integration.
              """
    return summary


def update_learning_progress() -> dict:
    st.session_state['total_questions'] = len(st.session_state["all_questions_info"])
    correct_answers = sum(1 for item in st.session_state["all_questions_info"].values() if item.get("is_correct_answer") is True)
    st.session_state['correct_answers'] = correct_answers
    st.session_state['incorrect_answers'] = st.session_state['total_questions'] - correct_answers


if "all_questions_info" not in st.session_state:
    st.session_state["all_questions_info"] = {}

if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0

state_keys = [
    'total_questions',
    'correct_answers',
    'incorrect_answers',
]

for key in state_keys:
    if key not in st.session_state:
        st.session_state[key] = 0


def show_question(current_question_info):
    question = current_question_info.get("question", None)
    # if the question does not exist
    if not question:
        # get the question from api
        question = get_question()
        # update the question in the current question info dictionary
        current_question_info["question"] = question
    
    st.subheader('Generated Question:')
    st.write(question)

    return current_question_info

    
def show_answer(current_question_info):
    question = current_question_info.get("question", None)
    
    answer = current_question_info.get("answer")
    if question and not answer:
        # get answer from user
        answer = get_answer()
    
    if answer:
        st.subheader('Your Answer:')
        st.write(answer)
        current_question_info["answer"] = answer
    
    return current_question_info
    
def show_feedback(current_question_info):
    question = current_question_info.get("question", None)
    answer = current_question_info.get("answer", None)
    feedback = current_question_info.get("feedback", None)
    
    if question and answer and feedback is None:
        feedback, is_correct_answer = get_feedback(question, answer)
        current_question_info["feedback"] = feedback
        current_question_info["is_correct_answer"] = is_correct_answer
        update_learning_progress()

    if feedback:
        st.subheader('Feedback:')
        st.write(feedback)

    return current_question_info
        

def main():
    current_question = st.session_state["current_question"]
    current_question_info = get_value_at_index(current_question)
    current_question_info = show_question(current_question_info)
    current_question_info = show_answer(current_question_info)
    current_question_info = show_feedback(current_question_info)

    return current_question_info
            

st.set_page_config(layout="wide")
st.image("asset/imgs/hero.jpg")
st.title('Personal Learning Assistant')

with st.container():
    # Subheader: Instructions
    st.subheader("Instructions")

    # Summary of instructions
    st.write("""
    1. Upload a PDF study material.
    2. The Assistant generate questions from document.
    3. Answer questions with text input.
    4. Receive immediate feedback on answer.
    5. Click 'Next Question' to continue learning.
    6. Monitor progress in the sidebar.
    """)

col1, col2  = st.columns(2)
uploaded_file = st.sidebar.file_uploader('Upload a PDF Document', type=['pdf'])

if uploaded_file is not None:
    with col1:
        current_question_info = main()
        is_valid_ques_dict = check_valid_ques_dict(current_question_info)

        if is_valid_ques_dict and st.session_state["current_question"] not in st.session_state["all_questions_info"]:
            st.session_state["all_questions_info"][st.session_state["current_question"]] = current_question_info
            update_learning_progress()
        
        if st.session_state["current_question"] != 0 and is_valid_ques_dict:
            if st.button('Previous Question'):
                st.session_state["current_question"] = max(0, st.session_state["current_question"] - 1)
                st.rerun()
        
        if is_valid_ques_dict and st.button('Next Question'):
            st.session_state["current_question"] = max(0, st.session_state["current_question"] + 1)
            st.rerun()

                    
    with col2:
        st.subheader("Document Summary")
        summary = get_summary(uploaded_file)
        st.write(summary)
    
    st.sidebar.header('Uploaded PDF Document')
    st.sidebar.write(f"**Filename:** {uploaded_file.name}")

    if len(st.session_state["all_questions_info"]) > 1:
        st.sidebar.header('Learning Progress')
        st.sidebar.write(f'Total Questions Answered: {st.session_state["total_questions"]}')
        st.sidebar.write(f'Correct Answers: {st.session_state["correct_answers"]}')
        st.sidebar.write(f'Incorrect Answers: {st.session_state["incorrect_answers"]}')

    st.write(st.session_state)