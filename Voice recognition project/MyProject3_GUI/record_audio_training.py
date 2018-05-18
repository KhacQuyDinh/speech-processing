# -*- coding: utf-8 -*-
import pyaudio
import wave

def record(cmd):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 2.5
	index = 0

	WAVE_OUTPUT_FILENAME = "word_training_set/" + str(cmd) + "/w"

	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	#frame_length = 0

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	print("* done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()
	wf = wave.open(WAVE_OUTPUT_FILENAME + str(index) + ".wav", 'wb')

	print index
	index += 1
	
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	print "done audio " + str(index + 1)
