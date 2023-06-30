import os

directory = 'dependent'

cmd = 'mv '

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    f_changed = os.path.join(directory, 'common_lines')
    cmd_mv = cmd + f + " " + f_changed
    os.system(cmd_mv)
    os.system("../Taint Analyzer/llvm-project-llvmorg-14.0.0/build/bin/opt -load ../Taint Analyzer/llvm-project-llvmorg-14.0.0/build/lib/libTestPass.so -enable-new-pm=0 -test mke2fs.ll")
    os.system('python3 phase3.py critical')
