# README #
# ConfD #

This repository contains the research prototype for the ConfD project and the following publications: 

- "[ConfD: Analyzing Configuration Dependencies of File Systems for Fun and Profit](https://www.usenix.org/conference/fast23/presentation/mahmud)",
Tabassum Mahmud, Om Rameshwar Gatla, Duo Zhang, Carson Love, Ryan Bumann, and Mai Zheng,
Proceedings of the 21st USENIX Conference on File and Storage Technologies ([FAST](https://www.usenix.org/conference/fast23)), 2023.

- "[Understanding Configuration Dependencies of File Systems](https://dl.acm.org/doi/abs/10.1145/3538643.3539756)",
Tabassum Mahmud, Duo Zhang, Om Rameshwar Gatla, and Mai Zheng, 
Proceedings of the 14th ACM Workshop on Hot Topics in Storage and File Systems ([HotStorage](https://www.hotstorage.org/2022/)), 2022. [**Best Paper Nominee**] 

- "[Understanding Configuration Issues in Storage Systems](https://www.usenix.org/conference/fast22/presentation/mahmud)",
Tabassum Mahmud and Mai Zheng,
Work-in-Progress reports (WiPs) & Poster Sessions, 20th USENIX Conference on File and Storage Technologies ([FAST-WiP](https://www.usenix.org/conference/fast22/wips)), 2022.

## ConfD ##
ConfD analyzes configuration dependencies of file systems. It has two main components.

- ConfD-core
- ConfD-plugins

The description of each component is as follows:

## ConfD-core ##

ConfD-core has three components: 

- **Taint Analyzer:**
  - Source code in ConfD-core/Taint Analyzer/
  - Generates the taint traces for configuratin parameters

- **Dependency Analyzer:**
  - Source code in ConfD-core/Dependency Analyzer/
  - Generates the dependency information for the configuration parameters

- **State Generator:**
  - Source code in ConfD-core/State Generator/
  - Generates dependency-guided configuration states based on the dependency information of the configuration parameters

## ConfD-plugins ##

Currently ConfD has six plugins:

- **Plugin#1: ConfD-specCk**
  - Source code in ConfD-plugins/Plugin#1:ConfD-specCk/
  - Automatically extracts dependency information from linux man-pages and compares with dependencies extracted from ConfD-core to check inconsistency

- **Plugin#2: ConfD-handlingCk**
  - Source code in ConfD-plugins/Plugin#2:ConfD-handlingCk/
  - Checks handling of (mis)configuration
 
- **Plugin#3: ConfD-rfsck**
  - Source code in ConfD-plugins/Plugin#2:ConfD-rfsck/
  - Leverages the dependency-guided configuration states for rfsck
  
- **Plugin#4: ConfD-gt-hydra**
  - Source code in ConfD-plugins/Plugin#2:ConfD-gt-hydra/
  - Leverages the dependency-guided configuration states for gt-hydra
  
- **Plugin#5: ConfD-xfstests**
  - Source code in ConfD-plugins/Plugin#2:ConfD-xfstests/
  - Replaces configuration states of the test cases in xfstests to increase configuration coverage and identify failed cases
  
- **Plugin#6: ConfD-e2fsprogs**
  - Source code in ConfD-plugins/Plugin#2:ConfD-e2fsprogs/
  - Replaces configuration states of the test cases in e2fsprogs to increase configuration coverage and identify failed cases

## System Requirements ##

ConfD requires Ubuntu 20.04 and LLVM-14.0.0

# Setup #

**Setting up LLVM**

```cd ConfD-core/Taint Analyzer/```

make sure the input json file is in the directory as "mke2fs_constraints.json"


```wget https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-14.0.0.zip```

```unzip llvm-project-llvmorg-14.0.0.zip```

```mkdir llvm-project-llvmorg-14.0.0/llvm/lib/Transforms/interPro/```

```cp interPro.cpp interPro.h CmakeLists.txt llvm-project-llvmorg-14.0.0/llvm/lib/Transforms/interPro/```

```cp -r ../dependency Analyzer/trace_analyzer llvm-project-llvmorg-14.0.0/llvm/lib/Transforms/```

Add the following lines to ../CMakeLists.txt file

  add_subdirectory(interPro)

  add_subdirectory(interPro)

```mkdir llvm-project-llvmorg-14.0.0/build/```

```cmake --build . -j48```

```cd llvm-project-llvmorg-14.0.0/build/```

**Generating LLVM-IR using clang**

  Use clang to generate the LLVM-IR of the target program enabling debug information and "-fno-discard-value-names" CFLAG

**Generating taint traces**

```cd ../../```

```python3 separate_objects.py```

**Generating dependency information**

```cd ConfD-core/Dependency Analyzer```

```python3 phase1.py *path to all the generated taint traces*```

For example, ```python3 phase1.py resize_inode meta_bg```
  
Store all the newly generated files to dependecy/ directory

```python3 phase2.py```

To see how to run each plugins, please refer to individual directories for the plugins.

# Citing ConfD #

If you cite ConfD in your research, please you following BibTeX entry:

        @inproceedings {mahmud2023confd,
          author = {Tabassum Mahmud and Om Rameshwar Gatla and Duo Zhang and Carson Love and Ryan Bumann and Mai Zheng},
          title = {{ConfD}: Analyzing Configuration Dependencies of File Systems for Fun and Profit},
          booktitle = {21st USENIX Conference on File and Storage Technologies (FAST 23)},
          year = {2023},
          isbn = {978-1-939133-32-8},
          address = {Santa Clara, CA},
          pages = {199--214},
          url = {https://www.usenix.org/conference/fast23/presentation/mahmud},
          publisher = {USENIX Association},
          month = feb,
        }

# Contact #

Tabassum Mahmud (tmahmud@iastate.edu)




