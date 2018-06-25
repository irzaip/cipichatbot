
# coding: utf-8

# In[1]:


import sounddevice as sd
import itertools
import librosa
import soundfile
import numpy as np
import time
import asyncio

waiter = False

class Listen:
    def __init__(self):
        self.DURATION = 20
        self.magnitudo = []
        self.audiodata = []
        self.recording = False
        self.end_count = 0
        self.start_count = 0
        self.samplerate = 16000.0
        self.high = 2000
        self.low = 100
        self.delta_f = (self.high - self.low) / 79
        self.fftsize = np.ceil(self.samplerate / self.delta_f).astype(int)
        self.low_bin = int(np.floor(self.low / self.delta_f))
        self.gain = 3
        self.waiter = False
        
    async def listening(self, length=1, thres=0, filename=None):
        self.thres=thres
        global cumulated_status, waiter
        try:
            cumulated_status = sd.CallbackFlags()

            with sd.InputStream(device=None, channels=1, callback=self.callback,
                                blocksize=int(self.samplerate * self.DURATION / 1000),
                                samplerate=self.samplerate):
                while True:
                    if waiter: break
                    await asyncio.sleep(0.0001)
                    #time.sleep(0.1)
                    #break
                if filename != None: soundfile.write(filename, self.audiodata, int(self.samplerate))
                
                
            if cumulated_status:
                logging.warning(str(cumulated_status))
        except Exception as e:
            print(e)
            

    def callback(self, indata, frames, time, status):
        global cumulated_status
        
        cumulated_status |= status
        if any(indata):
            
            magnitude = np.abs(np.fft.rfft(indata[:,0], n=self.fftsize))
            magnitude *= self.gain / self.fftsize
            
            rms = librosa.feature.rmse(S=indata)
            rms = int(rms*32768)

            self.start_count += 1
            if rms>=self.thres:
                self.end_count = 0
                if not self.recording and (self.start_count > 20):
                    self.audiodata = []
                    self.magnitudo = []
                    self.recording = True
                    if debug: print('O', end='', flush=True)
                    self.audiodata.extend(itertools.chain(indata.tolist()))
                    self.magnitudo.append(magnitude)
                    
                else:
                    if debug: print('x', end='', flush=True)
                    #just add to the list
                    self.audiodata.extend(itertools.chain(indata.tolist()))
                    self.magnitudo.append(magnitude)
            
            else:
                if self.recording:
                    self.audiodata.extend(itertools.chain(indata.tolist()))
                    self.magnitudo.append(magnitude)
                
                if (self.end_count > 20) and self.recording:
                    self.recording = False
                    self.end_count = 0
                    if debug: print('X', end='', flush=True)
                    self.start_count = 0
                else:
                    if debug: print('.', end='', flush=True)
                    self.end_count += 1
                    
    def gee(self):
        print("fftsize:",self.fftsize)
        
    def stop(self):
        self.waiter=True


# In[2]:


async def main():
    debug=True
    a=Listen()
    dp = loop.create_task(a.listening(length=1,filename="Test.wav",thres=800))
    await asyncio.wait([dp])
    print("I am finished")


# In[ ]:


debug=True
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


# In[ ]:


waiter=True


# In[ ]:


a.waiter=True

