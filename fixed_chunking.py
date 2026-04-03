from PyPDF2 import PdfReader

def fixed_size_chunking(file_path, chunk_size=1000, overlap=100):
    text = ""
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + " "

    print('text: ' + text)

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

my_chunks = fixed_size_chunking('CELEX_32006L0054_EN_TXT.pdf', chunk_size=500, overlap=50)
print(f'Created {len(my_chunks)} chunks.')

for chunk in my_chunks:
    print(chunk + "\n")
