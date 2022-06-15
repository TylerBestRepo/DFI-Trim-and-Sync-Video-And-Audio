from moviepy.editor import *
from tkinter import Tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import csv

from numpy import number

files_list = []
numberOfClips = input("How many files are you combining here?: ")
temp_file = []
print(numberOfClips)
numberOfClips = int(numberOfClips)

looper = 0

while looper < int(numberOfClips):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    messagebox.showinfo("Ahoy", "Select a video file in the correct order")
    temp_file = askopenfilename()
    files_list.append("file '" + temp_file + "'")

    looper += 1

print(files_list)

with open ('concatenationTXT.txt', 'w') as f:
    writer = csv.writer(f)
    i = 0
    for item in files_list:
        writer.writerow([item])
    

# This method works well and fast and doesnt re-encode and works properly so long as the file extensions/types are the same going into this.
shell_command = "ffmpeg -f concat -safe 0 -i concatenationTXT.txt -c copy" + files_list[0] +  ".MP4"



if (files_list != []):
    os.system(shell_command)


# This works but does it very slowly due to re-encoding

# if (numberOfClips == 1):
#     clip_1 = VideoFileClip(files_list[0])
#     print("Its only one clip so you dont need to combine anything.")
# elif (numberOfClips == 2):
#     clip_1 = VideoFileClip(files_list[0])
#     clip_2 = VideoFileClip(files_list[1])
#     result_clip = concatenate_videoclips([clip_1, clip_2])
# elif (numberOfClips == 3):
#     clip_1 = VideoFileClip(files_list[0])
#     clip_2 = VideoFileClip(files_list[1])
#     clip_3 = VideoFileClip(files_list[2])
#     result_clip = concatenate_videoclips([clip_1, clip_2, clip_3])


# result_clip.write_videofile('combined2Files.mp4')