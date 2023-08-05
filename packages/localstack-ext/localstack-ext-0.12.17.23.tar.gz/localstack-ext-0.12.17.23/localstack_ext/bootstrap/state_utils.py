import logging
UJdwf=bool
UJdwE=hasattr
UJdws=set
UJdwD=True
UJdwh=False
UJdwB=isinstance
UJdwl=dict
UJdwI=getattr
UJdwH=None
UJdwt=str
UJdwi=Exception
UJdwG=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[UJdwf,Set]:
 if UJdwE(obj,"__dict__"):
  visited=visited or UJdws()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return UJdwD,visited
  visited.add(wrapper)
 return UJdwh,visited
def get_object_dict(obj):
 if UJdwB(obj,UJdwl):
  return obj
 obj_dict=UJdwI(obj,"__dict__",UJdwH)
 return obj_dict
def is_composite_type(obj):
 return UJdwB(obj,(UJdwl,OrderedDict))or UJdwE(obj,"__dict__")
def api_states_traverse(api_states_path:UJdwt,side_effect:Callable[...,UJdwH],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except UJdwi as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with UJdwG(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except UJdwi as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
