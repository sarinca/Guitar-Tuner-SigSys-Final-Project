# main file for the tuner
import sounddevice as sd
import numpy

#defined variables
Notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


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
    print("start new recording")
    audio = sd.rec(int(seconds*sampling_rate), samplerate=sampling_rate, channels = 2)
    sd.wait()
    print("finished recording")
    sd.play(audio, sampling_rate)
    sd.wait()
    return audio




while True:
    #print(sd.query_devices()) used for debugging purposes
