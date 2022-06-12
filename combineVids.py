from moviepy.editor import *

clip_1 = VideoFileClip('1.MOV')
clip_2 = VideoFileClip('2.MOV')


result_clip = concatenate_videoclips([clip_1, clip_2])

result_clip.write_videofile('outputFile.mp4')