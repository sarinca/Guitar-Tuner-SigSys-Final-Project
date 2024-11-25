# main file for the tuner
import sounddevice as sd
import numpy as np
import math
import copy
import matplotlib.pyplot as plt

#defined variables
Notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
sampling_rate = 44100
harmonic_number = 4
#matching of guitar audios
def Find_Closest_Note(Fin):
  Notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
  Concert_Pitch = 440 #Hz
  x = round(12*math.log2(Fin/Concert_Pitch))
  Note = Notes[x%12]
  closest_pitch = round(Concert_Pitch*pow(2,(x/12)), 2)
  return Note, closest_pitch

def Determine_Sharp_Flat(Fin):
  note, close_pitch = Find_Closest_Note(Fin)
  print("closest note")
  print(note)
  print("close pitch")
  print(close_pitch)
  if (Fin < close_pitch):
    print("flat")
  elif (Fin > close_pitch):
    print("sharp")

#recording audio
def audio_record():
    seconds = 2 #in seconds
    sampling_rate = 44100
    print("Start new recording. Play your note and wait for recording to finish")
    audio = sd.rec(int(seconds*sampling_rate), samplerate=sampling_rate, channels = 1) #maybe need to change channels to 1
    sd.wait()
    Time = np.linspace(0,seconds, len(audio))
    print("finished recording")
    # sd.play(audio, sampling_rate)
    return audio, Time

# def plot_graph(fourier, aud,t):
#   fig = plt.subplot(2,1,1)
# #plot the time domain graph
#   fig.plot(t,aud)
#   fig.set_title("Time Domain Graph of Audio Recording")
#   fig.set_xlabel("Time")
#   fig.set_ylabel("Audio Recording")

# #plot to the magnitude of the dft
#   frequency = np.fft.fftfreq(len(aud), (1/sampling_rate))
#   fig = plt.subplot(2,1,2)
#   fig.plot(frequency, fourier)
#   fig.set_title("Discrete Fourier Transfrom Magnitude")
#   fig.set_xlabel("Frequency in Hz")
#   fig.set_ylabel("Density/Magnitude")
#   #presenting the 2 graphs
#   plt.tight_layout()
#   plt.show()
#   return
def Harmonic_Product_Spectrum(sig):
   
  # length = math.ceil(sig.size/i+1)
  sig_copy = copy.copy(sig) #due to unique behavior of the assignment statements
   #multiplication & downsampling
  harmonic_product_spectrum = copy.deepcopy(sig)
  for index in range(1,harmonic_number+1,1):
   length = int(np.ceil(sig.size/index))
   #potential place to debug
   #harmonic_product_spectrum_copy = np.multiply(harmonic_product_spectrum[:length],sig_copy[::index])
  #  print(harmonic_product_spectrum[:length])
  #  print(sig_copy[::index])
   harmonic_product_spectrum[:length] *= sig_copy[::index]
  
  return harmonic_product_spectrum


def compute_fft(recording, t): 
    # window = np.hanning(len(recording))
    # recording_windowed = recording.flatten() * window
    dft = np.fft.fft(recording)
    dft = abs(dft)
    # frequency_bins = np.fft.fftfreq(len(recording), d=1/sampling_rate)
    # magnitude_spectrum = np.abs(np.fft.fft(recording.flatten()))
    # print("Frequency Bins:", frequency_bins[:10])  # Print first 10 frequency bins
    # print("Magnitude Spectrum:", magnitude_spectrum[:10])  # Print first 10 magnitudes
    # magnitude_spectrum[:int(50 * len(recording) / sampling_rate)] = 0  # Remove below 50 Hz
    # max_index = np.argmax(magnitude_spectrum)
    # fundamental_frequency = abs(frequency_bins[max_index])
    # print("Fundamental Frequency from FFT:", fundamental_frequency)
    # print("dft")
    # print(dft)
    main_hum_suppression_index = 61 #main hum corresponds to outside noise which needs to get zerod out, typically occurs between 50 to 60 hz 
    # for index in range(61+1):
    #    dft[index] = 0
    return dft



def continuous_running():
  while (True):
  #print(sd.query_devices()) used for debugging purposes;
    recording, t = audio_record()
    transform = compute_fft(recording, t)
    print("dft array")
    print(transform)
    # plot_graph(dft,recording, Time)
    #do all the work
    hps_result = Harmonic_Product_Spectrum(transform)
    max_hps_result = np.argmax(hps_result)
    print("max hps: ", max_hps_result)
    fundamental_frequency = (sampling_rate*hps_result[max_hps_result]) / harmonic_number
    # fundamental_frequency = (sampling_rate*max_hps_result) / len(transform)
    window = recording.shape[0]/sampling_rate
    print("length of recording: ", len(recording))
    # fundamental_frequency = max_hps_result*(sampling_rate/window)/harmonic_number
    print("fundamental freq")
    print(fundamental_frequency)
    Determine_Sharp_Flat(fundamental_frequency)



#   while (determinant == False):
#     target = input("Please type in either S for start or Q for ending the program: s")
#     if (target.lower() == 's'):
#       determinant = True
#       continuous_running(determinant)
#     if (target.lower() == 'q'):
#       print("Exitting program")
#       return
    
continuous_running() 
    
  
