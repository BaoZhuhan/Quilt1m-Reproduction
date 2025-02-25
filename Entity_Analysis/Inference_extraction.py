import os
from openai import OpenAI


client = OpenAI(
    base_url='https://xiaoai.plus/v1',
    api_key='sk-yX1hmgEAxRq54Ck6n6ZIzRApwBoW4U8Lz3i5DUbnRLr0m8Wz'
)

# 获取 'Test' 目录及其子目录下的所有 .txt 文件
Origin_path = 'Test'
for root, dirs, files in os.walk(Origin_path):
    for file_name in files:
        # 只处理 .txt 文件
        if file_name.endswith('.txt'):
            file_path = os.path.join(root, file_name)

            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as input_file:
                test_lines = input_file.readlines()

            # 创建结果文件路径
            result_file_path = os.path.join(root, f"{file_name}_result.txt")

            # 打开 result.txt 文件以写入因果关系句子
            with open(result_file_path, 'w', encoding='utf-8') as output_file:
                for line in test_lines:
                    line = line.strip()  # 去掉每行的多余空白
                    if line:  #不是空行
                        # 修改的输入示例
                        prt = f"请从以下句子中提取因果关系或推断其中的逻辑：\n{line}\n"

                        # 获取回答
                        completion = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prt}]
                        )

                        ai_response = completion.choices[0].message.content  # 获取 AI 的回答内容

                        # 写入 result.txt 文件
                        output_file.write(f" {ai_response}\n\n")

            # 打印流程
            print(f"文件 {file_name} 处理完成，结果已保存到 {result_file_path} 文件中。")

print("所有文件处理完成！")
