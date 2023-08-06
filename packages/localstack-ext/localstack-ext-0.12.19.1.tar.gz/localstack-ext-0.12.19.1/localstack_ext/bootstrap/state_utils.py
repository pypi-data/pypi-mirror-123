import logging
vsIwr=bool
vsIwF=hasattr
vsIwX=set
vsIwS=True
vsIwR=False
vsIwG=isinstance
vsIwD=dict
vsIwU=getattr
vsIwO=None
vsIwL=str
vsIwY=Exception
vsIwE=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[vsIwr,Set]:
 if vsIwF(obj,"__dict__"):
  visited=visited or vsIwX()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return vsIwS,visited
  visited.add(wrapper)
 return vsIwR,visited
def get_object_dict(obj):
 if vsIwG(obj,vsIwD):
  return obj
 obj_dict=vsIwU(obj,"__dict__",vsIwO)
 return obj_dict
def is_composite_type(obj):
 return vsIwG(obj,(vsIwD,OrderedDict))or vsIwF(obj,"__dict__")
def api_states_traverse(api_states_path:vsIwL,side_effect:Callable[...,vsIwO],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except vsIwY as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with vsIwE(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except vsIwY as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
