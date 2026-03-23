import os
from dotenv import load_dotenv
from services.qdrant_service import search_data
from services.qdrant_service import search_diseases

from openai import OpenAI   # Grok uses OpenAI-compatible API

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_grok_answer(query: str):
    # 🔍 Step 1: Get context from Qdrant
    results = search_data(query)
    context = " ".join([item["text"] for item in results])

    # 🧠 Step 2: Prompt
    prompt = f"""
You are an expert agriculture assistant.

Context:
{context}

Question:
{query}

Give a practical answer for farmers in simple language.
"""

    # 🤖 Step 3: Call Grok API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful farming assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def generate_disease_advice(query: str):
    results = search_diseases(query)

    if not results:
        return "No relevant disease found."

    top = results[0]
    alternatives = [r["disease"] for r in results[1:]]

    prompt = f"""
    You are an expert agriculture assistant.

    Farmer query:
    {query}

    Most likely disease:
    {top['disease']}

    Cause:
    {top['pathogen']}

    Affected parts:
    {', '.join(top['affected_part'])}

    Severity:
    {top['severity_hint']}

    Possible confusion:
    {', '.join(top['confusion_with'])}

    Other possible diseases:
    {', '.join(alternatives)}

    Explain in simple language:
    - what is happening
    - why
    - mention uncertainty
    - be practical for farmers
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful farming assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content