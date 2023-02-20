## Plugin#6 ConfD-e2fsprogs ###

github: https://github.com/data-storage-lab/ConfD

This plugin utilizes the e2fsprogs testing suite to test configurations generated from the State Generator. 
There are two scripts included in this plugin:

single_test - allows for a list of configurations to be tested against a single e2fsprogs test
bulk_test - allows for a list of configurations to be tested against a list of e2fsprogs test

Setup:
	To run this script, you must first set up e2fsprogs. Directions to do this can be found on their github. 
	
	e2fsprogs: https://github.com/tytso/e2fsprogs

	After setting up e2fsprogs, place the files from this directory into the root directory of e2fsprogs


Inputs: 

	config_state.txt - file generated from the State Generator. Should be placed at the same directory level as the script. 

	valid_<list_name> - when running the bulk_test script, you must specify which list of tests to run. We have provided a number of examples prefixed with "valid_"


Running the script:

	./single_test <test_path>
	
	Example:
	./single_test d_fallocate
	
	
	./bulk_test <test_list>
	
	Example:
	./bulk_test valid_f_type.txt
	
	
Reading the results: 

	The script will print run time details to screen, which can be useful for identifying hangs. For the bulk_test script, a file called "bulk_results.txt" will also summarize how each individual e2fsprogs test went. 
	
	Whenever a test fails, a number of key files are stored in the ./fails/ directory. These include a copy of the modified test, and log files e2fsprogs provides. 
