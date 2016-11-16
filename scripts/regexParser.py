# -*- coding: utf-8 -*-

import re
import pdb
from itertools import cycle
import json
import io
import operator

districts = ["AÇORES", "AVEIRO", "BEJA", "BRAGA", "BRAGANÇA", "CASTELO BRANCO",
		 "COIMBRA", "ÉVORA", "FARO", "GUARDA", "LEIRIA", "LISBOA",
		 "MADEIRA", "PORTO", "PORTALEGRE", "SANTARÉM", "SETUBAL", "VIANA DO CASTELO",
		 "VILA REAL", "VISEU"]

#Default file name
filepath = "QuemOAvisa.txt"


#File creation in there is none
try: 
    open(filepath,'x')
except FileExistsError:
        print("File already exists!")

read_file = open(filepath,'r')
dictionary = {}

def finish(dictionary):
    f = io.open("QuemOAvisa.txt", 'w')
    f.write(json.dumps(dictionary, sort_keys = True, indent=4, separators=(',', ': ')))
    f.close()
    print('finish')

def parseOperation(operation):
    for district in districts:
        if operation.rstrip() == district:
            return -1
    newOperation = {}
    newOperation['date'] = operation.split(' ')[0]
    if len(operation.split(' ')) > 1:
        temp = operation.split(' ')[1]
        time = temp.split('/')
    else:
        time = operation.split(' ')[1]

    newOperation['start'] = time[0]
    if len(time) == 2:
        newOperation['finish'] = time[1]
    newOperation['address'] = operation.split(' ',2)[2]
    return newOperation

def regexParser():
    with open(filepath, 'r', encoding='utf-8') as f_in:
        lines = filter(None, (line.rstrip() for line in f_in))

    #itr = cycle(lines)
    #line = itr
        ops = []
        currentDistrict = ""
        districtFound = False
        for line in lines:
            if "THE END" in line:
                break
            if districtFound:
                currentOp = parseOperation(line)
                if not currentOp == -1:
                    ops.append(currentOp)
                    continue
                else:
                    dictionary[currentDistrict] = ops
                    districtFound = False
                    ops = []
            for district in districts:
                if district in line:
                    districtFound = True
                    currentDistrict = district
                    break
        finish(dictionary)
