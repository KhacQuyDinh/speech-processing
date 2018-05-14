# -*- coding: utf-8 -*-
import os
import cPickle
import numpy as np
from scipy.io.wavfile import read
from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time

#libs to record user speech.
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2.5
WAVE_OUTPUT_FILENAME = "word_test_set/predict"

#import tkMessageBox.
import Tkinter
import tkMessageBox
import subprocess
from subprocess import call #to execute command in linux.
from subprocess import Popen
import psutil

def closeFirefox():
	pid_firefox = [p.info['pid'] for p in psutil.process_iter(attrs=['pid', 'name']) if 'firefox' in p.info['name']]
	for p in pid_firefox:
		psutil.Process(p).terminate()  

import webbrowser
def openFirefox(link='https://google.com'):
	webbrowser.get("firefox").open(link)

#powered by pyalsaaudio which is running in kernel.
def decreaseVolumn(amount):
	call(["amixer", "-D", "pulse", "sset", "Master", str(amount)+"%-"])

#powered by pyalsaaudio which is running in kernel.
def increaseVolumn(amount):
	call(["amixer", "-D", "pulse", "sset", "Master", str(amount)+"%+"])

def openTerminal():
	call(["gnome-terminal"])	

def openNewGedit():
	call(["gedit","new_document.txt"])

def blockComputer():
	call(["gnome-screensaver-command","-l"])

def openSystemSettings():
	call(["unity-control-center"])	
	
def displayCalendar():
	call(["ncal"])

#powered by xdotool.
def closeTheActiverogram():
	call(["xdotool","getwindowfocus","windowkill"])

def playAudio(link):
	call(["vlc",link])

def openVlc():
	call(["vlc"])

def displayDate():
	call(["date"])

def doCommand(cmd):
	if (cmd == 'đóng cửa sổ dòng lệnh'):
		closeTheActiverogram()
	elif (cmd == 'mở cửa sổ dòng lệnh'):
		openTerminal()
	elif (cmd == 'mở trình duyệt'):
		openFirefox()
	elif (cmd == 'đóng trình duyệt'):
		closeFirefox()		
	elif (cmd == 'giảm âm lượng'):
		decreaseVolumn(2) #+2%
	elif (cmd == 'tăng âm lượng'):
		increaseVolumn(2) #-2%
	elif (cmd == 'mở bản đồ'):
		openFirefox('https://www.google.com/maps')
	elif (cmd == 'mở facebook'):
		openFirefox('https://facebook.com')
	elif (cmd == 'mở trình soạn thảo văn bản'):
		openNewGedit()
	elif (cmd == 'mở trình nghe nhạc'):
		openVlc()
	elif (cmd == 'khóa máy tính'):
	 	blockComputer()
	elif (cmd == 'mở cài đặt'):
	 	openSystemSettings()
	elif (cmd == 'hiển thị lịch'):
		displayCalendar()
	elif (cmd == 'hiển thị thời gian'):
		displayDate()
	elif (cmd == 'xin chào'):
		playAudio('word_test_set/xin_chao.wav')

while True:
	#INIT MODELS
	#path to training data.
	modelpath = "word_models/"

	test_file = "word_test_set_links.txt"        

	#models from training.
	gmm_files = [os.path.join(modelpath,fname) for fname in 
		      os.listdir(modelpath) if fname.endswith('.gmm')]

	#Load the Gaussian models.
	models = [cPickle.load(open(fname,'r')) for fname in gmm_files]

	words = [fname.split("/")[-1].split(".gmm")[0] for fname 
		      in gmm_files]

	#print all available cmds.
	listw = ""
	for i in range(len(words)):
		listw += words[i] + " | "
	print listw
	#END INIT MODELS	

	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
		        channels=CHANNELS,
		        rate=RATE,
		        input=True,
		        frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	print("* done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()

	#when save the recorded audio?
	wf = wave.open(WAVE_OUTPUT_FILENAME + ".wav", 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	isSaved = raw_input("Type: ")
	wf.close()

	#START PREDICT BY USING GMM WITH TRAINED MODELs
	#read recorded audio files.
	sr,amplitude = read("word_test_set/predict.wav")
	#features.
	vector = extract_features(amplitude,sr)
	    
	log_likelihood = np.zeros(len(models)) 

	#checking with each model one by one.
	#a model is equivalent to a word.    
	for i in range(len(models)):
		gmm    = models[i]      
		#compute probability of the vector under the models[i].   
		scores = np.array(gmm.score(vector))
		log_likelihood[i] = scores.sum()
	  	
	#LOG INFO
	print log_likelihood
	print np.amax(log_likelihood)
	#END LOG INFO

	spoken_word = ""
	if (np.amax(log_likelihood) < -10000):
		spoken_word = "unknown"
	else:
		winner = np.argmax(log_likelihood)
		print winner + 1	
		spoken_word = words[winner]	

	print "\n----------------------------------\n"
	print "Spoken word: ", spoken_word
	print "\n----------------------------------\n"

	#PROCESS USER COMMAND
	if (spoken_word != 'unknown'):
		response = tkMessageBox.askquestion("Command", "Are you sure want to " + spoken_word)			
		if (response == 'yes'):
			doCommand(spoken_word)
	#END PROCESS USER COMMAND
	
	#WAIT KEY
	#Enter to continue speech.
	#q if want to finish.
	isContinueRecording = True
	print('Type q to finish speaking otherwise will continue speaking')
	while True:
		name = raw_input("Type: ")
		if (name == 'q'):
			isContinueRecording = False
		break
	#to exit recording.
	if (isContinueRecording == False):
		break



