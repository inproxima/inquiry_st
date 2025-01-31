import uuid
from typing import Optional, List
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
import anthropic  # For fallback calls
import os

from daos.unit_plan_dao import UnitPlanDAO
from entities.unit_plan import UnitPlan
from constants import APP_OPENAI_MODEL, APP_OPENAI_MODEL_2, APP_OPENAI_MODEL_3

load_dotenv(override=True)

def get_openai_client():
    """
    Singleton-like pattern to reuse the same OpenAI client.
    """
    if not hasattr(get_openai_client, "client"):
        get_openai_client.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return get_openai_client.client

def get_anthropic_client():
    """
    Returns an Anthropic client for fallback usage.
    """
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

openai_model = APP_OPENAI_MODEL
openai_model_2 = APP_OPENAI_MODEL_2
openai_model_3 = APP_OPENAI_MODEL_3

# Fallback methods calling Anthropic (Claude) -- replicate the structure from app.py for each method
async def _generate_inquiry_claude(prompt: str, temperature: float) -> str:
    """
    Fallback approach to generate the inquiry-based plan via Claude.
    """
    try:
        client = get_anthropic_client()
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system="""
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
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."

async def _generate_assessment_claude(lesson: str, temperature: float) -> str:
    """
    Fallback approach to generate the assessment plan via Claude.
    """
    try:
        client = get_anthropic_client()
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system="""
            You are an expert in assessment design for inquiry-based lesson plans.

            Instructions:

            Design an assessment plan that aligns with the inquiry-based lesson plan you have created.
            Ensure the assessment is authentic, meaningful, and aligned with the curricular outcomes 
            and the principles of inquiry-based learning.

            Include:
              • Opportunities for assessment of learning, assessment for learning, and assessment as learning.
              • Ongoing assessment and feedback that supports student learning and growth.
              • Description of how the assessment will be used to evaluate student progress and inform instruction.
            """,
            messages=[
                {"role": "user", "content": f"The following is the Unit plan: {lesson}."}
            ],
        )
        return completion.content[0].text
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."

async def _generate_guiding_question_claude(unit_plan: str, temperature: float) -> str:
    """
    Fallback approach to generate the guiding question(s) via Claude.
    """
    try:
        client = get_anthropic_client()
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system="""
            You are an expert in inquiry-based lesson plan design in any scenario.
            """,
            messages=[
                {
                    "role": "user",
                    "content": f"""Instructions:

                        Evaluate the following lesson: {unit_plan}. 
                        Identify the guiding question that will drive the inquiry-based learning in this lesson: Facts, Concepts, and Debatable Questions.
                        For example, a factual question could be: "Why doesn't energy cycle within an ecosystem?" 
                        A conceptual question could be: "In what ways could humans impact the balance of this freshwater ecosystem and its biodiversity?" 
                        A debatable question could be: "Using all of the evidence and conclusions you made above, how would you rate the health of the freshwater ecosystem at FEC?"
                    """
                },
            ],
        )
        return completion.content[0].text
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."

async def _generate_essential_knowledge_claude(unit_plan: str, temperature: float) -> str:
    """
    Fallback approach to generate essential knowledge via Claude.
    """
    try:
        client = get_anthropic_client()
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system="""
            You are an expert in inquiry-based lesson plan design in any scenario.
            """,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Review the following inquiry-based lesson plan: {unit_plan} 
                    and identify the essential knowledge that students will acquire through the lesson. 
                    Specifically, outline the required background knowledge, essential skills needed, 
                    and key concepts that students need to know to successfully engage in the inquiry-based 
                    learning processes.
                    """
                },
            ],
        )
        return completion.content[0].text
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."

