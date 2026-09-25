import json
import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyse_symptoms(assessment):

    prompt = f"""
You are a cautious health information assistant.

The user reported:

Symptoms:
{", ".join(assessment.symptoms)}

Duration:
{assessment.duration}

Progress:
{assessment.progress}

Experienced before:
{assessment.experienced_before}

Medical history:
{assessment.medical_history}

Family history:
{assessment.family_history}

Additional information:
{assessment.additional_information}

Do not provide a definitive diagnosis.

Instead, provide possible explanations associated
with the reported symptoms.

Classify the recommended next step as exactly one of:

self_care
pharmacy
doctor
urgent

Also provide practical next steps and warning signs.

Return ONLY valid JSON using this structure:

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
        model="gpt-6-luna",
        input=prompt
    )

    try:
        return json.loads(response.output_text)

    except json.JSONDecodeError:
        raise ValueError(
            "The AI returned an invalid response."
        )