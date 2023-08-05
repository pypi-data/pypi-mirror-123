from localstack.utils.aws import aws_models
oIEXF=super
oIEXh=None
oIEXJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  oIEXF(LambdaLayer,self).__init__(arn)
  self.cwd=oIEXh
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.oIEXJ.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,oIEXJ,env=oIEXh):
  oIEXF(RDSDatabase,self).__init__(oIEXJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,oIEXJ,env=oIEXh):
  oIEXF(RDSCluster,self).__init__(oIEXJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,oIEXJ,env=oIEXh):
  oIEXF(AppSyncAPI,self).__init__(oIEXJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,oIEXJ,env=oIEXh):
  oIEXF(AmplifyApp,self).__init__(oIEXJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,oIEXJ,env=oIEXh):
  oIEXF(ElastiCacheCluster,self).__init__(oIEXJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,oIEXJ,env=oIEXh):
  oIEXF(TransferServer,self).__init__(oIEXJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,oIEXJ,env=oIEXh):
  oIEXF(CloudFrontDistribution,self).__init__(oIEXJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,oIEXJ,env=oIEXh):
  oIEXF(CodeCommitRepository,self).__init__(oIEXJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
