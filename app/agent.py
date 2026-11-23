import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from app.tools import format_system_status, get_docker_status

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY belum dikonfigurasi")


# 1. Define Agent Tools

@tool
def system_monitoring() -> str:
    """Periksa kondisi sistem Linux: CPU, RAM, disk, hostname, dan uptime."""
    return format_system_status()


@tool
def docker_monitoring() -> str:
    """Periksa daftar Docker containers, image, status, dan state."""
    return get_docker_status()


tools = [
    system_monitoring,
    docker_monitoring,
]


# 2. Initialize Gemini

llm = ChatGoogleGenerativeAI(
    model=MODEL,
    google_api_key=API_KEY,
    temperature=0.2,
)


# 3. Build LangGraph Agent

SYSTEM_PROMPT = """
Kamu adalah Hermes AI Technical Support Agent.

Tugas:
- Membantu troubleshooting Linux dan DevOps.
- Gunakan system_monitoring jika pengguna bertanya tentang CPU,
  RAM, disk, uptime, atau kondisi server.
- Gunakan docker_monitoring jika pengguna bertanya tentang
  Docker containers.
- Jangan mengarang hasil monitoring.
- Jelaskan hasil tools secara ringkas dalam bahasa Indonesia.
- Jangan menjalankan tindakan yang mengubah sistem.
"""

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT,
)


# 4. Conversation Interface

def ask_agent(
    message: str,
    history: list[dict[str, str]],
) -> str:

    messages = []

    for item in history[-10:]:
        if item["role"] == "user":
            messages.append(HumanMessage(content=item["content"]))
        elif item["role"] == "assistant":
            messages.append(AIMessage(content=item["content"]))

    messages.append(HumanMessage(content=message))

    result = agent.invoke({"messages": messages})

    content = result["messages"][-1].content

    # Ambil teks saja dari response LangGraph
    if isinstance(content, list):
        answer = "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict)
            and block.get("type") == "text"
        )
    elif isinstance(content, str):
        answer = content
    else:
        answer = "Agent tidak menghasilkan jawaban teks."

    return answer.strip()


