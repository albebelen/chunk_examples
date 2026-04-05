from PyPDF2 import PdfReader

def sliding_window_chunking(file_path, window_size = 1000, step_size = 500):
    text = ""
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content.replace('\n', ' ')

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

chunks = sliding_window_chunking('CELEX_32006L0054_EN_TXT.pdf') 

i = 1

with open('output.txt', 'w') as output:
    for chunk in chunks:
        output.write('chunk ' + str(i) + ' : ' + chunk + '\n')
        i+= 1

print(chunks)