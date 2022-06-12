from PIL import Image
 
def join(jpg1, jpg2):
    img1, img2 = Image.open(jpg1), Image.open(jpg2)
    size1, size2 = img1.size, img2.size
    joint = Image.new('RGB', (size1[0] + size2[0], size1[1]))
    loc1, loc2 = (0, 0), (size1[0], 0)
    joint.paste(img1, loc1)
    joint.paste(img2, loc2)
    joint.save('samples/compare/face_paint_512_v0.jpg')
 
 
if __name__ == '__main__':
    # 两张图片地址：
    png1 = "samples/inputs/1.jpg"
    png2 = "samples/outputs/1.jpg"
    # 横向拼接
    join(png1, png2)

