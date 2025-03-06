from django.shortcuts import render
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from .models import TourPackage

# Create your views here.


def load_vector_store():
    """Load the saved vector store"""
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
    )
    vector_store = FAISS.load_local(
        "data/vector_store",
        embeddings,
        allow_dangerous_deserialization=True,
    )
    return vector_store


def index(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        # Load vector store
        vector_store = load_vector_store()

        # The query is already enhanced with "kimchi" from the API
        enhanced_query = f"Find travel packages related to: {query}"

        # Search similar packages with MMR
        similar_docs = vector_store.max_marginal_relevance_search(
            enhanced_query,
            k=10,
            fetch_k=30,
            lambda_mult=1.0,
        )
        # Get the document metadata for each result
        results = [doc.metadata for doc in similar_docs]

    return render(request, "packages/index.html", {"results": results, "query": query})
