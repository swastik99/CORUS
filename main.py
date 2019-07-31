import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer
# pygame is used for gaming purpose for high-end pause and play and mixer is a class of pygame for music playing

# For UI PURPOSE
from tkinter import ttk
# This ttk class of tkinter package stands for themed tkinter
# It basically improves the looks of button and different widgets and making theme much better
from ttkthemes import themed_tk as tk
# We install ttktheme package and for theme selection we need to refer this link:
# https://github.com/RedFantom/ttkthemes/blob/master/docs/themes.rst

import tkinter.messagebox
from mutagen.mp3 import MP3
import time
import threading
# This will extract the metadata from the file and every file have meta data and mp3 file metadata also have length so we need to extract that


# For ttktheme usage and UI improvement
top = tk.ThemedTk()
top.get_themes()            # Returns a list of all themes that can be set
top.set_theme("radiance")    # sets an available theme
# For themes : https://github.com/RedFantom/ttkthemes/blob/master/docs/themes.rst


mixer.init()
muted = FALSE


# Definition
playlist = []

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    statusbar['text'] = os.path.basename(filename_path)
    add_to_playlist(filename_path)

# playlist contains the whole path and filename and playlistbox contain filename with same index
# Wholepath is required to play the music inside play_music load function and playlistbox is just t show the user
def add_to_playlist(filename):
    index = 0
    playlistbox.insert(index, os.path.basename(filename))
    playlist.insert(index,filename_path)
    playlistbox.pack()
    index+=1
    # A list inside a box is called list box. In listbox array starts from 0
    # This will help user to add multiple files in the playlist

def del_song():
    stop_music()
    time.sleep(1)
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlist.pop(selected_song)
    playlistbox.delete(selected_song)


def show_details(play_song):
    filelabel['text'] = "Playing" + ' - ' + os.path.basename(play_song)
    # To know the extension of the file...

    file_data = os.path.splitext(filename_path)
    if file_data[1] == '.mp3':
        # for .MP3 file as there length are big so pygame can't handle those files
        # For that we use mutagen which will extract the meta data from file so it will also extract the length
        audio = MP3(play_song)
        total_length = audio.info.length

    else:
        # for .WAV file as there length are small so pygame can handle small files only
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    # divmod divides total length by 60 and store the quotint part in mins and store the remainder part in secs
    # (mins = total_length/60, secs = total_length%60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    # 'd' stands for decimal value, '02' stands for it will be two digit and '0' will be add if the output will be '1' digit
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    # This is the way to initialize a thread for a function
    # Now the thread will take care of this start_count function and interpreter will take care of all other functions


def start_count(t):
    global paused
    current_time = 0
    # mixer.music.get_busy():- Returns FALSE when we press the stop button(Music stop playing)
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
            # Until the paused button is pressed the continue will ignores each iteration below it and value of 't' will stop increasing
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)  # Time package is base on seconds not milliseconds
            current_time = current_time + 1
            # This will increase the time by 1 sec after every 1 sec until it reach total time


# NOTE: After creating this current time our system will be hanged as soon as we execute our program bcoz as if the time will be 300s so our system will be engaged in this while loop above for 300sec and other statements will not be executed, so to solve this problem we use "Threading Concept"

def play_music():
    # Here when the application starts it checks whether paused is initialized or not and as it is not It will move to except part and do regular play_music button do and if paused is initialized from pause music function it will unpause the music from where it was paused
    global paused
    if paused:
        statusbar['text'] = "Playing Now" + ' - ' + os.path.basename(filename_path)
        mixer.music.unpause()
        paused = FALSE

    else:
        try:
            stop_music()
            time.sleep(1)
            #For changing the music we call this stop_music() func and for switching to next song and start new thread for time we take 1 sec
            selected_song = playlistbox.curselection()
            #This curselection is a function of playlist box for selecting the song from playlistbox and play that song using playlist song path
            #It basically gives the index value of selected song from playlistbox
            selected_song = int(selected_song[0])
            #print(selected_song)
            #As the tuple only contains one value of that selected song index, we always fetch [0]index position of tuple
            play_it = playlist[selected_song]
            #print(play_it)
            #Gives the full path of the song from playlist based on index
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'CORUS could not find the file... \nPlease try again')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped..."


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused..."


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded" + ' - ' + os.path.basename(filename_path)


def set_vol(val):
    volume = float(
        val) / 100
    # The value we get through parameter is string so we need to convert it into integer and we divide it by 100 because set_volume() function of mixer class have value 0-1 so it can be 0.54, 0.98 or like that upto 1 so divide by 100 will give decimal value upto one
    mixer.music.set_volume(volume)


