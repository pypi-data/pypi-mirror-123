from third_sdk.jd.api.base import RestApi

class AddressTownsByCountyIdQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.id = None

		def getapiname(self):
			return 'biz.address.townsByCountyId.query'

		def get_version(self):
			return '1.0'
			
	




