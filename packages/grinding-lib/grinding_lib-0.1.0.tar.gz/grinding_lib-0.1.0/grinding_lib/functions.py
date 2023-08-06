import time
import numpy as np
import pandas as pd
import sklearn as sl
import h5py
from tqdm import tqdm as tqdm
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Conv2D, Dense, LSTM, Concatenate, MaxPooling2D, Input, Dropout, Flatten, \
    ZeroPadding2D, ReLU, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.models import Model, Sequential
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.utils import shuffle
import librosa
import scipy.signal  as signal
import gc
from joblib import dump, load
import re
from sklearn.utils import class_weight

np.set_printoptions(threshold=np.inf)
from tensorflow.keras.utils import plot_model
import seaborn as sn
from pyAudioAnalysis import ShortTermFeatures as aF
from pyAudioAnalysis import audioBasicIO as aIO
from statistics import mode
import soundfile as sf
import shutil
from sound_waves import *
import sys
import warnings


###########################################################################
def get_f1(y_true, y_pred):
    '''
    f1 score for metrics
    '''
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2 * (precision * recall) / (precision + recall + K.epsilon())
    return f1_val

############################################################################################
def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def get_spec(y, Fs):
    b, a = butter_highpass(200, Fs)
    y = signal.filtfilt(b, a, y)
    #     print(len(y))
    n = len(y)
    k = np.arange(n)
    T = n / Fs
    frq = k / T
    frq = frq[:len(frq) // 2]

    Y = np.fft.fft(y) / n
    Y = Y[:n // 2]
    return y, abs(Y)[:len(frq) // 4]

##########################################################################################################
def get_time(preds):
    val = np.squeeze(np.where(preds == 1))
    ans = []
    curr = 0
    try:
        for i in range(len(val) - 1):
            if i < curr:
                continue
            #         print(i)
            curr = i + 1
            while curr < len(val) and val[curr] - val[i] <= 10:
                curr += 1
            if curr - i >= 5:
                ans.append((1, val[i] * 0.5, (val[curr - 1]) * 0.5))
                continue
            curr = i

        val = np.squeeze(np.where(preds == 2))
        curr = 0
        for i in range(len(val) - 1):
            ans.append((2, val[i] * 0.5, (val[i] + 1) * 0.5))
    except:
        pass

    return ans

    #############################################################################

#############################################################################
def get_pyaudio_features(path):
    fs, s = aIO.read_audio_file(path)
    win, step = 0.5, 0.1
    [f, fn] = aF.feature_extraction(s, fs, int(fs * win), int(fs * step))
    f = f.reshape(1, -1)
    return f

################################################################
def model_loader():
    ss1 = load('mfcc_cnn.bin')
    ss2 = load('pyaudio.bin')
    model = tf.keras.models.load_model('mfcc_cnn_58_1_1_v1.h5')
    model1 = tf.keras.models.load_model('Model_PA_Base_61_1510_.h5')
    model2 = tf.keras.models.load_model('py_all_finetune2.h5')
    return ss1, ss2, model, model1, model2

################################################################################################################
def features(X, sample_rate):
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,
                    axis=0)  # Generates a Short-time Fourier transform (STFT) to use in the chroma_stft
    stft = np.abs(librosa.stft(X))  # Computes a chromagram from a waveform or power spectrogram.
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,
                     axis=0)  # Computes a mel-scaled spectrogram.
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)  # Computes spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,
                       axis=0)  # Computes the tonal centroid features (tonnetz)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X),
                                              sr=sample_rate).T, axis=0)
    return np.concatenate((mfccs, chroma, mel, contrast, tonnetz), axis=0)

#############################################################################################################
def detla_mfcc(y, sr):
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
    mfcc = mfcc.reshape(-1, 20 * 16)
    mfcc_delta = mfcc_delta.reshape(-1, 20 * 16)
    mfcc_delta2 = mfcc_delta2.reshape(-1, 20 * 16)
    return mfcc, mfcc_delta, mfcc_delta2

# a,b,c =detla_mfcc(y,sr)
########################################################################################################
def inference(path, sr=16000, window=0.5):
    shutil.rmtree('raw_file', ignore_errors=True)
    warnings.filterwarnings("ignore")
    # os.rmdir('raw_file')
    os.makedirs('raw_file')
    l = int(window * sr)
    cnt = 1
    wave, sr = librosa.load(path, sr=sr)
    wave = np.append(wave, np.zeros(l - wave.shape[0] % l, dtype=float), axis=0)
    file = path.replace('wav', 'xlsx')
    preds, p, p1, p2 = ([] for i in range(4))

    s1, s2, m, m1, m2 = model_loader()
    w = 7200
    q = wave.shape[0] // l
    if q > w:
        q = w

    for i in tqdm(range(q - 1)):
        #         for j in range(0, 5, 2):
        #             x = int(j*0.1*sr)
        y, fft = get_spec(wave[i * l: (i + 1) * l], sr)
        a, b, c = detla_mfcc(y, sr)
        data = np.concatenate((np.array(b), np.array(c), np.array(a)), axis=1)
        data = s1.transform(data)
        data = data.reshape(len(data), 20, 16, 3)

        #             audio_fft = fft
        #             audio_spec = np.squeeze(signal.spectrogram(y, sr)[2])
        #             feat = features(y, sr)

        #             data = np.concatenate((np.array(audio_spec).reshape(-1, 129*35),np.array(audio_fft).reshape(1, 1000),np.array(feat).reshape(1,193)),axis=1)
        #             data1 = np.concatenate((np.array(audio_fft).reshape(1, 1000),np.array(audio_spec).reshape(-1, 129*35)),axis=1)
        path = 'raw_file/Audio_' + str(cnt) + '.wav'
        w = wave[i * l: (i + 1) * l]
        sf.write(path, w, 16000)
        data2 = get_pyaudio_features(path)
        data2 = np.array(data2).reshape(-1, 1 * 68)
        data2 = data2[0][:34].reshape(-1, 34)

        #           data = fft.reshape(1,1000)
        #             data = s1.transform(data)
        #             data1 = s3.transform(data1)
        data2 = s2.transform(data2)
        pred = np.squeeze(m.predict(data))
        pred = np.argmax(pred)
        pred1 = np.squeeze(m1.predict(data2))
        pred1 = np.argmax(pred1)
        pred2 = np.squeeze(m2.predict(data2))
        pred2 = np.argmax(pred2)

        if pred == 2 or pred1 == 2:
            preds.append(2)
        elif pred == 1 or pred1 == 1:
            preds.append(1)
        else:
            preds.append(0)

        p2.append(pred)
        p.append(pred1)
        p1.append(pred2)
        # preds.append(mode([pred1, pred2, pred]))

        cnt += 1

    df = pd.DataFrame(list(zip(np.squeeze(p), np.squeeze(p1), np.squeeze(p2))),
                      columns=['Model_PA_Base_61_1510', 'py_all_finetune2', 'mfcc_cnn_58_1_1_v1'])

    print('file is saved')
    df.to_excel(file, index=False)
    preds = np.squeeze(preds)
    intervals = get_time(preds)
    shutil.rmtree('raw_file', ignore_errors=True)
    return preds, intervals

#####################################################################################################
