import argparse
import numpy as np
import os
import soundfile as sf


def parse_arguments():
    parser = argparse.ArgumentParser(description='Usun cisze ze swoich nagrań')
    parser.add_argument("-f", "--folder", help='Podaj sciezke do folderu z plikami wave')
    arguments = parser.parse_args()
    return arguments


def remove_silence(wave_arg, new_path):
    data, fs = sf.read(wave_arg)
    count = 0
    chunk = []
    rms = []
    for i in data:
        count += 1
        chunk.append(i)
        if count == 300:
            rms.append(np.sqrt(np.mean(np.power(chunk, 2))))
            chunk.clear()
            count = 0

    begin = 0
    for i in rms:
        if i > 0.015:
            begin = rms.index(i)
            break

    rms.reverse()

    end = 0
    for i in rms:
        if i > 0.015:
            end = len(rms) - rms.index(i)
            break

    new_data = data[begin * 300:end * 300]
    zeros = 2 * fs - len(new_data)
    zeros_arr = np.zeros(zeros)
    new_data_with_zeros = np.append(new_data, zeros_arr)

    sf.write(os.path.join(new_path, os.path.split(wave_arg)[1]), new_data_with_zeros, fs)


if __name__ == '__main__':
    args = parse_arguments()
    sciezka = args.folder
    lista_plikow = os.listdir(sciezka)
    pop_sciezka = os.path.join(sciezka, r'poprawione')

    if not os.path.exists(pop_sciezka):
        os.mkdir(pop_sciezka)

    for plik in lista_plikow:
        remove_silence(os.path.join(sciezka, plik), pop_sciezka)

    print('Pliki bez ciszy znajduja sie tutaj: {}'.format(pop_sciezka))
