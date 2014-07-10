"""                                                                             
The script examples provided by Cisco for your use are provided for reference on
They are intended to facilitate development of your own scripts and software tha
and software.  Although Cisco has made efforts to create script examples that wi
or software development,  Cisco assumes no liability for or support obligations 
examples or any results obtained using or referring to the script examples.     
                                                                                
Author: Samuel Kommu                                                            
eMail:  sakommu@cisco.com                                                       
"""

from __future__ import division
import urllib2
import re
import json
from cli import *
from miscRoutines import *

def throughput_fmt(num):
   return "%1.2f" % (num/1024/1024/1024)

def get_interface_counters(port_list=[]):
   sh_int_output=json.loads(clid("show interface"))
   int_state = "{\"Interface Counters\": ["

   counter_list = ["eth_mtu", "eth_bw", "eth_inrate1_bits", "eth_outrate1_bits"]

   first_line = True
   for each_int in sh_int_output["TABLE_interface"]["ROW_interface"]:
      if "Ethernet" in each_int["interface"]:
         interface_name = each_int["interface"].replace("ernet","")
         for each_port in port_list:
            if each_port == interface_name:
               if first_line <> True:
                  int_state = int_state + ",{ \"Port\":\"" + interface_name + "\""
               else:
                  first_line = False
                  int_state = int_state + "{ \"Port\":\"" + interface_name + "\""

               for each_counter in counter_list:
                  int_state = int_state + ",\"" + each_counter + "\""
                  int_state = int_state + ":\"" + each_int[each_counter] + "\""
               int_state = int_state + "}" 
   int_state = int_state + "]}"
   return json.loads(int_state)

def get_ip2mac_map(ips_to_check=[]):
   for each_ip in ips_to_check:
      cli("ping " + each_ip)   
   
   ip_adj_counter_list = ["ip-addr-out", "mac"]
   mac_add_dyn_counter_list = ["disp_port", "disp_mac_addr"]

   sh_ip_adj_output=json.loads(clid("show ip adj"))
   sh_mac_add_dyn_output=json.loads(clid("show mac address-table dynamic"))

   ip_port_table = "{ \"IP Port Map\": ["

   first_line = True
   for each_ip in ips_to_check:
      for each_ip_mac in sh_ip_adj_output["TABLE_vrf"]["ROW_vrf"]["TABLE_afi"]["ROW_afi"]["TABLE_adj"]["ROW_adj"]:
         if each_ip == each_ip_mac["ip-addr-out"]:
            for each_mac_line in sh_mac_add_dyn_output["TABLE_mac_address"]["ROW_mac_address"]:
               if each_mac_line["disp_mac_addr"] == each_ip_mac["mac"]:
                  port_name = each_mac_line["disp_port"].replace("ernet","")
                  if first_line <> True:
                     ip_port_table = ip_port_table + ",{\"Port\":\"" + port_name + "\""
                  else:
                     ip_port_table = ip_port_table + "{\"Port\":\"" + port_name + "\""
                     first_line = False
                  ip_port_table = ip_port_table + ",\"IP\":\"" + each_ip_mac["ip-addr-out"] + "\"}"

   ip_port_table = ip_port_table + "]}"
   return json.loads(ip_port_table)

def get_cdp_neighbor_info(port_list=[]):
   cdp_info=json.loads(clid("show cdp neighbors"))
   
   cdp_list = "{\"CDP Info\": ["
   first_line = True
   for port in port_list:
      for cdp_neighbor in cdp_info["TABLE_cdp_neighbor_brief_info"]["ROW_cdp_neighbor_brief_info"]:
         if port == cdp_neighbor["intf_id"].replace("ernet",""):
            if first_line <> True:
               cdp_list += ","
            else:
               first_line = False
            cdp_list += "{" + get_kv_pair("Port",port)
            cdp_list += "," + get_kv_pair("Neighbor",cdp_neighbor["device_id"].split("(")[0]) 
            cdp_list += "}"
   cdp_list += "]}"
   return json.loads(cdp_list)
