import os
from dotenv import load_dotenv  # Add this to load your .env file
from loaders import load_pdf_pages
from summarizer import add_page_descriptions
from langchain_groq import ChatGroq

# Load the environment variables from your .env file right at the start
load_dotenv()

def main():
    # 1. Verify the key is loaded (optional, but good for debugging)
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY is missing! Please check your .env file.")

    # 2. Initialize the fast Llama 3 model via Groq
    print("Initializing LLM...")
    # Note: ChatGroq automatically looks for GROQ_API_KEY in the environment,
    # so we don't even need to pass it in directly!
    llm = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0
    )

    # 3. Load the PDF
    pdf_path = "data/raw/andrew-ng-machine-learning-yearning.pdf"
    print(f"Loading PDF from: {pdf_path}")
    all_pages = load_pdf_pages(pdf_path)
    
    # 4. Grab just the first 3 pages for a quick test
    test_pages = all_pages[0:3] 
    print(f"Loaded {len(all_pages)} total pages. Testing summarizer on the first {len(test_pages)} pages...")

    # 5. Apply the LLM Summarizer
    enriched_docs = add_page_descriptions(test_pages, llm)

    # 6. Print the results to the terminal
    print("\n" + "="*50)
    print("SUMMARIZATION TEST RESULTS")
    print("="*50)
    
    for doc in enriched_docs:
        page_num = doc.metadata['page_number']
        desc = doc.metadata['page_description']
        print(f"Page {page_num}: {desc}")
        print("-" * 50)

if __name__ == "__main__":
    main()