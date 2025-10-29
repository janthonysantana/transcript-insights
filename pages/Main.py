import json
import streamlit as st
from pydantic import BaseModel
from openai import AzureOpenAI

uploaded_file = None
bytes_data = None

def Navbar():
    with st.sidebar:
        st.page_link("app.py", label="Main Page")
        # st.page_link("", label="Analyze Transcript")
        # st.page_link("", label="Batch Transcript Analysis")
        # st.page_link("pages/Favorites.py", label="Favorites")

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

def display_insights(insights: TranscriptInsightsSet):
    insights_data = json.loads(insights)

    st.subheader("Call Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Duration", f"{insights_data["call_duration"]} min")
    with col2:
        st.metric("Status", insights_data["call_resolution_status"])
    with col3:
        st.metric("Complexity", insights_data["call_complexity"])
    with col4:
        sentiment = insights_data["call_sentiment"]
        st.metric("Sentiment", sentiment)

    # Alert box for escalation risk if high
    if insights_data['call_escalation_risk'].lower() in ['high', 'critical']:
        st.warning(f"⚠️ Escalation Risk: {insights_data['call_escalation_risk']}")
    else:
        st.info(f"✓ Escalation Risk: {insights_data['call_escalation_risk']}")
    
    st.subheader("Call Summary")
    st.write(insights_data["call_summary"])

    col_left, col_right = st.columns(2)
        
    with col_left:
        st.subheader("Classification")
        
        # Primary classification
        primary = insights_data['call_classification'][0]
        st.markdown(f"""
            <div style='background-color: #1f77b4; color: white; padding: 8px 16px; 
                        border-radius: 20px; display: inline-block; margin-bottom: 10px;'>
                <b>Primary:</b> {primary}
            </div>
        """, unsafe_allow_html=True)
    
    # Secondary classifications
    if len(insights_data['call_classification']) > 1:
        st.markdown("**Secondary Issues:**")
        for category in insights_data['call_classification'][1:]:
            st.markdown(f"- {category}")
    
    with col_right:
        st.subheader("Action Items")
        for action in insights_data['action_items']:
            st.markdown(f"- {action}")

def show_page():
    Navbar()

    st.title("Transcript Insights")
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        file_content = bytes_data.decode('utf-8')
            
        st.markdown(f"## {uploaded_file.name}")
        
        with st.expander("View Transcript", expanded=False):
            st.text_area(
                "Full Transcript", 
                file_content, 
                height=300,
                disabled=True,
                label_visibility="collapsed"
            )



    if st.button("Analyze", disabled=(uploaded_file is None)):
        with st.spinner("Analyzing transcript..."):
            insights = generate_summary(bytes_data.decode("utf-8"))
            st.session_state.insights = insights
            display_insights(insights)

    if "insights" in st.session_state:
        st.download_button("Export", 
                           st.session_state.insights, 
                           file_name="insights.json",
                           mime="application/json"
        )
