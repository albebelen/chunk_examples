from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama 

def context_enriched_chunking(file_path, model_name="llama3.2"):
    text = ""
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    base_chunks = text_splitter.split_text(text)

    enriched_chunks = []

    for i, chunk in enumerate(base_chunks):
        prompt = (f"Here is a chunk from an EU Directive:\n\n{chunk}\n\n"
            "Provide a 1-sentence succinct context to situate this chunk within the "
            "overall document to improve search retrieval. Return ONLY the context.")

        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}]
        )

        context_summary = response['message']['content'].strip()
        enriched_content = f"CONTEXT: {context_summary}\n\nContent: {chunk}"
        enriched_chunks.append(enriched_content)

    return enriched_chunks

chunks = context_enriched_chunking('CELEX_32006L0054_EN_TXT.pdf') 
i = 1

with open('output.txt', 'w') as output:
    for chunk in chunks:
        output.write('chunk ' + str(i) + ' : ' + chunk + '\n')
        i+= 1

print(chunks)