import pyaudio
import numpy as np
import soundfile as sf
import os

import processing_functions

pa = pyaudio.PyAudio()

FS = 11025
CHUNK = 300
WORD = []


def listen():
    p = pyaudio.PyAudio()
    from_microphone = p.open(format=pyaudio.paInt16, channels=1, rate=FS, input=True, frames_per_buffer=CHUNK)
    return from_microphone


def rms(input_data):
    rms_value = np.sqrt(np.mean(np.power(input_data, 2)))
    return rms_value


if __name__ == '__main__':
    args = processing_functions.parse_arguments()
    base = processing_functions.utworz_baze(args.folder)
    print('Mozesz mowic!')
    INIT = True
    IS_REC = False
    BUFF = np.zeros(CHUNK * 3)
    REC = np.array([])
    SILENT = 0
    THRESHOLD = 800
    obliczenia = list()
    try:
        stream = listen()

        while True:
            data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
            rms_from_data = rms(data.astype(float))
            BUFF = BUFF[300:]
            BUFF = np.append(BUFF, data)
            if rms_from_data > THRESHOLD or IS_REC:
                if INIT:
                    IS_REC = True
                    REC = np.array([])
                    REC = np.append(REC, BUFF)
                    INIT = False
                else:
                    REC = np.append(REC, data)
                    if rms_from_data < THRESHOLD:
                        SILENT += 1
                    else:
                        SILENT = 0

                    if SILENT > 15:
                        IS_REC = False
                        INIT = True
                        REC = REC.astype(np.int16)
                        zeros = 2 * FS - len(REC)
                        zeros_arr = np.zeros(zeros)
                        REC_with_zeros = np.append(REC, zeros_arr)
                        REC_with_zeros = REC_with_zeros.astype(np.int16)
                        sf.write(file='word.wav', data=REC_with_zeros, samplerate=FS)
                        # save_file(REC, 'word.wav')
                        #print('RECORDING COMPLETE')
                        vector = processing_functions.calc_mfcc('word.wav')
                        wynik = processing_functions.klasyfikator_knn(base, vector, 15)
                        os.system('cls')
                        if len(obliczenia) < 3:
                            obliczenia.append(wynik)
                        for cyfra in range(len(obliczenia)):
                            print (obliczenia[cyfra], end = '')
                        print()
                        if len(obliczenia) == 3:
                            a = obliczenia[0]
                            znak = obliczenia[1]
                            b = obliczenia[2]
                            obliczenia = list()
                            if znak == '+':
                                print('=', end = '')
                                print(a + b)
                            elif znak == '-':
                                print('=', end = '')
                                print(a - b)
                            else:
                                print("Bledna skladnia")

                        os.remove('word.wav')

    except KeyboardInterrupt:
        print('KeyboardInterrupt has been caught')
