from typing import List
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

def describe_page_with_llm(text: str, llm: BaseChatModel) -> str:
    """
    Uses an LLM to generate a concise summary of the page content.
    """
    clean_text = " ".join(text.replace("\n", " ").split())
    if not clean_text:
        return "Empty or OCR-unreadable page"
    
    # Truncate text to save tokens and prevent huge inputs
    truncated_text = clean_text[:3000]

    messages = [
        SystemMessage(content="You are a helpful assistant. Summarize the core topic of the provided document text in a single, concise sentence (maximum 20 words)."),
        HumanMessage(content=f"Document text:\n{truncated_text}")
    ]
    
    response = llm.invoke(messages)
    return response.content.strip()

def add_page_descriptions(docs: List[Document], llm: BaseChatModel) -> List[Document]:
    """
    Adds an LLM-generated short description to every page-level document metadata.
    """
    for i, doc in enumerate(docs):
        print(f"Summarizing page {i + 1}/{len(docs)}...")
        doc.metadata["page_description"] = describe_page_with_llm(doc.page_content, llm)
        
    return docs
