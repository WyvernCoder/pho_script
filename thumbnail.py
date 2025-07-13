"""
此脚本用于将旧照片生成pho读取的缩略图
"""
import os
import pathlib
import sys

import rawpy
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener
from datetime import datetime
from moviepy import VideoFileClip


# 获取目录下的总文件数量
def count_files_by_types(root_dir):
    count = 0
    for root, _, files in os.walk(root_dir):
        if ".thumbnail" in root:
            continue

        for file in files:
            if file.lower().endswith(tuple(ext.lower() for ext in supported_extensions)):
                count += 1

    return count


# 获取照片的拍摄日期
def get_img_datatime(file_path):
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            # 根据exif中的拍摄日期信息获取日期
            if 36867 in exif_data:
                date_str = exif_data[36867].strip().replace(" ", "")
                # print("info:",date_str)
                date_time = datetime.strptime(date_str, "%Y:%m:%d%H:%M:%S").date()
            else:
                # 如果获取不到则获取照片的最后修改日期
                date_time = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
    except (AttributeError, KeyError, IndexError, OSError, TypeError):
        # 如果获取不到则获取照片的最后修改日期
        date_time = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
    return date_time


def generate_thumbnail(photo_folder, thumbnail_size=(200, 200)):
    # 为 Pillow 启动 heic 图片格式支持
    register_heif_opener()

    # 计数支持
    total_files = count_files_by_types(photo_folder)
    file_count = 0

    # 遍历文件夹中的每个日期文件夹
    for root, dirs, files in os.walk(photo_folder):
        # 过滤缩略图文件夹不处理
        if ".thumbnail" in root:
            continue

        for file in files:
            # 增加计数器
            if pathlib.Path(os.path.join(root, file)).suffix in supported_extensions:
                file_count += 1

            # 获取图片文件路径
            file_path = os.path.join(root, file)

            # 获取照片的拍摄日期
            date_time = get_img_datatime(file_path)

            # 生成缩略图的文件夹路径
            thumbnail_folder = os.path.join(photo_folder, ".thumbnail", str(date_time.year),
                                            str(date_time.month).zfill(2), str(date_time.day).zfill(2))
            if not os.path.exists(thumbnail_folder):
                os.makedirs(thumbnail_folder)
            # 缩略图照片的路径
            thumbnail_path = os.path.join(thumbnail_folder, file)

            # 将缩略图路径的后缀设置为 jpg 用于 Pillow 生成缩略图。
            # 否则在生成 mp4 等格式缩略图时， Pillow 会抛出异常。 
            thumbnail_path_jpg = pathlib.Path(thumbnail_path).with_suffix(".jpg")

            # 缩略图存在则跳过不处理 
            if use_jpg_extension:
                if os.path.exists(thumbnail_path_jpg):
                    print('[%s%%] Exists %s' % (int(file_count / total_files * 100), thumbnail_path_jpg))
                    continue
            else:
                if os.path.exists(thumbnail_path):
                    print('[%s%%] Exists %s' % (int(file_count / total_files * 100), thumbnail_path))
                    continue

            # 处理常见图片文件
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # 生成缩略图并保存
                try:
                    with Image.open(file_path) as img:
                        img = ImageOps.exif_transpose(img)
                        img.thumbnail(thumbnail_size)
                        img = img.convert("RGB")
                        img.save(thumbnail_path_jpg)
                        if not use_jpg_extension:
                            os.rename(thumbnail_path_jpg, thumbnail_path)   # 将 jpg 格式的缩略图改回原名，以适配 Pho 的命名格式。
                            print('[%s%%] Created %s' % (int(file_count / total_files * 100), thumbnail_path))
                        else:
                            print('[%s%%] Created %s' % (int(file_count / total_files * 100), thumbnail_path_jpg))
                except OSError as e:
                    print(f"Error processing {file}: {e}")

            # 处理 heic 图片文件
            if file.lower().endswith('.heic'):
                # 生成缩略图并保存
                try:
                    with Image.open(file_path) as img:
                        img = ImageOps.exif_transpose(img)
                        img.thumbnail(thumbnail_size)
                        img = img.convert("RGB")
                        img.save(thumbnail_path_jpg)
                        if not use_jpg_extension:
                            os.rename(thumbnail_path_jpg, thumbnail_path)   # 将 jpg 格式的缩略图改回原名，以适配 Pho 的命名格式。
                            print('[%s%%] Created %s' % (int(file_count / total_files * 100), thumbnail_path))
                        else:
                            print('[%s%%] Created %s' % (int(file_count / total_files * 100), thumbnail_path_jpg))
                except OSError as e:
                    print(f"Error processing {file}: {e}")

            # 处理视频文件
            if file.lower().endswith('.mp4'):
                # 生成缩略图并保存
                try:
                    with VideoFileClip(file_path) as clip:
                        frame = clip.get_frame(clip.duration / 2)
                        img = Image.fromarray(frame)
                        img.thumbnail(thumbnail_size)
                        img = img.convert("RGB")
                        img.save(thumbnail_path_jpg)
                        if not use_jpg_extension:
                            os.rename(thumbnail_path_jpg, thumbnail_path)   # 将 jpg 格式的缩略图改回原名，以适配 Pho 的命名格式。
                            print('[%s%%] Created %s' % (int(file_count / total_files * 100), thumbnail_path))
                        else:
                            print('[%s%%] Created %s' % (int(file_count / total_files * 100), thumbnail_path_jpg))
                except OSError as e:
                    print(f"Error processing {file}: {e}")

            # 处理常见图片文件
            if file.lower().endswith('dng'):
                # 生成缩略图并保存
                try:
                    with rawpy.imread(file_path) as raw:
                        standard_rgb = raw.postprocess(use_camera_wb=True)
                        img = Image.fromarray(standard_rgb)
                        img.thumbnail(thumbnail_size)
                        img = img.convert("RGB")
                        img.save(thumbnail_path_jpg)
                        if not use_jpg_extension:
                            os.rename(thumbnail_path_jpg, thumbnail_path)   # 将 jpg 格式的缩略图改回原名，以适配 Pho 的命名格式。
                            print('[%s%%] Created %s' % (int(file_count / total_files * 100), thumbnail_path))
                        else:
                            print('[%s%%] Created %s' % (int(file_count / total_files * 100), thumbnail_path_jpg))
                except OSError as e:
                    print(f"Error processing {file}: {e}")


# 获取自身文件路径
def self_path():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe 文件
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        # 如果是普通的 .py 文件
        return os.path.abspath(os.path.dirname(__file__))


# Pho 缩略图后缀设置
print('注：Pho 要求缩略图的名称和扩展名与原图完全一样，因此以下可能会输出视频或其他非 jpg 格式的缩略图。这些缩略图实为 jpg 改后缀而成。')
use_jpg_extension = False

# 定义支持的文件
supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.heic', '.mp4', '.dng']

# 定义照片文件夹和缩略图尺寸
photo_folder = os.path.join(self_path(), "Completed")
print('处理目录：%s' % photo_folder)

# 找不到 Completed 输出目录时则询问是否用当前目录代替。
if not os.path.exists(photo_folder):
    answer = input('未找到 Completed 输出目录，是否使用当前目录继续？(y/n): ').lower()
    if answer == 'y':
        photo_folder = self_path()
        print('更正处理目录：%s' % photo_folder)

# 解除Pillow默认最大像素限制
Image.MAX_IMAGE_PIXELS = None

# 生成缩略图
generate_thumbnail(photo_folder)

print("缩略图生成完成！")

input("按下 Enter 键退出程序...")
