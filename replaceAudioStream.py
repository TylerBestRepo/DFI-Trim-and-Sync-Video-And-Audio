from tkinter import Tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import os
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
messagebox.showinfo("Ahoy", "Select the face frame video file.")
face_stream = askopenfilename()
# messagebox.showinfo("Ahoy", "Select the forward frame video file.")
# forward_stream = askopenfilename()
messagebox.showinfo("Ahoy", "Select the audio file.")
audio_stream = askopenfilename()


shell_command_face = "ffmpeg -i " + face_stream + " -i " + audio_stream + " -c:v copy -map 0:v:0 -map 1:a:0 -shortest faceReplacedAudio.mp4"

# shell_command_forward = "ffmpeg -i " + forward_stream + " -i a.wav -c:v copy -map 0:v:0 -map 1:a:0 -shortest forwardReplaceAudio.mp4"

print(shell_command_face)
# print(shell_command_forward)

os.system(shell_command_face)