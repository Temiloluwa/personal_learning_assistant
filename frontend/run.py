"""
Authors: Temiloluwa Adeoti
Date: March 13, 2024

This module contains the frontend code of personal learning assistant

Below are placeholder functions that should be replaced with the right REST API Calls
"""

import random
import time

import streamlit as st

# Utility functions


def get_ques_info_from_state(key: int):
    """
        Gets the current question infomation if available
        st.session_state["all_questions_info"] is a dictionary of dictionaries

        Each key is a integer and value as a dictionary with question, answer, feedback, is_correct_answer

        example:
        {
            {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "feedback": "Your answer is correct!",
            "is_correct_answer": True
            }
        }

        if the key is not present, it return a dictionary whose values are all null
    """
    return st.session_state["all_questions_info"].get(key,
                                                      {"question": None, "answer": None, "feedback": None, "is_correct_answer": None})


def check_valid_ques_info(current_question_info: dict):
    """
    Checks if all the values in current_question_info are not None
    It excludes the is_correct_answer key
    """
    for k, v in current_question_info.items():
        # exclude is_correct_answer
        if k != "is_correct_answer" and v is None:
            return False
    return True


# GET REST API METHODS


def get_question(document: str = ""):
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


def get_feedback(question: str = "", answer: str = ""):
    is_correct_answer = random.choice([True, False])
    feedback = "Your answer is correct!" if is_correct_answer else "Your answer is incorrect. Here is an explanation"

    return feedback, is_correct_answer


def get_summary(document: str = ""):
    summary = """
                The document provides an overview of recent advancements in renewable energy technologies. 
                It explores innovative approaches to solar, wind, and hydroelectric power generation, 
                highlighting their potential to mitigate climate change and meet growing energy demands sustainably. 
                Case studies illustrate successful implementation strategies and future prospects for renewable energy integration.
              """
    return summary


def get_document_info_from_db(document):
    document_details = {"user": "default_user",
                        "name": document.name,
                        "type": document.type,
                        "size": document.size}

    return document_details


def post_question_info_to_db(current_question_info: dict):
    """Simulate Posting Question to DB"""
    with st.status("Posting Question Info to Db...", expanded=True) as status:
        st.write("Posting")
        time.sleep(1)


def post_document_for_ingestion(document):
    """
    Function should
    1. upload document to s3 for ingestion to vector database
    """
    progress_text = f"Preparing document {document.name}. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.02)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()


def check_if_document_has_been_ingested(document):
    """
    Function should
    1. check if document has been ingested to vector database
    """
    get_document_info_from_db(document)

    return False


def check_if_new_document_has_been_added(document):
    """
    Function should
    1. check if document already exists in state
    """
    file_info = st.session_state["file_info"]
    if file_info:
        for k, v in file_info.items():
            if v != getattr(document, k, None):
                return False
        return True
    return False


def update_learning_progress():
    total_questions = len(st.session_state.all_questions_info)
    correct_answers = sum(1 for item in st.session_state.all_questions_info.values(
    ) if item.get("is_correct_answer") is True)
    incorrect_answers = total_questions - correct_answers

    st.session_state.total_questions = total_questions
    st.session_state.correct_answers = correct_answers
    st.session_state.incorrect_answers = incorrect_answers


# Initialize State Variables
if "all_questions_info" not in st.session_state:
    st.session_state["all_questions_info"] = {}

if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0

if "file_info" not in st.session_state:
    st.session_state["file_info"] = {}

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
    current_question_info = get_ques_info_from_state(current_question)
    current_question_info = show_question(current_question_info)
    current_question_info = show_answer(current_question_info)
    current_question_info = show_feedback(current_question_info)

    return current_question_info


st.set_page_config(layout="wide")
st.image("asset/imgs/hero.jpg")
st.title('Personal Learning Assistant')

with st.sidebar:
    
    uploaded_file = st.file_uploader('Upload a PDF Document', type=['pdf'])
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
        
col1, col2 = st.columns(2)

if uploaded_file is not None:
    # add document information to state
    if not check_if_new_document_has_been_added(uploaded_file):
        st.session_state["file_info"] = {"name": uploaded_file.name,
                                         "type": uploaded_file.type,
                                         "size": uploaded_file.size}

        # ingest file
        if not check_if_document_has_been_ingested(uploaded_file):
            post_document_for_ingestion(uploaded_file)

    with col1:
        current_question_info = main()
        is_valid_ques_dict = check_valid_ques_info(current_question_info)

        if is_valid_ques_dict and st.session_state["current_question"] not in st.session_state["all_questions_info"]:
            st.session_state["all_questions_info"][st.session_state["current_question"]
                                                   ] = current_question_info
            update_learning_progress()
            post_question_info_to_db(current_question_info)

        col_previous, col_next = st.columns(2)
        with col_previous:
            if st.session_state["current_question"] != 0 and is_valid_ques_dict:
                if st.button('Previous Question'):
                    st.session_state["current_question"] = max(
                        0, st.session_state["current_question"] - 1)
                    st.rerun()

        with col_next:
            if is_valid_ques_dict and st.button('Next Question'):
                st.session_state["current_question"] = max(
                    0, st.session_state["current_question"] + 1)
                st.rerun()

    with col2:
        st.subheader("Document Summary")
        summary = get_summary(uploaded_file)
        st.write(summary)

    st.sidebar.header('Uploaded PDF Document')
    st.sidebar.write(f"**Filename:** {uploaded_file.name}")

    if len(st.session_state["all_questions_info"]) > 1:
        st.sidebar.header('Learning Progress')
        st.sidebar.write(
            f'Total Questions Answered: {st.session_state["total_questions"]}')
        st.sidebar.write(
            f'Correct Answers: {st.session_state["correct_answers"]}')
        st.sidebar.write(
            f'Incorrect Answers: {st.session_state["incorrect_answers"]}')

    st.write(st.session_state)
