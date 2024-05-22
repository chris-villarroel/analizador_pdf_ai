import os
from dotenv import load_dotenv
import openai
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings

from analizador_pdf.vectorManager import ChromaManager
from analizador_pdf.serviceManager import ServiceContextManager

from traceloop.sdk import Traceloop

import mlflow
import time

from analizador_pdf import utilidades

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding


load_dotenv()



def init_and_save_vector(input_dir, 
                              collection_name, 
                              index_id,
                              path_save_index='datos/storage/index_storage/textos/', 
                              temperature=0.2,
                              max_tokens=512,
                              model_name='text-embedding-ada-002'):
    """
    Initialize and save index.

    Parameters:
    - input_dir (str): Path to the input directory containing documents.
    - collection_name (str): Name of the collection for ChromaManager.
    - path_save_index (str): Path to save the index.
    - temperature (float, optional): Temperature parameter for ServiceContextManager. Default is 0.2.
    - max_tokens (int, optional): Max tokens parameter for ServiceContextManager. Default is 512.
    - model_name (str, optional): Model name parameter for ServiceContextManager. Default is 'gpt-3.5-turbo'.
    """

    #input_dir='datos/textos/Why_Data_Debt_Is_the_Next_Technical_Debt_You_Need_to_Worry_About__pdf'
    #collection_name="version3"
    #index_id="nombre_index3"
    
    # Load environment variables and set OpenAI API key

    print('----------INICIANDO MLFOW------------')
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.start_run()
    print('----------eND-----------')

    mlflow.log_param("embedding_model", model_name)

    if model_name =='text-embedding-ada-002':
        Settings.embed_model = OpenAIEmbedding(model = model_name, embed_batch_size=100)
    elif model_name =='nomic-embed-text':
        Settings.embed_model = OllamaEmbedding(model_name = model_name)




    openai.api_key = os.getenv("OPENAI_API_KEY")
    os.environ["TRACELOOP_API_KEY"] = os.getenv("TRACELOOP_API_KEY")
    Traceloop.init()

  
    # Load documents
    documents = SimpleDirectoryReader(input_dir=input_dir, recursive=True, filename_as_id=True).load_data()
    print(f"Loaded {len(documents)} documents of text")

    #Save MetaData
    cantidad_de_palabras = utilidades.count_characters_in_list(documents)
    mlflow.log_metric("Cantidad de Palabras", cantidad_de_palabras)

    # Initialize managers
    print('iniciando Chroma')
    chroma_manager = ChromaManager(collection_name=collection_name)
  

    start_time = time.time()
    # Initialize and populate the GPTVectorStoreIndex
    print('Cargado datos')
    index = VectorStoreIndex.from_documents(
        documents=documents, 
        storage_context=chroma_manager.storage_context
    )
    elapsed_time = time.time() - start_time
    mlflow.log_metric("VectorTime", elapsed_time)


    # Save index and persist data
    print('Save')
    index.set_index_id(index_id)
    index.storage_context.persist(path_save_index)
    

    mlflow.end_run()

    print('Listo')