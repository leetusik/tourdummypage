import os

import dotenv
from django.core.management.base import BaseCommand
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from packages.models import TourPackage

dotenv.load_dotenv()


class Command(BaseCommand):
    help = "Create and save vector store from tour packages"

    def handle(self, *args, **kwargs):
        # Get all tour packages
        self.stdout.write("Fetching tour packages...")
        packages = TourPackage.objects.all()

        # Create texts and metadata for vector store
        texts = []
        metadatas = []
        for package in packages:
            text = f"{package.title} {package.description} {package.category}"
            metadata = {
                "product_code": package.product_code,
                "title": package.title,
                "price": package.price,
                "duration": package.duration,
                "airline": package.airline,
            }
            texts.append(text)
            metadatas.append(metadata)

        self.stdout.write("Creating vector store...")
        # Create vector store
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
        )
        vector_store = FAISS.from_texts(
            texts=texts, embedding=embeddings, metadatas=metadatas
        )

        # Save vector store
        self.stdout.write("Saving vector store...")
        vector_store_dir = "data/vector_store"
        os.makedirs(vector_store_dir, exist_ok=True)
        vector_store.save_local(vector_store_dir)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created and saved vector store to {vector_store_dir}"
            )
        )
