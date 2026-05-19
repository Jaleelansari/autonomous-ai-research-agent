import streamlit as st
import subprocess
import os
import sys
import chromadb
import json
import shutil

from openai import OpenAI
from dotenv import load_dotenv

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Autonomous AI Research Agent",
    page_icon="🤖",
    layout="wide"
)

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# NVIDIA CLIENT
# =========================

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

# =========================
# CHROMADB
# =========================

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="research_papers"
)

# =========================
# CHAT MEMORY
# =========================

MEMORY_FILE = "memory/chat_history.json"

os.makedirs("memory", exist_ok=True)

if not os.path.exists(MEMORY_FILE):

    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)


def load_chat_history():

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:

        return json.load(f)


def save_chat_message(question, answer):

    history = load_chat_history()

    history.append({
        "question": question,
        "answer": answer
    })

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:

        json.dump(history, f, indent=4)

# =========================
# RAG FUNCTIONS
# =========================


def retrieve_context(query):

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context


def answer_question(query):

    context = retrieve_context(query)

    response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct-v0.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert AI research assistant."
                )
            },
            {
                "role": "user",
                "content": f"""
                Context:
                {context}

                Question:
                {query}
                """
            }
        ],
        temperature=0.2,
        max_tokens=600
    )

    return response.choices[0].message.content


# =========================
# SIDEBAR
# =========================

st.sidebar.title("🤖 AI Research Agent")

st.sidebar.markdown("---")

st.sidebar.info("""
This platform can:
- Search research papers
- Upload PDFs
- Generate summaries
- Compare papers
- Generate reports
- Create presentations
- Answer research questions
- Store chat history
""")

st.sidebar.markdown("---")

st.sidebar.success("System Ready ✅")

# =========================
# MAIN TITLE
# =========================

st.title("🤖 Autonomous AI Research Platform")

st.markdown("""
### AI-Powered Research Automation System

This platform automates:
- Research paper discovery
- PDF processing
- AI summarization
- Comparative analysis
- Report generation
- PowerPoint generation
- RAG-based question answering
- Research memory storage
""")

st.markdown("---")

# =========================
# METRICS
# =========================

papers_count = len(
    os.listdir("data/papers")
) if os.path.exists("data/papers") else 0

summaries_count = len(
    os.listdir("data/summaries")
) if os.path.exists("data/summaries") else 0

reports_count = len(
    os.listdir("reports")
) if os.path.exists("reports") else 0

col1, col2, col3 = st.columns(3)

col1.metric(
    "📄 Papers",
    papers_count
)

col2.metric(
    "🧠 Summaries",
    summaries_count
)

col3.metric(
    "📊 Reports",
    reports_count
)

st.markdown("---")

# =========================
# RESEARCH GENERATION
# =========================

st.header("🔍 Generate Research")

topic = st.text_input(
    "Enter Research Topic"
)

