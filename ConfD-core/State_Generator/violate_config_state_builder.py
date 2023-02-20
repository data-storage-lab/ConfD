#!/usr/bin/python3

import cmd
import json
import copy
import math
import sys, getopt
import random
import pdb
import os

from setuptools import Command

depth = 0
states_made = 0

max_depth = 0
misspell = False

argument_key = {
    "blocksize": "-b", "cluster_size": "-C", "blocks-per-group": "-g", "flex_bg_size": "-G",
    "inode_size": "-I", "error_behavior": "-e", "inode_ratio": "-i", "num_inodes": "-N",
    "feature": "-O", "revision": "-r", "extended-options": "-E"                                             #Carson Added 10/30
    #"creator_os": "-o", "r_opt": "-r", "reserved_ratio": "-m", "filename": "-L", "fs_type": "-t" 
    #"version": "-V", "vebose": "-v" "force": "-F","quiet": "-q"
}

reverse_argument_key = {v: k for k, v in argument_key.items()}

feature_args = {
        "64bit", "bigalloc", "casefold", "dir_index", "dir_nlink",
        "ea_inode", "encrypt", "ext_attr", "extents", "extra_isize", 
        "filetype", "flex_bg", "has_journal", "huge_file", "inline_data",
        "journal_dev", "large_dir", "large_file", "metadata_csum", "metadata_csum_seed",
        "meta_bg", "mmp", "project", "quota", "resize_inode",
        "sparse_super", "sparse_super2", "stable_inodes", "uninit_bg", "verity"
        }
extended_args = {
    "encoding": "encoding=",
    "encoding_flags": "encoding_flags=",
    "mmp_update_interval": "mmp_update_interval=",
    "stride": "stride=",
    "stripe_width": "stride_width=",
    "offset": "offset=",
    "resize": "resize=",
    "lazy_itable_init": "lazy_itable_init=",  
    "lazy_journal_init": "lazy_journal_init=",  
    "no_copy_xattrs": None,
    "num_backup_sb": "num_backup_sb=",  
    "packed_meta_blocks": "packed_meta_blocks=",  
    "root_owner": "root_owner=",
    "test_fs": None,
    "discard": None,
    "nodiscard": None,
    "quotatype": "quotatype"  
}

journal_args = {
    "ext3_journal": "-j",
    "journal_size": "size=",
    "fast_commit_size": "fast_commit_size=",
    "location": "location=",
    "device": "device="
}


default_feature_args = {
        "64bit": "enable",
        "blocksize": 4096,
        "dir_index": "enable",
        "dir_nlink": "enable",
        "ext_attr": "enable",
        "extents": "enable",
        "extra_isize": "enable",
        "filetype": "enable",
        "flex_bg": "enable",
        "has_journal": "enable",
        "huge_file": "enable",
        "inode_size": 256,
        "inode_ratio": 16384,
        "large_file": "enable",
        "metadata_csum": "enable",
        "resize_inode": "enable",
        "sparse_super": "enable"
        }
        

class Configuration:
    arg = None
    
    def __init__(self):
        self.arg = dict()
        for a in default_feature_args:
            self.arg[a] = default_feature_args[a]

#finds next largest number power of 2
#https://www.techiedelight.com/round-next-highest-power-2/
def nextPow2(n):
    # decrement `n` (to handle cases when `n` itself
    # is a power of 2)
    n = n - 1
    
    # do till only one bit is left
    while n & n - 1:
        n = n & n - 1       # unset rightmost bit
    
    #'n' is now a power of two

    #return next power of two
    return n << 1

#looks up by id for constraint_data
def id_lookup(constraint_data, id):
    for i in constraint_data:
        if(constraint_data[i]['id'] == id):
            return(i)
    

#Takes command line style config, adds params to existing Configuration
def read_config(line, my_config):
    params = line.split(' -')
    #Parse command paramter
    for param in params:
        if(param != "(mke2fs)" and param != "\n" and param[0] != 'O'):
                    
            #print(param.strip().split(' '))
            key=param.strip().split(' ')[0]
            val=param.strip().split(' ')[1]
            my_config.arg[reverse_argument_key["-"+key]]=val
                    
            #print(reverse_argument_key["-"+key])
        
        #case '-O'
        elif (param[0] == 'O'):
            clean = param.strip().split(' ')[1].split(',')
            for c in clean:
                my_config.arg[c] = ""
            

