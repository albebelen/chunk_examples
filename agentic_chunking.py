import ollama
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def agentic_pdf_chunker(file_path, model_name="llama3.2"):
    reader = PdfReader(file_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    mini_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)
    mini_chunks = mini_splitter.split_text(text)
    
    final_chunks = []
    current_chunk = mini_chunks[0]


    for i in range(1, len(mini_chunks)):
        next_mini = mini_chunks[i]
        
        prompt = (
            f"Current Content: {current_chunk}\n\n"
            f"Next Sentence: {next_mini}\n\n"
            "Does the 'Next Sentence' continue the exact same legal topic or Article as the 'Current Content'? "
            "Respond with 'YES' to merge them or 'NO' to start a new chunk. Answer ONLY with YES or NO."
        )
        
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        decision = response['message']['content'].strip().upper()
        
        if "YES" in decision:
            current_chunk += " " + next_mini
        else:
            final_chunks.append(current_chunk)
            current_chunk = next_mini

    final_chunks.append(current_chunk)
    return final_chunks

chunks = agentic_pdf_chunker('CELEX_32006L0054_EN_TXT.pdf') 
i = 1

with open('output.txt', 'w') as output:
    for chunk in chunks:
        output.write('chunk ' + str(i) + ' : ' + chunk + '\n')
        i+= 1

print(chunks)
