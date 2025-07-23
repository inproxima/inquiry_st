#Libraries
from openai import OpenAI
import streamlit as st
import streamlit_ext as ste
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from serpapi import GoogleSearch

# Global model configuration
DEFAULT_MODEL = "gpt-4.1"

#page setting

# --- front-end
st.set_page_config(page_title="Inquiry Lesson Planner", page_icon="🤖", initial_sidebar_state="expanded", layout="wide")

hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
"""

# ---- backend
#OpenAI API Key
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# TAB 1: SUMMARIES
def generate_lesson_plan_summary(lesson_plan, temperature):
    """Generate a concise summary of what students will do in the lesson plan"""
    try:
        client = OpenAI()
        
        system_message = "You are an expert at analyzing lesson plans. Summarize what students will do during this lesson focusing on their activities and engagement. Limit your response to about 200 words."
        prompt = f"""Analyze the following lesson plan and create a concise summary of what students will do during this lesson.

Focus on:
- The main activities students will complete
- How students will engage with the content
- Specific student actions and tasks
- Learning modalities (individual, group work, etc.)

Limit your response to about 200 words.

Lesson Plan:
{lesson_plan}"""
        
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error while creating the summary: {str(e)}"

# TAB 2: GUIDING QUESTION
def generate_guiding_question(lesson_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": """
                    You are an expert search query development.
                """},
                {"role": "user", "content": f"""Instructions:
                        Evaluate the following lesson: {lesson_plan}. 
                        Identify the guiding question that will drive the inquiry-based learning in this lesson: Facts, Concepts, and Debatable Questions.
                        For example, a factual question could be: "Why doesn't energy cycle within an ecosystem?" A conceptual question could be: "In what ways could humans impact the
                        balance of this freshwater ecosystem and its biodiversity?" A debatable question could be: "Using all of the evidence and conclusions you made above, how would you rate the health of the freshwater ecosystem at FEC?"
                        """
                }
            ], 
            temperature=temperature
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

# TAB 3: LESSON PLAN
def generate_inquiry(prompt, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
            {"role": "system", "content": f"""
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
"""},
            {"role": "user", "content": prompt}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content    
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

# TAB 4: STUDENT ESSENTIAL KNOWLEDGE
def generate_essential_knowledge(lesson_plan, temperature, knowledge_to_be_gained=None, grade_level=None, selected_outcome=None):
    """Generate essential knowledge for the learning outcome"""
    system_prompt = """You are an educational assistant helping a teacher prepare for a lesson. 
    Based on the given learning outcome and grade level, generate essential knowledge that the teacher should know to teach this topic effectively."""
    
    # Use provided parameters or derive from lesson_plan
    if not knowledge_to_be_gained:
        knowledge_to_be_gained = "the knowledge, understanding, and skills outlined in this lesson plan"
    if not selected_outcome:
        selected_outcome = "the learning outcomes specified in this lesson plan"
    
    user_prompt = f"""Review the following knowledge, understanding, and skills that students need to know to successfully achieve the learning outcome ({selected_outcome}). 
    
    
            Based on {knowledge_to_be_gained}, generate the following:
            1.  "I know" statements: Create at least four "I know..." statements that focus on metacognition. 
            2.  "I can" statements: Create at least four "I can..." statements that focus on skills students will need to know to successfully achieve the learning outcome ({selected_outcome}).
            3.  Background Knowledge, Skills, and Concepts: Outline the required background knowledge, essential skills needed, and key concepts that students need to know to successfully achieve the learning outcome ({selected_outcome}).
    
            Organize your response clearly with headings for each of these three sections.
            
            Lesson Plan:
            {lesson_plan}
    """
    
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

# TAB 5: TEACHER ESSENTIAL KNOWLEDGE
def generate_teacher_knowledge(lesson_plan, temperature, essential_knowledge=None):
    """Generate teacher knowledge requirements"""
    try:
        client = OpenAI()
        
        system_message = "You are an expert in content knowledge for teachers. Please respond in English."
        
        # Use essential knowledge if provided, otherwise use a default message
        essential_knowledge_text = essential_knowledge if essential_knowledge else "the knowledge outlined in this lesson plan"
        
        user_message = f"""
        Review the following lesson plan: {lesson_plan}

        Also consider the following essential knowledge that students should acquire in the lesson:
        {essential_knowledge_text}

        Now identify the specific disciplinary content knowledge that teachers need to effectively implement the lesson.
        Outline the subject-specific knowledge that teachers must possess in order to support and deepen students' learning in this area.

        Focus on the following categories of disciplinary knowledge:
        • Core concepts, definitions, and interrelationships within the discipline
        • Foundational theories, evidence, or methods of inquiry in the field
        • Generalizations, patterns, exceptions, or anomalies relevant to the topic
        • Connections to other topics or domains within the discipline
        • Historical, cultural, or scientific context of the content

        IMPORTANT: For each category above, provide concrete examples that relate directly to the specific content of this lesson. For example:
        • Exact disciplinary definitions or terminology relevant to this lesson
        • Specific methods of analysis, interpretation, or reasoning associated with this content
        • Explicit links between this topic and other areas within the subject field
        • Actual historical or contextual background of the concepts covered in this lesson

        Provide a concise 'crash course' for the teacher covering the essential subject-specific knowledge they MUST understand to effectively teach this lesson and support student learning.
        Focus solely on the core concepts, facts, terminology, and information pertinent to the subject matter of this lesson.
        The goal is to quickly bring a teacher up to speed on the content itself.

        IMPORTANT: Do NOT include pedagogical strategies, teaching methods, classroom management advice, or how to teach the content. The output should be a straightforward explanation of the required content knowledge only.
        
        Do not provide a commentary as the beginning of the response.
        """
        
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

# TAB 6: ASSESSMENT PLAN
def generate_formative_assessment(lesson, temperature):
    """Generate formative assessment plan"""
    try:
        client = OpenAI()
        system_message = "You are an expert in assessment design for lesson plans."
        user_message = f"""
            The following is the lesson plan: {lesson}.
            
            First, identify the learning approach of the lesson.
            
            Next, examine the lesson plan and identify the learning outcomes and their associated action verbs (e.g., analyze, create, evaluate, synthesize, etc.). These verbs represent the assessment criteria for success for the lesson.
            
            Based on the identified learning outcomes and action verbs, determine what the teacher would need to see or hear students do or say during the lesson that tells the teacher students have achieved the learning outcomes.
            
            Identify how the students will demonstrate their newly acquired knowledge and skills. It's very important for students to demonstrate understanding of the content.
            
            Identify how the teacher will gather evidence of student learning and how the data will be triangulated.
            
            Provide formative assessments that will be used to evaluate student learning. Make sure to clearly list the specific action verbs and assessment criteria you identified from the learning outcomes.
            
            Absolutely do not provide a rubric for the assessment.
        """
        
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

def generate_rubrics_formative_assessment(formative_assessment_output, temperature):
    """Generate a rubric for formative assessment"""
    try:
        client = OpenAI()
        system_message = "You are an expert in assessment design and rubric creation for lesson plans."
        user_message = f"""
            Based on the following formative assessment plan: 
            {formative_assessment_output}

            Create a detailed rubric for the formative assessment that directly aligns with the assessment criteria and action verbs identified in the formative assessment plan above.

            First, carefully examine the formative assessment plan to identify:
            1. The specific action verbs mentioned (e.g., analyze, create, evaluate, synthesize, etc.)
            2. The assessment criteria outlined
            3. The learning outcomes and expectations described

            IMPORTANT: Format the rubric as a table using markdown table format (with | for columns). Do NOT use HTML elements like <br>, <strong>, <em>, etc. Use only markdown table formatting.

            The rubric MUST use the following performance levels and their exact descriptions:
            - EX: The student has demonstrated mastery of grade-level expectations and there are no areas for improvement.
            - PR: The student is able to demonstrate the grade-level expectations and to apply knowledge, skills, and strategies. However refinement is needed.
            - AC: The student demonstrates a basic understanding and is able to perform tasks and apply skills at a minimum level. Practice is needed for independent work.
            - NYM: The student has not met expectations and needs significant additional support to meet grade-level expectations.

            The criteria for the rubric MUST be directly derived from the action verbs and assessment criteria identified in the formative assessment plan. Each distinct verb or assessment criterion should form a separate criterion in the rubric. For each criterion, describe what student performance looks like at each of the EX, PR, AC, and NYM levels.

            Ensure complete cohesion between the formative assessment plan and this rubric by using the exact same terminology and assessment focus.
        """
        
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error while generating the rubric: {str(e)}"

def generate_summative_assessment(lesson, temperature):
    """Generate summative assessment plan"""
    try:
        client = OpenAI()
        system_message = "You are an expert in assessment design for lesson plans."
        user_message = f"""
            The following is the lesson plan: {lesson}.
            
            First, identify the approach of the lesson (e.g., play-based, performance-based, inquiry-based, etc.)
            
            Next, examine the lesson plan and identify the learning outcomes and their associated action verbs (e.g., analyze, create, evaluate, synthesize, apply, etc.). These verbs represent the assessment criteria for success for the lesson.
            
            Based on the identified learning outcomes and action verbs, determine what the teacher would need to see or hear students do or say that demonstrates students have achieved the learning outcomes.
            
            Identify how the students will demonstrate their newly acquired knowledge and skills. It's very important for students to demonstrate understanding of the content.
            
            Identify how the teacher will gather evidence of student learning and how the data will be triangulated.
            
            Provide only one comprehensive summative assessment that will be used to evaluate student learning. Make sure to clearly list the specific action verbs and assessment criteria you identified from the learning outcomes.
            
            Absolutely do not provide a rubric for the summative assessment.
        """
        
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

def generate_rubrics_summative_assessment(summative_assessment_output, temperature):
    """Generate a rubric for summative assessment"""
    try:
        client = OpenAI()
        system_message = "You are an expert in assessment design and rubric creation for lesson plans."
        user_message = f"""
            Based on the following summative assessment plan: 
            {summative_assessment_output}

            Create a detailed rubric for the summative assessment that directly aligns with the assessment criteria and action verbs identified in the summative assessment plan above.

            First, carefully examine the summative assessment plan to identify:
            1. The specific action verbs mentioned (e.g., analyze, create, evaluate, synthesize, apply, etc.)
            2. The assessment criteria outlined
            3. The learning outcomes and expectations described

            IMPORTANT: Format the rubric as a table using markdown table format (with | for columns). Do NOT use HTML elements like <br>, <strong>, <em>, etc. Use only markdown table formatting.

            The rubric MUST use the following performance levels and their exact descriptions:
            - EX: The student has demonstrated mastery of grade-level expectations and there are no areas for improvement.
            - PR: The student is able to demonstrate the grade-level expectations and to apply knowledge, skills, and strategies. However refinement is needed.
            - AC: The student demonstrates a basic understanding and is able to perform tasks and apply skills at a minimum level. Practice is needed for independent work.
            - NYM: The student has not met expectations and needs significant additional support to meet grade-level expectations.

            The criteria for the rubric MUST be directly derived from the action verbs and assessment criteria identified in the summative assessment plan. Each distinct verb or assessment criterion should form a separate criterion in the rubric. For each criterion, describe what student performance looks like at each of the EX, PR, AC, and NYM levels.

            Ensure complete cohesion between the summative assessment plan and this rubric by using the exact same terminology and assessment focus.
        """
        
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error while generating the rubric: {str(e)}"

# TAB 7: INQUIRY IMPACT
def generate_inquiry_impact(lesson_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {lesson_plan} and identify the real-world impact of the lesson on students' learning and development.
            Generate recommendations on how exemplary citizenship, social responsibility, and ethical considerations enacted beyond the school context.             
            Identify key concepts and skills that are transferable to other contexts and subjects.
            Assuming that the lesson is complete, generate debriefing questions that will help students reflect on their learning and the impact of the inquiry-based lesson.

"""}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

