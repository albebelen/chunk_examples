## use recursive chunking to "clean" file
## give clean file to semantic
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader 
from fpdf import FPDF

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

clean_file = recursive_chunking('CELEX_32006L0054_IT_TXT.pdf', 50, 20)
doc_chunked = semantic_chunking(clean_file)

i = 1

with open('hybrid_output.txt', 'w') as output:
    for chunk in doc_chunked:
        output.write('chunk ' + str(i) + ' : ' + chunk.page_content + '\n')
        i+= 1

pdf = FPDF()   
pdf.add_page()
pdf.set_font("Arial", size = 15)

f = open("hybrid_output.txt", "r")
for x in f:
    pdf.cell(200, 10, txt = x, ln = 1, align = 'C')

pdf.output("hybrid_output.pdf")  