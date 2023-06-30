**Building Taint Analyzer to generate taint traces**

1. Copy the interPro directory to llvm-project-llvmorg-14.0.0/llvm/lib/Transforms/
2. Add line "add_subdirectory(interPro)" in the CMakeLists.txt file in Transforms directory
3. Build the LLVM project again using ```cmake --build . -j48```

**Running Taint Analyzer to generate taint traces**

1. "sepatrate_objects.py" takes the mke2fs_constraints.josn file and runs taint analysis for each of the parameters automatically and generates taint traces.

2. Taint Analyzer can also be run manually by providing function_name and variable as input and running the following commands:
 
Provide the function name (the function where the taint analysis will start from) and variable name (source of the taint analysis) in function_name and variable file respectively inside the "build" directory. See examples of function_name and variable for mke2fs inside the interPro directory.

```cd llvm-project-llvmorg-14.0.0/build/```

```bin/opt -load build/lib/libinterProPass.so -enable-new-pm=0 -interpro <path-to-target-bitcode>```

example:

```bin/opt -load build/lib/libinterProPass.so -enable-new-pm=0 -interpro mke2fs.ll```
