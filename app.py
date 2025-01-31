#Libraries
from openai import OpenAI
import streamlit as st
import streamlit_ext as ste
import os
from dotenv import load_dotenv
import anthropic
from pydantic import BaseModel
from search import SearchEngine
from serpapi import GoogleSearch

#page setting
st.set_page_config(page_title="Inquiry Unit Planner", page_icon="🤖", initial_sidebar_state="expanded", layout="wide")

hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
"""

#OpenAI APA Key
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_guiding_question_claude(unit_plan, temperature):

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        temperature=temperature,
        max_tokens=1000,
        system="""
        You are an expert in inquiry-based lesson plan design in any scenario.
        """,
        messages=[
            {"role": "user", "content": f"""Instructions:

                    Evaluate the following lesson: {unit_plan}. 
                    Identify the guiding question that will drive the inquiry-based learning in this lesson: Facts, Concepts, and Debatable Questions.
                    For example, a factual question could be: "Why doesn't energy cycle within an ecosystem?" A conceptual question could be: "In what ways could humans impact the
                    balance of this freshwater ecosystem and its biodiversity?" A debatable question could be: "Using all of the evidence and conclusions you made above, how would you rate the health of the freshwater ecosystem at FEC?"
                    """
                    }
        ], 
        
    )

    return completion.content[0].text

def generate_essential_knowledge_claude(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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

def generate_differentiation_claude(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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

def generate_inquiry_impact_claude(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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

def generate_ipad_claude(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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

def generate_western_views_claude(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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

def generate_teacher_knowledge_claude(unit_plan, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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



def generate_inquiry_claude(prompt, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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

def generate_assessment_claude(lesson, temperature):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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

def generate_search_parameters_claude(unit_plan, temperature, grade):
    

    completion = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        temperature=temperature,
        max_tokens=1000,
        system=f"""You are an expert in search query development.
                 
""",
        messages=[
            {"role": "user", "content": f"""
                Review the following inquiry-based lesson plan: {unit_plan} and for each session generate a search quary to be used in google to find resources. 
                I need to create 10 google search terms for this lesson plan I could use to find resources to use in my {grade} class.
                Structure your response as a list of dictionaries with the following keys: "Session", "Search Query". Like this:
                [
                    <"Session": 1, "Search Query": "search term 1", "Search Query": "search term 2">,
                    <"Session": 2, "Search Query": "search term 3", "Search Query": "search term 4">,
                    ...
                ]
"""}
        ], 
        
    )

    return completion.content[0].text

def generate_ai_integration_claude(unit_plan, temperature):
    """
    Fallback approach to generate AI integration suggestions via Claude for the unit plan,
    using the same 5-level AI usage framework.
    """
    try:
        # Replace this with your code for calling Claude or any other Anthropic client
        import anthropic

        # Initialize Claude client (this is just an illustrative example)
        client = anthropic.Client(api_key="YOUR_ANTHROPIC_API_KEY")

        system_prompt = """You are an educational AI integration specialist.
You are provided with a framework consisting of five levels of AI usage:
• Level 1: No AI
• Level 2: AI-Assisted Planning
• Level 3: AI-Assisted Task Completion
• Level 4: Full AI Collaboration
• Level 5: AI Exploration

When responding, you should:
1. Review the inquiry-based unit plan.
2. Suggest a recommended level of AI usage (if any).
3. Explain why that level is appropriate for the content, learning objectives, and student context.
4. Offer a brief outline or recommendation of how generative AI could be integrated at this level.
5. Return only the text response.
"""

        user_prompt = f"""Please review the following unit plan:
{unit_plan}

