import json
import os

###### try to keep all the files in build dir
f= open('mke2fs_constraints.json')
data = json.load(f)
#print (json.dumps(data, indent=4))
print (data['function_name']) #prints entry function name
f1 = open("function_name", "w")
f1.write(data['function_name'])

print (data['superblock'])   #prints superblock name
f2 = open("superblock", "w")
f2.write(data['superblock'])
#print (data['parameters'])

json_object = json.dumps(data['parameters'], indent=4)

with open("mke2fs_constraints_parameters.json", "w") as outfile:
    outfile.write(json_object)

for key in data['parameters']:
    print (key)
    f3 = open("file_name", "w") #taint trace file name
    f3.write(key)
    #print (data['parameters'].get(key))
    for i in data['parameters'].get(key):
        if i == "variable":
            print (data['parameters'].get(key).get(i))
            f4 = open("variable", "w")
            f4.write(data['parameters'].get(key).get(i))
            print ("-----")
            #run llvm-pass
            os.system("llvm-project-llvmorg-14.0.0/build/bin/opt -load llvm-project-llvmorg-14.0.0/build/lib/libinterProPass.so -enable-new-pm=0 -interpro mke2fs.ll")
            f3.close()
            f4.close()
            os.remove("file_name")
            os.remove("variable")

outfile.close()
f.close()
f1.close()
f2.close()

