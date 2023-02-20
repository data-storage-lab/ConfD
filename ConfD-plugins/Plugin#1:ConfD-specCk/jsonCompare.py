import sys
import json
import pprint
from difflib import SequenceMatcher



def compare_strings(str1, str2, similarity_threshold=0.7):
    """
    Compares two strings and returns True if they are considered the same based on their similarity percentage,
    and False otherwise. The similarity threshold is a float between 0 and 1 that indicates the minimum similarity
    percentage required for the strings to be considered the same (default is 0.7).
    """
    # Use the SequenceMatcher class from the difflib module to compare the strings and calculate their similarity
    similarity = SequenceMatcher(None, str1, str2).ratio()

    # Return True if the similarity is greater than or equal to the similarity threshold, and False otherwise
    return similarity >= similarity_threshold



def compareLists(list1, list2):

    commonList = []

    for i in list2:
        if i in list1:
            commonList.append(i)
        elif i not in list1:
            for j in list1:
                if compare_strings(i, j):
                    commonList.append(i)
                    break
            
    return commonList

    

def getDependencyData(option, file):
    dictionary = {"option": option, "value_range_max": "null", "value_range_min": "null", "cpdParamOrCrit": []}

    if option in file:
        for i in file[option]:
            if i == "value_range_max":
                dictionary["value_range_max"] = file[option][i]
            if i == "value_range_min":
                dictionary["value_range_min"] = file[option][i]
            if i == "CPD_param" or i == "critical":
                dictionary["cpdParamOrCrit"].append(file[option][i])
    else:
        for i in file:
            if len(file[i]) > 6:
                k = 0
                for j in file[i]:
                    k+=1
                    if k > 6:
                        if option == j:
                            for dependency in file[i][j]:
                                if dependency == "value_range_max":
                                    dictionary["value_range_max"] = file[i][j][dependency]
                                if dependency == "value_range_min":
                                    dictionary["value_range_min"] = file[i][j][dependency]
                                if dependency == "CPD_param" or dependency == "critical":
                                    dictionary["cpdParamOrCrit"].append(file[i][j][dependency])
                        
    return dictionary

def compareDependencyData(specCheckerDict, testsDict):
    comparisonOutput = ""

    option = specCheckerDict["option"]
    value_range_max_Spec = specCheckerDict["value_range_max"]
    value_range_min_Spec = specCheckerDict["value_range_min"]
    cpdParamOrCrit_Spec = specCheckerDict["cpdParamOrCrit"]

    value_range_max_Tests = testsDict["value_range_max"]
    value_range_min_Tests = testsDict["value_range_min"]
    cpdParamOrCrit_Tests = testsDict["cpdParamOrCrit"]

    valueRangeMaxCheck = "null"
    valueRangeMinCheck = "null"
    cpdParamOrCritCheck = "null"

    if value_range_max_Spec == value_range_max_Tests:
        valueRangeMaxCheck = "Same"
    else:
        valueRangeMaxCheck = "Different"
    
    if value_range_min_Spec == value_range_min_Tests:
        valueRangeMinCheck = "Same"
    else:
        valueRangeMinCheck = "Different"

    if cpdParamOrCrit_Spec == cpdParamOrCrit_Tests:
        cpdParamOrCritCheck = "Same"
    else:
        #if cpdParamOrCrit_Spec contains a empty list remove the empty list
        for i in cpdParamOrCrit_Spec:
            if i == []:
                cpdParamOrCrit_Spec.remove(i)
        if cpdParamOrCrit_Spec == cpdParamOrCrit_Tests:
            cpdParamOrCritCheck = "Same"
        else:
            cpdParamOrCritCheck = "Different"                                                                

    header = f"Option: {option}\n"
    secondHeader = f"\t\t\t\t\t\t|                                   SpecCk_extracted                                       |                                  taint_analyzer_extracted                                |\n"
    thirdRow = f"\t\t\t\t\t\t|{'':-<90}|{'':-<90}|\n"

    fourthRow = f"\tvalue_range_max: {valueRangeMaxCheck:<8}\t|{'':^90}|{'':^90}|\n"
    fifthRow = f"\tvalue_range_min: {valueRangeMinCheck:<8}\t|{'':^90}|{'':^90}|\n"
    sixthRow = f"\tcpdParamOrCrit: {cpdParamOrCritCheck:<8}\t|{'':^90}|{'':^90}|\n"
    seventhRow = f"\t\t\t\t\t\t|{'':-<90}|{'':-<90}|\n"

    if valueRangeMaxCheck == "Different":
        fourthRow = f"\tvalue_range_max: {valueRangeMaxCheck:<8}\t|{str(value_range_max_Spec):^90}|{str(value_range_max_Tests):^90}|\n"
    else:
        fourthRow = ""

    if valueRangeMinCheck == "Different":
        fifthRow = f"\tvalue_range_min: {valueRangeMinCheck:<8}\t|{str(value_range_min_Spec):^90}|{str(value_range_min_Tests):^90}|\n"
    else:
        fifthRow = ""

    if cpdParamOrCritCheck == "Different":
        sixthRow = f"\tcpdParamOrCrit: {cpdParamOrCritCheck:<8}\t|{str(cpdParamOrCrit_Spec):^90}|{str(cpdParamOrCrit_Tests):^90}|\n"
    else:
        sixthRow = ""


    comparisonOutput = header + secondHeader + thirdRow + fourthRow + fifthRow + sixthRow + seventhRow



    return comparisonOutput


def main():
    specCheckerFile = sys.argv[1]
    testsFile = sys.argv[2]

    #open json file
    specCheckerFile = json.load(open(specCheckerFile))
    testsFile = json.load(open(testsFile))
    
    #loop through json file and add to list
    specCheckerList = []
    for i in specCheckerFile:
        specCheckerList.append(i)
        if len(specCheckerFile[i]) > 6:
            k = 0
            for j in specCheckerFile[i]:
                k += 1
                if k > 6:
                    specCheckerList.append(j)

    testsList = []

    #loop through json file and add to list
    for i in testsFile:
        testsList.append(i)

    commonList = compareLists(specCheckerList, testsList)
    
    comparisonOutput = []

    for i in commonList:
        if i == "flex_bg_size":
            continue
        if i in specCheckerList:
            specCheckerDict = getDependencyData(i, specCheckerFile)
        else:
            for j in specCheckerList:
                if compare_strings(i,j):
                    specCheckerDict = getDependencyData(j, specCheckerFile)
        testsDict = getDependencyData(i, testsFile)
        comparisonOutput.append(compareDependencyData(specCheckerDict, testsDict))


    txtfile = open("comparisonOutput.txt", "w")

    for i in comparisonOutput:
        txtfile.write(i)
    txtfile.close()


    newText = []
    txtfile = open("comparisonOutput.txt", "r")
    lines = txtfile.readlines()
    for line in lines:
        if "Option" in line:
            line = line.strip(" ")
        newText.append(line)

    txtfile.close()

    txtfile = open("comparisonOutput.txt", "w")
    for line in newText:
        txtfile.write(line + "\n")
    txtfile.close()


if __name__ == "__main__":
    main()