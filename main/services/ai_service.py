import json
import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyse_symptoms(assessment):
    """Send an assessment to the AI and return a structured result."""

    prompt = f"""
You are a health information assistant.

The user has reported the following:

Symptoms:
{", ".join(assessment.symptoms)}

Duration:
{assessment.duration}

Symptoms changing:
{assessment.progress}

Experienced this before:
{assessment.experienced_before}

Relevant medical history:
{assessment.medical_history}

Family history:
{assessment.family_history}

Additional information:
{assessment.additional_information}

Provide cautious health information.

Do not provide a definitive diagnosis.

Identify possible conditions or explanations that
could be associated with the reported symptoms.

Classify the recommended next step as exactly one of:

self_care
pharmacy
doctor
urgent

Also provide warning signs and practical next steps.

Return ONLY valid JSON in this format:

{{
    "possible_conditions": [
        {{
            "name": "...",
            "explanation": "..."
        }}
    ],
    "urgency": "...",
    "next_steps": [
        "..."
    ],
    "warning_signs": [
        "..."
    ]
}}
"""

    response = client.responses.create(
        model="YOUR_MODEL_NAME",
        input=prompt
    )

    return json.loads(response.output_text)