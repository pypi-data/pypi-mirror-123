import logging
latBN=bool
latBe=hasattr
latBL=set
latBu=True
latBp=False
latBP=isinstance
latBJ=dict
latBb=getattr
latBI=None
latBS=str
latBj=Exception
latBC=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[latBN,Set]:
 if latBe(obj,"__dict__"):
  visited=visited or latBL()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return latBu,visited
  visited.add(wrapper)
 return latBp,visited
def get_object_dict(obj):
 if latBP(obj,latBJ):
  return obj
 obj_dict=latBb(obj,"__dict__",latBI)
 return obj_dict
def is_composite_type(obj):
 return latBP(obj,(latBJ,OrderedDict))or latBe(obj,"__dict__")
def api_states_traverse(api_states_path:latBS,side_effect:Callable[...,latBI],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except latBj as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with latBC(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except latBj as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
