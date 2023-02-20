import sys
import subprocess
from pprint import pprint
import json
import re


#convert a K, M, G, or T bytes to bytes
def convertBytes(num):
    if num.isdigit():
        return int(num)
    elif num[-1] == "K":
        return int(num[:-1]) * 1024
    elif num[-1] == "M":
        return int(num[:-1]) * 1024 * 1024
    elif num[-1] == "G":
        return int(num[:-1]) * 1024 * 1024 * 1024
    elif num[-1] == "T":
        return int(num[:-1]) * 1024 * 1024 * 1024 * 1024

#return any self dependencies found for a given option
#Starts by searching the option description for keywords "value" and "values" if found it will search for a values and add them to a list. 
#If the list is not empty it will find the smallest and largest number in the list and add them to the value_range_min and value_range_max keys in the dictionary.
#Then it will search for keywords "greater than", "greater than or equal to", "less than", "less than or equal to", "more than", "more than or equal to", "larger than", 
# "larger than or equal to", "smaller than", "smaller than or equal to" and assign the value that follows the keyword to the value_range_min or value_range_max keys in the dictionary.
def selfDependencies(option, index,  dict):
    string = option[index][1].split()

    if "value" in option[index][1] or "values" in option[index][1]:
        valueList = []
        valueList = [int(s) for s in re.findall(r'\b\d+\b', option[index][1])]
        if len(valueList) > 0:
            smallestNum = valueList[0]
            largestNum = valueList[0]
            for i in valueList:
                if i < smallestNum:
                    smallestNum = i
                if i > largestNum:
                    largestNum = i
            dict[option[index][0]]["value_range_min"] = smallestNum
            dict[option[index][0]]["value_range_max"] = largestNum

    for i in range(len(string)):
        if string[i] == "greater":
            if string[i+1] == "than":
                if string[i+2].isdigit():
                    dict[option[index][0]]["value_range_min"] = int(string[i+2])
                elif string[i+2] == "or":
                    if string[i+3] == "equal":
                        if string[i+4] == "to":
                            if string[i+5].isdigit():
                                dict[option[index][0]]["value_range_min"] = int(string[i+5])
        if string[i] == "less":
            if string[i+1] == "than":
                if string[i+2].isdigit():
                    dict[option[index][0]]["value_range_max"] = int(string[i+2])
                elif string[i+2] == "or":
                    if string[i+3] == "equal":
                        if string[i+4] == "to":
                            if string[i+5].isdigit():
                                dict[option[index][0]]["value_range_min"] = int(string[i+5])
        if string[i] == "more":
            if string[i+1] == "than":
                if string[i+2].isdigit():
                    dict[option[index][0]]["value_range_min"] = int(string[i+2])
                elif string[i+2] == "or":
                    if string[i+3] == "equal":
                        if string[i+4] == "to":
                            if string[i+5].isdigit():
                                dict[option[index][0]]["value_range_min"] = int(string[i+5])
        if string[i] == "larger":
            if string[i+1] == "than":
                if string[i+2].isdigit():
                    dict[option[index][0]]["value_range_min"] = int(string[i+2])
                elif string[i+2] == "or":
                    if string[i+3] == "equal":
                        if string[i+4] == "to":
                            if string[i+5].isdigit():
                                dict[option[index][0]]["value_range_min"] = int(string[i+5])
            elif string[i+1] == "or":
                if string[i+3] == "equal":
                        if string[i+4] == "to":
                            if string[i+5].isdigit():
                                dict[option[index][0]]["value_range_min"] = int(string[i+5])
        if string[i] == "smaller":
            if string[i+1] == "than":
                if string[i+2].isdigit():
                    dict[option[index][0]]["value_range_max"] = int(string[i+2])
                elif string[i+2] == "or":
                    if string[i+3] == "equal":
                        if string[i+4] == "to":
                            if string[i+5].isdigit():
                                dict[option[index][0]]["value_range_min"] = int(string[i+5])

        if "value" in option[index][1] or "values" in option[index][1]:
            for i in range(len(string)):
                if string[i] == "value" or string[i] == "values":
                    if string[i+1] == "are":
                        if string[i+2] == "from":
                            if string[i+3].isdigit():
                                dict[option[index][0]]["value_range_min"] = int(string[i+3])
                                if string[i+4] == "to":
                                    if string[i+5].isdigit():
                                        dict[option[index][0]]["value_range_max"] = int(string[i+5])
                                    elif string[i+6] == "bytes":
                                        num = convertBytes(string[i+5])
                                        dict[option[index][0]]["value_range_max"] = num

