# 介绍
此脚本用于将旧照片转换成相册软件 [Pho](https://github.com/fregie/pho) 所支持读取的文件夹结构，也可用于按下列文件结构整理自己的文件而不用于 Pho 软件。
  
缩略图生成仅支持以下类型的媒体格式：  
```
['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.heic', '.mp4', '.dng']
```
  

# 使用步骤  
1. 将2个脚本放入带有照片的文件夹中。
2. 运行 build.py (或 PhoStructBuilder.exe)，该脚本会把照片按下列文件结构进行分类，无论照片是否位于子文件夹中都会被处理。
3. 运行 thumbnail.py (或 PhoThumbGenerator.exe)，该脚本会为上一步分类好的照片生成缩略图，所有缩略图均会位于 .thumbnail 文件夹中。
  
```
Completed # 默认情况下，build.py 脚本会自动在当前目录创建 Completed 文件夹并将照片剪切进该文件夹中。
│
├─2018
│  └─11
│      ├─18
│      │      IMG_20181118_225848_HDR.jpg
│      │
│      └─17
│             IMG_20181117_235245_HDR.jpg
│             IMG_20181117_171711_HDR.jpg
│
└─.thumbnail # 缩略图文件夹，由 thumbnail.py 脚本创建。
    └─2018
        └─11
            ├─18
            │      IMG_20181118_225848_HDR.jpg
            │
            └─17
                   IMG_20181117_235245_HDR.jpg
                   IMG_20181117_171711_HDR.jpg
```

# 截图  
<img width="991.5" height="548.5" alt="image" src="https://github.com/user-attachments/assets/0fbd2708-d374-4000-911f-a125344cdf57" />  
<img width="994" height="550" alt="image" src="https://github.com/user-attachments/assets/c6394a01-f955-4a85-81e5-e428daf582c6" />
