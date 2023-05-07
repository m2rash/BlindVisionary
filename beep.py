import pyaudio
import numpy as np


class beeper:

    def __init__(self, maxDistance = 2.0, queueLength = 3, duration=0.2):
        self.maxDistance = maxDistance
        self.distQueue = []
        self.duration = duration
        self.queueLength = queueLength

    def feedDistAndBeep(self,dist):
        if len(self.distQueue) == 0:
            self.distQueue = self.queueLength * [dist]
        else:
            self.distQueue.pop(0)
            self.distQueue.append(dist)

        meanDist = np.mean(self.distQueue)

        self.beep(meanDist)


    def play_stuff(self, samples, fs=44100, volume=0.5):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)

        # play. May repeat with different volume values (if done interactively) 
        stream.write(volume*samples)
        stream.stop_stream()
        stream.close()
        p.terminate()


    def beep(self,distance):
        f = max(740.0*(1-distance/self.maxDistance),0)
        #f = 740.0        # sine frequency, Hz, may be float    
        #duration = 0.2   # in seconds, may be float
        fs = 44100       # sampling rate, Hz, must be integer
        # generate samples, note conversion to float32 array
        # for paFloat32 sample values must be in range [-1.0, 1.0]
        samples = (np.sin(2*np.pi*np.arange(fs*self.duration)*f/fs)).astype(np.float32)


        self.play_stuff(samples, fs=44100, volume=0.5)
