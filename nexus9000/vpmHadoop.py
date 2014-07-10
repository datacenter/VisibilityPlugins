"""                                                                             
The script examples provided by Cisco for your use are provided for reference on
They are intended to facilitate development of your own scripts and software tha
and software.  Although Cisco has made efforts to create script examples that wi
or software development,  Cisco assumes no liability for or support obligations 
examples or any results obtained using or referring to the script examples.     
                                                                                
Author: Samuel Kommu                                                            
eMail:  sakommu@cisco.com                                                       
"""

import sys
from bufferInfo import *
from interfaceInfo import *
from apacheHadoopInfo import *
from miscRoutines import *

hadoop_cluster_list = "10.10.10.101"

data_nodes=get_data_nodes(hadoop_cluster_list)
node_managers=get_node_managers(hadoop_cluster_list)

ip_list = []
for each_node in data_nodes["Data Node List"]:
   ip_list.append(each_node["IP"])

port_list = []
ip2port_map=json.loads(open("/bootflash/hadoopModule/ip2port_map.dat").read())
for each_port in ip2port_map["IP Port Map"]:
   port_list.append(each_port["Port"])
sorted_port_list=sorted(set(port_list))

cdp_info=get_cdp_neighbor_info(sorted_port_list)

interface_counters=get_interface_counters(sorted_port_list)
buffer_info=get_buffer_info(sorted_port_list)

cluster=get_node_port_map(data_nodes,ip2port_map,cdp_info,interface_counters,buffer_info)

def print_port_info(cluster,port):
   found_port = False
   for node in cluster["Cluster"]:
      if node["Port"] == port:
         found_port = True;
         if node["Neighbor"] == "local":
            for key in node.keys():
               if key == "IP":
                  server_ip = node[key]
               for print_format in json.loads(print_formats)["Print Formats"]:                    
                  for pf_key in print_format.keys():                                              
                     if pf_key == key:                                                            
                        print print_format[key]["Title"].ljust(15) + "\t" + node[key]
   if found_port <> True:
      return "NA"
   return server_ip
 
def print_keys(cluster,keys,local=True,details=False):
   header_line = ""
   spine_printed = False
   hr_length=0
   for key in keys:
      for print_format in json.loads(print_formats)["Print Formats"]:
         for pf_key in print_format.keys(): 
            if pf_key == key:
               header_line += print_format[key]["Title"].ljust(int(print_format[key]["Pad"]))
               hr_length += int(print_format[key]["Pad"])

   print header_line
   hr_line = "-" * hr_length
   print hr_line

   for node in cluster["Cluster"]:
      line = ""
      for key in keys:
     
         for print_format in json.loads(print_formats)["Print Formats"]:
            for pf_key in print_format.keys():
               if pf_key == key:
                  pf_key_found = True
                  break

            if local == True:
               if node["Neighbor"] == "local":
                  if key == "eth_bw":
                     line += str(int(node[key])/1000/1000).ljust(int(print_format[key]["Pad"]))
                  else:
                     line += node[key].ljust(int(print_format[key]["Pad"]))
            else:
               if node["Neighbor"] != "local":
                  if spine_printed == True:
                     if key in ("eth_bw","eth_inrate1_bits","eth_outrate1_bits","Ingress Hairpin Traffic"):
                        continue
                  else:
                     if key == "eth_bw":
                        line += str(int(node[key])/1000/1000).ljust(int(print_format[key]["Pad"]))
                     else:
                        line += node[key].ljust(int(print_format[key]["Pad"]))
                     if key == "Ingress Hairpin Traffic": 
                        spine_printed = True
               else:
                  if key == "eth_bw":
                     line += str(int(node[key])/1000/1000).ljust(int(print_format[key]["Pad"]))
                  else:
                     line += node[key].ljust(int(print_format[key]["Pad"]))

               
      if line <> "":
         print line

def print_app_info():
   app_info=get_app_info(hadoop_cluster_list)
   print ""
   print "Job ID\t   Job Name\tHost Name\tApplication\tProgress %"
   print "------------------------------------------------------------------"
   for app in app_info["apps"]["app"]:
      if app["state"] ==  "RUNNING":
         print app["id"].split("_")[2] + "\t" + app["name"].rjust(10) + "\t" + app["amHostHttpAddress"].split(":")[0] + "\t" + app["applicationType"] + "\t" + str(app["progress"])
   print "------------------------------------------------------------------"


if len(sys.argv) > 1:                                                                                                          
   if sys.argv[1] == "localNodes":                                                                                              
      print_keys(cluster,["Name","Port","eth_bw","eth_inrate1_bits","eth_outrate1_bits","Ingress Hairpin Traffic"])
         
   elif sys.argv[1] == "allNodes":                                                                                              
      print_keys(cluster,["Name","Port","Neighbor","eth_bw"],False)

   elif sys.argv[1] == "allNodesJobs":
      print_keys(cluster,["Name","Port","Neighbor","eth_bw"],False)
      print_app_info()

   elif sys.argv[1] == "allNodesDetails":
      print_keys(cluster,["Name","Port","Neighbor","eth_bw","eth_inrate1_bits","eth_outrate1_bits","Ingress Hairpin Traffic"],False)
      print_app_info()

   elif sys.argv[1] == "port":    
      if len(sys.argv) > 2:                                                                                          
         server_ip=print_port_info(cluster,sys.argv[2])
         if server_ip <> "NA":
            print_app_info()

