import uuid
from typing import Optional
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
from typing import List

from daos.unit_plan_dao import UnitPlanDAO
from entities.unit_plan import UnitPlan
from constants import APP_OPENAI_MODEL


def get_openai_client():
    if not hasattr(get_openai_client, "client"):
        load_dotenv(override=True)
        get_openai_client.client = OpenAI()
    return get_openai_client.client


openai_model = APP_OPENAI_MODEL


async def generate_guiding_question(unit_plan):
    client = get_openai_client()
    print("guiding_question started")

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert in inquiry-based learning.""",
            },
            {
                "role": "user",
                "content": f"""Instructions:

                    Evaluate the following lesson: {unit_plan.unit_plan}. 
                    Identify the guiding question that will drive the inquiry-based learning in this lesson: Facts, Concepts, and Debatable Questions.
                    For example, a factual question could be: "Why doesn’t energy cycle within an ecosystem?" A conceptual question could be: "In what ways could humans impact the
                    balance of this freshwater ecosystem and its biodiversity?" A debatable question could be: "Using all of the evidence and conclusions you made above, how would you rate the health of the freshwater ecosystem at FEC?"
                    """,
            },
        ],
        temperature=float(unit_plan.temperature),
    )

    content = completion.choices[0].message.content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"guiding_question": content},
    )
    print("guiding_question finished")


async def generate_essential_knowledge(unit_plan):
    client = get_openai_client()
    print("essential_knowledge started")

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.

""",
            },
            {
                "role": "user",
                "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan.unit_plan} and identify the essential knowledge that students will acquire through the lesson. 
            Specifically, outline the required background knowledge, essential skills needed, and key concepts that student need to know to successfully engage in the inquiry-based learning processes.

""",
            },
        ],
        temperature=float(unit_plan.temperature),
    )

    content = completion.choices[0].message.content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"essential_knowledge": content},
    )
    print("essential_knowledge finished")


async def generate_differentiation(unit_plan):
    client = get_openai_client()
    print("differentiation started")

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.

""",
            },
            {
                "role": "user",
                "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan.unit_plan} and identify the strategies for differentiation that are embedded in the lesson. 
            Specifically, draw from Universal Design for Learning (UDL) principles and describe and recommend how students will communicate their learning in various ways.
            Provide recommendations to ensure learning opportunities are accessible to all students, including those with diverse needs and abilities.

""",
            },
        ],
        temperature=float(unit_plan.temperature),
    )

    content = completion.choices[0].message.content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"differentiation": content},
    )
    print("differentiation finished")


async def generate_inquiry_impact(unit_plan):
    client = get_openai_client()
    print("inquiry_impact started")

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.

""",
            },
            {
                "role": "user",
                "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan.unit_plan} and identify the real-world impact of the lesson on students' learning and development.
            Generate recommendations on how exemplary citizenship, social responsibility, and ethical considerations enacted beyond the school context.             
            Identify key concepts and skills that are transferable to other contexts and subjects.
            Assuming that the lesson is complete, generate debriefing questions that will help students reflect on their learning and the impact of the inquiry-based lesson.

""",
            },
        ],
        temperature=float(unit_plan.temperature),
    )

    content = completion.choices[0].message.content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"inquiry_impact": content},
    )
    print("inquiry_impact finished")


async def generate_ipad(unit_plan):
    client = get_openai_client()
    print("ipad started")

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.

""",
            },
            {
                "role": "user",
                "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan.unit_plan} and assuming that the context is using iPads in the classroom, generate recommendations on how to integrate technology to support inquiry-based learning.
            Use the SAMR model to describe how technology can be used to enhance the lesson and provide opportunities for students to engage in higher-order thinking and creativity.


""",
            },
        ],
        temperature=float(unit_plan.temperature),
    )

    content = completion.choices[0].message.content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"ipad": content},
    )
    print("ipad finished")


async def generate_western_views(unit_plan):
    client = get_openai_client()
    print("western_views started")

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.

""",
            },
            {
                "role": "user",
                "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan.unit_plan} and highlight how the unit plan amplifies Western views and perspectives.
            Generate recommendations on how to incorporate worldviews into the lesson to provide a more inclusive and diverse learning experience.

""",
            },
        ],
        temperature=float(unit_plan.temperature),
    )

    content = completion.choices[0].message.content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"western_views": content},
    )
    print("western_views finished")


async def generate_teacher_knowledge(unit_plan):
    client = get_openai_client()
    print("teacher_knowledge started")

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert in inquiry-based lesson plan design in any scenario.

""",
            },
            {
                "role": "user",
                "content": f"""
            Review the following inquiry-based lesson plan: {unit_plan.unit_plan} and identify the knowledge and skills that teachers need to effectively implement the lesson.
            Outline the subject-specific knowledge that teachers need to support students' inquiry-based learning.
            Ensure not to providde pedagogical strategies in this response.

""",
            },
        ],
        temperature=float(unit_plan.temperature),
    )
    content = completion.choices[0].message.content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"teacher_knowledge": content},
    )
    print("teacher_knowledge finished")


