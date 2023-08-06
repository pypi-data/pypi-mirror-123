import logging
GWcIu=bool
GWcIR=hasattr
GWcIq=set
GWcIQ=True
GWcIO=False
GWcIb=isinstance
GWcIk=dict
GWcIa=getattr
GWcIM=None
GWcIF=str
GWcIs=Exception
GWcIw=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[GWcIu,Set]:
 if GWcIR(obj,"__dict__"):
  visited=visited or GWcIq()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return GWcIQ,visited
  visited.add(wrapper)
 return GWcIO,visited
def get_object_dict(obj):
 if GWcIb(obj,GWcIk):
  return obj
 obj_dict=GWcIa(obj,"__dict__",GWcIM)
 return obj_dict
def is_composite_type(obj):
 return GWcIb(obj,(GWcIk,OrderedDict))or GWcIR(obj,"__dict__")
def api_states_traverse(api_states_path:GWcIF,side_effect:Callable[...,GWcIM],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except GWcIs as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with GWcIw(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except GWcIs as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
