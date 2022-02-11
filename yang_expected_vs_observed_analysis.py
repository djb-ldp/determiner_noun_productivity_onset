import pandas as pd
import glob
import sys
import os
import re
import string
import fileinput
import difflib
import random
import math

def org_yang_analysis_1_2(pdf, child_parent):

    result = []


    pdf = [x for x in pdf if (len(x.split()) == 2) and (x.split()[0] == 'a' or x.split()[0] == 'the')]


    def Harmonic(n):
        s=0
        for i in range(1, n+1):
            s+=1.0/i
        return s

    def expected_overlap(N, S, r, b):
        hN = Harmonic(N)
        p = 1.0/(r*hN)
        eo = 1 - sum( [ math.pow((p*di+1.0-p), S) for di in [b, 1.0-b] ] ) + math.pow(1-p, S)
        assert eo>=-1, '%d, %.6f'%(r, eo)
        return eo

    def average_expected_overlap(N, S, b):
        sumo = 0
        for r in range(1, N+1):
            sumo += expected_overlap(N, S, r, b)
        return sumo/N

    def freqcounts(word, data):
        ccc = 0
        for i in range(0, len(data)):
            if word == data[i].split()[1]:
                ccc += 1
        return ccc

    def uniqwords(data):
        ccc = 0
        uniqw = []
        for i in range(0, len(data)):
            nnn = data[i].split()[1]
            if nnn not in uniqw:
                uniqw.append(nnn)
                ccc += 1
        return ccc

    def calculate_overlap(data): # returns s, n, and empirical overlap
        result = []
        result.append(len(data))

        uniqnoun = []
        for i in range(0, len(data)):
            nnn = data[i].split()[1]
            if nnn not in uniqnoun:
                uniqnoun.append(nnn)
        result.append(len(uniqnoun))

        both = 0 # counts of nouns that have overlap
        for i in range(0, len(uniqnoun)):
            a = 0
            the = 0
            for j in range(0, len(data)):
                if uniqnoun[i] == data[j].split()[1]:
                    if data[j].split()[0] == 'a':
                        a = 1
                    if data[j].split()[0] == 'the':
                        the = 1
            if a == 1 and the == 1:
                both += 1

        result.append(both)

        return result

    def find_bias(data):

        uniqw = []
        for i in range(0, len(data)):
            nnn = data[i].split()[1]
            if nnn not in uniqw:
                uniqw.append(nnn)


        big = 0
        small = 0
        for i in range(0, len(uniqw)):
            a = 0
            the = 0
            for j in range(0, len(data)):
                if uniqw[i] == data[j].split()[1]:
                    if data[j].split()[0] == 'a':
                        a += 1
                    else:
                        the +=1
            if a >= the:
                big += a
                small += the
            else:
                big += the
                small += a
        return float(big)/float(big+small)
    
    p_tmp = calculate_overlap(pdf)
    p_S = int(p_tmp[0])
    p_N = int(p_tmp[1])
    p_O = int(p_tmp[2])
    p_bias = find_bias(pdf)
    
    



    
    
    return [child_parent, p_N, p_S, p_bias, (float(p_S)/float(p_N)), (float(p_O)/float(p_N)), average_expected_overlap(p_N, p_S, p_bias)]
    
    
