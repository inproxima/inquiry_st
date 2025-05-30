#Libraries
from openai import OpenAI
import streamlit as st
import streamlit_ext as ste
import os
import anthropic
from dotenv import load_dotenv


#page setting
st.set_page_config(page_title="Inquiry Unit Planner", page_icon="🤖", initial_sidebar_state="expanded", layout="wide")

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
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_guiding_question(unit_plan, temperature):

    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        temperature=temperature,
        max_tokens=1000,
        system="""
        You are an expert in inquiry-based lesson plan design in any scenario.
        """,
        messages=[
            {"role": "user", "content": f"""Instructions:

                    Evaluate the following lesson: {unit_plan}. 
                    Identify the guiding question that will drive the inquiry-based learning in this lesson: Facts, Concepts, and Debatable Questions.
                    For example, a factual question could be: "Why doesn’t energy cycle within an ecosystem?" A conceptual question could be: "In what ways could humans impact the
                    balance of this freshwater ecosystem and its biodiversity?" A debatable question could be: "Using all of the evidence and conclusions you made above, how would you rate the health of the freshwater ecosystem at FEC?"
                    """
                    }
        ], 
        
    )

    return completion.content[0].text

def generate_essential_knowledge(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        temperature=temperature,
        max_tokens=1000,
        system="""
        You are an expert in inquiry-based lesson plan design in any scenario.
        """,
        messages=[
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the essential knowledge that students will acquire through the lesson. 
            Specifically, outline the required background knowledge, essential skills needed, and key concepts that student need to know to successfully engage in the inquiry-based learning processes.
            
"""}
        ], 
        
    )

    return completion.content[0].text

def generate_differentiation(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        temperature=temperature,
        max_tokens=1000,
        system="""
        You are an expert in inquiry-based lesson plan design in any scenario.
        """,
        messages=[
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the strategies for differentiation that are embedded in the lesson. 
            Specifically, draw from Universal Design for Learning (UDL) principles and describe and recommend how students will communicate their learning in various ways.
            Provide recommendations to ensure learning opportunities are accessible to all students, including those with diverse needs and abilities.

"""}
        ], 

    )

    return completion.content[0].text

def generate_inquiry_impact(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        temperature=temperature,
        max_tokens=1000,
        system="""
        You are an expert in inquiry-based lesson plan design in any scenario.
        """,
        messages=[
            
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the real-world impact of the lesson on students' learning and development.
            Generate recommendations on how exemplary citizenship, social responsibility, and ethical considerations enacted beyond the school context.             
            Identify key concepts and skills that are transferable to other contexts and subjects.
            Assuming that the lesson is complete, generate debriefing questions that will help students reflect on their learning and the impact of the inquiry-based lesson.

"""}
        ], 
        
    )

    return completion.content[0].text

def generate_ipad(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        temperature=temperature,
        max_tokens=1000,
        system="""
        You are an expert in inquiry-based lesson plan design in any scenario.
        """,
        messages=[
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and assuming that the context is using iPads in the classroom, generate recommendations on how to integrate technology to support inquiry-based learning.
            Use the SAMR model to describe how technology can be used to enhance the lesson and provide opportunities for students to engage in higher-order thinking and creativity.
            

"""}
        ], 

    )

    return completion.content[0].text

def generate_western_views(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        temperature=temperature,
        max_tokens=1000,
        system="""
        You are an expert in inquiry-based lesson plan design in any scenario.
        """,
        messages=[
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and highlight how the unit plan amplifies Western views and perspectives.
            Generate recommendations on how to incorporate worldviews into the lesson to provide a more inclusive and diverse learning experience.

"""}
        ], 
        
    )

    return completion.content[0].text

def generate_teacher_knowledge(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        temperature=temperature,
        max_tokens=1000,
        system="""
        You are an expert in inquiry-based lesson plan design in any scenario.
        """,
        messages=[
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the knowledge and skills that teachers need to effectively implement the lesson.
            Outline the subject-specific knowledge that teachers need to support students' inquiry-based learning.
            Ensure not to providde pedagogical strategies in this response.

"""}
        ], 
        
    )

    return completion.content[0].text