uploaded_files = st.file_uploader(
    "Upload Research PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("🚀 Generate Research"):

    if topic.strip() == "" and not uploaded_files:

        st.warning(
            "Please enter a topic or upload PDFs."
        )

    else:

        # =========================
        # HANDLE PDF UPLOADS
        # =========================

        if uploaded_files:

            os.makedirs(
                "data/papers",
                exist_ok=True
            )

            # Clear old PDFs
            for old_file in os.listdir(
                "data/papers"
            ):

                old_path = os.path.join(
                    "data/papers",
                    old_file
                )

                if os.path.isfile(old_path):
                    os.remove(old_path)

            # Save uploaded PDFs
            for uploaded_file in uploaded_files:

                save_path = os.path.join(
                    "data/papers",
                    uploaded_file.name
                )

                with open(save_path, "wb") as f:
                    f.write(
                        uploaded_file.getbuffer()
                    )

            st.success(
                "PDFs uploaded successfully!"
            )

        progress_bar = st.progress(0)

        status = st.empty()

        # =========================
        # STEP 1
        # =========================

        if not uploaded_files:

            status.info(
                "📥 Downloading research papers..."
            )

            subprocess.run(
                [
                    sys.executable,
                    "src/search/download_papers.py"
                ],
                input=topic,
                text=True
            )

        else:

            status.info(
                "📂 Using uploaded PDFs..."
            )

        progress_bar.progress(15)

        # =========================
        # STEP 2
        # =========================

        status.info(
            "📄 Extracting PDF text..."
        )

        subprocess.run(
            [
                sys.executable,
                "src/extraction/pdf_extractor.py"
            ]
        )

        progress_bar.progress(30)

        # =========================
        # STEP 3
        # =========================

        status.info(
            "🧠 Generating summaries..."
        )

        subprocess.run(
            [
                sys.executable,
                "src/agents/research_agent.py"
            ]
        )

        progress_bar.progress(50)

        # =========================
        # STEP 4
        # =========================

        status.info(
            "📊 Comparing papers..."
        )

        subprocess.run(
            [
                sys.executable,
                "src/agents/comparison_agent.py"
            ]
        )

        progress_bar.progress(65)

        # =========================
        # STEP 5
        # =========================

        status.info(
            "📝 Generating research report..."
        )

        subprocess.run(
            [
                sys.executable,
                "src/report_generation/report_generator.py"
            ]
        )

        progress_bar.progress(80)

        # =========================
        # STEP 6
        # =========================

        status.info(
            "📽️ Generating PowerPoint..."
        )

        subprocess.run(
            [
                sys.executable,
                "src/ppt_generation/ppt_generator.py"
            ]
        )

        progress_bar.progress(90)

        # =========================
        # STEP 7
        # =========================

        status.info(
            "🧩 Creating embeddings..."
        )

        subprocess.run(
            [
                sys.executable,
                "src/embeddings/vector_store.py"
            ]
        )

        progress_bar.progress(100)

        status.success(
            "✅ Research pipeline completed!"
        )

st.markdown("---")

# =========================
# REPORT VIEWER
# =========================

st.header("📄 Research Report")

report_path = (
    "reports/final_research_report.txt"
)

if os.path.exists(report_path):

    with open(
        report_path,
        "r",
        encoding="utf-8"
    ) as f:

        report = f.read()

    st.text_area(
        "Generated Research Report",
        report,
        height=400
    )

    st.download_button(
        label="⬇️ Download Report",
        data=report,
        file_name="final_research_report.txt",
        mime="text/plain"
    )

else:

    st.info("No report generated yet.")

st.markdown("---")

# =========================
# PPT SECTION
# =========================

st.header("📽️ PowerPoint Presentation")

ppt_path = (
    "presentations/final_research_presentation.pptx"
)

if os.path.exists(ppt_path):

    with open(ppt_path, "rb") as ppt_file:

        st.download_button(
            label="⬇️ Download PowerPoint",
            data=ppt_file,
            file_name="final_research_presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    st.success(
        "Presentation generated successfully!"
    )

else:

    st.info("No presentation generated yet.")

st.markdown("---")

# =========================
# CHATBOT
# =========================

st.header("💬 AI Research Chatbot")

st.write("""
Ask questions about the processed research papers.
""")

user_question = st.text_input(
    "Ask a research question"
)

if st.button("🤖 Ask AI"):

    if user_question.strip() == "":

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner("Thinking..."):

            answer = answer_question(
                user_question
            )

        st.markdown("### 🤖 AI Answer")

        st.write(answer)

        save_chat_message(
            user_question,
            answer
        )

st.markdown("---")

# =========================
# RESEARCH MEMORY
# =========================

st.header("🧠 Research Memory")

history = load_chat_history()

if len(history) == 0:

    st.info("No chat history yet.")

else:

    recent_history = list(
        reversed(history[-5:])
    )

    for idx, item in enumerate(
        recent_history,
        start=1
    ):

        st.markdown(
            f"### Question {idx}"
        )

        st.write(item["question"])

        st.markdown(
            "#### 🤖 AI Answer"
        )

        st.write(item["answer"])

        st.markdown("---")

# =========================
# FOOTER
# =========================

st.caption(
    "Built using Streamlit, NVIDIA APIs, ChromaDB, RAG Architecture, and AI Automation"
)