from django.shortcuts import render
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

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


def index(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        # Load vector store
        vector_store = load_vector_store()

        # Search similar packages
        similar_docs = vector_store.similarity_search(
            query,
            k=10,  # Return top 10 results
        )

        # Extract results
        results = [doc.metadata for doc in similar_docs]

    return render(request, "packages/index.html", {"results": results, "query": query})