Using the 5-level AI usage framework, provide a recommended level (or levels) of AI integration and 
explain how it can positively impact student learning in this scenario. 
If no AI integration is beneficial, recommend Level 1. Keep your answer concise yet clear.
"""

        # Use Claude's API to send the messages
        response = client.completion(
            prompt=anthropic.AI_PROMPT + system_prompt +
                   anthropic.HUMAN_PROMPT + user_prompt +
                   anthropic.AI_PROMPT,
            model="claude-v1",
            temperature=temperature,
            max_tokens_to_sample=500
        )

        # The response text is found in "completion"
        text_response = response['completion']
        return text_response.strip()

    except Exception:
        try:
            return generate_ai_integration_claude(unit_plan, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."

def generate_guiding_question(unit_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """
                    You are an expert search query development.
                """},
                {"role": "user", "content": f"""Instructions:
                        Evaluate the following lesson: {unit_plan}. 
                        Identify the guiding question that will drive the inquiry-based learning in this lesson: Facts, Concepts, and Debatable Questions.
                        For example, a factual question could be: "Why doesn't energy cycle within an ecosystem?" A conceptual question could be: "In what ways could humans impact the
                        balance of this freshwater ecosystem and its biodiversity?" A debatable question could be: "Using all of the evidence and conclusions you made above, how would you rate the health of the freshwater ecosystem at FEC?"
                        """
                }
            ], 
            temperature=temperature
        )
        return completion.choices[0].message.content
        
    except Exception:
        try:
            return generate_guiding_question_claude(unit_plan, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."


def generate_essential_knowledge(unit_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the essential knowledge that students will acquire through the lesson. 
            Specifically, outline the required background knowledge, essential skills needed, and key concepts that student need to know to successfully engage in the inquiry-based learning processes.
            
"""}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception:
        try:
            return generate_essential_knowledge_claude(unit_plan, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."

def generate_differentiation(unit_plan, temperature):
    """Primary function using GPT-4"""
    try:
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
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception:
        try:
            return generate_differentiation_claude(unit_plan, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."

def generate_inquiry_impact(unit_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the real-world impact of the lesson on students' learning and development.
            Generate recommendations on how exemplary citizenship, social responsibility, and ethical considerations enacted beyond the school context.             
            Identify key concepts and skills that are transferable to other contexts and subjects.
            Assuming that the lesson is complete, generate debriefing questions that will help students reflect on their learning and the impact of the inquiry-based lesson.

"""}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception:
        try:
            return generate_inquiry_impact_claude(unit_plan, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."

def generate_ipad(unit_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and assuming that the context is using iPads in the classroom, generate recommendations on how to integrate technology to support inquiry-based learning.
            Use the SAMR model to describe how technology can be used to enhance the lesson and provide opportunities for students to engage in higher-order thinking and creativity.
            

"""}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception:
        try:
            return generate_ipad_claude(unit_plan, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."

def generate_western_views(unit_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()
    
        completion = client.chat.completions.create(
            model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and highlight how the unit plan amplifies Western views and perspectives.
            Generate recommendations on how to incorporate worldviews into the lesson to provide a more inclusive and diverse learning experience.

"""}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception:
        try:
            return generate_western_views_claude(unit_plan, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."

def generate_teacher_knowledge(unit_plan, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.
                
"""},
            {"role": "user", "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan} and identify the knowledge and skills that teachers need to effectively implement the lesson.
            Outline the subject-specific knowledge that teachers need to support students' inquiry-based learning.
            Ensure not to providde pedagogical strategies in this response.

"""}
        ], 
        temperature=temperature
    )

        return completion.choices[0].message.content
    except Exception:   
        try:
            return generate_teacher_knowledge_claude(unit_plan, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."



def generate_inquiry(prompt, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o",
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
    except Exception:
        try:
            return generate_inquiry_claude(prompt, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."



def generate_assessment(lesson, temperature):
    """Primary function using GPT-4"""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
            {"role": "system", "content": """
                You are an expert in assessment design for inquiry-based lesson plans.
                
                Instructions:

                Design an assessment plan that aligns with the inquiry-based lesson plan you have created. 
                Ensure the assessment is authentic, meaningful, and aligned with the curricular outcomes and the principles of inquiry-based learning. 
                Ensure to include the following components in your assessment plan: opportunities for assessment of learning, assessment for learning, and assessment as learning. 
                Plan for ongoing assessment and feedback that supports student learning and growth. 
                Describe how the assessment will be used to evaluate student progress and inform instruction. 
                

"""},
            {"role": "user", "content": f"The following is the Unit plan: {lesson}." }
        ], 
        temperature=temperature,
    )

        return completion.choices[0].message.content
    except Exception:
        try:
            return generate_assessment_claude(lesson, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."

class QueryExtraction(BaseModel):
    section: str
    query: str
           

class QueryStructure(BaseModel):
    Section: str
    query: list[QueryExtraction]
    

def generate_search_parameters(unit_plan, temperature, grade):
    try:
        client = OpenAI()

        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
            {"role": "system", "content": """
                You are an expert search query development.

"""},
            {"role": "user", "content": f"""Instructions:

                Review the following inquiry-based lesson plan: {unit_plan}. 
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
    except Exception:
        try:
            return generate_search_parameters_claude(unit_plan, temperature, grade)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."
    
def process_search_queries(search_queries: QueryStructure):
    search_engine = SearchEngine()
    all_results = []
    
    # Access the queries from the QueryStructure object
    for query_extraction in search_queries.query:
        try:
            results = search_engine.search(query_extraction.query)
            organic_results = results.get('organic_results', [])
            processed_results = [{
                'query': query_extraction.query,
                'section': query_extraction.section,
                'title': result.get('title'),
                'link': result.get('link'),
                'snippet': result.get('snippet')
            } for result in organic_results[:3]]  # Limiting to top 3 results
            all_results.extend(processed_results)
        except Exception as e:
            st.error(f"Error searching for query '{query_extraction.query}': {str(e)}")
    
    return all_results

def process_search_queries_video(search_queries: QueryStructure):
    """
    Takes a QueryStructure object containing queries and returns relevant YouTube video links
    by using the SerpApi YouTube engine.
    """
    search_engine = SearchEngine()
    all_videos = []
    
    for query_extraction in search_queries.query:
        try:
            # Pass the YouTube engine parameter alongside the query
            # The internal 'search' method or function you implement in 'search.py' 
            # needs to handle 'engine="youtube"' to route requests to the SerpApi YouTube engine.
            results = search_engine.search(query_extraction.query, engine="youtube")
            video_results = results.get('video_results', [])
            
            # Process only the first few results for brevity
            processed_videos = [{
                'section': query_extraction.section,
                'query': query_extraction.query,
                'title': video.get('title'),
                'link': video.get('link'),
                'description': video.get('descriptionSnippet'),
            } for video in video_results[:3]]
            
            all_videos.extend(processed_videos)
        except Exception as e:
            st.error(f"Error searching for YouTube query '{query_extraction.query}': {str(e)}")
    
    return all_videos

def generate_ai_integration(unit_plan, temperature):
    """
    Analyzes the unit_plan and provides recommended strategies for integrating
    generative AI into the lesson, referencing the 5-level AI integration framework.
    """

    try:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="o3-mini",
            messages=[
                {
                    "role": "developer",
                    "content": """You are an educational AI integration specialist. 
                    You are provided with a framework consisting of five levels of AI usage:
                    •Level 1: No AI

                    Description: Tasks completed entirely without AI tools.

                    Use Case: Ideal for foundational skills, such as handwriting, basic math, or in-person debates.

                    Example: A handwritten essay in a supervised setting to assess grammar and sentence structure.

                    Level 2: AI-Assisted Planning

                    Description: Students use AI for brainstorming or outlining but develop the final product independently.

                    Use Case: Encourages creative thinking while ensuring students engage deeply with the content.

                    Example: Students use AI to generate research questions but write the report without AI.

                    Level 3: AI-Assisted Task Completion

                    Description: AI tools help with drafting or improving specific aspects of work while maintaining the student's voice.

                    Use Case: Develops critical evaluation skills as students assess AI-generated content.

                    Example: Using AI to refine the clarity of lab reports while ensuring the conclusions are student-written.

                    Level 4: Full AI Collaboration

                    Description: Students leverage AI tools to solve problems and demonstrate their understanding.

                    Use Case: Focuses on strategic AI use and critical thinking.

                    Example: Students create AI-generated presentations, demonstrating effective tool use and content mastery.

                    Level 5: AI Exploration

                    Description: Encourages co-creation and innovation, pushing the boundaries of traditional assessments.

                    Use Case: Best for advanced students exploring cutting-edge AI applications.

                    Example: Students use AI to design a unique tool or system for solving real-world problems.
                    When responding, you should:
                    
                    1. Review the inquiry-based unit plan.
                    2. Suggest a recommended level of AI usage for each section of the unit plan.
                    3. Explain why that level is appropriate for the content, learning objectives, and student context.
                    4. Offer a brief outline or recommendation of how generative AI could be integrated at this level.
                    """
                },
                {
                    "role": "user",
                    "content": f"""Please review the following unit plan:
                    {unit_plan}

                    Using the 5-level AI usage framework, provide recommendations for integrating AI into the unit plan. Include all 5 levels. For each level provide activity suggestion aligning with one in the lesson plan and reasoning for why that level is appropriate for that actvity, learning objectives, and student context.
"""
                }
            ],
            reasoning_effort="low"
        )

        text_response = completion.choices[0].message.content    
        return text_response
    except Exception:
        # Fallback to Claude or another AI model if GPT-based call fails
        try:
            return generate_ai_integration_claude(unit_plan, temperature)
        except Exception:
            return "I apologize, but I encountered errors with both AI models. Please try again later."

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
        # Create 11 tabs for the output sections
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
            "Web Resources",
            "AI Integration"
        ])

        with tabs[0]:
            st.subheader("Guiding Question")
            guiding_question = generate_guiding_question(unit_plan, temperature)
            st.write(guiding_question)
            ste.download_button("Download Guiding Question", guiding_question, "Guiding_Question.txt")

        with tabs[1]:
            st.subheader("Unit Plan")
            st.write(unit_plan)
            ste.download_button("Download Unit Plan", unit_plan, "Unit_Plan.txt")

        with tabs[2]:
            st.subheader("Student Essential Knowledge")
            essential_knowledge = generate_essential_knowledge(unit_plan, temperature)
            st.write(essential_knowledge)
            ste.download_button("Download StudentEssential Knowledge", essential_knowledge, "Student_Essential_Knowledge.txt")

        with tabs[3]:
            st.subheader("Teacher Essential Knowledge")
            teacher_knowledge = generate_teacher_knowledge(unit_plan, temperature)
            st.write(teacher_knowledge)
            ste.download_button("Download Teacher Essential Knowledge", teacher_knowledge, "Teacher_Essential_Knowledge.txt")

        with tabs[4]:
            st.subheader("Assessment Plan")
            assessment_plan = generate_assessment(unit_plan, temperature)
            st.write(assessment_plan)
            ste.download_button("Download Assessment Plan", assessment_plan, "Assessment_Plan.txt")

        with tabs[5]:
            st.subheader("Inquiry Impact")
            inquiry_impact = generate_inquiry_impact(unit_plan, temperature)
            st.write(inquiry_impact)
            ste.download_button("Download Inquiry Impact", inquiry_impact, "Inquiry_Impact.txt")

        with tabs[6]:
            st.subheader("Differentiation")
            differentiation = generate_differentiation(unit_plan, temperature)
            st.write(differentiation)
            ste.download_button("Download Differentiation", differentiation, "Differentiation.txt")

        with tabs[7]:
            st.subheader("iPad Integration")
            ipad = generate_ipad(unit_plan, temperature)
            st.write(ipad)
            ste.download_button("Download iPad Integration", ipad, "iPad_Integration.txt")

        with tabs[8]:
            st.subheader("Worldviews")
            worldviews = generate_western_views(unit_plan, temperature)
            st.write(worldviews)
            ste.download_button("Download Worldviews", worldviews, "Worldviews.txt")

        with tabs[9]:
            st.subheader("Web Resources")
            search_queries = generate_search_parameters(unit_plan, temperature, grade)
            search_results = process_search_queries(search_queries)
            if search_results:
                st.markdown("### Web Links")
                for result in search_results:
                    st.markdown(f"**Section:** {result['section']}")
                    st.markdown(f"**Query:** {result['query']}")
                    st.markdown(f"[{result['title']}]({result['link']})")
                    st.write(result['snippet'])
                    st.divider()

            st.markdown("### YouTube Video Links")
            video_results = process_search_queries_video(search_queries)
            if video_results:
                for video in video_results:
                    st.markdown(f"**Section:** {video['section']}")
                    st.markdown(f"**Query:** {video['query']}")
                    st.markdown(f"[{video['title']}]({video['link']})")
                    st.write(video['description'] or "No description available.")
                    st.divider()

        with tabs[10]:
            st.subheader("AI Integration")
            ai_integration = generate_ai_integration(unit_plan, temperature)
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

    

    

    
    

        






            
    


