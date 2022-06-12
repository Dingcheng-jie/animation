import os
from PIL import Image
import glob
img_path = glob.glob("datasets/SummerWar/train/*.jpg") 
path_save = "datasets/SummerWar/train_256"
for file in img_path:
    img = Image.open(file)    #打开文件
    name=os.path.basename(file)
    new_img=img.resize((256,256))  #进行大小分辨率修改
    new_img.save(path_save+'/'+name)    #修改并保存图片
#     print(path_save+'/'+name)
    print(name+"修改成功")