from moviepy.editor import VideoFileClip, clips_array

clip1 = VideoFileClip('213.mp4')#读入视频
clip2 = VideoFileClip('213_2.mp4')
final_clip = clips_array([[clip1,clip2]])#左右拼接
final_clip.write_videofile('result.mp4')#保存视频