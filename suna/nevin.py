import pyaudio
import struct
import math
import pyautogui
INITIAL_TAP_THRESHOLD = 0.1
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME 
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME
global c
def get_rms( block ):

    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = MAX_TAP_BLOCKS+1 
        self.quietcount = 0 
        self.errorcount = 0

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None            
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No input device" )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def tapDetected(self):
        global c

        c=c+1
        
        

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except e:
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        amplitude = get_rms( block )
        if amplitude > self.tap_threshold:
            self.quietcount = 0
            self.noisycount += 1
        else:            
            if 1 <= self.noisycount <= MAX_TAP_BLOCKS:
                self.tapDetected()
            self.noisycount = 0
            self.quietcount += 1

def auto(c):
        if(selection==1):
            if c==1:
                pyautogui.press('right')
            if c==2:
                pyautogui.press('left')
            if c==3:
                pyautogui.press('esc')    
        if(selection==2):
            pyautogui.press('volumemute')
        if(selection==3):
            pyautogui.press('space',interval=0.25)
        print (c)

if __name__ == "__main__":
    c=0
    print("Welcome, What would you like to automate today?")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Press Number Followed by Enter")
    print("SlideShow-1, Music-2, Video-3")
    selection=int(input());
    tt = TapTester()
    
    for i in range(1000):
        if(i%20==0):
            if(c>0):
                auto(c)
            c=0
        tt.listen()




        
