from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def recursive_chunking(file_path, max_chunk_size, chunk_overlap):
    text = ""
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + " "

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["TITLE" ],
        chunk_size = max_chunk_size,
        chunk_overlap=chunk_overlap, # overlap chunk to mitigate loss of info
        length_function=len,
        is_separator_regex=False
    )

    chunks = text_splitter.split_text(text)
    return chunks

chunks = recursive_chunking('CELEX_32006L0054_EN_TXT.pdf', 50, 20)
with open('rec_chunked.txt', 'w') as output:
    for chunk in chunks:
        output.write('chunk: ' + ''.join(chunk) + '\n')
print(chunks)