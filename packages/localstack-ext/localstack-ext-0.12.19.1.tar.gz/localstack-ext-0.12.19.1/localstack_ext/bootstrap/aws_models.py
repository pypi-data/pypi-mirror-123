from localstack.utils.aws import aws_models
GsExe=super
GsExX=None
GsExr=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  GsExe(LambdaLayer,self).__init__(arn)
  self.cwd=GsExX
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.GsExr.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,GsExr,env=GsExX):
  GsExe(RDSDatabase,self).__init__(GsExr,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,GsExr,env=GsExX):
  GsExe(RDSCluster,self).__init__(GsExr,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,GsExr,env=GsExX):
  GsExe(AppSyncAPI,self).__init__(GsExr,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,GsExr,env=GsExX):
  GsExe(AmplifyApp,self).__init__(GsExr,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,GsExr,env=GsExX):
  GsExe(ElastiCacheCluster,self).__init__(GsExr,env=env)
class TransferServer(BaseComponent):
 def __init__(self,GsExr,env=GsExX):
  GsExe(TransferServer,self).__init__(GsExr,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,GsExr,env=GsExX):
  GsExe(CloudFrontDistribution,self).__init__(GsExr,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,GsExr,env=GsExX):
  GsExe(CodeCommitRepository,self).__init__(GsExr,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
