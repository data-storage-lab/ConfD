## Plugin#5 ConfD-xfstests ##

github: https://github.com/data-storage-lab/ConfD

This plugin utilizes the xfstests testing suite to test configurations generated from the State Generator. 
There are two scripts included in this plugin:

single_test - allows for a list of configurations to be tested against a single xfstests
bulk_test - allows for a list of configurations to be tested against a list of xfstests


Setup:
	To run this script, you must first set up xfstests. Directions to do this can be found on their github. 
	
	xfstests: https://github.com/kdave/xfstests

	After setting up xfstests, place the files from this directory into the root directory of xfstests (the one that has the "check" script)


Inputs: 

	config_state.txt - file generated from the State Generator. Should be placed at the same directory level as the script. 

	valid_<list_name> - when running the bulk_test script, you must specify which list of tests to run. We have provided a number of examples prefixed with "valid_"


Running the script:

	./single_test <test_path>
	
	Example:
	
	./single_test ext4/006
	
	./bulk_test <test_list>
	
	Example:
	
	./bulk_test valid_generic.txt


Reading the results: 

	The script will print run time details to screen, which can be useful for identifying hangs. For the bulk_test script, a file called "bulk_results.txt" will also summarize how each individual xfstest went. 
	
	Whenever a test fails, a number of key files are stored in the ./fails/ directory. These include a copy of the modified test, and log files XFSTests provides. 
