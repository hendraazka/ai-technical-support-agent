
from app.rag.vector_store import search_documents


def retrieve_context(query: str, limit: int = 3) -> str:
    results = search_documents(query, limit=limit)

    if not results:
        return "No relevant runbook found in the knowledge base."

    context_parts = []

    for index, result in enumerate(results, start=1):
        source = result["metadata"].get("source", "unknown")
        page = result["metadata"].get("page")

        source_info = f"Source: {source}"

        if page:
            source_info += f", Page: {page}"

        context_parts.append(
            f"""
[Runbook Result {index}]
{source_info}

{result["content"]}
"""
        )

    return "\n\n".join(context_parts)

