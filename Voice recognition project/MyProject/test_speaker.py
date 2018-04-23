import os
import cPickle
import numpy as np
from scipy.io.wavfile import read
from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time

#record user speech
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "word_test_set/predict"

while True:
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
	wf = wave.open(WAVE_OUTPUT_FILENAME + ".wav", 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	#START PREDICT BY USING GMM WITH TRAINED MODEL
	#path to training data
	modelpath = "word_models/"

	test_file = "word_test_set_links.txt"        

	#models from traning
	gmm_files = [os.path.join(modelpath,fname) for fname in 
		      os.listdir(modelpath) if fname.endswith('.gmm')]

	#Load the Gaussian gender Models
	models = [cPickle.load(open(fname,'r')) for fname in gmm_files]

	words = [fname.split("/")[-1].split(".gmm")[0] for fname 
		      in gmm_files]

	# Read the test directory and get the list of test audio files 
	sr,audio = read("word_test_set/predict.wav")
	#features
	vector = extract_features(audio,sr)
	    
	log_likelihood = np.zeros(len(models)) 
	    
	for i in range(len(models)):
		gmm    = models[i]         #checking with each model one by one
		scores = np.array(gmm.score(vector))
		log_likelihood[i] = scores.sum()
	    
	winner = np.argmax(log_likelihood)

	print "\n----------------------------------\n"
	print "Spoken word: ", words[winner]
	print "\n----------------------------------\n"

	#wait key:
	#Enter to continue speech.
	#q if want to finish.
	isContinueRecording = True
	print('Type q to finish speaking otherwise will continue speaking')
	while True:
		name = raw_input("Type: ")
		if (name == 'q'):
			isContinueRecording = False
		break
	#to exit recording
	if (isContinueRecording == False):
		break



