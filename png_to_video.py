import os
import glob
from natsort import natsorted
from moviepy.editor import *

base_dir = "data/images"
print(base_dir)

gif_name = 'pic'
fps = 24

file_list = glob.glob(base_dir+'/*.png')  # Get all the pngs in the current directory
file_list_sorted = natsorted(file_list,reverse=False)  # Sort the images

clips = [ImageClip(m).set_duration(0.1)
         for m in file_list_sorted]

print(len(file_list))
print(len(file_list_sorted))     
print(len(clips))

concat_clip = concatenate_videoclips(clips, method="compose")
concat_clip.write_videofile("test2.mp4", fps=fps)

