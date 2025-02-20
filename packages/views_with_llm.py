from django.shortcuts import render
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .models import TourPackage

# Create your views here.


def load_vector_store():
    """Load the saved vector store"""
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
    )
    vector_store = FAISS.load_local(
        "data/vector_store",
        embeddings,
        allow_dangerous_deserialization=True,
    )
    return vector_store


def filter_relevant_packages(query: str, docs: list) -> list:
    """Use LLM to filter and rank the most relevant packages"""

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=1,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a travel package recommendation expert. 
        Analyze the search query and the tour packages, then return the 5 most relevant packages.
        Consider factors like destination match, tour type, and overall relevance to the query.
        Only return packages that are truly relevant to the query.""",
            ),
            (
                "user",
                """Query: {query}

        Available packages:
        {packages}

        Return only the product_codes of the 5 most relevant packages in order of relevance.
        Format: ["code1", "code2", "code3", "code4", "code5"]
        If fewer than 5 packages are relevant, return fewer codes.""",
            ),
        ]
    )

    # Format packages for the prompt
    packages_text = "\n".join(
        [
            f"Product Code: {doc.metadata['product_code']}\n"
            f"Title: {doc.metadata['title']}\n"
            f"Duration: {doc.metadata['duration']}\n"
            f"Price: {doc.metadata['price']}\n"
            "---"
            for doc in docs
        ]
    )

    # Get LLM response
    chain = prompt | llm
    response = chain.invoke({"query": query, "packages": packages_text})

    try:
        # Parse the response to get product codes
        import ast

        relevant_codes = ast.literal_eval(response.content)

        # Filter and order the original results
        filtered_results = []
        for code in relevant_codes:
            for doc in docs:
                if doc.metadata["product_code"] == code:
                    filtered_results.append(doc.metadata)
                    break

        return filtered_results
    except:
        # Fallback to first 5 results if parsing fails
        return [doc.metadata for doc in docs[:5]]


def index(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        # Load vector store
        vector_store = load_vector_store()

        # Search similar packages
        similar_docs = vector_store.similarity_search(
            query,
            k=10,  # Get more results initially for better filtering
        )

        # Filter to most relevant results using LLM
        results = filter_relevant_packages(query, similar_docs)

    return render(request, "packages/index.html", {"results": results, "query": query})
