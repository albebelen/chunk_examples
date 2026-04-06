from pageindex import PageIndexClient
import time
import json
import ollama

def page_index_chunking(file_path, prompt):
    pi_client = PageIndexClient(api_key="fb2363d435a94aa2b64dfef42c653ad0")

    result = pi_client.submit_document(file_path)
    doc_id = result["doc_id"]

    is_ready = False
    while is_ready != True:
        status = pi_client.get_document(doc_id)["status"]
        if status == 'completed':
            is_ready = True
        else:
            print('not ready yet...')

    tree = pi_client.get_tree(doc_id, node_summary=True)
    print('tree length: ' + str(len(tree)))
    res_list = tree.get("result")
    print('res length: ' + str(len(res_list)))

    #print("PageIndex Tree Structure; ", res_list)
    with open('tree_output.txt', 'w') as tree_output:
        nodes = res_list[0]['nodes']
        full_text = print_nodes(nodes)
        tree_output.write(full_text)

    #answer = send_ollama_prompt(tree, prompt)

    return tree

def print_nodes(nodes, text_to_add = ""):
    for i in nodes:
        text_to_add.append('node_id:' + i['node_id'] + '\n')
        text_to_add.append('text:' + i['text'] + '\n')

        if i['nodes'] and len(i['nodes']) > 0:
            print_nodes(i[nodes], text_to_add)
    return text_to_add


def send_ollama_prompt(tree, prompt, model_name='llama3.2'):

    complete_prompt = "Using this document tree, return the node_ids needed to answer: " + prompt + f"\nTree: {json.dumps(tree)}"

    response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': complete_prompt}]
    )

    answer = response['message']['content'].strip()

    with open('answer.txt', 'w') as answer_output:
        answer_output.write(answer)

    return answer

resp = page_index_chunking('CELEX_32006L0054_EN_TXT.pdf', 'What are the equal opportunity rules?')

    