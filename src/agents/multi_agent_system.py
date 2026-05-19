import os
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, LLM

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# NVIDIA LLM CONFIG
# =========================

llm = LLM(
    model="openai/mistralai/mixtral-8x7b-instruct-v0.1",

    api_key=os.getenv("NVIDIA_API_KEY"),

    base_url="https://integrate.api.nvidia.com/v1"
)

# =========================
# SEARCH AGENT
# =========================

search_agent = Agent(
    role="Research Paper Search Specialist",

    goal=(
        "Find relevant information "
        "about AI research topics."
    ),

    backstory=(
        "Expert researcher specialized "
        "in discovering AI papers."
    ),

    llm=llm,

    verbose=True
)

# =========================
# SUMMARY AGENT
# =========================

summary_agent = Agent(
    role="Research Summarization Expert",

    goal=(
        "Generate concise summaries "
        "of research papers."
    ),

    backstory=(
        "AI scientist skilled at "
        "extracting key insights."
    ),

    llm=llm,

    verbose=True
)

# =========================
# COMPARISON AGENT
# =========================

comparison_agent = Agent(
    role="Research Comparison Specialist",

    goal=(
        "Compare AI research papers "
        "and identify similarities."
    ),

    backstory=(
        "Expert analyst in comparative "
        "research evaluation."
    ),

    llm=llm,

    verbose=True
)

# =========================
# REPORT AGENT
# =========================

report_agent = Agent(
    role="Research Report Writer",

    goal=(
        "Generate professional "
        "research reports."
    ),

    backstory=(
        "Technical writer specialized "
        "in AI and machine learning."
    ),

    llm=llm,

    verbose=True
)

# =========================
# USER INPUT
# =========================

research_topic = input(
    "Enter research topic: "
)

# =========================
# TASKS
# =========================

search_task = Task(
    description=(
        f"Search information about "
        f"{research_topic}"
    ),

    expected_output=(
        "Detailed research findings."
    ),

    agent=search_agent
)

summary_task = Task(
    description=(
        "Summarize the research findings."
    ),

    expected_output=(
        "Concise research summaries."
    ),

    agent=summary_agent
)

comparison_task = Task(
    description=(
        "Compare methodologies, "
        "findings, and limitations."
    ),

    expected_output=(
        "Comparative analysis report."
    ),

    agent=comparison_agent
)

report_task = Task(
    description=(
        "Generate a final "
        "professional report."
    ),

    expected_output=(
        "Complete AI research report."
    ),

    agent=report_agent
)

# =========================
# CREW
# =========================

research_crew = Crew(
    agents=[
        search_agent,
        summary_agent,
        comparison_agent,
        report_agent
    ],

    tasks=[
        search_task,
        summary_task,
        comparison_task,
        report_task
    ],

    verbose=True
)

# =========================
# RUN CREW
# =========================

result = research_crew.kickoff()

print("\n")
print("=" * 80)
print("FINAL OUTPUT")
print("=" * 80)
print("\n")

print(result)