
from langchain_core.tools import tool

from app.rag.retriever import retrieve_context


@tool
def search_runbook(query: str) -> str:
    """
    Search the technical support knowledge base for relevant
    runbooks, troubleshooting procedures, and incident solutions.
    Use this tool when investigating errors or technical incidents.
    """
    return retrieve_context(query)

