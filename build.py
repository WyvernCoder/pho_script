"""
此脚本用于将旧照片生成pho读取的目录格式
"""
import os
from PIL import Image
import shutil
from datetime import datetime

# 判断文件是否在某一文件夹以下
def is_in_directory(file_path, directory):
    file_path = os.path.realpath(file_path)
    directory = os.path.realpath(directory)
    return os.path.commonprefix([file_path, directory]) == directory

def process_photos(folder_path, target_folder):
    # 获取文件夹中所有文件和子文件夹
    items = os.listdir(folder_path)
    target_ext = ['jpg', 'jpeg', 'png', 'mp4', 'gif', 'dng']

    # 遍历每个文件或子文件夹
    for item in items:
        item_path = os.path.join(folder_path, item)
        
        # 排除目标文件夹，避免重复整理
        if is_in_directory(item_path, target_folder):
            continue
        
        # 扩展名黑名单
        if not os.path.isdir(item_path):
            if os.path.splitext(item)[1].removeprefix('.') not in target_ext:
                continue

        # 如果是文件夹，则递归处理子文件夹
        if os.path.isdir(item_path):
            process_photos(item_path, target_folder)
        else:
            # 使用Pillow库打开图片并获取拍摄日期
            try:
                with Image.open(item_path) as img:
                    exif_data = img._getexif()
                    # 根据exif中的拍摄日期信息获取日期
                    if 36867 in exif_data:
                        date_str = exif_data[36867].strip().replace(" ", "")
                        print("info:", date_str)
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
            shutil.move(item_path, os.path.join(target_date_folder, item))


# 定义照片文件夹和目标文件夹
photo_folder = os.path.dirname(os.path.abspath(__file__))   # 该py脚本所在路径
target_folder = "%s\\Completed" % photo_folder  # 该py脚本所在路径下的Completed文件夹

# 解除Pillow默认最大像素限制
Image.MAX_IMAGE_PIXELS = None

# 处理照片
process_photos(photo_folder, target_folder)

print("分类完成！")
