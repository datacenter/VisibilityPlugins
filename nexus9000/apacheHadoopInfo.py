"""                                                                             
The script examples provided by Cisco for your use are provided for reference on
They are intended to facilitate development of your own scripts and software tha
and software.  Although Cisco has made efforts to create script examples that wi
or software development,  Cisco assumes no liability for or support obligations 
examples or any results obtained using or referring to the script examples.     
                                                                                
Author: Samuel Kommu                                                            
eMail:  sakommu@cisco.com                                                       
"""

import urllib2
import re
import json
from cisco import *

set_global_vrf("default")
dnLiveNodes = []
TAG_RE = re.compile(r'<[^>]+>')

def get_data_nodes(server_ip):
   if len(server_ip) == 0:
      return json.loads("{ \"Data Node List\": [{\"Node Name\":\"Server Name/IP\", \"Node IP\":\"Not Provided\"}]}")
   dn_info=urllib2.urlopen("http://" + server_ip + ":50070/dfsnodelist.jsp?whatNodes=LIVE")
   dn_list = "{ \"Data Node List\": ["
   first_node=True
   for each_dn in dn_info.read().split("\n"):
      if "50010" in each_dn:
         data_node = ','.join(TAG_RE.sub(' ',each_dn).split()).split(",")
         if first_node <> True:
            dn_list = dn_list + ",{"
         else:
            first_node = False
            dn_list = dn_list + "{"
         dn_list = dn_list + "\"Name\":\"" + data_node[0] + "\""
         dn_list = dn_list + ", \"IP\":\"" + data_node[1].split(":")[0] + "\""
         dn_list = dn_list + "}"
   dn_list = dn_list + "]}"
   return json.loads(dn_list)

def get_node_managers_old(server_ip=[]):
   if len(server_ip) == 0:
      return json.loads("{ \"Node Managers List\": [{\"Node Name\":\"Server Name/IP not provided\"}]}")
   nm_info=urllib2.urlopen("http://" + server_ip + ":8088/cluster/nodes") 
   nm_list = "{ \"Node Managers List\": ["
   first_node=True
   for each_nm in nm_info:
      if "8042" in each_nm:
         node_manager=','.join(TAG_RE.sub(' ',each_nm).split()).split(":")[0]
         if first_node <> True:
            nm_list = nm_list + ",{\"Node Name\":\"" + node_manager + "\"}"
         else:
            nm_list = nm_list + "{\"Node Name\":\"" + node_manager + "\"}"
            first_node = False
   nm_list = nm_list + "]}"
   return json.loads(nm_list)

def get_node_managers(server_ip=[]):
   if len(server_ip) == 0:
      return json.loads("{ \"Node Managers List\": [{\"Node Name\":\"Server Name/IP not provided\"}]}")
   req = urllib2.Request("http://" + server_ip + ":8088/ws/v1/cluster/nodes")
   nm_info=urllib2.urlopen(req) 
   return json.loads(nm_info.read())

def get_job_info(server_ip=[]):
   if len(server_ip) == 0:
      return 
   req = urllib2.Request("http://" + server_ip + ":8088/ws/v1/cluster/apps")
   return json.loads(urllib2.urlopen(req).read())

def get_app_info(server_ip=[]):
   if len(server_ip) == 0:
      return 
   req = urllib2.Request("http://" + server_ip + ":8088/ws/v1/cluster/apps")
   return json.loads(urllib2.urlopen(req).read())

def get_task_info(server_ip=[], app_id=[]):
   if len(server_ip) == 0:
      return
   req = urllib2.Request("http://" + server_ip + ":8088/proxy/" + app_id + "/ws/v1/mapreduce/jobs/")
#   not implentend - per task info - is this really necessary?
#   job_info = json.loads(urllib2.urlopen(req.read())
#   req = urllib2.Request("http://" + server_ip + ":8088/proxy/" + app_id + "/ws/v1/mapreduce/jobs/" + + "tasks")
   return json.loads(urllib2.urlopen(req).read())

def get_app_stat_info(server_ip=[]):
   if len(server_ip) == 0:
      return 
   req = urllib2.Request("http://" + server_ip + ":8088/ws/v1/cluster/appstatistics?states=accepted,running,finished&applicationTypes=mapreduce")
   return json.loads(urllib2.urlopen(req).read())

