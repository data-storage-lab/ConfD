import os
import time
import subprocess

create_fs = os.system("truncate -s 500M image")
file1 = open("output_bad.txt", 'r')
file2 = open("further_checking", 'w')
lines = file1.readlines()


for line in lines:
    line1 = line.strip()
    line_stripped = line1.split(' ', 1)[1]
    line_add = 'mke2fs -F -t ext4 '
    image = " image"
    print(line_add+line_stripped+image)
    command = line_add+line_stripped+image
    result = os.system(command)
    exit_code = os.WEXITSTATUS(result)
    time.sleep(1)
    print(exit_code)
    #echo = os.system("echo $?")
    if (exit_code == 0):        
        file2.write(line_add+line_stripped+image+'\n')

file1.close()
file2.close()