#return any self dependencies found for a given feature
#Does the same thing as selfDependencies, but for features instead of options
def selfDependenciesFeatures(options, index, option, dict):
    flag = option.copy()
    dictflag = option[0]
    if len(flag) < 2:
        return
    
    for i in range(2):
        flag.pop(0)

    if len(flag[0][0]) < 2 or flag[0][0][1] == '':
        return

    for feature in flag:
        string = feature[0][1].split()
        
        if "value" in feature[0][1] or "values" in feature[0][1]:
            valueList = []
            valueList = [int(s) for s in re.findall(r'\b\d+\b', feature[0][1])]
            if len(valueList) > 0:
                smallestNum = valueList[0]
                largestNum = valueList[0]
                for i in valueList:
                    if i < smallestNum:
                        smallestNum = i
                    if i > largestNum:
                        largestNum = i
                dict[option[0]][feature[0][0]]["value_range_min"] = smallestNum
                dict[option[0]][feature[0][0]]["value_range_max"] = largestNum

        for i in range(len(string)):
            if string[i] == "greater":
                if string[i+1] == "than":
                    if string[i+2].isdigit():
                        dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+2])
                    elif string[i+2] == "or":
                        if string[i+3] == "equal":
                            if string[i+4] == "to":
                                if string[i+5].isdigit():
                                    dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+5])
            if string[i] == "less":
                if string[i+1] == "than":
                    if string[i+2].isdigit():
                        dict[option[0]][feature[0][0]]["value_range_max"] = int(string[i+2])
                    elif string[i+2] == "or":
                        if string[i+3] == "equal":
                            if string[i+4] == "to":
                                if string[i+5].isdigit():
                                    dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+5])
            if string[i] == "more":
                if string[i+1] == "than":
                    if string[i+2].isdigit():
                        dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+2])
                    elif string[i+2] == "or":
                        if string[i+3] == "equal":
                            if string[i+4] == "to":
                                if string[i+5].isdigit():
                                    dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+5])
            if string[i] == "larger":
                if string[i+1] == "than":
                    if string[i+2].isdigit():
                        dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+2])
                    elif string[i+2] == "or":
                        if string[i+3] == "equal":
                            if string[i+4] == "to":
                                if string[i+5].isdigit():
                                    dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+5])
                elif string[i+1] == "or":
                    if string[i+3] == "equal":
                            if string[i+4] == "to":
                                if string[i+5].isdigit():
                                    dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+5])
            if string[i] == "smaller":
                if string[i+1] == "than":
                    if string[i+2].isdigit():
                        dict[option[0]][feature[0][0]]["value_range_max"] = int(string[i+2])
                    elif string[i+2] == "or":
                        if string[i+3] == "equal":
                            if string[i+4] == "to":
                                if string[i+5].isdigit():
                                    dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+5])

            if "value" in feature[0][1] or "values" in feature[0][1]:
                for i in range(len(string)):
                    if string[i] == "value" or string[i] == "values":
                        if string[i+1] == "are":
                            if string[i+2] == "from":
                                if string[i+3].isdigit():
                                    dict[option[0]][feature[0][0]]["value_range_min"] = int(string[i+3])
                                    if string[i+4] == "to":
                                        if string[i+5].isdigit():
                                            dict[option[0]][feature[0][0]]["value_range_max"] = int(string[i+5])
                                        elif string[i+6] == "bytes":
                                            num = convertBytes(string[i+5])
                                            dict[option[0]][feature[0][0]]["value_range_max"] = num

#check for any cross dependencies using the option flag or version of it currently using -flag and if flag has - checks using string with - and without with space. ex. "-b", "block-size", "block size"
def crossDependencies(option, index, dict):
        flag = option[index][0]
        tokens = flag.split()
        if len(tokens) > 1 and "-" in tokens[1]:
            tokens.append(tokens[1])
            tokens[2] = tokens[2].replace("-", " ")

        for token in tokens:
            for i in range(len(option)):
                if token in option[i][1].split() and i != index:
                    dict[flag]["CPD_param"].append(option[i][0])

