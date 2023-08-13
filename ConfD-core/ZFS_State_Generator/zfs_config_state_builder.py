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

argument_key = {
    "blocksize": "-b", "feature": "-o"
}

reverse_argument_key = {v: k for k, v in argument_key.items()}

feature_args = {
    "volblocksize", "checksum", "compression", "copies"
}

default_feature_args = {
    "volblocksize": 8192,
    "checksum": 0,
    "compression": 0,
    "copies": 2
}


class Configuration:
    arg = None

    def __init__(self):
        self.arg = dict()
        for a in default_feature_args:
            self.arg[a] = default_feature_args[a]


# looks up by id for constraint_data
def id_lookup(constraint_data, id):
    for i in constraint_data:
        if (constraint_data[i]['id'] == id):
            return (i)


# Takes command line style config, adds params to existing Configuration
def read_config(line, my_config):
    params = line.split(' -')
    # Parse command parameter
    for param in params:
        if (param != "(mkezfs)" and param != "\n" and param[0] != 'O'):

            # print(param.strip().split(' '))
            key = param.strip().split(' ')[0]
            val = param.strip().split(' ')[1]
            my_config.arg[reverse_argument_key["-" + key]] = val

            # print(reverse_argument_key["-"+key])

        # case '-O'
        elif (param[0] == 'O'):
            clean = param.strip().split(' ')[1].split(',')
            for c in clean:
                my_config.arg[c] = ""


# Determines if a given Configuration is valid within given constraints
def verify_config(my_config, constraint_data):
    # Step 1 - verify all numerical constraints
    # TODO account for postfixs on numbers
    for a in my_config.arg:
        if (a != "revision" and a != "encoding"):
            # print(constraint_data[a])
            # print(a + " : " + my_config.arg[a])
            if (constraint_data[a]["takes_value"] == "yes"):
                # Tests Max
                if (constraint_data[a]["value_range_max"] != None and (
                        int(constraint_data[a]["value_range_max"]) < int(my_config.arg[a]))):
                    # print("Max:" + constraint_data[a]["value_range_max"])
                    # print("Act:" + my_config.arg[a])
                    # print(constraint_data[a])
                    # print(" Max violated")
                    return False
                # Tests Min
                if (constraint_data[a]["value_range_min"] != None and (
                        int(constraint_data[a]["value_range_min"]) > int(my_config.arg[a]))):
                    # print(constraint_data[a])
                    # print(" Min violated")
                    return False

    # Step 2 - verify critical enabled/disabled and smaller
    for a in my_config.arg:
        if (a != "revision" and a != "encoding"):
            # print(constraint_data[a])
            # print(a + " : " + my_config.arg[a])
            if (constraint_data[a].get("critical", None) != None):
                # print(constraint_data[a]["critical"])
                for crit in constraint_data[a]["critical"]:
                    # print(crit + " : " + constraint_data[a]["critical"][crit])
                    # enabled crit test
                    if ((constraint_data[a]["critical"][crit] == "enable") and (
                            (my_config.arg.get(crit, None) == None) or (my_config.arg[crit] == "disable"))):
                        # print(constraint_data[a])
                        # print(crit + " violated")
                        # print("")
                        return False
                    if ((constraint_data[a]["critical"][crit] == "disable") and (
                            my_config.arg.get(crit, None) != None) and (my_config.arg[crit] == "enable")):
                        # print(constraint_data[a])
                        # print(crit + " violated")
                        # print("")
                        return False
                    # tests smaller
                    if ((constraint_data[a]["critical"][crit] == "smaller") and (
                            my_config.arg.get(crit, None) != None)):
                        if (int(my_config.arg[a]) < int(my_config.arg[crit])):
                            # print(constraint_data[a])
                            # print(crit + " violated")
                            # print("")
                            return False
    return True


# gets critical dependencies where something needs to be disabled, also returns number of variables in the json
def getCritDisable(constraint_data):
    disable = []

    for a in constraint_data:
        for crit in constraint_data[a]["critical"]:
            if (constraint_data[a]["critical"][crit] == "disable"):
                disable.append(crit)

    return disable

