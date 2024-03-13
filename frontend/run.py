"""
Authors: Temiloluwa Adeoti
Date: March 13, 2024

This module contains the frontend code of personal learning assistant
"""

import streamlit as st
import random

## dummy functions to be replace and imported from src folder

def get_value_at_index(dictionary, index):
    return dictionary.get(index, {"question": None, "answer": None, "feedback": None, "is_correct_answer": None})
      
def all_values_are_not_none(current_question_info: dict):
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
    st.session_state["question_information"].append(question_info)


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

if "current_question_info" not in st.session_state:
    st.session_state["current_question_info"] = {"question": None, "answer": None, "feedback": None, "is_correct_answer": None}

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


def show_question():
    # get the current question number
    current_question = st.session_state["current_question"]
    # get the dictionary from the list of all questions using the current question number
    current_question_info = get_value_at_index(st.session_state["all_questions_info"], current_question)
    # get the actual question
    question = current_question_info.get("question")
    # if the question does not exist
    if not question:
        # get the question from api
        question = get_question()
        # update the question in the current question info dictionary
        st.session_state["all_questions_info"][current_question] = {"question": question, "answer": None, "feedback": None, "is_correct_answer": None}
    
    st.subheader('Generated Question:')
    st.write(question)

    
def show_answer():
    # get the current question number
    current_question = st.session_state["current_question"]
    # get the dictionary from the list of all questions using the current question number
    current_question_info = get_value_at_index(st.session_state["all_questions_info"], current_question)
    # get the actual question for the current question
    question = current_question_info.get("question")
    # get the actual answer for the current question
    if question is None:
        raise ValueError("Question is None")
    
    answer = current_question_info.get("answer")
   
    if question and not answer:
        # get answer from user
        answer = get_answer()
    
    if answer:
        st.subheader('Your Answer:')
        st.write(answer)
        # update the answer in the current question info dictionary
        st.session_state["all_questions_info"][current_question] = {"question": question, "answer": answer, "feedback": None, "is_correct_answer": None}
    
    return answer
    
def show_feedback():
    # get the actual feedback, question and answer for the current question, 
    current_question = st.session_state["current_question"]
    current_question_info = get_value_at_index(st.session_state["all_questions_info"], current_question)
    
    question = current_question_info.get("question")
    answer = current_question_info.get("answer")
    feedback = current_question_info.get("feedback")
    
    if question and answer and not feedback:
        feedback, is_correct_answer = get_feedback(question, answer)
        st.session_state["all_questions_info"][current_question] = {"question": question, "answer": answer, "feedback": feedback, "is_correct_answer": is_correct_answer}

    if feedback:
        st.subheader('Feedback:')
        st.write(feedback)
        


def main():
    # show question and answer
    show_question()
    show_answer()
    show_feedback()
            

st.set_page_config(layout="wide")
st.image("asset/imgs/hero.jpg")
st.title('Personal Learning Assistant')

st.write(st.session_state)

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
with col1:
    if uploaded_file is not None:
        main()
        
        if len(st.session_state["all_questions_info"]) > 0:
            if st.button('Previous Question'):
                st.session_state["current_question"] -= 1
                st.rerun()
       
        if st.session_state["current_question"] < len(st.session_state["all_questions_info"]):
            if st.button('Next Question'):
                st.session_state["current_question"] += 1
                st.rerun()

                
if uploaded_file is not None:
    with col2:
        st.subheader("Document Summary")
        summary = get_summary(uploaded_file)
        st.write(summary)
    st.sidebar.header('Uploaded PDF Document')
    st.sidebar.write(f"**Filename:** {uploaded_file.name}")

    if len(st.session_state["all_questions_info"]) > 0:
        update_learning_progress()
        st.sidebar.header('Learning Progress')
        st.sidebar.write(f'Total Questions Answered: {st.session_state["total_questions"]}')
        st.sidebar.write(f'Correct Answers: {st.session_state["correct_answers"]}')
        st.sidebar.write(f'Incorrect Answers: {st.session_state["incorrect_answers"]}')