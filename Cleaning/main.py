import os
import csv
import sys

# 定义视频路径和旧数据、新数据的路径
VIDEOS_PATH = "/home/bzh/Repos/quilt1m/data/quilt/videos"
OLD_QUILT_DATA_PATH = "/home/bzh/Repos/quilt1m/cleaning/old_data/quilt_data.csv"
OLD_QUILT_RECON_PATH = "/home/bzh/Repos/quilt1m/cleaning/old_data/quilt_recon.csv"
NEW_QUILT_DATA_PATH = "/home/bzh/Repos/quilt1m/data/quilt/quilt_data.csv"
NEW_QUILT_RECON_PATH = "/home/bzh/Repos/quilt1m/data/quilt/quilt_recon.csv"

# 获取视频名称列表
def get_video_names(path):
    videos_name = []
    for root, dirs, files in os.walk(path):  # 遍历目录
        for dir_name in dirs:  # 获取所有目录名
            videos_name.append(dir_name)
    return videos_name

# 过滤并保存数据
def filter_and_save_data_QUILT_DATA(old_path, new_path, videos_name, index=1):
    if not os.path.exists(old_path):  # 检查旧文件是否存在
        print(f"Error: {old_path} does not exist.")
        return
    csv.field_size_limit(sys.maxsize)  # 设置CSV字段大小限制
    with open(old_path, mode='r', newline='', encoding='utf-8') as old_file:
        reader = csv.DictReader(old_file)  # 读取旧CSV文件
        fieldnames = reader.fieldnames  # 获取字段名
        with open(new_path, mode='w', newline='', encoding='utf-8') as new_file:
            writer = csv.DictWriter(new_file, fieldnames=fieldnames)  # 写入新CSV文件
            writer.writeheader()  # 写入表头
            row_number = 0
            for row in reader:
                if row[fieldnames[index]] in videos_name:  # 过滤符合条件的行
                    row[fieldnames[0]] = row_number  # 更新行号
                    row_number += 1
                    writer.writerow(row)  # 写入新文件

def filter_and_save_data_QUILT_RECON(old_path, new_path, videos_name, index=1):
    if not os.path.exists(old_path):  # 检查旧文件是否存在
        print(f"Error: {old_path} does not exist.")
        return
    csv.field_size_limit(sys.maxsize)  # 设置CSV字段大小限制
    with open(old_path, mode='r', newline='', encoding='utf-8') as old_file:
        reader = csv.DictReader(old_file)  # 读取旧CSV文件
        fieldnames = reader.fieldnames  # 获取字段名
        with open(new_path, mode='w', newline='', encoding='utf-8') as new_file:
            writer = csv.DictWriter(new_file, fieldnames=fieldnames)  # 写入新CSV文件
            writer.writeheader()  # 写入表头
            row_number = 0
            for row in reader:
                if row[fieldnames[index]] in videos_name:  # 过滤符合条件的行
                    row[fieldnames[0]] = row_number  # 更新行号
                    row_number += 1
                    # 处理key_frame_times和predictions字段
                    row['key_frame_times'] = row['key_frame_times'].replace('[', '').replace(']', '')
                    row['predictions'] = row['predictions'].replace('[', '').replace(']', '')
                    writer.writerow(row)  # 写入新文件

if __name__ == "__main__":
    if not os.path.exists(OLD_QUILT_DATA_PATH) or not os.path.exists(OLD_QUILT_RECON_PATH):
        print("Error: One or both of the old CSV files do not exist.")  # 检查旧CSV文件是否存在
    else:
        videos_name = get_video_names(VIDEOS_PATH)  # 获取视频名称列表
        filter_and_save_data_QUILT_DATA(OLD_QUILT_DATA_PATH, NEW_QUILT_DATA_PATH, videos_name, 1)  # 过滤并保存数据
        filter_and_save_data_QUILT_RECON(OLD_QUILT_RECON_PATH, NEW_QUILT_RECON_PATH, videos_name, 0)  # 过滤并保存数据
        print("Done!")  # 完成
