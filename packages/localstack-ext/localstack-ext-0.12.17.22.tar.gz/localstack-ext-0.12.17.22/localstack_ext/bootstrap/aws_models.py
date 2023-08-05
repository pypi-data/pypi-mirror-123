from localstack.utils.aws import aws_models
donjI=super
donjy=None
donjM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  donjI(LambdaLayer,self).__init__(arn)
  self.cwd=donjy
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.donjM.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,donjM,env=donjy):
  donjI(RDSDatabase,self).__init__(donjM,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,donjM,env=donjy):
  donjI(RDSCluster,self).__init__(donjM,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,donjM,env=donjy):
  donjI(AppSyncAPI,self).__init__(donjM,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,donjM,env=donjy):
  donjI(AmplifyApp,self).__init__(donjM,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,donjM,env=donjy):
  donjI(ElastiCacheCluster,self).__init__(donjM,env=env)
class TransferServer(BaseComponent):
 def __init__(self,donjM,env=donjy):
  donjI(TransferServer,self).__init__(donjM,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,donjM,env=donjy):
  donjI(CloudFrontDistribution,self).__init__(donjM,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,donjM,env=donjy):
  donjI(CodeCommitRepository,self).__init__(donjM,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
