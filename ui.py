import streamlit as st
import streamlit_ext as ste

# Import the necessary functions from app.py
from app import (
    generate_inquiry,
    generate_guiding_question,
    generate_essential_knowledge,
    generate_teacher_knowledge,
    generate_assessment,
    generate_inquiry_impact,
    generate_differentiation,
    generate_ipad,
    generate_western_views,
    generate_search_parameters,
    process_search_queries,
    generate_ai_integration,
)

def render_ui():
    # Page setup
    st.set_page_config(
        page_title="Inquiry Unit Planner",
        page_icon="🤖",
        initial_sidebar_state="expanded",
        layout="wide"
    )

    # Hide default Streamlit style
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Sidebar settings
    st.sidebar.header("Unit Planner")
    st.sidebar.write("Please provide the following information to generate an inquiry-based lesson plan.")
    st.sidebar.divider()

    grade = st.sidebar.text_input("Grade Level", "e.g., Grade 7")
    temperature = st.sidebar.slider("Temperature", min_value=0.00, max_value=1.00, value=0.85)
    outcomes = st.sidebar.text_area(
        "curriculum outcomes",
        "e.g, Students will be able to analyze the impact of cyberbullying on individuals and communities."
    )

    # Additional context controls
    st.sidebar.write("Would you like to add a bit more to the context?")
    on = st.sidebar.toggle("Yes", value=False)

    if on:
        user_context = st.sidebar.text_area("Please provide context that you would like to be included in the unit plan.")
        prompt = f"""Develop an inquiry-based lesson plan for {grade} that aligns with the following curricular outcomes: {outcomes}.
The lesson should embed the principles of authentic and meaningful tasks, student-centered learning, collaborative learning, 
an interdisciplinary approach, critical thinking and problem-solving, ongoing assessment and feedback, the teacher as facilitator, 
and reflective practice. 
Ensure that the scenario includes the following consideration: {user_context}.
"""
    else:
        prompt = f"""Develop an inquiry-based lesson plan for {grade} that aligns with the following curricular outcomes: {outcomes}.
The lesson should embed the principles of authentic and meaningful tasks, student-centered learning, collaborative learning, 
an interdisciplinary approach, critical thinking and problem-solving, ongoing assessment and feedback, the teacher as facilitator, 
and reflective practice.
"""

    if st.sidebar.button("Generate Unit", type="primary"):
        # Generate the main unit plan
        unit_plan = generate_inquiry(prompt, temperature)

        # Create tabs for each output section
        tabs = st.tabs([
            "Guiding Question",
            "Unit Plan",
            "Student Essential Knowledge",
            "Teacher Essential Knowledge",
            "Assessment Plan",
            "Inquiry Impact",
            "Differentiation",
            "iPad Integration",
            "Worldviews",
            "Search Queries",
            "AI Integration"
        ])

        # 1. Guiding Question
        with tabs[0]:
            st.subheader("Guiding Question")
            guiding_question = generate_guiding_question(unit_plan, temperature)
            st.write(guiding_question)
            ste.download_button("Download Guiding Question", guiding_question, "Guiding_Question.txt")

        # 2. Unit Plan
        with tabs[1]:
            st.subheader("Unit Plan")
            st.write(unit_plan)
            ste.download_button("Download Unit Plan", unit_plan, "Unit_Plan.txt")

        # 3. Student Essential Knowledge
        with tabs[2]:
            st.subheader("Student Essential Knowledge")
            essential_knowledge = generate_essential_knowledge(unit_plan, temperature)
            st.write(essential_knowledge)
            ste.download_button("Download Student Essential Knowledge", essential_knowledge, "Student_Essential_Knowledge.txt")

        # 4. Teacher Essential Knowledge
        with tabs[3]:
            st.subheader("Teacher Essential Knowledge")
            teacher_knowledge = generate_teacher_knowledge(unit_plan, temperature)
            st.write(teacher_knowledge)
            ste.download_button("Download Teacher Essential Knowledge", teacher_knowledge, "Teacher_Essential_Knowledge.txt")

        # 5. Assessment Plan
        with tabs[4]:
            st.subheader("Assessment Plan")
            assessment_plan = generate_assessment(unit_plan, temperature)
            st.write(assessment_plan)
            ste.download_button("Download Assessment Plan", assessment_plan, "Assessment_Plan.txt")

        # 6. Inquiry Impact
        with tabs[5]:
            st.subheader("Inquiry Impact")
            inquiry_impact = generate_inquiry_impact(unit_plan, temperature)
            st.write(inquiry_impact)
            ste.download_button("Download Inquiry Impact", inquiry_impact, "Inquiry_Impact.txt")

        # 7. Differentiation
        with tabs[6]:
            st.subheader("Differentiation")
            differentiation = generate_differentiation(unit_plan, temperature)
            st.write(differentiation)
            ste.download_button("Download Differentiation", differentiation, "Differentiation.txt")

        # 8. iPad Integration
        with tabs[7]:
            st.subheader("iPad Integration")
            ipad_integration = generate_ipad(unit_plan, temperature)
            st.write(ipad_integration)
            ste.download_button("Download iPad Integration", ipad_integration, "iPad_Integration.txt")

        # 9. Worldviews
        with tabs[8]:
            st.subheader("Worldviews")
            worldviews = generate_western_views(unit_plan, temperature)
            st.write(worldviews)
            ste.download_button("Download Worldviews", worldviews, "Worldviews.txt")

        # 10. Web Resources
        with tabs[9]:
            st.subheader("Web Resources")
            search_queries = generate_search_parameters(unit_plan, temperature, grade)
            if isinstance(search_queries, str):
                # If it's a string, it's likely an error message or fallback
                st.write(search_queries)
            else:
                search_results = process_search_queries(search_queries)
                if search_results:
                    for result in search_results:
                        st.markdown(f"**Section:** {result['section']}")
                        st.markdown(f"**Query:** {result['query']}")
                        st.markdown(f"[{result['title']}]({result['link']})")
                        st.write(result['snippet'])
                        st.divider()

        # 11. AI Integration
        with tabs[10]:
            st.subheader("AI Integration")
            ai_integration = generate_ai_integration(unit_plan, temperature)
            st.write(ai_integration)
            ste.download_button("Download AI Integration", ai_integration, "AI_Integration.txt")

    # Additional side info
    st.sidebar.divider()
    st.sidebar.header("About")
    st.sidebar.write("""This application generates inquiry-based lesson plans for educators.""")
    st.sidebar.divider()
    st.sidebar.header("Developers")
    st.sidebar.markdown(
        """
        This application was created by [your team] using [Streamlit](https://streamlit.io/). 
        It is powered by [OpenAI API](https://openai.com/api/) for educational purposes.
        """
    )
    st.sidebar.header("Version")
    st.sidebar.markdown('September 23th, 2024')


# Run the UI
if __name__ == "__main__":
    render_ui() 