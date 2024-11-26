# main file for the tuner
import sounddevice as sd
import numpy as np
import math
import copy
import keyboard
#defined variables
Notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
#sampling_rate = 44100
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
def audio_record(sampling_rate):
    seconds = 1 #in seconds
    print("Start")
    audio = sd.rec(int(seconds*sampling_rate), samplerate=sampling_rate, channels = 1) 
    sd.wait()
    print("end")
    #sd.play(audio, sampling_rate)
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

    #for index in range(61+1):
     # dft[index] = 0
    dft = dft[:int(len(dft)/2)]
    return dft


def string_input():
  string_tune = input("String that needs to be tuned: ")
  if string_tune == "E":
    sampling_rate = 60000
    return sampling_rate
  if string_tune == "e":
    sampling_rate = 47000
    return sampling_rate
  string_tune = string_tune.capitalize()
  if string_tune == "B":
    sampling_rate = 48000
    return sampling_rate
  if string_tune == "G":
    sampling_rate = 48400
    return sampling_rate
  if string_tune == "D":
    sampling_rate = 49000
    return sampling_rate
  if string_tune == "A":
    sampling_rate = 55000
    return sampling_rate
  else:
    string_input()
    return

def continuous_running():
  sampling_rate = string_input()
  while (True):
    recording = audio_record(sampling_rate)
    transform = compute_fft(recording.flatten())
    hps_result = Harmonic_Product_Spectrum(transform)
    sampling_freq = 44100
    frequencies = np.fft.fftfreq(int((len(hps_result)*2)/1), 1 / sampling_freq)[:len(transform)]
    valid_indices = frequencies > 60
    hps_result[~valid_indices] = 0
    
    max_index = np.argmax(hps_result)
    fundamental_frequency = frequencies[max_index]
    print(fundamental_frequency+20)
    Determine_Sharp_Flat(fundamental_frequency+20)
    if keyboard.is_pressed('q') or keyboard.is_pressed('Q'):
      sampling_rate = string_input()



continuous_running() 
    
  