# TAB 8: DIFFERENTIATION
def generate_differentiation(lesson_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {lesson_plan} and identify the strategies for differentiation that are embedded in the lesson. 
            Specifically, draw from Universal Design for Learning (UDL) principles and describe and recommend how students will communicate their learning in various ways.
            Provide recommendations to ensure learning opportunities are accessible to all students, including those with diverse needs and abilities.

"""}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

# TAB 9: IPAD INTEGRATION
def generate_ipad(lesson_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {lesson_plan} and assuming that the context is using iPads in the classroom, generate recommendations on how to integrate technology to support inquiry-based learning.
            Use the SAMR model to describe how technology can be used to enhance the lesson and provide opportunities for students to engage in higher-order thinking and creativity.
            

"""}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

# TAB 10: WORLDVIEWS
def generate_western_views(lesson_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()
    
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {lesson_plan} and highlight how the lesson plan amplifies Western views and perspectives.
            Generate recommendations on how to incorporate worldviews into the lesson to provide a more inclusive and diverse learning experience.

"""}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

# TAB 11: WEB RESOURCES
class QueryExtraction(BaseModel):
    section: str
    query: str
           
class QueryStructure(BaseModel):
    Section: str
    query: list[QueryExtraction]
    
def generate_search_parameters(lesson_plan, temperature, grade):
    try:
        client = OpenAI()

        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
            {"role": "system", "content": """
                You are an expert search query development.

"""},
            {"role": "user", "content": f"""Instructions:

                Review the following inquiry-based lesson plan: {lesson_plan}. 
                I want to find resources to support the lesson plan.
                I need to create 5 google search terms for this lesson plan I could use to find resources to use in my {grade} class.
                Refain from providing any other information. """}
        ], 
        temperature=temperature,
        response_format=QueryStructure,
    )
        structured_response = completion.choices[0].message
        if structured_response.parsed:
            return structured_response.parsed
        else:
            return structured_response.refusal
    except Exception as e:
        # Return a default QueryStructure instead of an error string
        return QueryStructure(
            Section="Error",
            query=[QueryExtraction(section="General", query="educational resources")]
        )
    
def process_search_queries(search_queries: QueryStructure):
    """
    For each query in the QueryStructure, this function uses the SerpApi Google engine
    to retrieve organic search results. It then processes and returns only the top 3 entries.
    """
    all_results = []

    # Check if search_queries is a QueryStructure object
    if not isinstance(search_queries, QueryStructure):
        st.error(f"Error: Invalid search queries format - {search_queries}")
        return []

    for query_extraction in search_queries.query:
        try:
            # Construct the request parameters for the SerpApi
            params = {
                "q": query_extraction.query,      # The search query string
                "engine": "google",              # Use the Google engine
                "api_key": os.getenv("SERPAPI_API_KEY")   # <-- Replace with your SerpApi key
            }
            # Execute the search
            search = GoogleSearch(params)
            results = search.get_dict()
            print(results)
            # Get the organic results list
            organic_results = results.get("organic_results", [])

            # Process only the first 3 organic results
            processed_results = [{
                "query": query_extraction.query,
                "section": query_extraction.section,
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            } for item in organic_results[:3]]

            all_results.extend(processed_results)
        except Exception as e:
            st.error(f"Error searching for query '{query_extraction.query}': {str(e)}")

    return all_results

def generate_web_resources(lesson_plan, temperature, grade):
    search_queries = generate_search_parameters(lesson_plan, temperature, grade)
    search_results = process_search_queries(search_queries)
    #video_results = process_search_queries_video(search_queries)

    return search_results, search_queries #video_results 

# TAB 12: YOUTUBE VIDEOS
def process_search_queries_video(search_queries: QueryStructure):
    """
    For each query in the QueryStructure, this function uses the SerpApi YouTube engine
    to retrieve YouTube video results. It then processes and returns only the top 3 entries.
    """
    all_videos = []

    # Check if search_queries is a QueryStructure object
    if not isinstance(search_queries, QueryStructure):
        st.error(f"Error: Invalid search queries format for videos - {search_queries}")
        return []

    for query_extraction in search_queries.query:
        try:
            # Construct the request parameters for the SerpApi YouTube engine
            params = {
                "engine": "youtube",
                "search_query": query_extraction.query,   # <-- Must use 'search_query' instead of 'q' for YouTube
                "api_key": os.getenv("SERPAPI_API_KEY")   # <-- Replace with your SerpApi key
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            print(results)
            video_results = results["video_results"]

            # Process only the first 3 video results
            processed_videos = [{
                "section": query_extraction.section,
                "query": query_extraction.query,
                "title": video.get("title"),
                "link": video.get("link"),
                "description": video.get("description")
            } for video in video_results[:3]]

            all_videos.extend(processed_videos)
        except Exception as e:
            st.error(f"Error searching for YouTube query '{query_extraction.query}': {str(e)}")

    return all_videos

# TAB 13: AI INTEGRATION
def generate_ai_integration(lesson_plan, temperature):
    """
    Analyze a lesson plan using the UNESCO AI Competency Framework for Students (2024).
    Output includes:
    - Core Competency Reference Table
    - Identified Competency Connection
    - Reasoning
    - Connection to Student Learning Outcomes
    - Explaining the Connection to Students
    """
    try:
        client = OpenAI()
        
        system_message = (
            "You are an expert in curriculum design and AI literacy. You analyze lesson plans to identify their alignment with the UNESCO AI Competency Framework for Students (2024). "
            "Your response should begin with a table listing the four core AI competency aspects and their definitions. "
            "Next, name the single most relevant core competency that the lesson connects to, along with the most relevant sub-competency block. "
            "Then, explain the connection using the following three structured sections: Reasoning, Connection to Student Learning Outcomes, and Explaining the Connection to Students."
        )
        
        user_message = f"""
Please analyze the following lesson plan using the UNESCO AI Competency Framework for Students (2024). Structure your output as follows:

1. **Reference Table**: Present a table with two columns:
   - Column 1: Core Competency Aspect
   - Column 2: Definition

2. **Competency Connection**:
   - Core Competency Aspect: <Name>
   - Sub-Competency Block: <Block Name>

3. **Reasoning**:
Explain why this competency best aligns with the lesson. Use bullet points and a short concluding paragraph.

4. **Connection to Student Learning Outcomes**:
List 2–3 observable behaviors or goals from the lesson that align with the selected competency.

5. **Explaining the Connection to Students**:
Provide one short paragraph in student-friendly language that helps them understand why this competency matters in the lesson.

Lesson Plan:
{lesson_plan}
"""
        
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error with the AI model: {str(e)}"

if __name__ == '__main__':
    
    #Sidebar settings
    st.sidebar.header("Lesson Planner")
    st.sidebar.write("Please provide the following information to generate an inquiry-based lesson plan.")
    st.sidebar.divider()
    grade = st.sidebar.text_input("Grade Level", "e.g., Grade 7")
    temperature = st.sidebar.slider("Temperature", min_value=0.00, max_value=1.00, value=0.85)
    outcomes = st.sidebar.text_area("curriculum outcomes", "e.g, Students will be able to analyze the impact of cyberbullying on individuals and communities.")
    #prompts
    
    st.sidebar.write("Would you like to add a bit more to the context?")
    on = st.sidebar.toggle("Yes", value=False)
    if on: 
            user_context = st.sidebar.text_area("Please provide context that you would like to be included in the lesson plan.")
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
    if st.sidebar.button("Generate Lesson", type="primary"):
        lesson_plan = generate_inquiry(prompt, temperature)
        # Create 13 tabs for the output sections
        tabs = st.tabs([
            "Lesson Summary",
            "Guiding Question",
            "Lesson Plan",
            "Student Essential Knowledge",
            "Teacher Essential Knowledge",
            "Assessment Plan",
            "Inquiry Impact",
            "Differentiation",
            "iPad Integration",
            "Worldviews",
            "Web Resources",
            "YouTube Videos",
            "AI Integration"
        ])

        with tabs[0]:
            st.subheader("Lesson Summary")
            lesson_summary = generate_lesson_plan_summary(lesson_plan, temperature)
            st.write(lesson_summary)
            ste.download_button("Download Lesson Summary", lesson_summary, "Lesson_Summary.txt")

        with tabs[1]:
            st.subheader("Guiding Question")
            guiding_question = generate_guiding_question(lesson_plan, temperature)
            st.write(guiding_question)
            ste.download_button("Download Guiding Question", guiding_question, "Guiding_Question.txt")

        with tabs[2]:
            st.subheader("Lesson Plan")
            st.write(lesson_plan)
            ste.download_button("Download Lesson Plan", lesson_plan, "Lesson_Plan.txt")

        with tabs[3]:
            st.subheader("Student Essential Knowledge")
            essential_knowledge = generate_essential_knowledge(lesson_plan, temperature, 
                                                             grade_level=grade, 
                                                             selected_outcome=outcomes)
            st.write(essential_knowledge)
            ste.download_button("Download StudentEssential Knowledge", essential_knowledge, "Student_Essential_Knowledge.txt")

        with tabs[4]:
            st.subheader("Teacher Essential Knowledge")
            teacher_knowledge = generate_teacher_knowledge(lesson_plan, temperature, essential_knowledge=essential_knowledge)
            st.write(teacher_knowledge)
            ste.download_button("Download Teacher Essential Knowledge", teacher_knowledge, "Teacher_Essential_Knowledge.txt")

        with tabs[5]:
            st.subheader("Assessment Plan")
            
            # Generate formative assessment
            st.markdown("### Formative Assessment")
            formative_assessment = generate_formative_assessment(lesson_plan, temperature)
            st.write(formative_assessment)
            ste.download_button("Download Formative Assessment", formative_assessment, "Formative_Assessment.txt")
            
            # Generate formative assessment rubric
            st.markdown("### Formative Assessment Rubric")
            formative_rubric = generate_rubrics_formative_assessment(formative_assessment, temperature)
            st.write(formative_rubric)
            ste.download_button("Download Formative Rubric", formative_rubric, "Formative_Rubric.txt")
            
            # Generate summative assessment
            st.markdown("### Summative Assessment")
            summative_assessment = generate_summative_assessment(lesson_plan, temperature)
            st.write(summative_assessment)
            ste.download_button("Download Summative Assessment", summative_assessment, "Summative_Assessment.txt")
            
            # Generate summative assessment rubric
            st.markdown("### Summative Assessment Rubric")
            summative_rubric = generate_rubrics_summative_assessment(summative_assessment, temperature)
            st.write(summative_rubric)
            ste.download_button("Download Summative Rubric", summative_rubric, "Summative_Rubric.txt")

        with tabs[6]:
            st.subheader("Inquiry Impact")
            inquiry_impact = generate_inquiry_impact(lesson_plan, temperature)
            st.write(inquiry_impact)
            ste.download_button("Download Inquiry Impact", inquiry_impact, "Inquiry_Impact.txt")

        with tabs[7]:
            st.subheader("Differentiation")
            differentiation = generate_differentiation(lesson_plan, temperature)
            st.write(differentiation)
            ste.download_button("Download Differentiation", differentiation, "Differentiation.txt")

        with tabs[8]:
            st.subheader("iPad Integration")
            ipad = generate_ipad(lesson_plan, temperature)
            st.write(ipad)
            ste.download_button("Download iPad Integration", ipad, "iPad_Integration.txt")

        with tabs[9]:
            st.subheader("Worldviews")
            worldviews = generate_western_views(lesson_plan, temperature)
            st.write(worldviews)
            ste.download_button("Download Worldviews", worldviews, "Worldviews.txt")

        with tabs[10]:
            st.subheader("Web Resources")
            try:
                search_results, search_queries = generate_web_resources(lesson_plan, temperature, grade)
                
                # Debug information
                st.write(f"Generated {len(search_results) if search_results else 0} search results")
                
                if search_results:
                    st.markdown("### Web Links")
                    for result in search_results:
                        st.markdown(f"**Section:** {result['section']}")
                        st.markdown(f"**Query:** {result['query']}")
                        st.markdown(f"[{result['title']}]({result['link']})")
                        st.write(result['snippet'])
                        st.divider()
                else:
                    st.warning("No web search results found. This could be due to:")
                    st.write("- SerpAPI key not configured")
                    st.write("- API quota exceeded") 
                    st.write("- Network connectivity issues")
                    
            except Exception as e:
                st.error(f"Error generating web resources: {str(e)}")
                st.write("Please check your API configurations and try again.")

        with tabs[11]:
            st.subheader("YouTube Videos")
            try:
                search_queries = generate_search_parameters(lesson_plan, temperature, grade)
                video_results = process_search_queries_video(search_queries)
                
                # Debug information
                st.write(f"Generated {len(video_results) if video_results else 0} video results")
                
                if video_results:
                    st.markdown("### YouTube Video Links")
                    for video in video_results:
                        st.markdown(f"**Section:** {video['section']}")
                        st.markdown(f"**Query:** {video['query']}")
                        st.markdown(f"[{video['title']}]({video['link']})")
                        st.write(video['description'] or "No description available.")
                        st.divider()
                else:
                    st.warning("No YouTube video results found. This could be due to:")
                    st.write("- SerpAPI key not configured")
                    st.write("- API quota exceeded")
                    st.write("- Network connectivity issues")
                    
            except Exception as e:
                st.error(f"Error generating YouTube videos: {str(e)}")
                st.write("Please check your API configurations and try again.")

        with tabs[12]:
            st.subheader("AI Integration")
            ai_integration = generate_ai_integration(lesson_plan, temperature)
            st.write(ai_integration)
            ste.download_button("Download AI Integration", ai_integration, "AI_Integration.txt")

    #Sidebar settings
    st.sidebar.divider()
    st.sidebar.header("About")
    st.sidebar.write("""This application generates inquiry-based lesson plans for educators.""")
    st.sidebar.divider()
    st.sidebar.header("Developers")
    st.sidebar.markdown(
    """
    This application was created by [add peopel] using [Streamlit](https://streamlit.io/) . It is powered by [OpenAI API](https://openai.com/api/)'s 
    [gpt-4o-2024-08-06 API](https://platform.openai.com/docs/models/overview) for educational purposes. 
    """
    )
    st.sidebar.header("Version")
    st.sidebar.markdown('September 23th, 2024')

    

    

    
    

        






            
    


