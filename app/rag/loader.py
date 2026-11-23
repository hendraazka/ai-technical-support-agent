
from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document

KNOWLEDGE_BASE_DIR = (
    Path(__file__).resolve().parents[2] / "knowledge_base"
)


def load_documents():
    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.rglob("*"):
        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()
        source = str(file_path.relative_to(KNOWLEDGE_BASE_DIR))

        try:
            if suffix in (".md", ".txt"):
                content = file_path.read_text(encoding="utf-8")

                documents.append(
                    Document(
                        page_content=content,
                        metadata={"source": source},
                    )
                )

            elif suffix == ".pdf":
                reader = PdfReader(str(file_path))

                for page_number, page in enumerate(reader.pages):
                    content = page.extract_text() or ""

                    if content.strip():
                        documents.append(
                            Document(
                                page_content=content,
                                metadata={
                                    "source": source,
                                    "page": page_number + 1,
                                },
                            )
                        )

        except Exception as error:
            print(f"Failed to load {source}: {error}")

    return documents

