# main file for the tuner
import sounddevice as sd
import numpy as np
import math
import mathplotlib.pyplot as plt

#defined variables
Notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
sampling_rate = 44100

#matching of guitar audios
def Find_Closest_Note(Fin):
  Notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
  Concert_Pitch = 440 #Hz
  x = round(12*math.log2(Fin/Concert_Pitch))
  Note = Notes[x%12]
  closest_pitch = round(Concert_Pitch*pow(2,(x/12)), 2)
  return Note, closest_pitch

def Determine_Sharp_Flat(Fin):
  close_pitch = Find_Closest_Note(Fin)[1]
  if (Fin < close_pitch):
    print("flat")
  elif (Fin > close_pitch):
    print("sharp")

#recording audio

def audio_record():
    seconds = 5 #in seconds
    sampling_rate = 44100
    print("Start new recording. Play your note and wait for recording to finish")
    audio = sd.rec(int(seconds*sampling_rate), samplerate=sampling_rate, channels = 2)
    sd.wait()
    print("finished recording")
    sd.play(audio, sampling_rate)
    sd.wait()
    return audio

def plot_graph(fourier, aud,t):
  fig = plt.subplot(2,1,1)
#plot the time domain graph
  fig.plot(t,aud)
  fig.set_title("Time Domain Graph of Audio Recording")
  fig.set_xlabel("Time")
  fig.set_ylabel("Audio Recording")

#plot to the magnitude of the dft
  frequency = np.fft.fftfreq(len(aud), (1/sampling_rate))
  fig = plt.subplot(2,1,2)
  fig.plot(frequency, fourier)
  fig.set_title("Discrete Fourier Transfrom Magnitude")
  fig.set_xlabel("Frequency in Hz")
  fig.set_ylabel("Density/Magnitude")
  #presenting the 2 graphs
  plt.tight_layout()
  plt.show()
  return

while True:
    #print(sd.query_devices()) used for debugging purposes;
    recording = audio_record()
    Time = np.linspace(0,len(recording), 1000, endpoint=True)
    dft = np.fft.fft(recording)
    dft = np.abs(dft)
    plot_graph(dft,recording, Time)
    

    break