#Determines if a given Configuration is valid within given constraints
def verify_config(my_config, constraint_data):
    #Step 1 - verify all numerical constraints
    #TODO account for postfixs on numbers
    for a in my_config.arg:
        if(a != "revision" and a != "encoding"):
            #print(constraint_data[a])
            #print(a + " : " + my_config.arg[a])
            if(constraint_data[a]["takes_value"] == "yes"):
                #Tests Max
                if(constraint_data[a]["value_range_max"] != None and (int(constraint_data[a]["value_range_max"]) < int(my_config.arg[a]))):
                    #print("Max:" + constraint_data[a]["value_range_max"])
                    #print("Act:" + my_config.arg[a])
                    #print(constraint_data[a])
                    #print(" Max violated")
                    return False
                #Tests Min
                if(constraint_data[a]["value_range_min"] != None and (int(constraint_data[a]["value_range_min"]) > int(my_config.arg[a]))):
                    #print(constraint_data[a])
                    #print(" Min violated")
                    return False
    
    #Step 2 - verify critical enabled/disabled and smaller
    for a in my_config.arg:
        if(a != "revision" and a != "encoding"):
            #print(constraint_data[a])
            #print(a + " : " + my_config.arg[a])
            if(constraint_data[a].get("critical", None) != None):
                #print(constraint_data[a]["critical"])
                for crit in constraint_data[a]["critical"]:
                    #print(crit + " : " + constraint_data[a]["critical"][crit])
                    #enabled crit test
                    if((constraint_data[a]["critical"][crit] == "enable") and ((my_config.arg.get(crit, None) == None) or (my_config.arg[crit] == "disable"))):
                        #print(constraint_data[a])
                        #print(crit + " violated")
                        #print("")
                        return False
                    if((constraint_data[a]["critical"][crit] == "disable") and (my_config.arg.get(crit, None) != None) and (my_config.arg[crit] == "enable")):
                        #print(constraint_data[a])
                        #print(crit + " violated")
                        #print("")
                        return False
                    #tests smaller
                    if((constraint_data[a]["critical"][crit] == "smaller") and (my_config.arg.get(crit, None) != None)):
                        if(int(my_config.arg[a]) < int(my_config.arg[crit])):
                            #print(constraint_data[a])
                            #print(crit + " violated")
                            #print("")
                            return False
    return True
    
