"""Streamlit UI Application for Interview Preparation Coach with Modern Interactive Design."""

import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root using absolute path so Streamlit always finds it
_ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_ROOT / ".env")

import streamlit as st
from agents.orchestrator import InterviewOrchestrator

# -------------------------------------------------
# Page configuration & Modern Styling
# -------------------------------------------------
st.set_page_config(
    page_title="Interview Preparation Coach",
    page_icon="🎓",
    layout="wide",
)

# Custom CSS for Modern Dark Glassmorphism Aesthetics
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Card Container */
    .custom-card {
        background: linear-gradient(135deg, #1e2640 0%, #151b2e 100%);
        border: 1px solid #2d3748;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25);
    }
    
    /* Badges */
    .badge-role {
        background: linear-gradient(90deg, #4f46e5 0%, #6366f1 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-right: 8px;
    }
    
    .badge-topic {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-right: 8px;
    }
    
    .badge-diff {
        background: linear-gradient(90deg, #d97706 0%, #fbbf24 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }

    /* Score Badges */
    .score-green {
        background-color: #059669;
        color: white;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .score-yellow {
        background-color: #d97706;
        color: white;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .score-red {
        background-color: #dc2626;
        color: white;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Interview Preparation Coach")
st.caption("Agentic AI Interview Preparation Assistant (IT41043)")

# -------------------------------------------------
# Session state initialisation
# -------------------------------------------------
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = InterviewOrchestrator()
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "Software Engineer"

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

orchestrator: InterviewOrchestrator = st.session_state.orchestrator

# -------------------------------------------------
# Sidebar – session metrics & role selector
# -------------------------------------------------
with st.sidebar:
    st.header("📋 Session Dashboard")
    stats = orchestrator.get_summary()
    q_count = stats["questions_asked"]
    running = stats["running_score"]
    max_pts = q_count * 10
    pct = round((running / max_pts * 100), 1) if max_pts > 0 else 0.0

    st.metric("Total Score", f"{running} / {max_pts}")
    st.metric("Questions Answered", q_count)
    st.metric("Average Score", f"{stats['average_score']} / 10")
    st.metric("Accuracy Rate", f"{pct}%")
    
    st.divider()
    # Role selection (interactive)
    selected = st.selectbox(
        "Select Target Role",
        ["Software Engineer", "Data Analyst", "Product Manager", "UX Designer"],
        index=0,
    )
    if selected != st.session_state.selected_role:
        st.session_state.selected_role = selected
        # Reset session when role changes to avoid mixing scores
        st.session_state.orchestrator = InterviewOrchestrator()
        st.session_state.t1_question_res = None
        st.session_state.t1_coach_res = None
        st.session_state.t1_answered = False
        st.session_state.t1_finished = False
        st.session_state.t2_tip_res = None
        st.session_state.t3_expert_res = None
        st.rerun()

    st.divider()
    if st.button("🔄 Reset Session", type="secondary", use_container_width=True):
        st.session_state.orchestrator = InterviewOrchestrator()
        st.session_state.t1_question_res = None
        st.session_state.t1_coach_res = None
        st.session_state.t1_answered = False
        st.session_state.t1_finished = False
        st.session_state.t2_tip_res = None
        st.session_state.t3_expert_res = None
        st.rerun()

# -------------------------------------------------
# Main navigation tabs
# -------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🎯 Practice Questions",
    "💡 How to Face an Interview",
    "🤝 Connect with Industry Experts",
])

# -------------------------------------------------
# Tab 1 – Practice Questions (role‑aware & modern)
# -------------------------------------------------
with tab1:
    summary_stats = orchestrator.get_summary()
    running_score = summary_stats["running_score"]
    q_asked = summary_stats["questions_asked"]
    max_possible = q_asked * 10

    # Prominent score header
    st.markdown(
        f"### 📊 Active Track – **{st.session_state.selected_role}**: **Score: {running_score}/{max_possible}** ({q_asked} Attempted)"
    )
    st.divider()

    # ---------------------------------------------
    # FINISHED SESSION REPORT DASHBOARD
    # ---------------------------------------------
    if st.session_state.t1_finished:
        st.markdown("## 🎉 Interactive Session Performance Report")
        
        # Calculate summary grade badge
        avg_s = summary_stats['average_score']
        if avg_s >= 8.5:
            grade_badge = "🌟 Master Class Performance (90%+ Accuracy)"
            grade_color = "success"
        elif avg_s >= 6.5:
            grade_badge = "👍 Solid Competency (70%+ Accuracy)"
            grade_color = "info"
        else:
            grade_badge = "💪 Practice Recommended (<65% Accuracy)"
            grade_color = "warning"

        if grade_color == "success":
            st.success(f"**Overall Assessment:** {grade_badge}")
        elif grade_color == "info":
            st.info(f"**Overall Assessment:** {grade_badge}")
        else:
            st.warning(f"**Overall Assessment:** {grade_badge}")

        # Metrics Columns
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Score Earned", f"{running_score} / {max_possible}")
        with m2:
            st.metric("Questions Attempted", q_asked)
        with m3:
            st.metric("Average Score", f"{avg_s} / 10")
        with m4:
            acc_val = round((running_score / max_possible * 100), 1) if max_possible > 0 else 0
            st.metric("Accuracy Rate", f"{acc_val}%")

        st.divider()

        # Interactive Performance Chart
        if summary_stats["history"]:
            st.markdown("### 📈 Question Performance Chart")
            chart_data = {
                f"Q{i+1}: {h['question'][:30]}...": h['score']
                for i, h in enumerate(summary_stats["history"])
            }
            st.bar_chart(chart_data)

            st.divider()

            # Detailed Expandable Question Review
            st.markdown("### 🔍 Detailed Question & Feedback Review")
            for idx, h in enumerate(summary_stats["history"], 1):
                score_val = h['score']
                icon = "🟢" if score_val >= 8 else ("🟡" if score_val >= 6 else "🔴")
                
                with st.expander(f"{icon} Question {idx}: {h['question'][:70]}... (Score: {score_val}/10)", expanded=(idx==1)):
                    st.markdown(f"**Full Question:** {h['question']}")
                    st.markdown(f"**Your Submitted Answer:**\n>{h['user_answer']}")
                    st.markdown(f"**AI Reference Answer:**\n>{h['correct_answer']}")
                    st.markdown(f"**Coach Feedback & Evaluation:**\n{h['feedback']}")

            st.divider()

            # Generate Downloadable Markdown Report
            report_lines = [
                f"# Interview Performance Report - {st.session_state.selected_role}",
                f"**Total Score:** {running_score} / {max_possible}",
                f"**Average Score:** {avg_s} / 10",
                f"**Overall Grade:** {grade_badge}\n",
                "## Detailed History\n"
            ]
            for i, item in enumerate(summary_stats["history"], 1):
                report_lines.append(f"### Q{i}: {item['question']}")
                report_lines.append(f"- **Your Answer:** {item['user_answer']}")
                report_lines.append(f"- **Reference Answer:** {item['correct_answer']}")
                report_lines.append(f"- **Score:** {item['score']} / {item['max_score']}")
                report_lines.append(f"- **Feedback:** {item['feedback']}\n")

            full_report_text = "\n".join(report_lines)

            col_rep1, col_rep2 = st.columns([2, 1])
            with col_rep1:
                st.download_button(
                    label="📥 Download Performance Report (.md)",
                    data=full_report_text,
                    file_name=f"interview_report_{st.session_state.selected_role.lower().replace(' ', '_')}.md",
                    mime="text/markdown",
                    type="primary"
                )
            with col_rep2:
                if st.button("Start New Practice Session"):
                    st.session_state.t1_finished = False
                    st.session_state.t1_question_res = None
                    st.session_state.t1_coach_res = None
                    st.session_state.t1_answered = False
                    st.rerun()

    # ---------------------------------------------
    # ACTIVE PRACTICE QUESTION VIEW
    # ---------------------------------------------
    else:
        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            btn_label = "Get Question" if st.session_state.t1_question_res is None else "Next Question"
            if st.button(btn_label, type="primary", key="btn_get_q"):
                try:
                    with st.spinner(f"Fetching {st.session_state.selected_role} question…"):
                        q_res = orchestrator.start_panel(
                            "practice_questions",
                            role=st.session_state.selected_role
                        )
                        st.session_state.t1_question_res = q_res
                        st.session_state.t1_coach_res = None
                        st.session_state.t1_answered = False
                        st.rerun()
                except Exception as e:
                    print(f"[Tab 1 Error]: {e}")
                    st.error("Something went wrong retrieving your question — please try again.")
        with col_btn2:
            if q_asked > 0 and st.button("Finish Session & View Report"):
                st.session_state.t1_finished = True
                st.rerun()

        # Display Active Question Card
        if st.session_state.t1_question_res:
            q_data = st.session_state.t1_question_res
            
            st.markdown(f"""
            <div class="custom-card">
                <div>
                    <span class="badge-role">🎯 {st.session_state.selected_role}</span>
                    <span class="badge-topic">📌 {q_data.topic}</span>
                </div>
                <h3 style="margin-top: 15px; color: #f8fafc;">{q_data.question}</h3>
            </div>
            """, unsafe_allow_html=True)

            # Interactive Hint Expander
            with st.expander("💡 Need a Hint / Key Concepts to Include?"):
                st.write(f"Focus on explaining the underlying **{q_data.topic}** principles clearly with practical examples or step-by-step logic.")

            # Candidate Input Area
            user_ans_text = st.text_area(
                "Type your response below:",
                height=160,
                disabled=st.session_state.t1_answered,
                key="txt_user_answer"
            )
            
            word_count = len(user_ans_text.strip().split()) if user_ans_text.strip() else 0
            st.caption(f"Word count: {word_count} words")

            if not st.session_state.t1_answered:
                if st.button("Submit Answer for AI Evaluation", type="secondary", key="btn_submit_ans"):
                    if not user_ans_text.strip():
                        st.warning("Please type an answer before submitting.")
                    else:
                        try:
                            with st.spinner("Evaluating your response with AI Coach…"):
                                coach_res = orchestrator.submit_answer(user_ans_text)
                                st.session_state.t1_coach_res = coach_res
                                st.session_state.t1_answered = True
                                st.rerun()
                        except Exception as e:
                            print(f"[Tab 1 Submit Error]: {e}")
                            st.error("Something went wrong retrieving your evaluation — please try again.")

            # Display Evaluation Results
            if st.session_state.t1_coach_res:
                c_res = st.session_state.t1_coach_res
                score = c_res.score
                max_s = c_res.max_score
                
                st.divider()
                st.markdown("### 📝 AI Coach Evaluation")
                
                if score >= 8:
                    st.success(f"**🏆 Excellent Answer! Score: {score}/{max_s}**\n\n{c_res.feedback}")
                elif score >= 6:
                    st.info(f"**👍 Good Attempt! Score: {score}/{max_s}**\n\n{c_res.feedback}")
                else:
                    st.warning(f"**💪 Needs Improvement. Score: {score}/{max_s}**\n\n{c_res.feedback}")

                with st.expander("🔍 Compare with Reference Answer Key"):
                    st.info(f"**Reference Answer Concept:**\n\n{q_data.correct_answer}")

# -------------------------------------------------
# Tab 2 – Interview Technique Coaching (role‑aware)
# -------------------------------------------------
with tab2:
    st.markdown("### 💡 Interview Technique & Strategy Guidance")
    st.write(f"Tailored advice and best practices for **{st.session_state.selected_role}** interviews.")
    
    btn_label = "Get Coaching Tip" if st.session_state.t2_tip_res is None else "Fetch Another Tip"
    if st.button(btn_label, type="primary", key="btn_get_tip"):
        try:
            with st.spinner("Retrieving interview technique advice…"):
                tip_res = orchestrator.start_panel(
                    "how_to_face_interview",
                    role=st.session_state.selected_role
                )
                st.session_state.t2_tip_res = tip_res
                st.rerun()
        except Exception as e:
            print(f"[Tab 2 Error]: {e}")
            st.error("Something went wrong retrieving your tip — please try again.")
            
    if st.session_state.t2_tip_res:
        t_data = st.session_state.t2_tip_res
        st.divider()
        st.subheader(f"📌 Role: {st.session_state.selected_role} | Topic: {t_data.topic}")
        clean_tip_text = re.sub(r'^##\s*', '', t_data.question).strip()
        st.markdown(clean_tip_text)

# -------------------------------------------------
# Tab 3 – Connect with Industry Experts (Modern Remake)
# -------------------------------------------------
with tab3:
    st.markdown("## 🤝 Expert Networking & Outreach Studio")
    st.caption(f"Build genuine industry connections, request 15-minute informational interviews, and land job referrals for **{st.session_state.selected_role}** roles.")
    st.divider()

    # SECTION 1: 3-Step Networking Playbook
    st.markdown("### 🚀 Step-by-Step Networking Playbook")
    col_pb1, col_pb2, col_pb3 = st.columns(3)
    
    with col_pb1:
        st.markdown("""
        #### 🔎 1. Identify & Prospect
        - **Target**: Senior {role}s, Lead Engineers, or University Alumni at your dream companies.
        - **Research**: Read their recent posts, patents, or shared articles before reaching out.
        """.format(role=st.session_state.selected_role))
        
    with col_pb2:
        st.markdown("""
        #### ✍️ 2. The 300-Char Hook
        - Keep LinkedIn notes **under 300 characters**.
        - Include 1 personal hook (e.g. shared university, specific post, or common tech stack).
        - **Never** ask for a job in the first message.
        """)

    with col_pb3:
        st.markdown("""
        #### ☕ 3. 15-Min Info Chat
        - Ask for a brief 15-minute virtual coffee chat.
        - Prepare 3 thoughtful questions about their career growth and technical challenges.
        - Send a warm thank-you note within 24 hours.
        """)

    st.divider()

    # SECTION 2: Interactive Outreach Template Builder
    st.markdown("### ✉️ Interactive Message Template Builder")
    st.write("Customize outreach messages tailored to your target role and scenario:")

    template_type = st.selectbox(
        "Select Outreach Scenario",
        [
            "🎓 University Alumni Connection",
            "☕ Informational Interview Request",
            "🎤 Post-Event / Webinar Follow-Up",
            "🚀 Respectful Job Referral Request",
            "⚡ Role-Specific Cold Outreach",
        ],
        key="sb_template_type"
    )

    with st.expander("⚙️ Customize Message Placeholders (Optional)", expanded=True):
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            your_name = st.text_input("Your Name", value="Alex", key="input_your_name")
            expert_name = st.text_input("Expert / Professional Name", value="Sarah", key="input_expert_name")
        with c_p2:
            target_company = st.text_input("Target Company", value="Google", key="input_target_company")
            specific_topic = st.text_input("Specific Topic / Event / Project", value="System Design & AI Agent Architecture", key="input_topic")

    # Generate custom template string based on choice
    role_curr = st.session_state.selected_role

    if "Alumni" in template_type:
        template_text = (
            f"Hi {expert_name}, I noticed we both graduated from University! I am currently preparing for "
            f"roles in {role_curr} and am really inspired by your career journey at {target_company}. "
            f"I would love to connect and follow your work in the field.\n\nBest regards,\n{your_name}"
        )
        pro_tip = "💡 Pro-Tip: Mentioning shared school or university background boosts LinkedIn connection acceptance rates by over 40%!"

    elif "Informational Interview" in template_type:
        template_text = (
            f"Hi {expert_name}, thank you for connecting! I really enjoyed reading your insights on {specific_topic}. "
            f"As an aspiring {role_curr}, I would be incredibly grateful to hear about your experience at {target_company}. "
            f"Would you be open to a brief 15-minute virtual coffee chat sometime next week?\n\nThanks so much,\n{your_name}"
        )
        pro_tip = "💡 Pro-Tip: Be specific about why you want to talk to them. Respect their time by promising to keep it strictly under 15 minutes."

    elif "Post-Event" in template_type:
        template_text = (
            f"Hi {expert_name}, it was great attending your talk on {specific_topic}! I really resonated with "
            f"your points regarding {role_curr} best practices. I'd love to stay connected here on LinkedIn "
            f"and keep in touch as I pursue opportunities in the industry.\n\nBest,\n{your_name}"
        )
        pro_tip = "💡 Pro-Tip: Send this within 24 hours of the event while the conversation is still fresh in their memory!"

    elif "Referral Request" in template_type:
        template_text = (
            f"Hi {expert_name}, hope you are having a great week! I recently applied for the {role_curr} position "
            f"at {target_company}. Having followed your team's work on {specific_topic}, I'm extremely excited about "
            f"the direction. If you have a few minutes, I'd appreciate any advice on the team culture, or a brief "
            f"referral if appropriate.\n\nThanks for your time!\n{your_name}"
        )
        pro_tip = "💡 Pro-Tip: Only ask for a referral if you have built initial rapport or have a mutual connection."

    else:  # Role-Specific Cold Outreach
        template_text = (
            f"Hi {expert_name}, I came across your profile while researching lead {role_curr} professionals working "
            f"on {specific_topic} at {target_company}. As someone passionate about {role_curr}, I would love to connect "
            f"and follow your work!\n\nBest,\n{your_name}"
        )
        pro_tip = f"💡 Pro-Tip: Tailor your message to focus specifically on {role_curr} skills and project topics!"

    st.markdown("#### 📋 Ready-to-Send Message Card:")
    st.code(template_text, language="text")
    st.info(pro_tip)

    st.divider()

    # SECTION 3: RAG AI Knowledge Base Insights
    st.markdown("### 🤖 Deep-Dive Knowledge Base Advice (AI RAG)")
    st.write(f"Pull advanced strategic guides from our vector knowledge base for **{role_curr}**:")

    btn_t3_label = "Fetch AI Knowledge Base Insight" if st.session_state.t3_expert_res is None else "Fetch Another AI Insight"
    if st.button(btn_t3_label, type="primary", key="btn_get_expert"):
        try:
            with st.spinner("Retrieving expert networking insight from Knowledge Base…"):
                expert_res = orchestrator.start_panel(
                    "connect_with_experts",
                    role=st.session_state.selected_role
                )
                st.session_state.t3_expert_res = expert_res
                st.rerun()
        except Exception as e:
            print(f"[Tab 3 Error]: {e}")
            st.error("Something went wrong retrieving your guide — please try again.")

    if st.session_state.t3_expert_res:
        e_data = st.session_state.t3_expert_res
        st.markdown(f"#### 🌐 Topic: **{e_data.topic}**")
        raw_text = e_data.question
        clean_text = re.sub(r'^##\s*', '', raw_text).strip()
        st.success(f"**Knowledge Insight:**\n\n{clean_text}")
