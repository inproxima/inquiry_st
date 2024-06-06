#Libraries
from openai import OpenAI
import streamlit as st
import streamlit_ext as ste
import os
from dotenv import load_dotenv


#page setting
st.set_page_config(page_title="Inquiry Unit Planer", page_icon="🤖", initial_sidebar_state="expanded", layout="wide")

hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
"""
#st.markdown(hide_st_style, unsafe_allow_html=True)

#OpenAI APA Key
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY") 

def generate_guiding_question(unit_plan):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
                You are an expert in inquiry-based learning.
            
"""},
            {"role": "user", "content": f"""Instructions:

                    Evaluate the following lesson: {unit_plan}. 
                    Identify the guiding question that will drive the inquiry-based learning in this lesson: Facts, Concepts, and Debatable Questions.
                    For example, a factual question could be: "Why doesn’t energy cycle within an ecosystem?" A conceptual question could be: "In what ways could humans impact the
                    balance of this freshwater ecosystem and its biodiversity?" A debatable question could be: "Using all of the evidence and conclusions you made above, how would you rate the health of the freshwater ecosystem at FEC?"
                    """
                    }
        ]
    )

    return completion.choices[0].message.content

def generate_essential_knowledge(unit_plan):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the essential knowledge that students will acquire through the lesson. 
            Specificly, outline the required background knowledge, Essential skills needed, and key concpets that student need to know to successfully engage in the inquiry-based learning process.

"""}
        ]
    )

    return completion.choices[0].message.content

def generate_differentiation(unit_plan):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the strategies for differentiation that are embedded in the lesson. 
            Specifically, draw from Universal Design for Learning (UDL) principles and describe and recommend how students will communicate their learning in various ways.
            Provide recommendations to ensure learning opportunities are accessible to all students, including those with diverse needs and abilities.

"""}
        ]
    )

    return completion.choices[0].message.content

def generate_inquiry_impact(unit_plan):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the real-world impact of the lesson on students' learning and development.
            Also, identify key concepts and skills that are transferable to other contexts and subjects.

"""}
        ]
    )

    return completion.choices[0].message.content

def generate_inquiry(prompt):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
                You are in expert in inquiry-based lesson plan design in any scenario.
                
                Instructions:

                Authentic and Meaningful Tasks:

                Design tasks that are relevant and meaningful to students' lives, connecting to real-world problems particulary in the Canadian context. Ensure the tasks promote engagement and foster a deeper understanding of the subject matter.
                Student-Centered Learning:

                Create opportunities for students to take an active role in their learning. Encourage them to pose questions, investigate solutions, and construct their own understanding. Outline activities that allow for student choice and voice.
                Collaborative Learning:

                Incorporate activities that promote learning as a social process. Plan for students to collaborate with peers, teachers, and experts, sharing ideas and constructing knowledge collectively. Include group projects or discussions that require teamwork.
                Interdisciplinary Approach:

                Integrate multiple disciplines into the lesson plan, allowing students to see connections and apply knowledge in various contexts. Ensure the lesson draws on concepts from different subject areas to provide a holistic learning experience.
                Critical Thinking and Problem Solving:

                Develop activities that encourage students to think critically, question assumptions, analyze information, and solve complex problems. Include scenarios or problems that require deep thinking and innovative solutions.
                Ongoing Assessment and Feedback:

                Integrate assessment into the learning process, providing ongoing feedback to guide students' inquiry and deepen their understanding. Plan formative assessments, peer reviews, and reflective activities that help monitor progress.
                Teacher as Facilitator:

                Outline the teacher's role in guiding and supporting students' inquiries. Describe how the teacher will provide resources, ask probing questions, and scaffold learning as needed to help students reach their goals.
                Reflective Practice:

                Include opportunities for both students and teachers to engage in reflection. Plan activities where students can assess their learning process, outcomes, and their roles within it. Describe how the teacher will facilitate reflection to promote continuous improvement.
             
                Ensure not to provide an assessment component in this response.
"""},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

