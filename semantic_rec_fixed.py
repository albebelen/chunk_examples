## use recursive chunking to "clean" file
## give clean file to semantic
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader 

def recursive_chunking(file_path, max_chunk_size, chunk_overlap):
    text = ""
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + " "

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["TITOLO"],
        chunk_size = max_chunk_size,
        chunk_overlap=chunk_overlap, # overlap chunk to mitigate loss of info
        length_function=len,
        is_separator_regex=False
    )

    chunks = text_splitter.split_text(text)
    path_chunked_file = 'chunked_file.txt'
    with open(path_chunked_file, 'w') as output:
        for chunk in chunks:
            output.write(''.join(chunk) + '\n\n')

    return path_chunked_file

def semantic_chunking(file_path, model="llama3.2"):
    
    with open(file_path, 'r') as file:
        # reader = PdfReader(file)
        # text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        text = file.read()

    embeddings = OllamaEmbeddings(model=model)

    text_splitter = SemanticChunker(
        embeddings, 
        breakpoint_threshold_type="percentile"
    )
    
    docs = text_splitter.create_documents([text])

    print(f"number of chunks: {len(docs)}\n")
    
    return docs

def fixed_size_chunking(file_path, chunk_size=1000, overlap=100):
    text = ""
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])


    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        # Move start forward, but subtract overlap to keep context
        start += (chunk_size - overlap)
        print(chunk)

    return chunks

clean_file = recursive_chunking('CELEX_32006L0054_IT_TXT.pdf', 50, 20)
doc_chunked = semantic_chunking(clean_file)

i = 1

with open('hybrid_output.txt', 'w') as output:
    for chunk in doc_chunked:
        output.write('chunk ' + str(i) + ' : ' + chunk.page_content + '\n')
        i+= 1
        
fixed_chunks = fixed_size_chunking('hybrid_output.txt', chunk_size=500, overlap=50)
i = 1
with open('fixed_hybrid_output.txt', 'w') as output:
    for chunk in fixed_chunks:
        output.write('chunk ' + str(i) + ' : ' + chunk.page_content + '\n')
        i+= 1
        

