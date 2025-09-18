# factspeak_ai.py

from transformers import pipeline

# Load QA pipeline model (this is FactSpeak AI for now)
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def get_fact_based_answer(question: str, context: str) -> str:
    result = qa_pipeline(question=question, context=context)
    return result['answer']
