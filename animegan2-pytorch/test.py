import os
import argparse

from PIL import Image
import numpy as np

import torch
from torchvision.transforms.functional import to_tensor, to_pil_image

from model import Generator


torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

def join(jpg1, jpg2):
    img1, img2 = Image.open(jpg1), Image.open(jpg2)
    size1, size2 = img1.size, img2.size
    joint = Image.new('RGB', (size1[0] + size2[0], size1[1]))
    loc1, loc2 = (0, 0), (size1[0], 0)
    joint.paste(img1, loc1)
    joint.paste(img2, loc2)
#     joint.save('samples/compare/face_paint_512_v0.jpg')
    joint.save('samples/compare/'+os.path.basename(args.checkpoint).split('.')[0]+'.jpg')

def load_image(image_path, x32=False):
    img = Image.open(image_path).convert("RGB")

    if x32:
        def to_32s(x):
            return 256 if x < 256 else x - x % 32
        w, h = img.size
        img = img.resize((to_32s(w), to_32s(h)))

    return img


def test(args):
    print(args)
    device = args.device
    input_file=args.input_file
#     input_path=os.path.dirname(input_file) 
    net = Generator()
    net.load_state_dict(torch.load(args.checkpoint, map_location="cpu"))
    net.to(device).eval()
    print(f"model loaded: {args.checkpoint}")
    
#     os.makedirs(input_path, exist_ok=True)
    
    if os.path.splitext(input_file)[-1].lower() in [".jpg", ".png", ".bmp", ".tiff"]:
        image = load_image(input_file, args.x32)
        image_name=os.path.basename(input_file)
        print(image_name)
        with torch.no_grad():
            image = to_tensor(image).unsqueeze(0) * 2 - 1
            out = net(image.to(device), args.upsample_align).cpu()
            out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
            out = to_pil_image(out)

        out.save(os.path.join(args.output_dir, image_name))
        print(f"image saved: {image_name}")
    else:
        print('error')
    print(input_file,os.path.join(args.output_dir, image_name))
    join(input_file,os.path.join(args.output_dir, image_name))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--checkpoint',
        type=str,
        default='./weights/paprika.pt',
    )
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='./samples/inputs/1.jpg',
    )
    parser.add_argument(
        '--output_dir', 
        type=str, 
        default='./samples/results',
    )
    parser.add_argument(
        '--device',
        type=str,
        default='cuda:0',
    )
    parser.add_argument(
        '--upsample_align',
        type=bool,
        default=False,
        help="Align corners in decoder upsampling layers"
    )
    parser.add_argument(
        '--x32',
        action="store_true",
        help="Resize images to multiple of 32"
    )
    args = parser.parse_args()
    test(args)
