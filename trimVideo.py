import string
from turtle import forward
from moviepy.editor import *
import os
import glob
import csv
import time,datetime
import math
from tkinter import Tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import time

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

#getting the phone txt file
messagebox.showinfo("Ahoy", "Select the phone text file")
timesFile = askopenfilename()

times = []
# Getting the input times from the smartphone text file
with open(timesFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if (row[0] == 'Video started at'):
                times.append(row)
            elif (row[0] == 'Forward video started at'):
                times.append(row)
            elif (row[0] == 'Audio started at'):
                times.append(row)

# For testing i hard code the 

# Converting to date time varibales from strings
bool_check = []
for x in times:
    if x[0] == 'Video started at':
        faceFacing = datetime.datetime.strptime(x[1], "%H:%M:%S")
        bool_check.append(True)
    elif x[0] == 'Forward video started at':
        forwardFacing = datetime.datetime.strptime(x[1], "%H:%M:%S")
        bool_check.append(True)
    elif x[0] == 'Audio started at':
        temp = x[1]
        audioTime = datetime.datetime.strptime(x[1], "%H:%M:%S")
        bool_check.append(True)

all_reference_times_exist = True
counter = 0
for x in bool_check:
    if x == True:
        counter += 1
if counter != 3:
    all_reference_times_exist = False

if all_reference_times_exist:
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


    # Close to editing any two of the three files to make a good sync
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    messagebox.showinfo("Ahoy", "Select the face frame video file")
    face_vid_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    messagebox.showinfo("Ahoy", "Select the forward frame video file")
    forward_vid_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    messagebox.showinfo("Ahoy", "Select the audio file")
    audio_file_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file

    face_vid = os.path.basename(face_vid_path)
    forward_vid = os.path.basename(forward_vid_path)
    audio = os.path.basename(audio_file_path)
    print(face_vid)

    # The subject file from this will be dependant of if checks to do the right one

    if (unix_times_used_to_cut_vid_or_audio[0][0] == "Face facing"):
        shell_command_1 = "ffmpeg -ss " + cutoff_1_string + " -i " + face_vid + " -c copy output/" + face_vid[:-4] + "Synced.mp4"
    elif (unix_times_used_to_cut_vid_or_audio[0][0] == "Forward facing"):
        shell_command_1 = "ffmpeg -ss " + cutoff_1_string + " -i " + forward_vid + " -c copy output/" + forward_vid[:-4]  + "Synced.mp4"
    elif (unix_times_used_to_cut_vid_or_audio[0][0] == "audio time"):
        shell_command_1 = "ffmpeg -ss " + cutoff_1_string + " -i " + audio + " -c copy output/" + audio[:-4]  + "Synced.mp4"

    if (unix_times_used_to_cut_vid_or_audio[1][0] == "Face facing"):
        shell_command_2 = "ffmpeg -ss " + cutoff_2_string + " -i " + face_vid + " -c copy output/" + face_vid[:-4]  + "Synced.mp4"
    elif (unix_times_used_to_cut_vid_or_audio[1][0] == "Forward facing"):
        shell_command_2 = "ffmpeg -ss " + cutoff_2_string + " -i " + forward_vid + " -c copy output/" + forward_vid[:-4]  + "Synced.mp4"
    elif (unix_times_used_to_cut_vid_or_audio[1][0] == "audio time"):
        shell_command_2 = "ffmpeg -ss " + cutoff_2_string + " -i " + audio + " -c copy output/" + audio[:-4]  + "Synced.wav"




    print(shell_command_1)
    start_time = time.time()
    os.system(shell_command_1)
    print("My program took", round(time.time() - start_time,3), "to run 1st trimming")
    print(shell_command_2)
    start_time_2 = time.time()
    os.system(shell_command_2)
    print("My program took", round(time.time() - start_time_2,3), "to run second trimming")


    # This is just for printing to see what was happening and or with the times for use later

    # Printing the time differences between the face facing cam and the audio start
    # if (cutoff_1 < 0 ):
    #     print(f"Time diff 1 is {abs(cutoff_1)} seconds before the latest starting recording")
    #     #This part here seems all good

    # # Printing the time differences between the forward facing cam and the audio start
    # #time_diff_forward_audio = forwardFacing - audioTime
    # if (cutoff_2 < 0):
    #         print(f"Time diff 2 is {abs(cutoff_2)} seconds before the latest starting recording")

    # print(f"The latest started recording is: {biggest_name}")

else:
    print("The input text file doesnt contain the 3 necessary time stamps for syncing")

#print(f"Face start = {time_diff_face_audio}\nForward Start = {time_diff_forward_audio}")
