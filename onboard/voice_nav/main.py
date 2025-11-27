#!/usr/bin/env python3
# coding: utf-8

import sys
import os

from jetson_voice import ASR, AudioInput, ConfigArgParser, list_audio_devices

original_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')


    
    
parser = ConfigArgParser()

parser.add_argument('--model', default='matchboxnet', type=str, help='path to model, service name, or json config file')
parser.add_argument('--mic', default=11, type=str, help='device name or number of input microphone')
parser.add_argument('--wav', default=None, type=str, help='path to input wav/ogg/flac file')
parser.add_argument('--list-devices', action='store_true', help='list audio input devices')
args = parser.parse_args()
    
# load the model
asr = ASR(args.model)

# create the audio input stream
stream = AudioInput(wav=args.wav, mic=args.mic, 
                     sample_rate=asr.sample_rate, 
                     chunk_size=asr.chunk_size)

print("Start speaking")
# run transcription
for samples in stream:
    results = asr(samples)
    
    if asr.classification:
        with open("/jetson-voice/VoiceNav/data.txt", "w") as file:
            file.write(f"{results[0]},{results[1]}")
        print(f"class '{results[0]}' ({results[1]:.3f})")

print('\naudio stream closed.')
