"""
The script examples provided by Cisco for your use are provided for reference only as a customer courtesay.
They are intended to facilitate development of your own scripts and software that interoperate with Cisco switches
and software.  Although Cisco has made efforts to create script examples that will be effective as aids to script
or software development,  Cisco assumes no liability for or support obligations related to the use of the script
examples or any results obtained using or referring to the script examples.

Author: Samuel Kommu
eMail:  sakommu@cisco.com
"""

from cisco import *
from cli import *
import json

def get_buffer_info(portList = []):
   buffer_info=json.loads(clid("show hardware internal buffer info pkt-stats detail"))
   buffer_info_ns=json.loads(clid("show hardware internal ns buffer info pkt-stats detail"))
   buffer_port_map_all=cli("show interface hardware-mappings | grep Eth")
   
   buffer_used="{ \"Buffer Info\" : [";
   buffer_port_map = []
   for each_port in portList:
      for eachLine in buffer_port_map_all.split("\n"):
         if eachLine <> "":
            if each_port == eachLine.split()[0]:
               buffer_port_map.append(eachLine)

   first_run=True
   for each_port in buffer_port_map:
      if first_run == True:
         buffer_used=buffer_used + "{\"Port\":\"" + each_port.split()[0] + "\""
      else:
         buffer_used=buffer_used + ", {\"Port\":\"" + each_port.split()[0] + "\""
      first_run=False
      module_no=each_port.split()[2]
      port_no=int(each_port.split()[4])
      for each_module in buffer_info["TABLE_module"]["ROW_module"]["module_number"]:
         if buffer_info["TABLE_module"]["ROW_module"]["module_number"] == module_no:
            buffer_used=buffer_used + ",\"ucast_count_4\":\"" + buffer_info["TABLE_module"]["ROW_module"]["TABLE_instance"]["ROW_instance"]["TABLE_interface"]["ROW_interface"][port_no]["ucast_count_4"] + "\""

      for each_row in buffer_info_ns["TABLE_module"]["ROW_module"]["TABLE_instance"]["ROW_instance"]["TABLE_direction"]["ROW_direction"]:
         found_eoq=False
         buffer_used=buffer_used + ",\"" + each_row["direction"] + "\""
         try:
            for each_eoq in each_row["TABLE_eoq"]["ROW_eoq"]:
               if "BCM " + str(port_no) in str(each_eoq):
                  found_eoq=True
                  buffer_used=buffer_used + ":\"" + each_eoq["eoq_count_0"] + "\""
         except KeyError:  
            buffer_used = buffer_used + ":\"NA\""
            found_eoq = True
            pass
         if found_eoq == False:
            buffer_used = buffer_used + ":\"0\""
      buffer_used=buffer_used + "}"

   buffer_used=buffer_used + "]}"
   return json.loads(buffer_used)