async def _generate_differentiation_claude(unit_plan: str, temperature: float) -> str:
    """
    Fallback approach to identify strategies for differentiation embedded in the lesson plan.
    """
    try:
        client = get_anthropic_client()
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system="""
            You are an expert in inquiry-based lesson plan design in any scenario.
            """,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Review the following inquiry-based lesson plan: {unit_plan} 
                    and identify the strategies for differentiation that are embedded in the lesson. 
                    Specifically, draw from Universal Design for Learning (UDL) principles 
                    and describe and recommend how students will communicate their learning in various ways.
                    Provide recommendations to ensure learning opportunities are accessible to all students,
                    including those with diverse needs and abilities.
                    """
                },
            ],
        )
        return completion.content[0].text
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."

async def _generate_inquiry_impact_claude(unit_plan: str, temperature: float) -> str:
    """
    Fallback approach to identify real-world impacts of the inquiry-based lesson plan.
    """
    try:
        client = get_anthropic_client()
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system="""
            You are an expert in inquiry-based lesson plan design in any scenario.
            """,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Review the following inquiry-based lesson plan: {unit_plan} 
                    and identify the real-world impact of the lesson on students' learning and development.
                    Generate recommendations on how exemplary citizenship, social responsibility, 
                    and ethical considerations are enacted beyond the school context.             
                    Identify key concepts and skills that are transferable to other contexts and subjects.
                    Assuming that the lesson is complete, generate debriefing questions that will help students 
                    reflect on their learning and the impact of the inquiry-based lesson.
                    """
                },
            ],
        )
        return completion.content[0].text
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."

async def _generate_ipad_claude(unit_plan: str, temperature: float) -> str:
    """
    Fallback approach to integrate technology for inquiry-based learning, referencing the SAMR model.
    """
    try:
        client = get_anthropic_client()
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system="""
            You are an expert in inquiry-based lesson plan design in any scenario.
            """,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Review the following inquiry-based lesson plan: {unit_plan} 
                    and assuming that the context is using iPads in the classroom, 
                    generate recommendations on how to integrate technology to support inquiry-based learning.
                    Use the SAMR model to describe how technology can enhance the lesson 
                    and provide opportunities for students to engage in higher-order thinking and creativity.
                    """
                },
            ],
        )
        return completion.content[0].text
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."

async def _generate_western_views_claude(unit_plan: str, temperature: float) -> str:
    """
    Fallback approach to highlight how the unit plan amplifies Western views
    and suggests ways to incorporate more inclusive worldviews.
    """
    try:
        client = get_anthropic_client()
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system="""
            You are an expert in inquiry-based lesson plan design in any scenario.
            """,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Review the following inquiry-based lesson plan: {unit_plan} 
                    and highlight how the unit plan amplifies Western views and perspectives.
                    Generate recommendations on how to incorporate additional worldviews 
                    into the lesson to provide a more inclusive and diverse learning experience.
                    """
                },
            ],
        )
        return completion.content[0].text
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."

