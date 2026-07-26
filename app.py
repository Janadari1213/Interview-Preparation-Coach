"""Streamlit UI Application for Interview Preparation Coach."""

import streamlit as st
from agents.orchestrator import InterviewOrchestrator

# Page setup
st.set_page_config(
    page_title="Interview Preparation Coach",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Interview Preparation Coach")
st.caption("Agentic AI Interview Preparation Assistant (IT41043)")

# Initialize Orchestrator in session state if not present
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = InterviewOrchestrator()

# Session State for Tab 1
if "t1_question_res" not in st.session_state:
    st.session_state.t1_question_res = None
if "t1_coach_res" not in st.session_state:
    st.session_state.t1_coach_res = None
if "t1_answered" not in st.session_state:
    st.session_state.t1_answered = False
if "t1_finished" not in st.session_state:
    st.session_state.t1_finished = False

# Session State for Tab 2 & Tab 3
if "t2_tip_res" not in st.session_state:
    st.session_state.t2_tip_res = None
if "t3_expert_res" not in st.session_state:
    st.session_state.t3_expert_res = None

# Main navigation tabs
tab1, tab2, tab3 = st.tabs([
    "🎯 Practice Questions",
    "💡 How to Face an Interview",
    "🤝 Connect with Industry Experts"
])

with tab1:
    st.info("Welcome to Practice Questions panel. Click 'Get Question' below to begin your session.")

with tab2:
    st.info("Welcome to Interview Technique Coaching panel.")

with tab3:
    st.info("Welcome to Networking & Expert Outreach panel.")
