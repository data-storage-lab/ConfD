**Building Taint Analyzer to generate taint traces**
1. Copy the interPro directory to llvm-project-llvmorg-14.0.0/llvm/lib/Transforms/
2. Add line "add_subdirectory(interPro)" in the CMakeLists.txt file in Transforms directory
3. Build the LLVM project again using ```cmake --build . -j48```
4. Provide the function name (the function where the taint analysis will start from) and variable name (source of the taint analysis) in function_name and variable file respectively

**Running Taint Analyzer to generate taint traces**
Provide the function name (the function where the taint analysis will start from) and variable name (source of the taint analysis) in function_name and variable file respectively inside the "build" directory.

```cd llvm-project-llvmorg-14.0.0/build/```
```bin/opt -load build/lib/libinterProPass.so -enable-new-pm=0 -interpro <path-to-target-bitcode>```
example:
```bin/opt -load build/lib/libinterProPass.so -enable-new-pm=0 -interpro mke2fs.ll```