async def _generate_teacher_knowledge_claude(unit_plan: str, temperature: float) -> str:
    """
    Fallback approach to identify teacher-specific knowledge and skills required 
    to effectively implement the inquiry-based lesson plan.
    """
    try:
        client = get_anthropic_client()
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system="""
            You are an expert in inquiry-based lesson plan design in any scenario.
            """,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Review the following inquiry-based lesson plan: {unit_plan} 
                    and identify the knowledge and skills that teachers need to effectively implement the lesson.
                    Outline the subject-specific knowledge that teachers need to support students' inquiry-based learning.
                    Ensure not to provide pedagogical strategies in this response.
                    """
                },
            ],
        )
        return completion.content[0].text
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."

async def _generate_ai_integration_claude(unit_plan: str, temperature: float) -> str:
    """
    Fallback approach to integrate AI tools into the lesson plan,
    referencing a 5-level AI usage framework (Claude).
    """
    try:
        client = get_anthropic_client()
        system_prompt = """You are an educational AI integration specialist.
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
"""
        user_prompt = f"""
        Please review the following unit plan:
        {unit_plan}

        Using the 5-level AI usage framework, provide a recommended level (or levels) of AI integration 
        for each section of the unit plan and explain how it can positively impact student learning 
        in this scenario.
        """
        completion = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
        return completion.content[0].text
    except Exception:
        return "I apologize, but I encountered errors with the fallback model as well. Please try again later."


# Primary public methods with fallback logic.
async def generate_inquiry(unit_plan: UnitPlan) -> str:
    """
    Asynchronously generates an inquiry-based lesson plan.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    prompt_with_context = None
    if unit_plan.user_context and len(unit_plan.user_context) > 0:
        prompt_with_context = f"""Develop an inquiry-based lesson plan for {unit_plan.grade} 
        that aligns with the following curricular outcomes: {unit_plan.outcomes}.
        The lesson should embed the principles of authentic and meaningful tasks, 
        student-centered learning, collaborative learning, an interdisciplinary approach,
        critical thinking and problem-solving, ongoing assessment and feedback, 
        the teacher as facilitator, and reflective practice.
        Ensure that the scenario includes the following consideration: {unit_plan.user_context}.
        """
    else:
        prompt_with_context = f"""Develop an inquiry-based lesson plan for {unit_plan.grade} 
        that aligns with the following curricular outcomes: {unit_plan.outcomes}.
        The lesson should embed the principles of authentic and meaningful tasks, 
        student-centered learning, collaborative learning, an interdisciplinary approach,
        critical thinking and problem-solving, ongoing assessment and feedback, 
        the teacher as facilitator, and reflective practice.
        """

    client = get_openai_client()
    try:
        print("inquiry started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are in expert in inquiry-based lesson plan design in any scenario.

                    Instructions:

                    Authentic and Meaningful Tasks:
                      • Design tasks that are relevant and meaningful to students' lives, 
                        connecting to real-world problems particularly in the Canadian context. 
                      • Ensure the tasks promote engagement and foster a deeper understanding of the subject matter.

                    Student-Centered Learning:
                      • Create opportunities for students to take an active role in their learning. 
                      • Encourage them to pose questions, investigate solutions, and construct their own understanding. 
                      • Outline activities that allow for student choice and voice.

                    Collaborative Learning:
                      • Incorporate activities that promote learning as a social process. 
                      • Plan for students to collaborate with peers, teachers, and experts, sharing ideas and constructing knowledge collectively.
                      • Include group projects or discussions that require teamwork.

                    Interdisciplinary Approach:
                      • Integrate multiple disciplines into the lesson plan, allowing students to see connections and apply knowledge in various contexts.
                      • Ensure the lesson draws on concepts from different subject areas to provide a holistic learning experience.

                    Critical Thinking and Problem Solving:
                      • Develop activities that encourage students to think critically, question assumptions, analyze information, and solve complex problems.
                      • Include scenarios or problems that require deep thinking and innovative solutions.

                    Ongoing Assessment and Feedback:
                      • Integrate assessment into the learning process, providing ongoing feedback to guide students' inquiry and deepen their understanding.
                      • Plan formative assessments, peer reviews, and reflective activities that help monitor progress.

                    Teacher as Facilitator:
                      • Outline the teacher's role in guiding and supporting students' inquiries.
                      • Describe how the teacher will provide resources, ask probing questions, and scaffold learning as needed to help students reach their goals.

                    Reflective Practice:
                      • Include opportunities for both students and teachers to engage in reflection.
                      • Plan activities where students can assess their learning process, outcomes, and their roles within it.
                      • Describe how the teacher will facilitate reflection to promote continuous improvement.

                    Ensure not to provide an assessment component in this response.
                    """
                },
                {"role": "user", "content": prompt_with_context}
            ],
            temperature=float(unit_plan.temperature),
        )

        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_inquiry_claude(
            prompt_with_context, float(unit_plan.temperature)
        )

    unit_plan.unit_plan = content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"unit_plan": content}
    )
    print("inquiry finished")
    return content

async def generate_assessment(unit_plan: UnitPlan):
    """
    Generates an assessment plan for the previously created unit plan.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    client = get_openai_client()
    assessment_prompt = f"The following is the Unit plan: {unit_plan.unit_plan}."

    try:
        print("assessment_plan started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert in assessment design for inquiry-based lesson plans.

                    Instructions:

                    Design an assessment plan that aligns with the inquiry-based lesson plan you have created.
                    Ensure the assessment is authentic, meaningful, and aligned with the curricular outcomes 
                    and the principles of inquiry-based learning.
                    
                    Include:
                      • Opportunities for assessment of learning, assessment for learning, and assessment as learning.
                      • Ongoing assessment and feedback that supports student learning and growth.
                      • Description of how the assessment will be used to evaluate student progress and inform instruction.
                    """
                },
                {"role": "user", "content": assessment_prompt}
            ],
            temperature=float(unit_plan.temperature),
        )
        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_assessment_claude(
            unit_plan.unit_plan, float(unit_plan.temperature)
        )

    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"assessment_plan": content},
    )
    print("assessment_plan finished")

async def generate_guiding_question(unit_plan: UnitPlan):
    """
    Generates the guiding question(s) for the inquiry-based lesson plan.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    client = get_openai_client()
    prompt = f"""Instructions:

                    Evaluate the following lesson: {unit_plan.unit_plan}. 
                    Identify the guiding question that will drive the inquiry-based learning in this lesson: 
                    Facts, Concepts, and Debatable Questions.
                    
                    For example, a factual question: "Why doesn't energy cycle within an ecosystem?" 
                    A conceptual question: "In what ways could humans impact the balance of this freshwater ecosystem and its biodiversity?" 
                    A debatable question: "Using all of the evidence and conclusions you made above, how would you rate the health of the freshwater ecosystem at FEC?"
                """

    try:
        print("guiding_question started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert in inquiry-based learning.
                    """
                },
                {"role": "user", "content": prompt},
            ],
            temperature=float(unit_plan.temperature),
        )
        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_guiding_question_claude(
            unit_plan.unit_plan, float(unit_plan.temperature)
        )

    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"guiding_question": content},
    )
    print("guiding_question finished")

async def generate_essential_knowledge(unit_plan: UnitPlan):
    """
    Identifies essential knowledge and skills needed for successful engagement in the lesson plan.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    client = get_openai_client()
    prompt = f"""
    Review the following inquiry-based lesson plan: {unit_plan.unit_plan} 
    and identify the essential knowledge that students will acquire through the lesson. 
    Specifically, outline the required background knowledge, essential skills needed, 
    and key concepts that students need to know to successfully engage in the inquiry-based 
    learning processes.
    """

    try:
        print("essential_knowledge started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert in inquiry-based lesson plan design in any scenario.
                    """
                },
                {"role": "user", "content": prompt},
            ],
            temperature=float(unit_plan.temperature),
        )
        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_essential_knowledge_claude(
            unit_plan.unit_plan, float(unit_plan.temperature)
        )

    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"essential_knowledge": content},
    )
    print("essential_knowledge finished")

async def generate_differentiation(unit_plan: UnitPlan):
    """
    Identifies strategies for differentiation embedded in the lesson plan, 
    with emphasis on UDL principles.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    client = get_openai_client()
    prompt = f"""
    Review the following inquiry-based lesson plan: {unit_plan.unit_plan} 
    and identify the strategies for differentiation that are embedded in the lesson. 
    Specifically, draw from Universal Design for Learning (UDL) principles 
    and describe and recommend how students will communicate their learning in various ways.
    Provide recommendations to ensure learning opportunities are accessible to all students,
    including those with diverse needs and abilities.
    """

    try:
        print("differentiation started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert in inquiry-based lesson plan design in any scenario.
                    """
                },
                {"role": "user", "content": prompt},
            ],
            temperature=float(unit_plan.temperature),
        )
        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_differentiation_claude(
            unit_plan.unit_plan, float(unit_plan.temperature)
        )

    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"differentiation": content},
    )
    print("differentiation finished")

async def generate_inquiry_impact(unit_plan: UnitPlan):
    """
    Identifies real-world impacts of the inquiry-based lesson plan, 
    and generates recommendations for extending learning beyond the classroom.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    client = get_openai_client()
    prompt = f"""
    Review the following inquiry-based lesson plan: {unit_plan.unit_plan} 
    and identify the real-world impact of the lesson on students' learning and development.
    Generate recommendations on how exemplary citizenship, social responsibility, 
    and ethical considerations are enacted beyond the school context.             
    Identify key concepts and skills that are transferable to other contexts and subjects.
    Assuming that the lesson is complete, generate debriefing questions that will help students 
    reflect on their learning and the impact of the inquiry-based lesson.
    """

    try:
        print("inquiry_impact started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert in inquiry-based lesson plan design in any scenario.
                    """
                },
                {"role": "user", "content": prompt},
            ],
            temperature=float(unit_plan.temperature),
        )
        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_inquiry_impact_claude(
            unit_plan.unit_plan, float(unit_plan.temperature)
        )

    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"inquiry_impact": content},
    )
    print("inquiry_impact finished")

async def generate_ipad(unit_plan: UnitPlan):
    """
    Offers recommendations on integrating iPads (or similar technology) 
    to enhance inquiry-based learning, leveraging the SAMR model.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    client = get_openai_client()
    prompt = f"""
    Review the following inquiry-based lesson plan: {unit_plan.unit_plan} 
    and assuming that the context is using iPads in the classroom, 
    generate recommendations on how to integrate technology to support inquiry-based learning.
    Use the SAMR model to describe how technology can enhance the lesson 
    and provide opportunities for students to engage in higher-order thinking and creativity.
    """

    try:
        print("ipad started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert in inquiry-based lesson plan design in any scenario.
                    """
                },
                {"role": "user", "content": prompt},
            ],
            temperature=float(unit_plan.temperature),
        )
        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_ipad_claude(
            unit_plan.unit_plan, float(unit_plan.temperature)
        )

    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"ipad": content},
    )
    print("ipad finished")

async def generate_western_views(unit_plan: UnitPlan):
    """
    Highlights how the unit plan amplifies Western views and perspectives, 
    and suggests ways to incorporate more inclusive worldviews.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    client = get_openai_client()
    prompt = f"""
    Review the following inquiry-based lesson plan: {unit_plan.unit_plan} 
    and highlight how the unit plan amplifies Western views and perspectives.
    Generate recommendations on how to incorporate additional worldviews into the lesson 
    to provide a more inclusive and diverse learning experience.
    """

    try:
        print("western_views started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert in inquiry-based lesson plan design in any scenario.
                    """
                },
                {"role": "user", "content": prompt},
            ],
            temperature=float(unit_plan.temperature),
        )
        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_western_views_claude(
            unit_plan.unit_plan, float(unit_plan.temperature)
        )

    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"western_views": content},
    )
    print("western_views finished")

async def generate_teacher_knowledge(unit_plan: UnitPlan):
    """
    Outlines teacher-specific knowledge and skills required 
    to effectively implement the inquiry-based lesson plan.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    client = get_openai_client()
    prompt = f"""
    Review the following inquiry-based lesson plan: {unit_plan.unit_plan} 
    and identify the knowledge and skills that teachers need to effectively implement the lesson.
    Outline the subject-specific knowledge that teachers need to support students' inquiry-based learning.
    Ensure not to provide pedagogical strategies in this response.
    """

    try:
        print("teacher_knowledge started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert in inquiry-based lesson plan design in any scenario.
                    """
                },
                {"role": "user", "content": prompt},
            ],
            temperature=float(unit_plan.temperature),
        )
        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_teacher_knowledge_claude(
            unit_plan.unit_plan, float(unit_plan.temperature)
        )

    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"teacher_knowledge": content},
    )
    print("teacher_knowledge finished")

async def generate_ai_integration(unit_plan: UnitPlan):
    """
    Provides recommendations for integrating AI tools into the lesson plan, 
    referencing a 5-level AI usage framework.
    Tries an OpenAI call first; on error, falls back to Claude.
    """
    client = get_openai_client()
    prompt = f"""Please review the following unit plan:
    {unit_plan.unit_plan}

    Using the 5-level AI usage framework, provide recommendations for integrating AI into the unit plan. 
    Include all 5 levels. For each level provide an activity suggestion aligning with one in the lesson plan 
    and reasoning for why that level is appropriate for that activity, learning objectives, and student context.
    """

    try:
        print("ai_integration started - attempting OpenAI GPT call")
        completion = client.chat.completions.create(
            model=openai_model_3,  # Alternatively "o3-mini" or your chosen model
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
                    """ 
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            # This property is from the code in app.py. 
            # If your OpenAI library doesn't support "reasoning_effort", omit it.
            # reasoning_effort="low",
            temperature=float(unit_plan.temperature),
        )
        content = completion.choices[0].message.content
    except Exception:
        print("OpenAI GPT call failed, attempting Claude fallback.")
        content = await _generate_ai_integration_claude(
            unit_plan.unit_plan, float(unit_plan.temperature)
        )

    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"ai_integration": content},
    )
    print("ai_integration finished")
    return content

async def generate_search_parameters(unit_plan: UnitPlan) -> str:
    """
    Creates search queries that could be used to find supporting web resources 
    for the lesson plan. Returns the generated content (JSON, list, or string) for processing.
    No fallback is currently implemented for search parameters in app.py, so we keep it as is.
    """
    client = get_openai_client()
    print("search_parameters started")

    prompt = f"""Review the following inquiry-based lesson plan: {unit_plan.unit_plan} 
                 and for each session generate a search query to be used in Google to find resources. 
                 I need to create 10 google search terms for this lesson plan I could use to find resources 
                 to use in my {unit_plan.grade} class.
                 Structure your response as a list of dictionaries with the following keys: 
                 "Session", "Search Query".
              """

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert in search query development.
                """
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=float(unit_plan.temperature),
    )

    content = completion.choices[0].message.content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"search_parameters": content},
    )
    print("search_parameters finished")
    return content


async def store_initial_unit_plan(
    grade: int,
    temperature: str,
    outcomes: str,
    user_context: Optional[str] = None,
    user_id: str = "0",
) -> UnitPlan:
    """
    Creates a new UnitPlan record in the data store 
    with basic information (grade, temperature, outcomes, user_context).
    """
    if not outcomes:
        raise ValueError("Curriculum outcomes cannot be empty.")
    if (not grade) or (grade > 12) or (grade < 1):
        raise ValueError("Grade level should be between 1 and 12.")
    created_at = datetime.now().isoformat()

    plan = UnitPlan(
        grade=int(grade),
        temperature=temperature,
        outcomes=outcomes,
        user_context=user_context,
        user_id=user_id,
        progress_percentage=10,
        title=created_at,
        created_at=created_at,
        is_favorite=False,
    )

    result = await UnitPlanDAO().insert(plan)
    plan.unit_plan_id = result
    return plan

async def get_unit_plans(
    user_id: str,
    is_favorite: Optional[bool],
    search_tags: Optional[List[str]] = None,
    search_title: Optional[str] = None,
    page_size: int = 5,
    page_number: int = 1,
):
    """
    Retrieves paginated list of unit plans by user ID.
    Optionally filters by favorite, tags, or partial text matching on title.
    """
    if not page_size or is_favorite:
        page_size = 5

    items, page_count = await UnitPlanDAO().find_unit_plans_by_user(
        user_id, page_size, page_number, is_favorite, search_tags, search_title
    )
    mapped_list = []
    for item in items:
        current_item = {
            "unit_plan_id": item["unit_plan_id"],
            "title": item["title"],
        }
        mapped_list.append(current_item)

    return mapped_list, page_count

async def add_unit_plans(unit_plan: UnitPlan):
    """
    Inserts a UnitPlan object into the data store.
    """
    await UnitPlanDAO().insert(unit_plan)

async def update_fav_unit_plans(unit_plan_id: int):
    """
    Toggles the 'favorite' status of a UnitPlan identified by unit_plan_id.
    """
    unit_plan = await UnitPlanDAO().find(unit_plan_id)
    if not unit_plan:
        raise ValueError("Unit plan not found")

    is_favorite = not unit_plan.is_favorite
    await UnitPlanDAO().update_favorite_unit_plan(unit_plan_id, is_favorite)

async def get_unit_plan(unit_plan_id: int) -> UnitPlan:
    """
    Retrieves a single UnitPlan by its ID.
    """
    return await UnitPlanDAO().find(unit_plan_id)

async def remove_unit_plans(unit_plan_id: int):
    """
    Deletes a UnitPlan record from the data store by ID.
    """
    await UnitPlanDAO().delete(unit_plan_id)
    print(f"Removed unit plan {unit_plan_id}") 