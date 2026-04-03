from PyPDF2 import PdfReader
import nltk

nltk.download('punkt')

def sentence_chunking(file_path):
    text = ""
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + " "

    sentences = nltk.sent_tokenize(text.strip())
    return sentences

chunks = sentence_chunking('CELEX_32006L0054_EN_TXT.pdf')
i = 1

with open('output.txt', 'w') as output:
    for chunk in chunks:
        output.write('chunk: ' + str(i) + ' ' + ''.join(chunk) + '\n')
        i+= 1

print(chunks)