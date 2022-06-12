import string
from turtle import forward
from moviepy.editor import *
import os
import glob
import csv
import time,datetime
import math

# Functions

def calc_starting_time(time_diff_raw) -> string:
    no_cutoff = True
    if (time_diff_raw < 0):
    # gotta generate the string very differently if the time difference is greather than 1 minute
        if (abs(time_diff_raw) >= 60):
            print("more complicated section")
            time_diff = int(abs(time_diff_raw))
            mins = math.floor(time_diff/60)
            seconds = time_diff%60

            print(f"The time difference is: {mins} minute and {seconds} seconds")
            base = "00:"
            if (mins < 10 and mins > 0):
                mins = str(int(mins))
                base = base + "0" + mins + ":"
            elif (mins >= 10):
                mins = str(int(mins))
                base = base + mins + ":"
            else: 
                base = base + "00:"

            if seconds == 0:
                string_new_start = base + "00"
            elif (abs(seconds) < 10):
                seconds = int(abs(seconds))
                string_new_start = base + "0" + str(seconds)
            else: #this condition means that the time difference is between 10 and 59 seconds
                seconds = int(abs(seconds))
                string_new_start = base + str(seconds)

        elif (abs(time_diff_raw) < 10):
            time_diff = int(abs(time_diff_raw))
            string_new_start = "00:00:0" + str(time_diff)
        else: #this condition means that the time difference is between 10 and 59 seconds
            time_diff = int(abs(time_diff_raw))
            string_new_start = "00:00:" + str(time_diff)
    elif (time_diff_raw > 0):
        # If this happens theres a good chance something has gone wrong
        string_new_start = "00:00:00"
        no_cutoff = False
    return string_new_start, no_cutoff


# in case things get automated in a different sort of way then this list can be used to store all the mp4 files
list_of_files = []

os.system("clear")

for file in glob.glob("*.MP4"):
    list_of_files.append(file)

print(list_of_files)
# Looking for .mp4 files
for file in glob.glob("*.txt"):
    timesFile = file
times = []
# Getting the input times from the smartphone text file
with open(timesFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            times.append(row[1])

# Converting to date time varibales from strings
faceFacing = datetime.datetime.strptime(times[0], "%H:%M:%S")
forwardFacing = datetime.datetime.strptime(times[1], "%H:%M:%S")
audioTime = datetime.datetime.strptime(times[2], "%H:%M:%S")

# Now datetimes can be converted to unix times
faceFacing = (time.mktime(faceFacing.timetuple()))
forwardFacing = (time.mktime(forwardFacing.timetuple()))
audioTime = (time.mktime(audioTime.timetuple()))

unix_vals = [["Face facing",faceFacing], ["Forward facing", forwardFacing], ["audio time", audioTime]]

print(f"Unix values unsorted: {unix_vals}")

i = 0
y = len(unix_vals)
biggest = unix_vals[0][1]
index = 0
while i < y:
    if unix_vals[i][1] == biggest:
        print("Good to know")
    elif unix_vals[i][1] > biggest:
        biggest = unix_vals[i][1]
        index = i
    i += 1
# Biggest is the latest startig times unix value, index is relative to the original unix_vals list and the string will also be written
print(biggest, index)
biggest_name = unix_vals[index][0]

del unix_vals[index]
unix_times_used_to_cut_vid_or_audio = unix_vals
print(unix_times_used_to_cut_vid_or_audio)

# only a maxiumum of two out of three files will need to be trimmed
cutoff_1 = unix_times_used_to_cut_vid_or_audio[0][1] - biggest
cutoff_2 = unix_times_used_to_cut_vid_or_audio[1][1] - biggest



# Calling function to generate a string in the format 00:00:30 if the first 30 seconds of video needs to be cut off
cutoff_1_string, no_cutoff_1 = calc_starting_time(cutoff_1)
cutoff_2_string, no_cutoff_2 = calc_starting_time(cutoff_2)
print(cutoff_1_string, no_cutoff_1) 
print(cutoff_2_string, no_cutoff_2)


# dont want exact start time we need to know how much to trim off
#shell_command_1 = "ffmpeg -ss " + string_new_face_start + " -i " + list_of_files[0] + " -c copy NewFaceStart.mp4"



#print(shell_command)

#os.system(shell_command_1)







# This is just for printing to see what was happening and or with the times for use later

# Printing the time differences between the face facing cam and the audio start
if (cutoff_1 < 0 ):
    print(f"Time diff 1 is {abs(cutoff_1)} seconds before the latest starting recording")
    #This part here seems all good

# Printing the time differences between the forward facing cam and the audio start
#time_diff_forward_audio = forwardFacing - audioTime
if (cutoff_2 < 0):
        print(f"Time diff 2 is {abs(cutoff_2)} seconds before the latest starting recording")

print(f"The latest started recording is: {biggest_name}")

#print(f"Face start = {time_diff_face_audio}\nForward Start = {time_diff_forward_audio}")
