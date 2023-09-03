import os
import time
import json
import openai
import argparse


# proxy = {
#     'http': 'http://127.0.0.1:7890',
#     'https': 'http://127.0.0.1:7890'
# }

# openai.proxy = proxy

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def save2json(dataset, save_path):
    json_data = json.dumps(dataset, indent=4, ensure_ascii=False)
    with open(save_path, 'w', newline='\n') as wf:
        wf.write(json_data)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--api_key", default="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", type=str)
    parser.add_argument("--model_name", default="gpt-3.5-turbo", type=str)
    parser.add_argument("--prompt_path", default="prompt_v5.txt", type=str)
    parser.add_argument("--dialogues_path", default="", type=str)
    parser.add_argument("--completions_path", default="", type=str)

    args = parser.parse_args()

    openai.api_key = args.api_key
    model_name = args.model_name
    prompt_path = args.prompt_path
    dialogues_path = args.dialogues_path
    completions_path = args.completions_path

    existed_indexs = [int(i[:-5]) for i in os.listdir(completions_path)]
    existed_indexs.sort()
    print("existed_indexs:", existed_indexs)
    print("length of existed_indexs:", len(existed_indexs), '\n')

    prompt = read_txt_file(prompt_path)
    with open(dialogues_path, 'r') as rf:
        json_data = json.load(rf)
        print(json_data)
        if len(json_data) == len(existed_indexs):
            print("all dialogues have been cleaned and augmented\n")
            exit()
        for index in range(len(json_data)):
            print("processing:", index, "\n")
            if index in existed_indexs:
                print(index, "is existed", "\n")
                continue
            dialogue = str(json_data[index])
            chatgpt_input = prompt + '\n' + dialogue
            # print(chatgpt_input)
            # exit()
            try:
                completion = openai.ChatCompletion.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content":"现在需要你担任专业数据评分者的角色。我将提供一条指令微调数据，以JSON字符串的形式呈现。其中，'instruction'字段表示问题，'output'字段表示答案。你需要逐步仔细思考并评估数据的质量。每条数据的评分都需要附上相应的理由。"},
                            {"role": "user", "content": chatgpt_input}
                        ],
                        temperature=0
                )
                save_name = completions_path + '/' + str(index) + '.json'
                json_data[index]['revision'] = json.loads(completion['choices'][0]['message']['content'])
                json_data[index]['completion'] = completion
                save2json(json_data[index], save_name)
                print(index, "is saved", "\n")
            except Exception as e:
                print(e, "\n")
                continue


if __name__ == '__main__':
    main()