#Generates states up to target number 
def generate(my_config, constraint_data, target_num, final_states, invalid_states, try_list):
    global states_made
    global depth
    global misspell
    depth += 1
    for id in try_list:
        #checks if valid id num
        if(id_lookup(constraint_data, id) != None):
            #print("lookin at " + id_lookup(constraint_data, id))
            #check if completed task
            if(states_made >= target_num):
                depth -= 1  
                return
               
            #checks if too deep
            if(depth > max_depth):
                depth -= 1
                return
               
               
            #creates new state(s) 
            new_configs = []
            temp = copy.deepcopy(my_config)
            new_configs.append(temp)
            
            #checks if arg already present
            if(my_config.arg.get(id_lookup(constraint_data, id), None) != None):
                if(default_feature_args.get(id_lookup(constraint_data, id), None) == None):
                    #case not defualt but dup
                    continue
                else:
                    #case default
                    if(constraint_data[id_lookup(constraint_data, id)]["takes_value"] == "no"):
                        #case no parameter
                        temp.arg[id_lookup(constraint_data, id)]="disable"
                    elif(constraint_data[id_lookup(constraint_data, id)]["value_range_min"] != None):
                        if(constraint_data[id_lookup(constraint_data, id)]["value_range_max"] != None):
                            #case min and max
                            temp2 = copy.deepcopy(my_config)
                            new_configs.append(temp2)
                            temp3 = copy.deepcopy(my_config)
                            new_configs.append(temp3)
                            
                            temp.arg[id_lookup(constraint_data, id)]=constraint_data[id_lookup(constraint_data, id)]["value_range_min"]
                            temp2.arg[id_lookup(constraint_data, id)]=constraint_data[id_lookup(constraint_data, id)]["value_range_max"]
                            temp3.arg[id_lookup(constraint_data, id)]=nextPow2(int(constraint_data[id_lookup(constraint_data, id)]["value_range_min"]) + 1)
                        else:
                            #case just min
                            temp.arg[id_lookup(constraint_data, id)]=constraint_data[id_lookup(constraint_data, id)]["value_range_min"]
                    else:
                        #case just max
                        temp.arg[id_lookup(constraint_data, id)]=1
                    
            else:  
                #case not a dup
                if(constraint_data[id_lookup(constraint_data, id)]["takes_value"] == "no"):
                    #case no parameter
                    temp.arg[id_lookup(constraint_data, id)]="enable"
                elif(constraint_data[id_lookup(constraint_data, id)]["value_range_min"] != None):
                    if(constraint_data[id_lookup(constraint_data, id)]["value_range_max"] != None):
                        #case min and max
                        temp2 = copy.deepcopy(my_config)
                        new_configs.append(temp2)
                        temp3 = copy.deepcopy(my_config)
                        new_configs.append(temp3)
                        
                        temp.arg[id_lookup(constraint_data, id)]=constraint_data[id_lookup(constraint_data, id)]["value_range_min"]
                        temp2.arg[id_lookup(constraint_data, id)]=constraint_data[id_lookup(constraint_data, id)]["value_range_max"]
                        temp3.arg[id_lookup(constraint_data, id)]=nextPow2(int(constraint_data[id_lookup(constraint_data, id)]["value_range_min"]) + 1)
                    else:
                        #case just min
                        temp.arg[id_lookup(constraint_data, id)]=constraint_data[id_lookup(constraint_data, id)]["value_range_min"]
                else:
                    if(constraint_data[id_lookup(constraint_data, id)]["value_range_max"] != None):
                        #case just max
                        temp2 = copy.deepcopy(my_config)
                        new_configs.append(temp2)
                        
                        temp.arg[id_lookup(constraint_data, id)]=constraint_data[id_lookup(constraint_data, id)]["value_range_max"]
                        temp2.arg[id_lookup(constraint_data, id)]=1
                    else:
                        #case no min/max
                        temp.arg[id_lookup(constraint_data, id)]=1
            
            
            
            for temp_config in new_configs:
                #print(temp_config.arg)
                #checks if state already been added
                seen = False
                for past in final_states:
                    if(past.arg == temp_config.arg):                #TODO write comparator?
                        seen = True
                if(seen == False):
                    #adds configuration if deep enough & valid
                    if(depth > 0 and verify_config(temp_config, constraint_data) == True):
                        states_made += 1
                        print("depth: " + str(depth) + "; states made: " + str(states_made))
                        print(temp_config.arg)
                        print(id_lookup(constraint_data, id))
                        print("")
                        final_states.append(temp_config)
                        
                        #mis-spell feature
                        if(misspell):
                                word = random.choice(list(temp_config.arg))
                                if(constraint_data[word]["flag"] == "-O"):
                                    mis_copy = copy.deepcopy(temp_config)
                                    mis_copy.arg.pop(word,None)
                                    #print("remove " + word)
                                    #print(mis_copy.arg)
                                    replace_num = random.randint(0,len(word)-1)
                                    word = word[:replace_num] + chr(ord(word[replace_num]) + 1) + word[replace_num + 1:]
                                    #print(word)
                                    mis_copy.arg[word]="enable"
                                    invalid_states.append(mis_copy)
                    else:
                        #adds invalid states to list (assuming non-dup)
                        seen2 = False
                        for past in invalid_states:
                            if(past.arg == temp_config.arg):
                                seen2 = True
                        if(seen == False):
                            invalid_states.append(temp_config)
                            
                    
                    #determine what to try next
                    next_list = []
                    for name in constraint_data[id_lookup(constraint_data, id)]["dependency"]:
                        next_list.append(constraint_data[name]["id"])
                    if(constraint_data[id_lookup(constraint_data, id)].get("critical", None) != None):
                        for name in constraint_data[id_lookup(constraint_data, id)]["critical"].keys():
                            next_list.append(constraint_data[name]["id"])
                    #print(next_list)
                    #print("")
                    
                    #go deeper
                    generate(temp_config, constraint_data, target_num, final_states, invalid_states, next_list)
    
    depth -= 1