def simpleCMD(state, constraint_data, place):
    command = "zfs create "

    id = 1

    for a in state:
        broken = False

        if a == "disabled":
            id += 1
            continue

        variable = constraint_data[id_lookup(constraint_data, id)]["variable"]
        variable = variable[9:]
        variable = variable.lower()

        for b in default_feature_args:
            if (variable == b and a == default_feature_args[b]):
                id += 1
                broken = True
                continue
        if broken == True:
            continue

        if variable == "blocksize":
            command += "-b "
        else:
            command += "-o "

        value = a
        if (variable == "checksum" or variable == "compression"):
            if a == 1:
                value = "off"
            else:
                value = "on"
        command += str(variable) + "=" + str(value) + " "
        id += 1

    command += place
    return command


def simpleVerify(state, constraint_data):
    if state[0] == "disabled" and state[1] == "disabled":
        return False
    if state[0] != "disabled" and state[1] != "disabled":
        return False
    return True


# attempt to generate the correct number of states with a different algorithm
def simpleGenerate(initial_state, constraint_data, disable, max_depth):
    global states_created, state_depth
    state_depth += 1

    # if all variables have been added, add state to list
    if state_depth > max_depth:
        if simpleVerify(initial_state, constraint_data):
            state_list.append(initial_state.copy())
            states_created += 1
            print(initial_state)
            print(str(states_created) + " states created")
        state_depth -= 1
        return

    variable = constraint_data[id_lookup(constraint_data, state_depth)]["variable"]
    print("looking at " + variable)

    # if this variable is on the disable list, make states without it
    for a in disable:
        if a == id_lookup(constraint_data, state_depth):

            initial_state.append("disabled")
            simpleGenerate(initial_state, constraint_data, disable, max_depth)
            initial_state.pop(state_depth - 1)


    temp = int(constraint_data[id_lookup(constraint_data, state_depth)]["value_range_min"])

    while temp <= int(constraint_data[id_lookup(constraint_data, state_depth)]["value_range_max"]):

        initial_state.append(temp)
        simpleGenerate(initial_state, constraint_data, disable, max_depth)
        initial_state.pop(state_depth - 1)

        if (constraint_data[id_lookup(constraint_data, state_depth)]["variable"] == "ZFS_PROP_BLOCKSIZE" or constraint_data[id_lookup(constraint_data, state_depth)]["variable"] == "ZFS_PROP_VOLBLOCKSIZE"):
            temp *= 2
        else:
            temp += 1

    state_depth -= 1
    return


def main(argv):
    global default_feature_args
    global max_depth

    if (not os.path.exists("zfs_constraints.json")):
        print("Missing zfs_constraints.json file")
        return -1

    # if(not os.path.exists("zfs_default_config.json")):
    #    print("Missing zfs_default_config.json file")
    #    return -1

    if (len(sys.argv) != 2):
        print("Invalid arguments")
        return -1

    location = sys.argv[1]

    # get constraints
    json_file = open('zfs_constraints.json')
    constraint_data = json.load(json_file)
    json_file.close()

    # id_lookup(constraint_data, 1)
    # print(constraint_data['blocksize'])

    # get default configuration
    # json_file=open('zfs_default_config.json')
    # default_feature_args = json.load(json_file)
    # json_file.close()

    # Checking some states
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
    #generate(copy.deepcopy(my_config), constraint_data, max_final_states, final_states, list(range(1, 6)))

    disable = getCritDisable(constraint_data)

    # Get the number of variables
    num_vars = 0
    for a in constraint_data:
        num_vars += 1

    global state_list
    state_list = []
    blank_config = []

    global state_depth
    global states_created
    state_depth = 0
    states_created = 0

    simpleGenerate(blank_config, constraint_data, disable, num_vars)

    print("\nFinal States:")
    output_file = open("zfs_output.txt", "w")
    for state in state_list:

        cmd = simpleCMD(state, constraint_data, location)
        print(cmd)
        output_file.write(cmd + "\n")


    output_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
