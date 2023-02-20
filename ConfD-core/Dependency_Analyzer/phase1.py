import operator as op
import sys
import json
import os
import subprocess

###################################################
input_json = open("mke2fs_constraints_parameters.json", "r")
data = json.load(input_json)


####################################################
#value Type
####################################################

def value_type_identify(line):
    for line1 in line:
        if "Data type = " in line1:
            result = line1.strip("Data type = *")
            return result

def value_type_extract(files,json_dic):
    for file_name in files:
        tmp=json_dic[file_name]
        tmp["value_type"] = value_type_identify(files[file_name])
        tmp1 = data[file_name]
        tmp["flag"] = tmp1["flag"]
        tmp["takes_value"] = tmp1["takes_value"]
    return json_dic

#######################################################
#Data Range constraint extract
#######################################################

def value_range_max_identify(line):
    print("inside value range")
    for line1 in line:
        if "Max value = " in line1:
            result=line1.split(' ')
            #result = line1.strip("Max value = i32") #strip contain 3,2 so cannot use it
            print(result)
            return result[4]

def value_range_min_identify(line):
    for line1 in line:
        if "Min value" in line1:
            result=line1.split(' ')
            #result = line1.strip("Min value = i32") #strip contain 3,2 so cannot use it
            return result[4]

def whole_constrint(files,json_dic):
    for file_name in files:
        tmp=json_dic[file_name]
        tmp["value_range_max"] = value_range_max_identify(files[file_name])
        tmp["value_range_min"] = value_range_min_identify(files[file_name])
    return json_dic

####################################################
#trace comparison for dependency
####################################################

def depen_error_line(file1, file2):
    for line1 in file1:
        for line2 in file2:
            line1 = line1.replace(" ", "")  # delate space
            line2 = line2.replace(" ","")
            if line1 == line2:
                if "@com_err" in line1 or "@fprintf" in line1:
                    #print("found error line")
                    return line1
    return False


def dic_revise(json_dic, file_name1, file_name2, result):  #update json_dic dependency
    #update trace1 dependency

    tmp_dic1=json_dic[file_name1].copy()
    # revsie json "dependency"
    tmp1_arr=tmp_dic1["dependency"].copy()
    #tmp1_arr.append(file_name2)
    tmp1_arr.append(result)
    tmp_dic1["dependency"]=tmp1_arr
    json_dic[file_name1]=tmp_dic1
    #update trace2 dependency
    tmp_dic2 = json_dic[file_name2].copy()
    #revise json dependency
    tmp2_arr=tmp_dic2["dependency"].copy()
    tmp2_arr.append(file_name1)
    tmp_dic2["dependency"]=tmp2_arr
    json_dic[file_name2]=tmp_dic2
    return json_dic


def Trace_compare(file1,file2, f1_name, f2_name):# compare the trace and print the common line
    for line1 in file1:
        for line2 in file2:
            #line1 = line1.replace(" ", "")  # delate space
            #line2 = line2.replace(" ","")
            if line1 == line2:
                print ("found common line")
                if "@com_err" in line1 or "@fprintf" in line1:
                    print ("found error line")
                    text_file = open(f1_name+f2_name, "w")
                    n = text_file.write(line1)  #add file names to exising file so that we can find out which parameter we need to revise in the future
                    text_file.close()
                    #cmd='opt -load ~/projects/llvm-project-llvmorg-13.0.1/llvm/build1/lib/libTestPass.so -enable-new-pm=0 -test ~/projects/e2fsprogs-1.46.5/build/misc/mke2fs.ll'
                    #subprocess.call(cmd)
                    #text_file1 = open("sample1.txt", "r")
                    #for line3 in text_file1:
                       # if f1_name not in line3:
                            #return line3

    for line1 in file1:
        for line2 in file2:
            #if line1 == line2:
            if line1 == line2 and ("Data type =" not in line1) and ("Max value =" not in line1) and ("Min value =" not in line1):
                # add "Data type, Max value, Min value" commne line identification
                return f2_name
    return False

def Trace_whole_compare(files,json_dic):#comapre all files and fill out the dependency
    file_arr=[]
    file_name_arr=[]
    for file_name in files:
        file_arr.append(file_content_dic[file_name])
        file_name_arr.append(file_name)
    for i in range(len(file_arr)-1):
        for j in range(i+1, len(file_arr)):
            print(file_name_arr[i])
            result = Trace_compare(file_arr[i], file_arr[j], file_name_arr[i], file_name_arr[j])
            if result:
                json_dic=dic_revise(json_dic, file_name_arr[i], file_name_arr[j], result)
                depen = depen_error_line(file_arr[i], file_arr[j])
    return json_dic


####################################################################
#file initialization
####################################################################

default_dic={"id": 0,
                # "arg": "-b",
                "flag": None,
                "value_type": "unknown",
                "takes_value": None,
                "value_range_max": None, # (2^0 to 2^2)*1024
                "value_range_min": None,
                #"dependency":{}}
                "dependency":[]}
        #"operation":[]}

def read_files(argv):#get default dic and file lines
    file={}
    json_dic = {}
    for i in range(1,len(sys.argv)):
        tmp_dic=default_dic.copy()
        tmp_dic["id"]=i
        json_dic[sys.argv[i]]=tmp_dic
        with open(sys.argv[i], "r") as c:
            file[sys.argv[i]] = c.read().splitlines()
    return file,json_dic

###########################################################
#main run
###########################################################

print(sys.argv)
print(len(sys.argv))

file_content_dic,json_dic=read_files(sys.argv) #get default dic and file lines
json_dic=value_type_extract(file_content_dic,json_dic)
json_dic=whole_constrint(file_content_dic,json_dic) #revise icmp contraint

if len(sys.argv) > 2:
    json_dic=Trace_whole_compare(file_content_dic,json_dic) ## extract dependency and revise dependency

with open('result.json', 'w') as f:             #json file write
        json.dump(json_dic, f, ensure_ascii=False, indent=4)

#print(file_content_dic)
print(json_dic)
