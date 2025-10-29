import streamlit as st
from pydantic import BaseModel
from openai import AzureOpenAI

class TranscriptInsightsSet(BaseModel):
    call_summary: str
    call_duration: int
    call_resolution_status: str
    call_classification: list[str]
    call_complexity: str
    call_sentiment: str
    call_escalation_risk: str
    action_items: list[str]

def generate_summary(file_content):
    api_version = st.secrets["AOAI_VERSION"]
    api_key = st.secrets["AOAI_KEY"]
    endpoint = st.secrets["AOAI_ENDPOINT"]
    deployment = "o4-mini"

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )

    response = client.beta.chat.completions.parse(
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a pharmacy benefits management transcript analyzer. Generate the following based on the provided transcript:
                - a brief overview summary as a single paragraph
                - The duration of the call in minutes
                - The call's resolution status (Resolved, Pending, Escalated)
                - A list with the primary reason for call (refill, prior auth, billing question, coverage inquiry) and optionally, secondary issues addressed
                - Call complexity score
                - Classification on sentiment (single word)
                - Escalation risk (single word)
                - A list of action items for the PBM company, its representative, or other staff
                """
            },
            {
                "role": "user",
                "content": f"{file_content}",
            }
        ],
        response_format=TranscriptInsightsSet,
        max_completion_tokens=40000,
        model=deployment
    )

    return response.choices[0].message.content