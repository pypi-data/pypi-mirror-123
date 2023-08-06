from localstack.utils.aws import aws_models
WnczI=super
Wnczh=None
WnczX=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  WnczI(LambdaLayer,self).__init__(arn)
  self.cwd=Wnczh
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.WnczX.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,WnczX,env=Wnczh):
  WnczI(RDSDatabase,self).__init__(WnczX,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,WnczX,env=Wnczh):
  WnczI(RDSCluster,self).__init__(WnczX,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,WnczX,env=Wnczh):
  WnczI(AppSyncAPI,self).__init__(WnczX,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,WnczX,env=Wnczh):
  WnczI(AmplifyApp,self).__init__(WnczX,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,WnczX,env=Wnczh):
  WnczI(ElastiCacheCluster,self).__init__(WnczX,env=env)
class TransferServer(BaseComponent):
 def __init__(self,WnczX,env=Wnczh):
  WnczI(TransferServer,self).__init__(WnczX,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,WnczX,env=Wnczh):
  WnczI(CloudFrontDistribution,self).__init__(WnczX,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,WnczX,env=Wnczh):
  WnczI(CodeCommitRepository,self).__init__(WnczX,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
