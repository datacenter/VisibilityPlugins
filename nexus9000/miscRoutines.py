"""
The script examples provided by Cisco for your use are provided for reference on
They are intended to facilitate development of your own scripts and software tha
and software.  Although Cisco has made efforts to create script examples that wi
or software development,  Cisco assumes no liability for or support obligations
examples or any results obtained using or referring to the script examples.

Author: Samuel Kommu
eMail:  sakommu@cisco.com
"""
import json
from types import *

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1000.0

def print_hd(hadoop_details):
   toPrint = ""
   print "Server\tPort\tInRate\tOutRate\tBuffer"
   for line in hadoopDetails.split("\n"):
      if "Eth" in line:
         fields = line.split()
         toPrint = fields[0] + "\t"
         toPrint = to_print + fields[1] + "\t"
         toPrint = to_print + fields[2] + "\t"
         toPrint = to_print + sizeof_fmt(fields[3]) + "\t"
         toPrint = to_print + sizeof_fmt(fields[4]) + "\t"
         toPrint = to_print + fields[5]
   print toPrint

def get_node_port_map(data_nodes,ip2port_map,cdp_info,interface_counters,buffer_info):                                  
                                                                               
   first_line = True                                                       
   cluster_node_list = "{\"Cluster\": ["            
   for node in data_nodes["Data Node List"]:   
      for port in ip2port_map["IP Port Map"]:  
         if node["IP"] == port["IP"]:     
            if first_line <> True:                  
               cluster_node_list += "," + "{\"Name\":\"" + node["Name"] + "\""
            else:                                                                  
               cluster_node_list += "{\"Name\":\"" + node["Name"] + "\""      
               first_line = False                                                  
            for key in port.keys():
               cluster_node_list += "," + get_kv_pair(key,port[key])
            break

      for interface in cdp_info["CDP Info"]:
         remote = False
         if port["Port"] == interface["Port"]:
            for key in interface.keys():                      
               if key <> "Port":
                  cluster_node_list += "," + get_kv_pair(key,interface[key])
                  remote = True
            break
         if remote == False:
            cluster_node_list += "," + get_kv_pair("Neighbor","local")

      for interface in interface_counters["Interface Counters"]:
         if port["Port"] == interface["Port"]:
            for key in interface.keys():                      
               if key <> "Port":
                  cluster_node_list += "," + get_kv_pair(key,interface[key])
            break

      for interface in buffer_info["Buffer Info"]:
         if port["Port"] == interface["Port"]:
            for key in interface.keys():                      
               if key <> "Port":
                  cluster_node_list += "," + get_kv_pair(key,interface[key])
            break

      cluster_node_list += "}"
   cluster_node_list += "]}"

   return json.loads(cluster_node_list)

def get_kv_pair(key,value):                                                   
   return "\"" + key + "\":\"" + value + "\""
   
print_formats = """{\"Print Formats\": [ {
   \"Name\" : { \"Pad\":\"12\", \"Title\":\"Node Name\" },
   \"eth_mtu\" : { \"Pad\":\"5\", \"Title\":\"MTU\" },
   \"IP\" : { \"Pad\":\"16\", \"Title\":\"IP\" },
   \"eth_bw\" : { \"Pad\":\"6\", \"Title\":\"Speed\" },
   \"Egress Straight Traffic\" : { \"Pad\":\"5\", \"Title\":\"B-EST\" },
   \"eth_outrate1_bits\" : { \"Pad\":\"16\", \"Title\":\"OutRate\" },
   \"ucast_count_4\" : { \"Pad\":\"5\", \"Title\":\"Buffer\" },
   \"Ingress Straight Traffic\" : { \"Pad\":\"5\", \"Title\":\"B-IST\" },
   \"eth_inrate1_bits\" : { \"Pad\":\"16\", \"Title\":\"InRate\" },
   \"Ingress Hairpin Traffic\" : { \"Pad\":\"5\", \"Title\":\"B-IHT\" },
   \"Neighbor\" : { \"Pad\":\"12\", \"Title\":\"Neighbor\" },
   \"Port\" : { \"Pad\":\"8\", \"Title\":\"Port\" }}]}"""

