# -*- coding: utf-8 -*-
#train_models.py

import cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GMM 
from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")


#path to training data.
source   = "word_training_set/"   

#path where training speakers will be saved.
dest = "word_models/"

train_file = "word_training_set_links.txt"        

file_paths = open(train_file,'r')

count = 0

#Extracting features for each speaker.
features = np.asarray(())
for path in file_paths:    
    path = path.strip()   
    print path
    
    #read the audio.
    sr,amplitude = read(source + path)
   
    #extract 40 dimensional MFCC & delta MFCC features.-> more details?
    vector = extract_features(amplitude,sr)
    
    if features.size == 0:
        features = vector
    else:
	#vertical stack features belongs to various audios of the same word.
        features = np.vstack((features, vector))
    #when features of 5 files of speaker are concatenated, then do model training.
    if count == 15:
        #using GMM 
        gmm = GMM(n_components = 16, n_iter = 200, covariance_type='diag',n_init = 3)
        gmm.fit(features)
        
        #save the trained gaussian model.
        picklefile = path.split("/")[0]+".gmm"

        cPickle.dump(gmm,open(dest + picklefile,'w'))
        print '+ modeling completed for word:',picklefile," with data point = ",features.shape    
        features = np.asarray(())
        count = 0
    count = count + 1
    
