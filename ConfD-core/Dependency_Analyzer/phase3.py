import operator as op
import sys
import json
import os
import subprocess

###########################################
# load final json file
#input: fianl json file, critical dependency file
###########################################
def read_json(argv): # json file to be a dictionary
    with open(argv) as json_file:
        data = json.load(json_file)
        return data

##########################################
#   revise final json file
##########################################
def revise_dic(dic,argv):
    with open(argv, "r") as c:
        file = c.read().splitlines()
    for line in file:
        print(line)
        tmp=line.split(" ")
        print(tmp[0])
        if len(tmp)!=3: #if cannot be split into three parts, the file is problematic
            print("The second file is problematic")
            continue
        else:
            org = dic[tmp[0]]    #revise dependency parts
            de=org["dependency"]
            if tmp[1] not in de:
                print("not in dependency")
            else:
                de.remove(tmp[1])
            if "critical" not in org:    #add critical parts
                org["critical"]={tmp[1]:tmp[2]}
            else:
                next_org=org["critical"]
                if tmp[1] in next_org:
                    print("Existing in critical")
                    continue
                else:
                    next_org[tmp[1]]=tmp[2]
    return dic

##########################################
#                main
##########################################
print(sys.argv)
print(len(sys.argv))
if len(sys.argv) == 3:
    dic=read_json(sys.argv[1])
    dic=revise_dic(dic,sys.argv[2])
else:
    print("error, lack files")
with open(sys.argv[1], 'w') as f:  # json file write
    json.dump(dic, f, ensure_ascii=False, indent=4)
print(dic)
