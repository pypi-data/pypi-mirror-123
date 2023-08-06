from localstack.utils.aws import aws_models
NdUIE=super
NdUIB=None
NdUIw=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  NdUIE(LambdaLayer,self).__init__(arn)
  self.cwd=NdUIB
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.NdUIw.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,NdUIw,env=NdUIB):
  NdUIE(RDSDatabase,self).__init__(NdUIw,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,NdUIw,env=NdUIB):
  NdUIE(RDSCluster,self).__init__(NdUIw,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,NdUIw,env=NdUIB):
  NdUIE(AppSyncAPI,self).__init__(NdUIw,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,NdUIw,env=NdUIB):
  NdUIE(AmplifyApp,self).__init__(NdUIw,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,NdUIw,env=NdUIB):
  NdUIE(ElastiCacheCluster,self).__init__(NdUIw,env=env)
class TransferServer(BaseComponent):
 def __init__(self,NdUIw,env=NdUIB):
  NdUIE(TransferServer,self).__init__(NdUIw,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,NdUIw,env=NdUIB):
  NdUIE(CloudFrontDistribution,self).__init__(NdUIw,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,NdUIw,env=NdUIB):
  NdUIE(CodeCommitRepository,self).__init__(NdUIw,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
