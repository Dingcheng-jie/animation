1、创建环境：

conda create -n animeganv2 python=3.6.5

conda create cudatoolkit=10.0

conda create cudnn=7.6
2、安装需求库：
pip install tensorflow-gpu=1.15.0
pip install torch >= 1.7.1

![image](https://user-images.githubusercontent.com/82815279/173214462-2c220e19-e82a-4ecd-ad8a-fc52923df80f.png)

	
3、整理数据集，将其整理成如下结构(其中FC_style即为一种动漫风格的图片，train_photo为现实生活中的图片)

![554EQ9FXSDQ2SZY(~~2N~ C](https://user-images.githubusercontent.com/82815279/173214477-3c6a0922-364e-44be-ad60-d0a1d1c41d26.png)


4、处理数据集，将动漫图片边缘平滑化并调整图像大小，这样可以减少图像的噪声，便于动漫化
python edge_smooth.py --dataset datasets/F2C_style--img_size 256

5、开始训练，设定101轮，前十轮进行权重的初始化，每10轮进行一次模型权重保存
python train.py --dataset datasets/F2C_style--epoch 101 --init_epoch 10 --save_freq > log.txt
 
 ![image](https://user-images.githubusercontent.com/82815279/173214489-4a5f2a06-03b8-45e6-82f6-b9eea2613d5f.png)

 
模型已保存至文件夹

![image](https://user-images.githubusercontent.com/82815279/173214493-7a462a8c-5a5c-4adc-9d72-c9d59251abdb.png)

 
6、提取模型的权重，得到权重文件
python get_generator_ckpt.py --checkpoint_dir checkpoint/AnimeGANv2_F2C_style_lsgan_300_300_1_2_10_1 --style_name F2C_style

![image](https://user-images.githubusercontent.com/82815279/173214501-4b877003-011f-4f13-99b2-e0de70544d7b.png)


7、基于tensorflow模型图片动漫化，生成动漫图片和对比图片
python test.py --checkpoint_dir checkpoint/generator_F2C_style_weight --test_dir testdata/input --save_dir testdata/onput

![image](https://user-images.githubusercontent.com/82815279/173214508-ab4afe59-18e2-4f1e-a158-55a631d30347.png)

![image](https://user-images.githubusercontent.com/82815279/173214514-a4e3ec1c-0c86-4d98-a4a2-bb096f403d52.png)


8、基于tensorflow模型视频动漫化，生成动漫视频和对比视频
python video2anime.py --checkpoint_dir checkpoint/generator_F2C_style_weight --video testdata/input/2.mp4 --output testdata/output

![image](https://user-images.githubusercontent.com/82815279/173214519-49149dcf-f1cc-459e-aac3-fc50fac441a3.png)


9、在此基础上，我们又增加了tensorflow模型转pytorch模型的部分
进入animegan2-pytorch文件夹
python convert_weights.py --tf_checkpoint_path ../AnimeGANv2/checkpoint/generator_F2C_style_weight --save_name models/pytorch_generator_F2C_style.pt

![image](https://user-images.githubusercontent.com/82815279/173214520-b883c32d-7364-44cb-84c0-a3fd4dfb64ce.png)

10、基于pytorch模型图片动漫化，生成动漫图片和对比图片
python test.py --checkpoint model/pytorch_generator_F2C_style.pt --input_file samples/inputs/2.jpg --output_dir samples/outputs --device ‘cuda’

11、基于pytorch模型视频动漫化，生成动漫视频和对比视频
python video2anime.py --checkpoint model/pytorch_generator_F2C_style.pt --input_file samples/inputs/1.mp4 --output_dir samples/outputs --device ‘cuda’
