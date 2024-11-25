# main file for the tuner
import sounddevice as sd
import numpy as np
import math
import copy
import matplotlib.pyplot as plt

#defined variables
Notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
sampling_rate = 44100
harmonic_number = 3
#matching of guitar audios
def Find_Closest_Note(Fin):
  Notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
  Concert_Pitch = 440 #Hz
  x = round(12*math.log2(Fin/Concert_Pitch))
  Note = Notes[x%12]
  closest_pitch = round(Concert_Pitch*pow(2,((x)/12)), 2)
  return Note, closest_pitch

def Determine_Sharp_Flat(Fin):
  print(f"Input Frequency: {Fin}")
  note, close_pitch = Find_Closest_Note(Fin)
  print(f"Closest note: {note} ")
  print(f"Closest pitch: {close_pitch}")
  if (Fin < close_pitch):
    print("Flat")
  elif (Fin > close_pitch):
    print("Sharp")

#recording audio
def audio_record():
    seconds = 1 #in seconds
    sampling_rate = 48000
    audio = sd.rec(int(seconds*sampling_rate), samplerate=sampling_rate, channels = 1) 
    sd.wait()
    sd.play(audio, sampling_rate)
    return audio

def Harmonic_Product_Spectrum(sig):
  harmonic_product_spectrum = copy.deepcopy(sig)
  for index in range(2, harmonic_number + 1):
    downsampled = sig[::index]
    harmonic_product_spectrum[:len(downsampled)] *= downsampled

  return harmonic_product_spectrum


def compute_fft(recording): 
    dft = np.fft.fft(recording)
    dft = abs(dft)

    for index in range(61+1):
      dft[index] = 0
    dft = dft[:int(len(dft)/2)]
    return dft



def continuous_running():
  while (True):
    recording = audio_record()
    transform = compute_fft(recording.flatten())
    hps_result = Harmonic_Product_Spectrum(transform)
    
    frequencies = np.fft.fftfreq(int((len(hps_result)*2)/1), 1 / sampling_rate)[:len(transform)]
    valid_indices = frequencies > 60
    hps_result[~valid_indices] = 0
    
    max_index = np.argmax(hps_result)
    fundamental_frequency = frequencies[max_index]
    Determine_Sharp_Flat(fundamental_frequency+40)
    
continuous_running() 
    
  
