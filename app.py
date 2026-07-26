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

orchestrator: InterviewOrchestrator = st.session_state.orchestrator

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

# ==========================================
# TAB 1: PRACTICE QUESTIONS
# ==========================================
with tab1:
    summary_stats = orchestrator.get_summary()
    running_score = summary_stats["running_score"]
    q_asked = summary_stats["questions_asked"]
    max_possible = q_asked * 10

    # Prominent score header
    st.markdown(f"### 📊 Live Performance: **Score: {running_score}/{max_possible}** across **{q_asked}** question(s)")
    st.divider()

    if st.session_state.t1_finished:
        st.subheader("🏁 Session Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Score", f"{running_score} / {max_possible}")
        with col2:
            st.metric("Questions Asked", q_asked)
        with col3:
            st.metric("Average Score", f"{summary_stats['average_score']} / 10")
        
        st.divider()
        if summary_stats["history"]:
            st.write("#### Question History")
            for idx, h in enumerate(summary_stats["history"], 1):
                st.write(f"**Q{idx}:** {h['question']}")
                st.caption(f"Score: {h['score']}/{h['max_score']} | Feedback: {h['feedback']}")
                st.divider()

        if st.button("Start New Practice Session"):
            st.session_state.t1_finished = False
            st.session_state.t1_question_res = None
            st.session_state.t1_coach_res = None
            st.session_state.t1_answered = False
            st.rerun()

    else:
        # Question Control Buttons
        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            btn_label = "Get Question" if st.session_state.t1_question_res is None else "Next Question"
            if st.button(btn_label, type="primary", key="btn_get_q"):
                try:
                    with st.spinner("Fetching question from Knowledge Base..."):
                        q_res = orchestrator.start_panel("practice_questions")
                        st.session_state.t1_question_res = q_res
                        st.session_state.t1_coach_res = None
                        st.session_state.t1_answered = False
                        st.rerun()
                except Exception as e:
                    st.error("Something went wrong retrieving your question — please try again.")

        with col_btn2:
            if q_asked > 0 and st.button("Finish Session"):
                st.session_state.t1_finished = True
                st.rerun()

        # Display Active Question
        if st.session_state.t1_question_res:
            q_data = st.session_state.t1_question_res
            st.markdown(f"#### **Topic:** {q_data.topic}")
            st.info(q_data.question)

            # Candidate Input Area
            user_ans_text = st.text_area(
                "Type your response below:",
                height=150,
                disabled=st.session_state.t1_answered,
                key="txt_user_answer"
            )

            if not st.session_state.t1_answered:
                if st.button("Submit Answer", type="secondary", key="btn_submit_ans"):
                    if not user_ans_text.strip():
                        st.warning("Please type an answer before submitting.")
                    else:
                        try:
                            with st.spinner("Evaluating your response with AI Coach..."):
                                coach_res = orchestrator.submit_answer(user_ans_text)
                                st.session_state.t1_coach_res = coach_res
                                st.session_state.t1_answered = True
                                st.rerun()
                        except Exception as e:
                            st.error("Something went wrong retrieving your evaluation — please try again.")
            
            # Display Evaluation Results
            if st.session_state.t1_coach_res:
                c_res = st.session_state.t1_coach_res
                score_str = f"Score: {c_res.score} / {c_res.max_score}"
                
                st.divider()
                st.markdown("#### 📝 Coach Feedback")
                if c_res.score >= 6:
                    st.success(f"**{score_str}**\n\n{c_res.feedback}")
                else:
                    st.warning(f"**{score_str}**\n\n{c_res.feedback}")

# ==========================================
# TAB 2: HOW TO FACE AN INTERVIEW
# ==========================================
with tab2:
    st.markdown("### 💡 Interview Technique & Strategy Guidance")
    st.write("Browse best practices on STAR methodology, body language, and avoiding common candidate pitfalls.")
    
    btn_t2_label = "Get Coaching Tip" if st.session_state.t2_tip_res is None else "Fetch Another Tip"
    if st.button(btn_t2_label, type="primary", key="btn_get_tip"):
        try:
            with st.spinner("Retrieving interview technique advice..."):
                tip_res = orchestrator.start_panel("how_to_face_interview")
                st.session_state.t2_tip_res = tip_res
                st.rerun()
        except Exception as e:
            st.error("Something went wrong retrieving your tip — please try again.")

    if st.session_state.t2_tip_res:
        t_data = st.session_state.t2_tip_res
        st.divider()
        st.subheader(f"📌 Topic: {t_data.topic}")
        st.markdown(t_data.question)

# ==========================================
# TAB 3: CONNECT WITH INDUSTRY EXPERTS
# ==========================================
with tab3:
    st.markdown("### 🤝 Networking & Outreach Strategies")
    st.write("Learn how to connect with professionals on LinkedIn and leverage ready-to-use message templates.")

    btn_t3_label = "Get Outreach Guide / Template" if st.session_state.t3_expert_res is None else "Fetch Another Guide"
    if st.button(btn_t3_label, type="primary", key="btn_get_expert"):
        try:
            with st.spinner("Retrieving networking guidance..."):
                expert_res = orchestrator.start_panel("connect_with_experts")
                st.session_state.t3_expert_res = expert_res
                st.rerun()
        except Exception as e:
            st.error("Something went wrong retrieving your guide — please try again.")

    if st.session_state.t3_expert_res:
        e_data = st.session_state.t3_expert_res
        st.divider()
        st.subheader(f"🌐 Topic: {e_data.topic}")
        
        # Check if text contains message templates and highlight accordingly
        content_text = e_data.question
        if "Template" in content_text or "Hi [" in content_text:
            st.write("#### Message Template:")
            st.code(content_text, language="markdown")
        else:
            st.markdown(content_text)
