from localstack.utils.aws import aws_models
OumCc=super
OumCy=None
OumCQ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  OumCc(LambdaLayer,self).__init__(arn)
  self.cwd=OumCy
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.OumCQ.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,OumCQ,env=OumCy):
  OumCc(RDSDatabase,self).__init__(OumCQ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,OumCQ,env=OumCy):
  OumCc(RDSCluster,self).__init__(OumCQ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,OumCQ,env=OumCy):
  OumCc(AppSyncAPI,self).__init__(OumCQ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,OumCQ,env=OumCy):
  OumCc(AmplifyApp,self).__init__(OumCQ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,OumCQ,env=OumCy):
  OumCc(ElastiCacheCluster,self).__init__(OumCQ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,OumCQ,env=OumCy):
  OumCc(TransferServer,self).__init__(OumCQ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,OumCQ,env=OumCy):
  OumCc(CloudFrontDistribution,self).__init__(OumCQ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,OumCQ,env=OumCy):
  OumCc(CodeCommitRepository,self).__init__(OumCQ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
