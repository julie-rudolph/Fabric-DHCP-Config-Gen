#!/usr/bin/python

# This script creates tcl scripts to configure a Nexus 9000 to support DHCP relay.  A JSON file provides
# the necessary information to generate the config.  

# This script takes a file in JSON format as input.
## Specify the file name in the parameter json_parameter_file below.
## Sample format of the JSON file is below.

# The script then renders a configuration based upon a Jinja2 template file.
## Specify the jinja2 file in the template_file parameter below.

# For each hostname in the JSON file, the script outputs a Cisco NX-OS tcl script that can then be
# copied to the switch and run from the switch itself.

# SAMPLE JSON FILE #
#{
#  "switch1": {
#    "Vlan415": {
#      "vlannum": "415",
#      "dhcploopaddr": "10.205.0.161"
#    },
#    "Vlan416": {
#      "vlannum": "416",
#      "dhcploopaddr": "10.205.0.193"
#    },
#    "Vlan417": {
#      "vlannum": "417",
#      "dhcploopaddr": "10.205.0.225"
#    },
#    "Vlan466": {
#      "vlannum": "466",
#      "dhcploopaddr": "10.204.0.65"
#    },
#    "Vlan467": {
#      "vlannum": "467",
#      "dhcploopaddr": "10.204.0.97"
#    },
#     "Vlan478": {
#      "vlannum": "478",
#      "dhcploopaddr": "10.205.3.33"
#    }
#  },
#  "switch2": {
#    "Vlan415": {
#      "vlannum": "415",
#      "dhcploopaddr": "10.205.0.162"
#    },
#    "Vlan416": {
#      "vlannum": "416",
#      "dhcploopaddr": "10.205.0.194"
#    },
#    "Vlan417": {
#      "vlannum": "417",
#      "dhcploopaddr": "10.205.0.226"
#    },
#    "Vlan466": {
#      "vlannum": "466",
#      "dhcploopaddr": "10.204.0.66"
#    },
#    "Vlan467": {
#      "vlannum": "467",
#      "dhcploopaddr": "10.204.0.98"
#    },
#     "Vlan478": {
#      "vlannum": "478",
#      "dhcploopaddr": "10.205.3.34"
#    }
#  }


import jinja2
import os
import json

json_parameter_file = "sample-dhcp-jsonfile.json"
template_file = "fabricdhcp.j2.sample"

config_parameters = []
output_directory = "_output-sample"

# 1. Create Python dictionary from the JSON file. 
print("Read JSON parameter file...")
json1_file = open(json_parameter_file)
json1_str = json1_file.read()
json1_dict = json.loads(json1_str)

# 3. Create the central Jinja2 environment and we will load
# the Jinja2 template file
print("Create Jinja2 environment...")
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
template = env.get_template(template_file)

# 4. We will create the output directory if it doesn't already exist.
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# 5. For each hostname in the Python dictionary, process the Jinja2 template and output to unique file
# per hostname.
for hostname, values in json1_dict.iteritems():
	print "hostname is %s" % (hostname)
	valtype = type(values)
	#print "valtype is %s" % (valtype)
	result = template.render(values=values)
	#print result
	f = open(os.path.join(output_directory, hostname + ".config.tcl"), "w")
	f.write(result)
	f.close()
	print("Configuration '%s' created..." % (hostname + ".config.tcl"))
	print("DONE")
