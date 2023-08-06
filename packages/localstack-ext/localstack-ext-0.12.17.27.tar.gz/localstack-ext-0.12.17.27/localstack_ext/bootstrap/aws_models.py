from localstack.utils.aws import aws_models
XEuAy=super
XEuAG=None
XEuAg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  XEuAy(LambdaLayer,self).__init__(arn)
  self.cwd=XEuAG
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.XEuAg.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,XEuAg,env=XEuAG):
  XEuAy(RDSDatabase,self).__init__(XEuAg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,XEuAg,env=XEuAG):
  XEuAy(RDSCluster,self).__init__(XEuAg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,XEuAg,env=XEuAG):
  XEuAy(AppSyncAPI,self).__init__(XEuAg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,XEuAg,env=XEuAG):
  XEuAy(AmplifyApp,self).__init__(XEuAg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,XEuAg,env=XEuAG):
  XEuAy(ElastiCacheCluster,self).__init__(XEuAg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,XEuAg,env=XEuAG):
  XEuAy(TransferServer,self).__init__(XEuAg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,XEuAg,env=XEuAG):
  XEuAy(CloudFrontDistribution,self).__init__(XEuAg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,XEuAg,env=XEuAG):
  XEuAy(CodeCommitRepository,self).__init__(XEuAg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
