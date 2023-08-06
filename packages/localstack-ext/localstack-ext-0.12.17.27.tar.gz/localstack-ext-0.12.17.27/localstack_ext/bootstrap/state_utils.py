import logging
eyHva=bool
eyHvX=hasattr
eyHvI=set
eyHvQ=True
eyHvC=False
eyHvk=isinstance
eyHvs=dict
eyHvr=getattr
eyHvz=None
eyHvW=str
eyHvL=Exception
eyHvt=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[eyHva,Set]:
 if eyHvX(obj,"__dict__"):
  visited=visited or eyHvI()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return eyHvQ,visited
  visited.add(wrapper)
 return eyHvC,visited
def get_object_dict(obj):
 if eyHvk(obj,eyHvs):
  return obj
 obj_dict=eyHvr(obj,"__dict__",eyHvz)
 return obj_dict
def is_composite_type(obj):
 return eyHvk(obj,(eyHvs,OrderedDict))or eyHvX(obj,"__dict__")
def api_states_traverse(api_states_path:eyHvW,side_effect:Callable[...,eyHvz],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except eyHvL as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with eyHvt(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except eyHvL as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
