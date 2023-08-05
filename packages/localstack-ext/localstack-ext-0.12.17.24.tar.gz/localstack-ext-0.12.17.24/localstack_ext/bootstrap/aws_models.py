from localstack.utils.aws import aws_models
aDlOJ=super
aDlOP=None
aDlOn=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  aDlOJ(LambdaLayer,self).__init__(arn)
  self.cwd=aDlOP
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.aDlOn.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,aDlOn,env=aDlOP):
  aDlOJ(RDSDatabase,self).__init__(aDlOn,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,aDlOn,env=aDlOP):
  aDlOJ(RDSCluster,self).__init__(aDlOn,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,aDlOn,env=aDlOP):
  aDlOJ(AppSyncAPI,self).__init__(aDlOn,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,aDlOn,env=aDlOP):
  aDlOJ(AmplifyApp,self).__init__(aDlOn,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,aDlOn,env=aDlOP):
  aDlOJ(ElastiCacheCluster,self).__init__(aDlOn,env=env)
class TransferServer(BaseComponent):
 def __init__(self,aDlOn,env=aDlOP):
  aDlOJ(TransferServer,self).__init__(aDlOn,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,aDlOn,env=aDlOP):
  aDlOJ(CloudFrontDistribution,self).__init__(aDlOn,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,aDlOn,env=aDlOP):
  aDlOJ(CodeCommitRepository,self).__init__(aDlOn,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
