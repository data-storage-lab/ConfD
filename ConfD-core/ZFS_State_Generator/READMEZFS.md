CONFIG STATE BUILDER 
github: https://github.com/data-storage-lab/ConfD

The configuration state builder is a script which generates configuration states to be tested/used in the ConfD-plugins.
There are actually two scripts which handle generating states for zfs. The first is zfs_config_state_builder, which creates valid states to be used in most of the plugins. There is also zfs_violate_config_state_builder, which creates intentionally invalid states to be used in plugin #2 
The script requires a json file input:

	zfs_constraints.json - Generated from the Dependency Analyzer script. Describes configuration parameter constraints.

Running the script:

	python3 zfs_config_state_builder.py <pool sizeforvolumes>
	
	Example:
	python3 zfs_config_state_builder.py zpool 512M
	
	
	
	python3 violate_config_state_builder.py <pool sizeforvolumes>
	
	Example:
	python3 zfs_violate_config_state_builder.py pool 512M

Reading the results:
	
	The script outputs to the terminal runtime information. Every time a new valid state is generated it notes the depth, total number of states generated, current state, and current configuration parameter being modified. This information is useful for debuging. 
	
	There is also a file generated called zfs_output.txt. This file contains all the final states generated, in a format that can be used by ConfD-plugins. 
