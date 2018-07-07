import sounddevice as sd
import itertools
import librosa
import soundfile
import numpy as np
import time
import logging


class Listen:
    def __init__(self):
        self.DURATION = 20                    #ms clip
        self.magnitudo = []                   #array for the magnitude
        self.audiodata = []                   #processing the audio data
        self.recording = False                #flag start recording
        self.end_count = 0                    #counter for ending flag
        self.start_count = 0                  #counter for the beginning
        self.samplerate = 16000.0             #samplerate
        self.high = 2000                      #highest freq
        self.low = 100                        #lowest freq
        self.delta_f = (self.high - self.low) / 79           #79 adalah pembagi layar
        self.fftsize = np.ceil(self.samplerate / self.delta_f).astype(int) 
        self.low_bin = int(np.floor(self.low / self.delta_f))
        self.gain = 3                         #gain volume
        self.stopper = False                  #flag untuk stop
        self.debug = False                    
        self.phrase = ""
        self.avg_rms = []                     #untuk keperluan rms dan kalibrasi trigger

        
    def start(self, thres=0, timeout=5, process=None, 
              startpadding=10,
              endpadding=20,
              fullfilename=None, 
              partfilename=None):
        
        if process != None:
            if not callable(process): 
                raise TypeError('process must be function not called.')
            else:
                self.fnc = process
                
        self.startpadding = startpadding
        self.endpadding = endpadding
        self.fullfilename = fullfilename
        self.partfilename = partfilename
        self.starttime = time.time()
        self.avg_rms = []
        self.recording = False
        self.stopper = False
        self.start_count = 0
        self.end_count = 0
        self.thres = thres
        global cumulated_status
        try:
            cumulated_status = sd.CallbackFlags()

            with sd.InputStream(device=None, channels=1, callback=self.callback,
                                blocksize=int(self.samplerate * self.DURATION / 1000),
                                samplerate=self.samplerate):
                while True:
                    if self.stopper: break
                    self.endtime = time.time()
                    if timeout > 0:
                        if (self.endtime - self.starttime) >= timeout:
                            if process != None: 
                                self.pred_process()
                                if partfilename != None:
                                    self.write_to_file(self, partfilename)
                            break
                            
                    #await asyncio.sleep(0.1)
                    #time.sleep(0.1)
                    #break
                if self.fullfilename != None: soundfile.write(self.fullfilename, self.audiodata, int(self.samplerate))
                
            
            if cumulated_status:
                logging.warning(str(cumulated_status))
                
        except Exception as e:
            logging.info("=====================CRASH AT THIS=listen.py start")
            logging.debug(e)
            print(e)
            

    def callback(self, indata, frames, time, status):
        global cumulated_status

        try:

            cumulated_status |= status
            if any(indata):

                magnitude = np.abs(np.fft.rfft(indata[:,0], n=self.fftsize))
                magnitude *= self.gain / self.fftsize

                rms = librosa.feature.rmse(S=indata)
                rms = int(rms*32768)
                self.avg_rms.append(rms)

                self.start_count += 1
                if rms >= self.thres:
                    self.end_count = 0
                    if not self.recording and (self.start_count > self.startpadding):
                        self.audiodata = []
                        self.magnitudo = []
                        self.recording = True
                        if self.debug: print('O', end='', flush=False)
                        self.audiodata.extend(itertools.chain(indata.tolist()))
                        self.magnitudo.append(magnitude)

                    else:
                        if self.debug: print('x', end='', flush=False)
                        #just add to the list
                        self.audiodata.extend(itertools.chain(indata.tolist()))
                        self.magnitudo.append(magnitude)

                else:
                    if self.recording:
                        self.audiodata.extend(itertools.chain(indata.tolist()))
                        self.magnitudo.append(magnitude)

                    if (self.end_count > self.endpadding) and self.recording:
                        self.recording = False
                        self.end_count = 0
                        if self.debug: print('X', end='', flush=False)
                        self.start_count = 0
                        self.stop()
                        self.pred_process()
                    else:
                        if self.debug: print('.', end='', flush=False)
                        self.end_count += 1
        except Exception as e:
            logging.warning("ERROR- Callback in listen.py problem : " + str(e))
            pass
        
    def stop(self):
        self.stopper=True
    
    def calibrate(self, timeout=5):
        self.start(thres=0, timeout=timeout)
        if self.debug: print("\n\nThe average rms is :",np.average(self.avg_rms), 
                             ", Maximum:", np.max(self.avg_rms),
                             ", Minimum:", np.min(self.avg_rms))
        
    def pred_process(self):
        self.fnc()
        
    def set_process(self, fnc):
        self.fnc = fnc
        
    def listen_phrase(self):
        self.stopper = False
    
    def write_to_file(self,filename):
        soundfile.write(filename, self.audiodata, 16000)
        if self.debug: print("Done writing File", filename)


#async def begin_listen():
#    global loop
#    ear.waiter = False
#    await asyncio.sleep(0.1)
#    dp = loop.create_task(ear.start(filename="Test.wav",thres=800))
#    await asyncio.wait([dp])
#    ear.stop_listen()
    
#async def stop_listen():
#    print("Called - stopmer")
#    for i in range(11):
#        await asyncio.sleep(1)
#        print(i)
#        if i == 10:
#            ear.stop()