def generate_assessment(lesson):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
                You are an expert in assessment design for inquiry-based lesson plans.
                
                Instructions:

                Design an assessment plan that aligns with the inquiry-based lesson plan you have created. 
                Ensure the assessment is authentic, meaningful, and aligned with the curricular outcomes and the principles of inquiry-based learning. 
                Ensure to include the following components in your assessment plan: opportunities for for assessment of learning, assessment for learning, and assessment as learning. 
                Plan for ongoing assessment and feedback that supports student learning and growth. 
                Describe how the assessment will be used to evaluate student progress and inform instruction. 
                

"""},
            {"role": "user", "content": lesson}
        ]
    )

    return completion.choices[0].message.content


if __name__ == '__main__':
    
    #Sidebar settings
    st.sidebar.header("Unit Plan Generator")
    st.sidebar.write("Please provide the following information to generate an inquiry-based lesson plan.")
    st.sidebar.divider()
    grade = st.sidebar.text_input("Grade Level", "e.g., Grade 7")
    outcomes = st.sidebar.text_area("curriculum outcomes", "e.g, Students will be able to analyze the impact of cyberbullying on individuals and communities.")
    #prompts
    
                    

    
    st.sidebar.write("Would you like to add a bit more to the context?")
    on = st.sidebar.toggle("Yes", value=False)
    if on: 
            user_context = st.sidebar.text_area("Please provide context that you would like to be included in the unit plan.")
            prompt = f"""Develop an inquiry-based lesson plan for {grade} that aligns with the following curricular outcomes: {outcomes}.
                        The lesson should embed the principles of authentic and meaningful tasks, student-centered learning, collaborative learning, an interdisciplinary approach, 
                        critical thinking and problem-solving, ongoing assessment and feedback, the teacher as facilitator, and reflective practice. 
                        Ensure that the scenario includes the following consideration: {user_context}.
                        
        """
    else:
        prompt = f"""Develop an inquiry-based lesson plan for {grade} that aligns with the following curricular outcomes: {outcomes}.
                    The lesson should embed the principles of authentic and meaningful tasks, student-centered learning, collaborative learning, an interdisciplinary approach, 
                    critical thinking and problem-solving, ongoing assessment and feedback, the teacher as facilitator, and reflective practice. 
    """
    if st.sidebar.button("Generate Unit", type="primary"):
        st.subheader("Unit Plan")
        unit_plan = generate_inquiry(prompt)
        st.write(unit_plan)
        ste.download_button("Download Unit Plan", unit_plan, "Unit_Plan.txt")
        st.divider()
        st.subheader("Assessment Plan")
        assessment_plan = generate_assessment(unit_plan)
        st.write(assessment_plan)
        ste.download_button("Download Assessment Plan", assessment_plan, "Assessment_Plan.txt")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Guiding Question")
            guiding_question = generate_guiding_question(unit_plan)
            st.write(guiding_question)
            ste.download_button("Download Guiding Question", guiding_question, "Guiding_Question.txt")
        with col2:
            st.subheader("Inquiry Impact")
            inquiry_impact = generate_inquiry_impact(unit_plan)
            st.write(inquiry_impact)
            ste.download_button("Download Inquiry Impact", inquiry_impact, "Inquiry_Impact.txt")
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Essential Knowledge")
            essential_knowledge = generate_essential_knowledge(unit_plan)
            st.write(essential_knowledge)
            ste.download_button("Download Essential Knowledge", essential_knowledge, "Essential_Knowledge.txt")
        with col4:
            st.subheader("Differentiation")
            differentiation = generate_differentiation(unit_plan)
            st.write(differentiation)
            ste.download_button("Download Differentiation", differentiation, "Differentiation.txt")


    #Sidebar settings
    st.sidebar.divider()
    st.sidebar.header("About")
    st.sidebar.write("""This application generates inquiry-based lesson plans for educators.""")
    st.sidebar.divider()
    st.sidebar.header("Developers")
    st.sidebar.markdown(
    """
    This application was created by [add peopel] using [Streamlit](https://streamlit.io/) . It is powered by [OpenAI API](https://openai.com/api/)'s 
    [GPT-4o API](https://platform.openai.com/docs/models/overview) for educational purposes. 
    """
    )
    st.sidebar.header("Version")
    st.sidebar.markdown('June 5th, 2024 - Version 1.0')

    

    

    
    

        






            
    


