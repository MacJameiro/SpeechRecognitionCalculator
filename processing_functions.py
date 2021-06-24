import argparse
import math
import os
from python_speech_features import mfcc
import scipy.io.wavfile as wav

def parse_arguments():
    parser = argparse.ArgumentParser(description='Oblicz MFCC')
    parser.add_argument("-f", "--folder", help='Podaj sciezke do folderu')
    arguments = parser.parse_args()
    return arguments


def odleglosc_euklidesowa_wektorow(test, baza):
    distance = 0.0
    for i in range(len(baza)-1):
        for j in range(len(baza[i])):
            distance += (baza[i][j] - test[i][j]) ** 2
    return math.sqrt(distance)


def calc_mfcc(file_name):
    (rate, sig) = wav.read(file_name)
    mfcc_feat = mfcc(sig, rate)
    return mfcc_feat


def klasyfikator_knn(train, test, k):
    distances = list()
    for train_vec in train:
        dist = odleglosc_euklidesowa_wektorow(test, train_vec)
        distances.append((train_vec, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(k):
        neighbors.append(distances[i][0])

    #predykcja
    output_values = [vec[-1] for vec in neighbors]
    predicition = max(set(output_values), key=output_values.count)
    return predicition


def identyfikator(nazwa_pliku):
    indeks = nazwa_pliku.find('.')
    nowa_nazwa = nazwa_pliku[:indeks]
    return (nowa_nazwa)


def utworz_baze(path):
    lista_plikow = os.listdir(path)

    baza = list()

    for plik in lista_plikow:
        sciezka_pliku = os.path.join(path, plik)
        mfcc_pliku = calc_mfcc(sciezka_pliku)
        mfcc_pliku_lista = mfcc_pliku.tolist()
        nazwa_pliku_bez_indeksu = identyfikator(plik)
        if nazwa_pliku_bez_indeksu[-3] == '+':
            mfcc_pliku_lista.append('+')
        elif nazwa_pliku_bez_indeksu[-3] == '-':
            mfcc_pliku_lista.append('-')
        elif int(nazwa_pliku_bez_indeksu[-4]) == 0:
            mfcc_pliku_lista.append(int(nazwa_pliku_bez_indeksu[-3]))
        else:
            mfcc_pliku_lista.append(int(nazwa_pliku_bez_indeksu[-4]) * 10 + int(nazwa_pliku_bez_indeksu[-3]))
        baza.append(mfcc_pliku_lista)
    return baza


if __name__ == '__main__':

    args = parse_arguments()
    path = args.folder
    lista_plikow = os.listdir(path)

    baza = list()

    for plik in lista_plikow:
        sciezka_pliku = os.path.join(path, plik)
        mfcc_pliku = calc_mfcc(sciezka_pliku)
        mfcc_pliku_lista = mfcc_pliku.tolist()
        nazwa_pliku_bez_indeksu = identyfikator(plik)
        if nazwa_pliku_bez_indeksu[-3] == '+':
            mfcc_pliku_lista.append('+')
        elif nazwa_pliku_bez_indeksu[-3] == '-':
            mfcc_pliku_lista.append('-')
        elif int(nazwa_pliku_bez_indeksu[-4]) == 0:
            mfcc_pliku_lista.append(int(nazwa_pliku_bez_indeksu[-3]))
        else:
            mfcc_pliku_lista.append(int(nazwa_pliku_bez_indeksu[-4]) * 10 + int(nazwa_pliku_bez_indeksu[-3]))
        baza.append(mfcc_pliku_lista)



