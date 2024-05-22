import chromadb
from chromadb.config import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

class ChromaManager:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.chroma_client = self.initialize_chroma_client()
        self.chroma_collection = self.get_or_create_collection()
        self.storage_context = self.initialize_storage_context()

    def initialize_chroma_client(self):
        return chromadb.PersistentClient(
                   path="datos/storage/vector_storage/chromadb/"
            )

    def get_or_create_collection(self):
        try:
            return self.chroma_client.get_or_create_collection(self.collection_name)
        except Exception as e:
            print(f"An error occurred while creating the collection: {str(e)}")
            try:
                print(f"Cargando Collection ya existente")
                return self.chroma_client.get_or_create_collection(self.collection_name)
            except Exception as e:
                print(f"Failed to get the collection: {str(e)}")
                raise

    def initialize_storage_context(self):
        vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        try:
            return StorageContext.from_defaults(vector_store=vector_store,
                                                persist_dir="datos/storage/index_storage/textos/")
        except FileNotFoundError:
            return StorageContext.from_defaults(vector_store=vector_store)