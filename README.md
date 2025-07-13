# ![store_check (Custom)](https://github.com/user-attachments/assets/e34ec6ea-de4b-450e-873f-981c317dff82) 介绍
此脚本用于将旧照片转换成相册软件 [Pho](https://github.com/fregie/pho) 所支持读取的文件夹结构，也可用于按下列文件结构整理自己的文件而不用于 Pho 软件。
  
缩略图生成仅支持以下类型的媒体格式：  
```
['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.heic', '.mp4', '.dng']
```
  

# ![store_backpack_bg_highlight (Custom)](https://github.com/user-attachments/assets/3e2e7008-920a-491a-96cb-4d8ba24d8811) 使用步骤  
1. 将2个脚本放入带有照片的文件夹中。
2. 运行 build.py (或 PhoStructBuilder.exe)，该脚本会把照片按下列文件结构进行分类，无论照片是否位于子文件夹中都会被处理。
3. 运行 thumbnail.py (或 PhoThumbGenerator.exe)，该脚本会为上一步分类好的照片生成缩略图，所有缩略图均会位于 .thumbnail 文件夹中。

注：14位时间戳前缀是 Pho 软件的命名规则。根据实际测试来看，Pho 软件并不会遵守其 README.md 中声明的文件结构。
如果你不想要14位时间戳前缀而只达成整理文件的目的，只需修改源码中 use_pho_standard 为 False 即可。
如果你想批量删掉14位时间戳，运行 PhoStructRestore.exe 即可。
```
Completed # 默认情况下，build.py 脚本会自动在当前目录创建 Completed 文件夹并将照片剪切进该文件夹并为其添加14位时间戳前缀。
│
├─2018
│  └─11
│      ├─18
│      │      20250215082557_IMG_20181118_225848_HDR.jpg
│      │
│      └─17
│             20250215082557_IMG_20181117_235245_HDR.jpg
│             20250215082557_20181117_171711_HDR.mp4
│
└─.thumbnail # 缩略图文件夹，由 thumbnail.py 脚本创建。
    └─2018
        └─11
            ├─18
            │      20250215082557_IMG_20181118_225848_HDR.jpg
            │
            └─17
                   20250215082557_IMG_20181117_235245_HDR.jpg
                   20250215082557_20181117_171711_HDR.mp4
```

# ![invited (Custom)](https://github.com/user-attachments/assets/049e62f1-8acd-4d58-9082-95a8701fe39b) 截图  
<img width="991.5" height="548.5" alt="image" src="https://github.com/user-attachments/assets/0fbd2708-d374-4000-911f-a125344cdf57" />  
<img width="994" height="550" alt="image" src="https://github.com/user-attachments/assets/c6394a01-f955-4a85-81e5-e428daf582c6" />