def generate_inquiry(prompt, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        temperature=temperature,
        max_tokens=1000,
        system=f"""
                You are in expert in inquiry-based lesson plan design in any scenario.
                
                Instructions:

                Authentic and Meaningful Tasks:

                Design tasks that are relevant and meaningful to students' lives, connecting to real-world problems particularly in the Canadian context. Ensure the tasks promote engagement and foster a deeper understanding of the subject matter.
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
""",
        messages=[
            {"role": "user", "content": prompt}
        ], 
        
    )

    return completion.content[0].text

def generate_assessment(lesson, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        temperature=temperature,
        max_tokens=1000,
        system=
        f"""
                You are an expert in assessment design for inquiry-based lesson plans.
                
                Instructions:

                Design an assessment plan that aligns with the inquiry-based lesson plan you have created. 
                Ensure the assessment is authentic, meaningful, and aligned with the curricular outcomes and the principles of inquiry-based learning. 
                Ensure to include the following components in your assessment plan: opportunities for assessment of learning, assessment for learning, and assessment as learning. 
                Plan for ongoing assessment and feedback that supports student learning and growth. 
                Describe how the assessment will be used to evaluate student progress and inform instruction. 
                

""",
        
        messages=[
            {"role": "user", "content": f"The following is the Unit plan: {lesson}." }
        ], 
        
    )

    return completion.content[0].text


if __name__ == '__main__':
    
    #Sidebar settings
    st.sidebar.header("Unit Planner")
    st.sidebar.write("Please provide the following information to generate an inquiry-based lesson plan.")
    st.sidebar.divider()
    grade = st.sidebar.text_input("Grade Level", "e.g., Grade 7")
    temperature = st.sidebar.slider("Temperature", min_value=0.00, max_value=1.00, value=0.85)
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
        unit_plan = generate_inquiry(prompt, temperature)
        st.subheader("Guiding Question")
        guiding_question = generate_guiding_question(unit_plan, temperature)
        st.write(guiding_question)
        ste.download_button("Download Guiding Question", guiding_question, "Guiding_Question.txt")
        st.divider()
        st.subheader("Unit Plan")
        st.write(unit_plan)
        ste.download_button("Download Unit Plan", unit_plan, "Unit_Plan.txt")
        st.divider()
        st.subheader("Student Knowledge")
        essential_knowledge = generate_essential_knowledge(unit_plan, temperature)
        st.write(essential_knowledge)
        ste.download_button("Download StudentEssential Knowledge", essential_knowledge, "Student_Essential_Knowledge.txt")
        st.divider()
        st.subheader("Teacher Knowledge")
        teacher_knowledge = generate_teacher_knowledge(unit_plan, temperature)
        st.write(teacher_knowledge)
        ste.download_button("Download Teacher Essential Knowledge", teacher_knowledge, "Teacher_Essential_Knowledge.txt")
        st.divider()
        st.subheader("Assessment Plan")
        assessment_plan = generate_assessment(unit_plan, temperature)
        st.write(assessment_plan)
        ste.download_button("Download Assessment Plan", assessment_plan, "Assessment_Plan.txt")
        st.divider()
        st.subheader("Inquiry Impact")
        inquiry_impact = generate_inquiry_impact(unit_plan, temperature)
        st.write(inquiry_impact)
        ste.download_button("Download Inquiry Impact", inquiry_impact, "Inquiry_Impact.txt")
        st.divider()
        st.subheader("Differentiation")
        differentiation = generate_differentiation(unit_plan, temperature)
        st.write(differentiation)
        ste.download_button("Download Differentiation", differentiation, "Differentiation.txt")
        st.divider()
        st.subheader("iPad Integration")
        ipad = generate_ipad(unit_plan, temperature)
        st.write(ipad)
        ste.download_button("Download iPad Integration", ipad, "iPad_Integration.txt")
        st.divider()
        st.subheader("Worldviews")
        western_views = generate_western_views(unit_plan, temperature)
        st.write(western_views)
        ste.download_button("Download Western Views", western_views, "Western_Views_Analysis.txt")
        


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
    st.sidebar.markdown('September 23th, 2024')

    

    

    
    

        






            
    


