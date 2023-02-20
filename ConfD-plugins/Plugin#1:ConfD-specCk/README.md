## ConfD-specCk ##

This program will take a manpage as input and parse out the options and features part of the manpage. Then look for self dependencies and cross dependencies to determine if there are any dependencies that have a enable/disable relationship. Then print out the discovered dependencies in a json format to a file named jsonfile.json.

**Running ConfD-specCk**

```python3 main.py \<manfile\>```  

For example, ```python3 main.py mke2fs.8```


**Running Json Compare**

```python3 jsonCompare.py \<ConfD-specCK jsonfile\> \<taint analysis jsonfile\>```

For example, ```python3 jsonCompare.py jsonfile.json mke2fs_constraints.json
