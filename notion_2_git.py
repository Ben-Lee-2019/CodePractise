import os
import shutil
import pandas as pd
from urllib import parse


def rename_notion(notion_path):
    for filename in os.listdir(notion_path):
        if filename.startswith(".") :
            continue
        
        full_path = os.path.join(notion_path, filename)

        if filename.endswith(".md"):
            new_filename = filename[:-36] + ".md"
        elif filename.endswith(".csv"):
            new_filename = filename[:-37] + ".csv"
        else:
            new_filename = filename[:-33]
        new_full_path = os.path.join(notion_path, new_filename)
        os.rename(full_path, new_full_path)


def rename_problem(problem_path):
    # 获取所有md文档的奇怪后缀，保存到map中，用于替换md中的图片路径
    dic = {}

    # 这里将奇怪后缀去掉
    for filename in os.listdir(problem_path):
        if filename.startswith(".") :
            continue
        full_path = os.path.join(problem_path, filename)

        if filename.endswith(".md"):
            new_filename = filename[:-36] + ".md"
            replace_content = filename[-35:-3]
            dic[new_filename] = '%20' + replace_content
        else:
            new_filename = filename[:-33]
        new_full_path = os.path.join(problem_path, new_filename)
        os.rename(full_path, new_full_path)

    # 读取文件夹中的markdown格式文档，如果文档中有数据包含集合A中的32位字符串，将其去掉
    for filename in os.listdir(problem_path):
        if filename.endswith(".md"):  # 仅处理markdown格式文档
            file_path = os.path.join(problem_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                ## 将 xxx/png 替换成 image/xxx/png ,xxx中文做了url encode 需要处理一下
                filename_prefix = parse.quote(filename.replace(".md",""))
                re = filename_prefix + dic[filename]
                content = content.replace(re, 'image/'+ filename_prefix)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)


def move_tag(path, csv_path, git_path):
    ## 将csv中的数据解析成  question:tag的形式

    df = pd.read_csv(csv_path, encoding='utf-8')
    data_dict = df.set_index('Problems')['Tag'].to_dict()

    for key, value in data_dict.items():
        # question 带了一个. 需要去掉
        key = key.replace('.', '')


        tags = value.split(",")
        for tag in tags:
            tag = tag.strip()
            source_path = os.path.join(path, key)

            target_path = os.path.join(git_path, tag)

            ## 目标文件夹不存在就创建
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            ## 不是所有的都有题解
            ## 目标路径是 git/solution/dp/image/"problems"/png
            if os.path.exists(source_path):
                shutil.copytree(source_path, os.path.join(target_path, "image/" + key), dirs_exist_ok=True)

            source_path = source_path + ".md"
            if os.path.exists(source_path):
                shutil.copy(source_path, target_path)


if __name__ == '__main__':

    ## notion 的第一层路径
    parent_path = 'notion/Leetcode review a960419385cc48ccbfd847dd9cb34280'
    ## problem 的路径
    problem_path = parent_path + "/Problem(总）"
    ## 题目csv文件的路径
    problem_csv = parent_path + "/Problem(总）.csv"
    ## git文件夹的路径
    git_folder_path = "/Users/xx/Documents/GitHub/CodePractise/solution"


    ## 将最上层文件重命名
    rename_notion(parent_path)
    ## 重命名题目
    rename_problem(problem_path)
    ## 将题解md文档移动到对应的git文件夹中
    move_tag(problem_path, problem_csv, git_folder_path)

    shutil.copy(os.path.join(parent_path, "注意点.md"), git_folder_path)
