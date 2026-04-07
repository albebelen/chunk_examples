from langchain_experimental.text_splitter import SemanticChunker
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
import ollama
from PyPDF2 import PdfReader 

def semantic_chunking(file_path, model="llama3.2"):
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    embeddings = OllamaEmbeddings(model=model)

    text_splitter = SemanticChunker(
        embeddings, 
        breakpoint_threshold_type="percentile"
    )
    
    docs = text_splitter.create_documents([text])

    print(f"number of chunks: {len(docs)}\n")
    
    return docs 

chunks = semantic_chunking("CELEX_32006L0054_IT_TXT.pdf")
i = 1
with open('output.txt', 'w') as output:
    for chunk in chunks:
        output.write('chunk ' + str(i) + ' : ' + chunk.page_content + '\n')
        i+= 1