#checks for features that are dependencies in both the options or other features. If feature is separated by a = sign it will add the substring after the equal sign and if
#feature is separated by a - sign it will add both the string with the - and without the - sign to the list of features to check for. 
# ex. "encoding=encoding-name" search list will be ["encoding-name", "encoding name"]. Otherwise it will just use the feature name.
def crossDependenciesFeatures(options, index, option, dict):
    flag = option.copy()
    dictflag = option[0]
    if len(flag) < 2:
        return
    
    for i in range(2):
        flag.pop(0)

    if len(flag[0][0]) < 2 or flag[0][0][1] == '':
        return

    #check for feature dependencies in parsedOptions
    for feature in flag:
        #if feature[0] contains a = get the substring after the = and check if it is in the parsedOptions
        checkStrs = []
        if "=" in feature[0][0]:
            checkStrs.append(feature[0][0].split("=")[1])
            if "-" in checkStrs[0]:
                temp = checkStrs[0].split("-")
                checkStrs.append(temp[0] + " " + temp[1])
        else:
            checkStrs.append(feature[0][0])

        if 'value' in checkStrs:
            checkStrs.remove('value')

        for option in options:
            for string in checkStrs:
                if string in option[1]:
                    dict[dictflag][feature[0][0]]["CPD_param"].append(option[0])

        checkStrs = []
        if "=" in feature[0][0]:
            checkStrs.append(feature[0][0].split("=")[1])
            if "-" in checkStrs[0]:
                temp = checkStrs[0].split("-")
                checkStrs.append(temp[0] + " " + temp[1])
        else:
            checkStrs.append(feature[0][0])

        if 'value' in checkStrs:
            checkStrs.remove('value')


        for option in options:
            if len(option) > 2:
                for afeature in option[2:]:
                    for string in checkStrs:
                        if string in afeature[0][1] and afeature[0][0] != feature[0][0]:
                            dict[dictflag][feature[0][0]]["CPD_param"].append(afeature[0][0])
        
#get the O features of mke2fs from ext4 by running man ext4.
def getOFeatures():
    p = subprocess.run(["man", "ext4"], stdout=subprocess.PIPE, text=True)
    features = []
    feature = False
    for line in p.stdout.splitlines():
        if line.startswith("FILE SYSTEM FEATURES"):
            feature = True
            continue
        if feature:
            if line.startswith(" "):
                features.append(line)
            elif line.startswith("MOUNT OPTIONS"):
                break

    for i in range(3):
        features.pop(0)

    parsedFeatures = []
    featureString = ""
    for feature in features:
        if feature.startswith("       ") and feature[8] != " ":
            if featureString != "":
                parsedFeatures[-1].append(featureString.strip())
            parsedFeatures.append([feature.strip()])
            featureString = ""

        elif feature.startswith("       ") and feature[8] == " ":
            featureString += feature.strip() + " "
        
    parsedFeatures[-1].append(featureString.strip())
    return parsedFeatures

#count the number of cross dependencies found in json file
def crossDependencyCounter(dict):
    count = 0
    for key in dict:
        if len(dict[key]["CPD_param"]) > 0:
            count += len(dict[key]["CPD_param"])
        if len(dict[key]) > 6:
            i = 0
            for feature in dict[key]:
                i += 1
                if i <= 6:
                    continue
                if len(dict[key][feature]["CPD_param"]) > 0:
                    count += len(dict[key][feature]["CPD_param"])
    return count

#count the number of self dependencies found in json file
def selfDependencyCounter(dict):
    count = 0
    for key in dict:
        if dict[key]['value_range_max'] != None:
            count += 1
        if dict[key]['value_range_min'] != None:
            count += 1
        if len(dict[key]) > 6:
            i = 0
            for feature in dict[key]:
                i += 1
                if i <= 6:
                    continue
                if dict[key][feature]['value_range_max'] != None:
                    count += 1
                if dict[key][feature]['value_range_min'] != None:
                    count += 1
    return count

