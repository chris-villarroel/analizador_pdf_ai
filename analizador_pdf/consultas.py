from llama_index.core import load_index_from_storage
from llama_index.llms.openai import OpenAI
from analizador_pdf.vectorManager import ChromaManager
from llama_index.core import Settings

import mlflow
import time

from traceloop.sdk import Traceloop

from analizador_pdf import utilidades

from llama_index.llms.ollama import Ollama

def hacer_consulta(query, collection_name, index_id, temperature=0.8, max_tokens=512, model_name='gpt-3.5-turbo'):
    """
    Query the index and return results.

    Parameters:
    - query (str): The query string to search the index.
    - collection_name (str): Name of the collection for ChromaManager.
    - temperature (float, optional): Temperature parameter for ServiceContextManager. Default is 0.2.
    - max_tokens (int, optional): Max tokens parameter for ServiceContextManager. Default is 512.
    - model_name (str, optional): Model name parameter for ServiceContextManager. Default is 'gpt-3.5-turbo'.

    Returns:
    - results: The results from querying the index.
    """
    #collection_name='version3'
    #query='Wha is this about'
    #index_id= "nombre_index3"

    print('----------INICIANDO MLFOW------------')
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.start_run()
    print('----------eND-----------')

    mlflow.log_param("llm_model", model_name)

    Traceloop.init()



    if model_name in ["gpt-3.5-turbo","gpt-4","gpt-4-turbo-2024-04-09"]:
        Settings.llm = OpenAI(model=model_name, temperature=0.1)
    elif model_name =="llama3":
        Settings.llm = Ollama(model=model_name, request_timeout=360.0)
    

    # Initialize managers
    chroma_manager = ChromaManager(collection_name=collection_name)

    # Load the index
    load_index = load_index_from_storage(
        storage_context=chroma_manager.storage_context,
        index_id=index_id
    )

    # Query the index and return results
    start_time = time.time()
    results = load_index.as_query_engine().query(query)
    elapsed_time = time.time() - start_time
    mlflow.log_metric("ReultsTime", elapsed_time)
    mlflow.end_run()

    print('Listo')
    return results
    
