# imports 
import argparse
import numpy as np
import bci_helper as BCI  
from pylsl import StreamInlet, resolve_byprop
import os

class MuseStream:
    
    # Attributes
    BUFFER_LENGTH   = 5  
    EPOCH_LENGTH    = 1
    OVERLAP_LENGTH  = 0.8
    SHIFT_LENGTH    = EPOCH_LENGTH - OVERLAP_LENGTH
    TRAINING_LENGTH = 20
    INDEX_CHANNEL   = [0, 1 , 2, 3] # use all four electrodes
    N_CHANNELS      = 4

    # Class Variables 
    freq = 256
    eeg_raw = []
    recording = False
    filter_state = None
    
    def __init__(self):
        
        print('Connecting...')
        streams = resolve_byprop('type', 'EEG', timeout=2)
        if len(streams) == 0:
            raise RuntimeError('Can\'t find EEG stream.')
        
        # set up Inlet
        inlet = StreamInlet(streams[0], max_chunklen=12)
        eeg_time_correction = inlet.time_correction()

        # Pull relevant information
        info            = inlet.info()
        self.desc       = info.desc()
        self.freq       = int(info.nominal_srate())

        ## TRAIN DATASET HERE 

    def startRecording(self):
        self.recording = True
        
        try:
            while (self.recording == True):
                streams = resolve_byprop('type', 'EEG', timeout=2)
                inlet  = StreamInlet(streams[0], max_chunklen=12)
                # Obtain EEG data from the LSL stream
                eeg_data, timestamp = inlet.pull_chunk(
                    timeout=1, max_samples=int(self.SHIFT_LENGTH * self.freq))

                ch_data = np.array(eeg_data)[:, self.INDEX_CHANNEL]

                # Update EEG data and apply filter
                self.eeg_raw, self.filter_state = BCI.update_buffer(
                    self.eeg_raw, 
                    ch_data, 
                    notch=True,
                    filter_state = self.filter_state)
        except KeyboardInterrupt:
            print("Exception")

    def stopRecording(self):
        self.recording = False