#search for options and features that need to be enabled or disabled in other options and features
def enableDisable(dict, dictCopy, parsedOptions):
    #search for options that need to be enabled or disabled in other options
    for key in dict:
        if len(dict[key]["CPD_param"]) > 0:
            for dependency in dict[key]["CPD_param"]:
                for listt in parsedOptions:
                    if dependency == listt[0]:
                        enableindex = []
                        disableindex = []
                        stringsplit = listt[1].split(" ")
                        
                        for i in range(len(stringsplit)):
                            if "enable" in stringsplit[i]:
                                enableindex.append(i)
                            if "disable" in stringsplit[i]:
                                disableindex.append(i)
                        
                        if len(enableindex) > 0:
                            dependencyFound = checkIndexes(enableindex, stringsplit, key)
                            if dependencyFound:
                                index = dict[key][feature]["CPD_param"].index(dependency)
                                dictCopy[key][feature]["CPD_param"][index] = dependency + " enable"
                        if len(disableindex) > 0:
                            dependencyFound = checkIndexes(disableindex, stringsplit, key)
                            if dependencyFound:
                                index = dict[key][feature]["CPD_param"].index(dependency)
                                dictCopy[key][feature]["CPD_param"][index] = dependency + " disable"


    #Search for features that need to be enabled or disabled in other options
    for key in dict:
        if len(dict[key]) > 6:
            i = 0
            for feature in dict[key]:
                i+=1
                if i > 6:
                    for dependency in dict[key][feature]["CPD_param"]:
                        for listt in parsedOptions:
                            if dependency == listt[0]:
                                enableindex = []
                                disableindex = []
                                stringsplit = listt[1].split(" ")
                                
                                for i in range(len(stringsplit)):
                                    if "enable" in stringsplit[i]:
                                        enableindex.append(i)
                                    if "disable" in stringsplit[i]:
                                        disableindex.append(i)

                                if len(enableindex) > 0:
                                    dependencyFound = checkIndexes(enableindex, stringsplit, feature)
                                    if dependencyFound:
                                        index = dict[key][feature]["CPD_param"].index(dependency)
                                        dictCopy[key][feature]["CPD_param"][index] = dependency + " enable"
                                if len(disableindex) > 0:
                                    dependencyFound = checkIndexes(disableindex, stringsplit, feature)
                                    if dependencyFound:
                                        index = dict[key][feature]["CPD_param"].index(dependency)
                                        dictCopy[key][feature]["CPD_param"][index] = dependency + " disable"


    #search for features that need to be enabled or disabled in other features       
    for key in dict:
        if len(dict[key]) > 6:
            i = 0
            for feature in dict[key]:
                i+=1
                if i > 6:
                    for dependency in dict[key][feature]["CPD_param"]:
                        for listt in parsedOptions:
                            if len(listt) > 2:
                                for j in range(2, len(listt)):
                                    if dependency == listt[j][0][0]:
                                        enableindex = []
                                        disableindex = []
                                        stringsplit = listt[j][0][1].split(" ")
                                        
                                        for i in range(len(stringsplit)):
                                            if "enable" in stringsplit[i]:
                                                enableindex.append(i)
                                            if "disable" in stringsplit[i]:
                                                disableindex.append(i)

                                        if len(enableindex) > 0:
                                            dependencyFound = checkIndexes(enableindex, stringsplit, feature)
                                            if dependencyFound:
                                                index = dict[key][feature]["CPD_param"].index(dependency)
                                                dictCopy[key][feature]["CPD_param"][index] = dependency + " enable"
                                        if len(disableindex) > 0:
                                            dependencyFound = checkIndexes(disableindex, stringsplit, feature)
                                            if dependencyFound:
                                                index = dict[key][feature]["CPD_param"].index(dependency)
                                                dictCopy[key][feature]["CPD_param"][index] = dependency + " disable"
    return dictCopy

#check if dependency is in the range of the enable or disable. Checks 5 indexes before and after the enable or disable index 
def checkIndexes(indexes, stringsplit, feature):
    dependencyFound = False
    for index in indexes:
        min = index - 5
        max = index + 5
        if min < 0:
            min = 0
        if max > len(stringsplit):
            max = len(stringsplit)
        for i in range(min, max):
            if feature in stringsplit[i]:
                dependencyFound = True
                break
    return dependencyFound


#This program will take a inputted manfile and parse out the options and features part of the manfile. Then look for self dependencies and cross dependencies. Determine if there 
#are any dependencies that have a enable/disable relationship. Then print out the discovered dependencies in a json format to a file named jsonfile.json.
#TO RUN: python3 main.py <manfile> ex. python3 main.py mke2fs.8     python3 main.py mkfs.8      python3 main.py mke2fs

