from third_sdk.jd.api.base import RestApi

class UnionDoubanBookServiceQueryBookUrlListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)

		def getapiname(self):
			return 'jingdong.UnionDoubanBookService.queryBookUrlList'

			





