## use semantic then sliding

from PyPDF2 import PdfReader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings

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

def sliding_window_chunking(file_path, window_size = 1000, step_size = 500):
    text = ""
    
    with open(file_path, 'r') as file:
        text = file.read()

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + window_size
        chunk = text[start:end]
        chunks.append(chunk.strip())

        start += step_size

        if start >= text_len - (window_size // 4):
            break

    return chunks

#window_chunk = sliding_window_chunking('CELEX_32006L0054_IT_TXT.pdf')
docs_chunked = semantic_chunking('CELEX_32006L0054_IT_TXT.pdf')

with open('semantic_sliding_output.txt', 'w') as output:
    for chunk in docs_chunked:
        output.write(chunk.page_content + '\n\n')

window_chunk = sliding_window_chunking('semantic_sliding_output.txt')
i = 1

with open('sliding_output.txt', 'w') as output:
    for chunk in window_chunk:
        output.write('chunk ' + str(i) + ' : ' + chunk + '\n')
        i+= 1