def mute_music():
    global muted
    if muted:  # unmute the music
        mixer.music.set_volume(0.6)
        unmuteBtn.configure(image=unmutePhoto)
        scale.set(60)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        unmuteBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


def about_us():
    tkinter.messagebox.showinfo('About Corus',
                                'This is a light weight music player built using python 3.7\nBy Swastik Shrivastava')

def on_closing():
    stop_music()
    # This will foramlly stops the music so the thread responsible for running music wont give errors
    top.destroy()
    # Close the window approprately when click the windows by_default close button

statusbar = ttk.Label(top, text="Welcome to CORUS", relief=SUNKEN, anchor=W, font = "Times 8 italic")
statusbar.pack(side=BOTTOM, fill=X)
# It will create a status bar with some difference from rest of the page
# It print a message or status on the left hand side so we use W for west
# Styles = nrmal,bold,roman, italic,underline, and overstrike
# Fonts = MS Sans Serif, MS Serif, Symbol, Sstem, Times New Roman(Times), and Verdana
# Arial, Courier New, Comic Sans MS, Fixedsys
# Add statusbar in the bottom and we need status bar from left to right corner so we fill =  X for X-axis


# Create Menu Bar

menubar = Menu(top)
# Adds an empty menubar on the top
top.config(menu=menubar)
# top.config is to ensure that menu is on the top and is ready to receive submenu

# create Submenu File

subMenu = Menu(menubar, tearoff=0)
# Adds menu items also called as submenu to the menubar and tearoff removes the dashed line from the submenu
menubar.add_cascade(label="file", menu=subMenu)  # creates a dropdown menu name as file
subMenu.add_command(label="Open", command=browse_file)  # creates submenu of file
subMenu.add_command(label="Exit", command=top.destroy)  # creates submenu of file

# create Submenu Help
subMenu = Menu(menubar, tearoff=0)
# Adds menu items also called as submenu to the menubar and tearoff removes the dashed line from the submenu
menubar.add_cascade(label="Help", menu=subMenu)
# creates a dropdown menu name as Help
subMenu.add_command(label="About Us", command=about_us)
# creates submenu of Help


top.title("CORUS")
top.iconbitmap(r'images/corus.ico')

leftframe = Frame(top)
leftframe.pack(side = LEFT, padx = 30, pady = 30)

rightframe = Frame(top)
rightframe.pack(pady = 30)

topframe = Frame(rightframe)
topframe.pack()

playlistbox = Listbox(leftframe)
playlistbox.pack()

filelabel = Label(topframe)
filelabel.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=10)
# It allows a widget to show on the window and the widget is arranged on after another in a vertical manner means one below another

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()


addbtn = ttk.Button(leftframe, text = "+ ADD", command = browse_file)
addbtn.pack(side = LEFT)
#To add in the playlist

delbtn = ttk.Button(leftframe, text = "- DELETE", command = del_song)
delbtn.pack()
#To delete from the playlist


middleframe = Frame(rightframe, relief=RAISED)
middleframe.pack(padx=30, pady=30)
# This is a hidden frame inside the main frame tk like DIV tag in HTML and this is like a division where we don't disturb other widgets just disturm those which are need to be adjust so this will create a hidden division of selected widgets and any rule applied on middleframe will be applied on them so it just isolates the widget
# A frame allows to use pack and grid layout manager at the same time to make a complex GUI, without frame we can't use them in the same time
# padding in x direction on beth sides

playPhoto = PhotoImage(file='images/play.png')
# select the images from dir i.e play button
# labelphoto = Label(top,images = playPhoto)
# #label is worked as a container for
# labelphoto.pack()

playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
# Command tell what need to do when we need to click button play_btn function will be called on clicking the images
# This button will be inside middleframe which is a part of main frame or window
playBtn.grid(row=0, column=0, padx=10)
# grid layout manager can only be used in frames if we want to use both pack and grid at the same time.
# this combo is used for making complex GUI like pycharm

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()
# Bottomframe for mute, rewind scale etc...


rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0, padx=30)

mutePhoto = PhotoImage(file='images/mute.png')
unmutePhoto = PhotoImage(file='images/unmute.png')
unmuteBtn = ttk.Button(bottomframe, image=unmutePhoto, command=mute_music)
unmuteBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
# It adds a scale volume controller having range 0-100 in a horizontal manner
scale.set(60)  # implementing the default value as 60
mixer.music.set_volume(0.6)
scale.grid(row=0, column=2, pady=15, padx=20)


top.protocol("WM_DELETE_WINDOW", on_closing)
# This is called as Events and Binding bcoz we override an event(windows by default closing button)
# On clicking the close button of the application window this will take to the on_closing button which will perform task whatever we want
top.resizable(0,0)
# For disabling mzximize /minnimize button from the main window

top.mainloop()