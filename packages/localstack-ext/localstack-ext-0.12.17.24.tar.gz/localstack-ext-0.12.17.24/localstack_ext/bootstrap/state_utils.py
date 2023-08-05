import logging
sqtke=bool
sqtkU=hasattr
sqtkO=set
sqtkM=True
sqtkl=False
sqtkp=isinstance
sqtkP=dict
sqtkR=getattr
sqtkK=None
sqtkf=str
sqtkS=Exception
sqtkr=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[sqtke,Set]:
 if sqtkU(obj,"__dict__"):
  visited=visited or sqtkO()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return sqtkM,visited
  visited.add(wrapper)
 return sqtkl,visited
def get_object_dict(obj):
 if sqtkp(obj,sqtkP):
  return obj
 obj_dict=sqtkR(obj,"__dict__",sqtkK)
 return obj_dict
def is_composite_type(obj):
 return sqtkp(obj,(sqtkP,OrderedDict))or sqtkU(obj,"__dict__")
def api_states_traverse(api_states_path:sqtkf,side_effect:Callable[...,sqtkK],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except sqtkS as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with sqtkr(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except sqtkS as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
