from llama_index.core import  ServiceContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain.chat_models import ChatOpenAI
from llama_index.llms.openai import OpenAI


class ServiceContextManager:
    def __init__(self, temperature=0.2, max_tokens=512, model_name='gpt-3.5-turbo'):
        self.llm_predictor = self.initialize_llm_predictor(temperature, max_tokens, model_name)
        self.embed_model = self.initialize_embed_model()
        self.service_context = self.initialize_service_context()

    def initialize_llm_predictor(self, temperature, max_tokens, model_name):
        return OpenAI(model=model_name, temperature=temperature)

    def initialize_embed_model(self):
        return HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


    def initialize_service_context(self):
        return ServiceContext.from_defaults(
            llm_predictor=self.llm_predictor,
            embed_model=self.embed_model
        )