from localstack.utils.aws import aws_models
KykTr=super
KykTm=None
KykTB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KykTr(LambdaLayer,self).__init__(arn)
  self.cwd=KykTm
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.KykTB.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,KykTB,env=KykTm):
  KykTr(RDSDatabase,self).__init__(KykTB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,KykTB,env=KykTm):
  KykTr(RDSCluster,self).__init__(KykTB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,KykTB,env=KykTm):
  KykTr(AppSyncAPI,self).__init__(KykTB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,KykTB,env=KykTm):
  KykTr(AmplifyApp,self).__init__(KykTB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,KykTB,env=KykTm):
  KykTr(ElastiCacheCluster,self).__init__(KykTB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,KykTB,env=KykTm):
  KykTr(TransferServer,self).__init__(KykTB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,KykTB,env=KykTm):
  KykTr(CloudFrontDistribution,self).__init__(KykTB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,KykTB,env=KykTm):
  KykTr(CodeCommitRepository,self).__init__(KykTB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
