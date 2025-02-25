import os
import sys
from moviepy import VideoFileClip, ImageSequenceClip

def convert_to_mp4(input_file, output_file, fps=30):
    """
    将输入的 .webm 或 .mkv 文件转换为 .mp4 格式。
    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    :param fps: 帧率（默认30）
    """
    # 获取文件的扩展名
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension == ".webp":
        # 如果是 .webp 文件
        print(f"正在转换 {input_file} 为 .mp4 格式...")
        clip = ImageSequenceClip([input_file], fps=fps)  # 使用帧率
        clip.write_videofile(output_file, codec="libx264", fps=fps)
    elif file_extension in [".mkv", ".webm"]:
        # 如果是 .mkv 或 .webm 文件，直接读取并保存为 .mp4
        print(f"正在转换 {input_file} 为 .mp4 格式...")
        clip = VideoFileClip(input_file)
        clip.write_videofile(output_file, codec="libx264")
    else:
        print(f"不支持的文件格式: {file_extension}. 请提供 .webm 或 .mkv 文件。")




if len(sys.argv) == 3 and sys.argv[1] == '-n':
    input_file = sys.argv[2]
    output_file = os.path.splitext(input_file)[0] + '.mp4'
    convert_to_mp4(input_file, output_file)
else:
    print("Usage: python trans.py -n <file>")
