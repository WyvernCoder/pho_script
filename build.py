"""
此脚本用于将旧照片生成pho读取的目录格式
"""
import os
import pathlib
from PIL import Image
import shutil
from datetime import datetime


# 判断文件是否在某一文件夹以下
def is_in_directory(file_path, directory):
    file_path = os.path.realpath(file_path)
    directory = os.path.realpath(directory)
    return os.path.commonprefix([file_path, directory]) == directory


# 获取目录下的总文件数量
def count_files_by_types(root_dir):
    count = 0

    for root, dirs, files in os.walk(root_dir):
        if is_in_directory(root, target_folder):
            continue

        for file in files:
            if file.lower().endswith(tuple(ext.lower() for ext in supported_extensions)):
                count += 1

    return count


def process_photos(folder_path, target_folder):
    # 获取文件夹中所有文件和子文件夹
    items = os.listdir(folder_path)

    # 计数支持
    total_files = count_files_by_types(photo_folder)
    file_count = 0

    # 遍历每个文件或子文件夹
    for item in items:
        item_path = os.path.join(folder_path, item)

        # 排除目标文件夹，避免重复整理
        if is_in_directory(item_path, target_folder):
            continue

        # 如果是文件夹，则递归处理子文件夹
        if os.path.isdir(item_path):
            process_photos(item_path, target_folder)
        else:
            # 增加计数器
            if pathlib.Path(item_path).suffix in supported_extensions:
                file_count += 1
            else:
                continue

            # 使用Pillow库打开图片并获取拍摄日期
            try:
                with Image.open(item_path) as img:
                    exif_data = img._getexif()
                    # 根据exif中的拍摄日期信息获取日期
                    if 36867 in exif_data:
                        date_str = exif_data[36867].strip().replace(" ", "")
                        # print("info:", date_str)
                        date_time = datetime.strptime(date_str, "%Y:%m:%d%H:%M:%S").date()
                    else:
                        date_time = datetime.fromtimestamp(os.path.getmtime(item_path)).date()
            except (AttributeError, KeyError, IndexError, OSError, TypeError):
                date_time = datetime.fromtimestamp(os.path.getmtime(item_path)).date()

            # 创建目标文件夹，如果不存在
            target_date_folder = os.path.join(target_folder, str(date_time.year), str(date_time.month).zfill(2),
                                              str(date_time.day).zfill(2))
            if not os.path.exists(target_date_folder):
                os.makedirs(target_date_folder)

            # 移动文件到目标文件夹
            dest_path = os.path.join(target_date_folder, item)
            shutil.move(item_path, dest_path)
            print('[%s%%] Moved %s' % (int(file_count/total_files * 100), dest_path))


# 获取自身文件路径
def self_path():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe 文件
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        # 如果是普通的 .py 文件
        return os.path.abspath(os.path.dirname(__file__))


# 定义支持的文件
supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.heic', '.mp4', '.dng']

# 定义照片文件夹和目标文件夹
photo_folder = self_path()  # 该py脚本所在路径
target_folder = "%s\\Completed" % photo_folder  # 该py脚本所在路径下的Completed文件夹
print('处理目录：%s' % target_folder)

# 解除Pillow默认最大像素限制
Image.MAX_IMAGE_PIXELS = None

# 处理照片
process_photos(photo_folder, target_folder)

print("分类完成！")

input("按下 Enter 键退出程序...")
