import streamlit as st
import os
from shutil import copyfile
import re
 
from analizador_pdf import utilidades 
from analizador_pdf import document2texto 
from analizador_pdf import texto2vector
from analizador_pdf import consultas

config = utilidades.load_config('config.yaml')

utilidades.ensure_directories_exist(["datos/raws", "datos/textos", "datos/storage"])

options1 = ["gpt-3.5-turbo", "gpt-3.5-turbo", "llama3","gpt-4-turbo-2024-04-09","gpt-4"]
options2 = ["text-embedding-ada-002", "nomic-embed-text", "Option 3"]
options3 = ["ChromaDB", "Option 2", "Option 3"]

# Streamlit app ------------------------------------------------------------------
col1, col2 = st.columns([0.7,0.3],gap="large")

with col1:
    st.title("Analizador de PDF")

    selected_models = st.sidebar.selectbox("Elige el Modelo LLM:", options1,index=1, key="unique_modelo_llm_key")
    selected_embeddins = st.sidebar.selectbox("Elige el Modelo Embeddings:", options2,index=1, key="unique_embeddings_key")
    selected_option2 = st.sidebar.selectbox("Elige el Base Vectorial:", options3,index=1, key="unique_base_vectorial_key")


    #----- Modulo para subir archivos
    st.subheader("1. Subir Document al Sistema")
    uploaded_file = st.file_uploader("Subi tu archivo en formato PDF", type=["pdf","epub"])

    if uploaded_file is not None:
        file_name = utilidades.clean_filename(uploaded_file.name)
        

        if uploaded_file is not None:
            if uploaded_file.name.endswith('.epub'):
                nombre_temporal = 'temp.epub'
            elif uploaded_file.name.endswith('.pdf'):
                nombre_temporal = 'temp.pdf' 
        

        with open(nombre_temporal, "wb") as f:
            f.write(uploaded_file.read())

        # Copy the temporary PDF to the 'datos' folder
        copyfile(nombre_temporal, f"datos/raws/{file_name}")
        st.write("Documento successfully saved to datos folder.")

    #----- Modulo para mostrar los archivos en la carpeta

    st.subheader("2. Archivos en Sistema")

    file_list = os.listdir("datos/raws/")
    st.write('Archivos en  la carpeta:')
    for file_name in file_list:
        st.text(file_name)

    #----- Modulo para Pasar PDF a TXT

    st.subheader("3. Convertir Documents a TXT")

    # Button to analyze the PDF
    if st.button("Convertir Documentos a TXT"):
        document2texto.pdf2texto()
        document2texto.pub2texto()

    st.text("Archivos en formato texto")
    file_list = os.listdir("datos/textos/")
    st.write('Archivos en  la carpeta:')
    for file_name in file_list:
        st.text(file_name)


    #------ Seleccionar Documentos de Trabajo:

    main_folder = 'datos/textos'
    subfolders = [f.name for f in os.scandir(main_folder) if f.is_dir()]

    selected_folder = st.selectbox("Select a folder:", subfolders,key='select_folder_key')
    st.write(f"You selected: {selected_folder}")


    selected_folder_short_name = utilidades.validate_and_shorten_name(selected_folder)
    model_embedding_short_name = utilidades.validate_and_shorten_name(selected_embeddins)

    #------ Modulo pasar TXT a Vector
    if st.button("Convertir Documento a VECTOR"):
        texto2vector.init_and_save_vector( 
            input_dir=main_folder + '/' + selected_folder, 
            collection_name='collection' + selected_folder_short_name + model_embedding_short_name,
            index_id='index_id' + selected_folder_short_name  + model_embedding_short_name,
            model_name=selected_embeddins
            )
        st.text('Archivos cargados como Vector')


    #------ Modulo hacer consulta
    st.subheader('4. Hacer Consultas')

    user_input = st.text_input("Por favor, ingrese su consulta:")

    if st.button("Hacer Consultas"):
        if user_input:
            results = consultas.hacer_consulta(user_input,'collection' + selected_folder_short_name  + model_embedding_short_name,
                                                          'index_id'  + selected_folder_short_name  + model_embedding_short_name,
                                                          model_name=selected_models) 
            st.write(results.response)
            
            st.subheader('Las Fuentes')
            for index, item in enumerate(results.source_nodes): 
                st.subheader(index)
                st.write(item.node.text)
        else:        
            st.warning("Por favor, ingrese una consulta antes de presionar el botón.")

with col2:
    st.header('Metricas')

