"""
此脚本用于将旧照片生成pho读取的目录格式
"""
import os
import pathlib

import win32com.universal
from PIL import Image
import shutil
from datetime import datetime
import sys
from PIL.ExifTags import TAGS
from win32com.propsys import propsys, pscon
import win32timezone


# 判断文件是否在某一文件夹以下
def is_in_directory(file_path, directory):
    file_path = os.path.realpath(file_path)
    directory = os.path.realpath(directory)
    return os.path.commonprefix([file_path, directory]) == directory


def process_photos(folder_path):
    # 文件计数功能
    file_count_total: int = 0
    file_count: int = 0

    for _, _, files in os.walk(folder_path):
        for file in files:
            # 跳过不支持的文件
            if pathlib.Path(file).suffix not in supported_extensions:
                continue

            file_count_total += 1

    # 遍历每个文件或子文件夹
    for root, dirs, files in os.walk(photo_folder):
        for file in files:
            # 跳过不支持的文件
            if pathlib.Path(file).suffix not in supported_extensions:
                continue

            file_fullpath = os.path.join(root, file)

            if is_14_digit_timestamp(file):
                filename_newname = file[15:]

                os.rename(file_fullpath, os.path.join(root, filename_newname))
                file_count += 1
                print(f'[{int(file_count / file_count_total * 100)}%] Renamed {file_fullpath} to {os.path.join(root, filename_newname)}')


def is_14_digit_timestamp(s):
    # 举例：20250713052157_20250713_172154

    # 提取 _ 之前的部分 
    name_split_by_line = s.split('_')

    if len(name_split_by_line) <= 1:
        return False

    prefix = name_split_by_line[0]

    # 判断长度是否为14位
    if len(prefix) != 14 or not prefix.isdigit():
        return False

    # 尝试解析为 datetime 格式，即20250713052157
    try:
        datetime.strptime(prefix, '%Y%m%d%H%M%S')
        return True
    except ValueError:
        return False


# 获取自身文件路径
def self_path():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe 文件
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        # 如果是普通的 .py 文件
        return os.path.abspath(os.path.dirname(__file__))


# Pho 命名规则
print(
    '注：Pho 的命名规则要求在文件名称前增添时间戳，该程序用于删掉对应时间戳以恢复文件原名。')
print('名称示例：20250215082557_AAA.mp4 -> AAA.mp4')

# 定义支持的文件
supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.heic', '.mp4', '.dng']

# 定义照片文件夹和目标文件夹
photo_folder = self_path()  # 该py脚本所在路径
print('输入目录：%s' % photo_folder)

# 解除Pillow默认最大像素限制
Image.MAX_IMAGE_PIXELS = None

# 处理照片
process_photos(photo_folder)

print("恢复完成！")

input("按下 Enter 键退出程序...")