#converts fron Configuration to command line style 
def ConfigToCMD(config, constraint_data):
    output="(mke2fs)"
    hasFeature = False
    features = []
    hasExtended = False
    extends = []
    hasJournal = False
    journal = []
    
    for arg in config.arg:
        #Skips if part of defualt config
        if((default_feature_args.get(arg, None) == None) or ((default_feature_args.get(arg, None) != None) and (str(default_feature_args[arg]) != str(config.arg[arg])))):
            #if flag lookup fails, assume -O
            try:
                flag = constraint_data[arg]["flag"]
            except:
                flag = "-O"
            if(flag == "-O"):
                if(config.arg[arg] == "enable"):
                    features.append(arg)
                else:
                    features.append("^"+arg)
                hasFeature = True
            elif(flag == "-E"):
                extends.append(arg + "=" + str(config.arg[arg]))
                hasExtended = True
            elif(flag == "-J"):
                journal.append(arg + "=" + str(config.arg[arg]))
                hasJournal = True
            else:
                output += " " + flag + " " + str(config.arg[arg])
    
    
    if(hasFeature):
        output += " -O "
        output += ",".join(str(item) for item in features)
        
    if(hasExtended):
        output += " -E "
        output += ",".join(str(item) for item in extends)
        #output += ", ".join(str(item + " " + str(config.arg[item])) for item in extends)
    
    if(hasJournal):
        output += " -J "
        output += ",".join(str(item) for item in journal)
    
    return output


def main(argv):
    global default_feature_args
    global max_depth
    global misspell
    
    if(not os.path.exists("mke2fs_constraints.json")):
        print("Missing mke2fs_constraints.json file")
        return -1
    
    if(not os.path.exists("default_config.json")):
        print("Missing default_config.json file")
        return -1
        
    if(len(sys.argv) != 4):
        print("Invalid arguments")
        return -1
        
    max_depth = int(sys.argv[1])
    max_final_states = int(sys.argv[2])
    
    if(sys.argv[3] == "True" or sys.argv[3] == "true"):
        misspell = True
    
    #get constraints 
    json_file=open('mke2fs_constraints.json')
    constraint_data = json.load(json_file)
    json_file.close()
    
    #id_lookup(constraint_data, 1)
    #print(constraint_data['blocksize'])
    
    
    #get default configuration
    json_file=open('default_config.json')
    default_feature_args = json.load(json_file)
    json_file.close()
    
    
    #Checking some states
    """
    config_file='config_state_ext4.txt'
    with open(config_file, "r", encoding='utf-8') as f:
        Lines = f.readlines()
        
        #Looking at 1 configuration
        for line in Lines:
            
            #Build default config
            my_config = Configuration()
            
            print()
            print(line.strip())
            
            #Modify config based on command line params
            read_config(line, my_config)
            print(my_config.arg)
            
            
            #Verify config
            print(verify_config(my_config, constraint_data))
    """
    my_config = Configuration()
    final_states = []
    invalid_states = []
    generate(copy.deepcopy(my_config), constraint_data, max_final_states, final_states, invalid_states, list(range(1,51)))
    
    
    print("Final (Invalid) States")
    output_file = open("output_bad.txt", "w")
    for state in invalid_states:
        #print(state.arg)
        print(ConfigToCMD(state, constraint_data))
        output_file.write(ConfigToCMD(state, constraint_data) + "\n")
    output_file.close()
    
    
    

if __name__ == "__main__":
    main(sys.argv[1:])

