# from glob import glob
# import cv2, os, argparse

# print(os.getcwd()+'/datasets/{}/{}/*.jpg'.format('F2C_style', 'style_256'))
# print(glob(os.getcwd()+'/datasets/{}/{}/*.jpg'.format('F2C_style', 'style_256')))


import argparse
from utils import *
import os
import generator

checkpoint_dir='root/AnimeGANv2/checkpoint/AnimeGANv2_shensuistyle_lsgan_300_300_1_2_10_1/'
print(tf.train.get_checkpoint_state(checkpoint_dir))