async def generate_inquiry(unit_plan):
    client = get_openai_client()
    print("inquiry started")

    # TODO: add more conditions here
    if unit_plan.user_context and len(unit_plan.user_context) > 0:
        prompt = f"""Develop an inquiry-based lesson plan for {unit_plan.grade} that aligns with the following curricular outcomes: {unit_plan.outcomes}.
                            The lesson should embed the principles of authentic and meaningful tasks, student-centered learning, collaborative learning, an interdisciplinary approach,
                            critical thinking and problem-solving, ongoing assessment and feedback, the teacher as facilitator, and reflective practice.
                            Ensure that the scenario includes the following consideration: {unit_plan.user_context}.

            """
    else:
        prompt = f"""Develop an inquiry-based lesson plan for {unit_plan.grade} that aligns with the following curricular outcomes: {unit_plan.outcomes}.
                            The lesson should embed the principles of authentic and meaningful tasks, student-centered learning, collaborative learning, an interdisciplinary approach,
                            critical thinking and problem-solving, ongoing assessment and feedback, the teacher as facilitator, and reflective practice.
            """

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": f"""
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
            },
            {"role": "user", "content": prompt},
        ],
        temperature=float(unit_plan.temperature),
    )

    content = completion.choices[0].message.content
    unit_plan.unit_plan = content
    await UnitPlanDAO().update(unit_plan.unit_plan_id, {"unit_plan": content})
    print("inquiry finished")
    return content


async def generate_assessment(unit_plan):
    client = get_openai_client()
    print("assessment_plan started")

    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert in assessment design for inquiry-based lesson plans.

                Instructions:

                Design an assessment plan that aligns with the inquiry-based lesson plan you have created. 
                Ensure the assessment is authentic, meaningful, and aligned with the curricular outcomes and the principles of inquiry-based learning. 
                Ensure to include the following components in your assessment plan: opportunities for assessment of learning, assessment for learning, and assessment as learning. 
                Plan for ongoing assessment and feedback that supports student learning and growth. 
                Describe how the assessment will be used to evaluate student progress and inform instruction. 


""",
            },
            {
                "role": "user",
                "content": f"The following is the Unit plan: {unit_plan.unit_plan}.",
            },
        ],
        temperature=float(unit_plan.temperature),
    )

    content = completion.choices[0].message.content
    await UnitPlanDAO().update(
        unit_plan.unit_plan_id,
        {"assessment_plan": content},
    )
    print("assessment_plan finished")


async def store_initial_unit_plan(
    grade: int,
    temperature: str,
    outcomes: str,
    user_context: str = None,
    user_id: str = "0",
) -> UnitPlan:
    if not outcomes:
        raise ValueError("Curriculum outcomes cannot be empty.")
    if (not grade) or (grade > 12) or (grade < 1):
        raise ValueError("Grade level should be between 1 and 12.")
    created_at = datetime.now().isoformat()

    plan = UnitPlan(
        # unit_plan_id=str(uuid.uuid4().hex),
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
    search_tags: List[str] = None,
    search_title: str = None,
    page_size: int = 5,
    page_number: int = 1,
):
    if not page_size or is_favorite:
        page_size = 5

    items, page_count = await UnitPlanDAO().find_unit_plans_by_user(
        user_id, page_size, page_number, is_favorite, search_tags, search_title
    )
    mapped_list = []
    for item in items:
        current_item: any = {
            "unit_plan_id": item["unit_plan_id"],
            "title": item["title"],
        }
        mapped_list.append(current_item)

    return mapped_list, page_count


async def add_unit_plans(unit_plan: UnitPlan):
    # unit_plan.unit_plan_id = str(uuid.uuid4().hex)
    await UnitPlanDAO().insert(unit_plan)
    # run_async_function(UnitPlanDAO().insert(unit_plan))


async def update_fav_unit_plans(unit_plan_id: int):
    unit_plan = await UnitPlanDAO().find(unit_plan_id)
    if not unit_plan:
        raise ValueError("Unit plan not found")

    is_favorite = not unit_plan.is_favorite
    await UnitPlanDAO().update_favorite_unit_plan(unit_plan_id, is_favorite)


async def get_unit_plan(unit_plan_id: int) -> UnitPlan:
    response = await UnitPlanDAO().find(unit_plan_id)
    # print(f"unit plan is {response}")
    return response


async def remove_unit_plans(unit_plan_id: int):
    await UnitPlanDAO().delete(unit_plan_id)