def main():
    #inputted manfile arg
    manfile = sys.argv[1]
    
    #run man against the manfile give the file to p
    p = subprocess.run(["man", manfile], stdout=subprocess.PIPE, text=True)
    

    options = []

    #final list of options
    parsedOptions = []
    #final list of -O features if mke2fs is the manfile
    oFeatures = []

    #go to options line in p.stdout print the options
    option = False
    for line in p.stdout.splitlines():
        if line.startswith("OPTIONS"):
            option = True
            continue
        if option:
            #if line starts with a letter 
            if line.startswith(" "):
                #print(line)
                options.append(line)
            elif len(line) == 0:
                #print(line)
                pass
            elif line[0].isalpha():
                break
    
    # if inputted manfile is mke2fs get the -O features
    if manfile == "mke2fs" or manfile == "mke2fs.8":
        oFeatures = getOFeatures()

    
    #parse options
    i = 0
    num = 0
    optionNum = 0
    string = ""
    for option in options:
        if num != optionNum:
            num += 1
            continue
        num += 1

        word = ""
        if option.startswith("       -"):
            #get flag
            flag = option.split()[0]
            if option[option.index('-') + 2] == ' ' and option[option.index('-') + 3] != ' ':
                word = option.split()[1]
            if len(word) > 0:
                fullFlag = flag + " " + word
            else:
                fullFlag = flag
            listFullFlag = [fullFlag]
            parsedOptions.append(listFullFlag)
            if len(option.split()) > 2:
                #remove flag and word from option or just flag
                option = option.replace(fullFlag, "")
                parsedOptions[i].append(option.strip())
            i += 1
            if len(parsedOptions[i-2]) > 2:
                optionToOneString = ""
                #extend all lists from 2 to len(parsedOptions[i-1]) to parsedOptions[i-1][1]
                while len(parsedOptions[i-2]) >= 3 and not isinstance(parsedOptions[i-2][2], list):
                    optionToOneString += (parsedOptions[i-2].pop(2) + "\n")
                parsedOptions[i-2][1] += " " + optionToOneString
        elif option.startswith("                  "):
            # #start at option optionNum and go till option starts with "       -"
            nextOption = -1
            for j in range(optionNum, len(options)):
                if options[j].startswith("       -"):
                    nextOption = j
                    break
            for j in range(optionNum, nextOption):
                if options[j].startswith("                  ") and options[j][19] != ' ':
                    parsedOptions[i-1].append([[options[j].strip()]])
                    description = -1
                    for k in range(j+1, nextOption):
                        # if options[k].startswith("                  "): and next character is not a space
                        if options[k].startswith("                  ") and options[k][19] != " ": #or (options[k].startswith("                          ") and options[k][27] != " " ):
                            description = k
                            break
                    if description != -1:
                        string = ""
                        for k in range(j+1, description):
                            string += options[k].strip() + "\n"
                        
                    parsedOptions[i-1][-1][-1].append(string)
                if j + 1 == nextOption:
                    optionNum = j
                    break
        

        elif option.startswith("              "):
            parsedOptions[i-1].append(option.strip())
        optionNum += 1


    #if parsedOptions[-1] len > 2 and last element is not a list then add all to the 2nd element
    if len(parsedOptions[-1]) > 2 and not isinstance(parsedOptions[-1][2], list):
        optionToOneString = ""
        while len(parsedOptions[-1]) >= 3 and not isinstance(parsedOptions[-1][2], list):
            optionToOneString += (parsedOptions[-1].pop(2) + "\n")
        parsedOptions[-1][1] += " " + optionToOneString

    # add -O features to parsedOptions
    if len(oFeatures) > 0:
        for feature in oFeatures:
            parsedOptions[21].append([feature])

    jsonobj = {}

    #create and initialize json object
    id = 1
    for option in parsedOptions:
        jsonobj.update({option[0]: {"id": id, "value_type": None, "value_range_max": None, "value_range_min": None, "CPD_optional_param": [], "CPD_param":[]}})
        id += 1


    #if option has features add the features to option's json object
    for option in parsedOptions:
        if len(option) > 2:
            for i in range(2, len(option)):
                tempdict = {option[i][0][0]: {"value_type": None, "value_range_max": None, "value_range_min": None,"CPD_optional_param": [], "CPD_param":[]}}
                jsonobj[option[0]].update(tempdict)

    #Look for different dependencies
    i = 0
    for option in parsedOptions:
        selfDependencies(parsedOptions, i,  jsonobj)
        crossDependencies(parsedOptions, i, jsonobj)
        if len(option) > 2:
            crossDependenciesFeatures(parsedOptions, i, option, jsonobj)
            selfDependenciesFeatures(parsedOptions, i, option, jsonobj)
        i += 1


    print("Cross Dependencies found: " + str(crossDependencyCounter(jsonobj)))
    print("Self Dependencies found: " + str(selfDependencyCounter(jsonobj)))

    copyOfJsonobj = jsonobj.copy()

    #search for dependencies that have a enable/disable relationship
    jsonobj = enableDisable(jsonobj, copyOfJsonobj, parsedOptions)
    
    jsonfile = open("jsonfile.json", "w")
    jsonobj = json.dumps(jsonobj, indent=4)
    jsonfile.write(jsonobj)
    jsonfile.close()

    
if __name__ == '__main__':
    main()
