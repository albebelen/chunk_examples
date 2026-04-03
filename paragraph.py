from PyPDF2 import PdfReader

def paragraph_chunking(file_path):
    text = ""
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

    paragraphs = [p.strip() for p in text.split('Article') if p.strip]
    return paragraphs

chunks = paragraph_chunking('CELEX_32006L0054_EN_TXT.pdf') 
i = 1

with open('output.txt', 'w') as output:
    for chunk in chunks:
        output.write('chunk: ' + str(i) + ' ' + ''.join(chunk) + '\n')
        i+= 1

print(chunks)