# -*- coding: utf-8 -*-
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
def closeTheActiveprogram():
	call(["xdotool","getwindowfocus","windowkill"])

def playAudio(link):
	call(["vlc",link])

def openVlc():
	call(["vlc"])

def displayDate():
	call(["date"])

def doCommand(cmd):
	if (cmd == 'đóng cửa sổ dòng lệnh'):
		closeTheActiveprogram()
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

