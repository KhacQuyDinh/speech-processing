import wolframalpha
import wikipedia
import wx
import re
import pyttsx
import os
import speech_recognition as sr

##lib for text to speech.
engine = pyttsx.init()
##say welcome by using pyttsx.
#engine.say("Welcome to virtual assistant. My name is your assistant!")
#engine.runAndWait()

##say welcome by using espeak.
os.system("espeak 'Welcome'")		

#app_id supported by wolframal.
#visit products.wolframalpha.com/api/
app_id = "267KEA-KQ5YKTYEVR"
client = wolframalpha.Client(app_id)

#set language by its locale.
wikipedia.set_lang("en")

pattern_sample = {
		"do you think (.*)"
		, "do you remember (.*)"
		, "what is (.*)"
		, "who is (.*)"
		, "where is (.*)"
		, "i want (.*)"
		, "if (.*)"						
	}
	
class MyFrame(wx.Frame):
	def __init__(self):
		#The whole window.
		wx.Frame.__init__(self, None,
			pos=wx.DefaultPosition, size=wx.Size(450, 100),
			style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN, title = "PyDa")

		#self is the instant
		panel = wx.Panel(self)
		#display vertically
		my_sizer = wx.BoxSizer(wx.VERTICAL)
		lbl = wx.StaticText(panel, label="I am glad to see you! How may I help you?")
		my_sizer.Add(lbl, 0, wx.ALL, 5)	
		#setup a textbox.
		self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(400,30))
		self.txt.SetFocus()
		#bindin event calls func OnEnter
		self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
		my_sizer.Add(self.txt, 0, wx.ALL, 5)
		panel.SetSizer(my_sizer)
		#show the window
		self.Show()				

	#func OnEnter for the event above.
	def OnEnter(self, event):
		input = self.txt.GetValue()	
		if input == "":
			#get recognizer.
			r = sr.Recognizer()
			#hear from the person.
			with sr.Microphone() as source:	
				#listen and take audio
				audio = r.listen(source)
			try:
				#trans value of audio to text and display it.
				self.txt.SetValue(r.recognize_google(audio))	
			except sr.UnknownValueError:
				print("I  do not hear you clearly")
				print("Please try again.")
			except sr.RequestError as e:
				print("Please check Internet access: {0}".format(e))
				print("Please try again.")
		else:
			#search group matching pattern.	
			for pattern in pattern_sample:
				match = re.search(pattern, str(input).lower())
				if (match is not None): 				
					input = match.group(1)
					#print(input)
					break
			#input = input.lower()
			#while True: 
			##raw_input to enter text from the command line.
			#input = raw_input("Question: ")
			##if (input == 'q'): break			
			try:
				res = client.query(input)
				#next func returns the next item = the first item here.	
				answer = next(res.results).text	
			#if query failed.
			except:
				#limit sentences.
				answer = wikipedia.summary(input, sentences=3)

			print answer
			#engine.say(answer)
			#engine.runAndWait()
			__answer = str("espeak '{0}'".format(answer.encode('utf-8')))
			os.system(__answer)


if __name__ == "__main__":
	#get the current app.
	app = wx.App(True)
	#my frame.
	frame = MyFrame()
	#run app. -> a loop
	app.MainLoop()		

print('goodbye')		