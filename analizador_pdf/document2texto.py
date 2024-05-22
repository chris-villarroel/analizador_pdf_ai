from langchain.document_loaders import PyPDFLoader
import os
from langchain_community.document_loaders import UnstructuredEPubLoader

def pdf2texto():
    input_dir = "datos/raws/"
    output_dir = "datos/textos/"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Loop through each file in the input directory
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        
        # Check if it's a file and has a .pdf extension
        if os.path.isfile(filepath) and filepath.lower().endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            documents = loader.load_and_split()
            
            print(f"Loaded {len(documents)} documents from {filename}")
            
            # Create a valid folder name
            folder_name = ''.join([char if char.isalpha() or char == ' ' else '_' for char in filename]).replace(' ', '_').replace('.pdf', '')
            pdf_output_dir = os.path.join(output_dir, folder_name)
            
            # Ensure PDF-specific output directory exists
            os.makedirs(pdf_output_dir, exist_ok=True)
            
            for i, document in enumerate(documents):
                output_filepath = os.path.join(pdf_output_dir, f"{folder_name}_{i}.txt")
                
                # Save document content as plain text
                with open(output_filepath, "w") as outfile:
                    outfile.write(document.page_content)


 
def pub2texto():
    input_dir = "datos/epub/"
    output_dir = "datos/textos/"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Loop through each file in the input directory
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        
        # Check if it's a file and has a .pdf extension
        if os.path.isfile(filepath) and filepath.lower().endswith(".epub"):
            loader = UnstructuredEPubLoader(filepath)
            documents = loader.load_and_split()
            
            print(f"Loaded {len(documents)} documents from {filename}")
            
            # Create a valid folder name
            folder_name = ''.join([char if char.isalpha() or char == ' ' else '_' for char in filename]).replace(' ', '_').replace('.pdf', '')
            pdf_output_dir = os.path.join(output_dir, folder_name)
            
            # Ensure PDF-specific output directory exists
            os.makedirs(pdf_output_dir, exist_ok=True)
            
            for i, document in enumerate(documents):
                output_filepath = os.path.join(pdf_output_dir, f"{folder_name}_{i}.txt")
                
                # Save document content as plain text
                with open(output_filepath, "w") as outfile:
                    outfile.write(document.page_content)                   