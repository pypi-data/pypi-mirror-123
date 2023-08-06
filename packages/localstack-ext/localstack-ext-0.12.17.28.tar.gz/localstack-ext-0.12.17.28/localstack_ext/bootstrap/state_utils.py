import logging
chAla=bool
chAlz=hasattr
chAlV=set
chAlD=True
chAlw=False
chAlj=isinstance
chAlP=dict
chAlr=getattr
chAlb=None
chAlC=str
chAlR=Exception
chAlu=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[chAla,Set]:
 if chAlz(obj,"__dict__"):
  visited=visited or chAlV()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return chAlD,visited
  visited.add(wrapper)
 return chAlw,visited
def get_object_dict(obj):
 if chAlj(obj,chAlP):
  return obj
 obj_dict=chAlr(obj,"__dict__",chAlb)
 return obj_dict
def is_composite_type(obj):
 return chAlj(obj,(chAlP,OrderedDict))or chAlz(obj,"__dict__")
def api_states_traverse(api_states_path:chAlC,side_effect:Callable[...,chAlb],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except chAlR as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with chAlu(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except chAlR as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
