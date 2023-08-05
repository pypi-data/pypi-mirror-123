# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkecs.endpoint import endpoint_data

class CreateAutoSnapshotPolicyRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ecs', '2014-05-26', 'CreateAutoSnapshotPolicy','ecs')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_ResourceOwnerId(self): # Long
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self, ResourceOwnerId):  # Long
		self.add_query_param('ResourceOwnerId', ResourceOwnerId)
	def get_CopiedSnapshotsRetentionDays(self): # Integer
		return self.get_query_params().get('CopiedSnapshotsRetentionDays')

	def set_CopiedSnapshotsRetentionDays(self, CopiedSnapshotsRetentionDays):  # Integer
		self.add_query_param('CopiedSnapshotsRetentionDays', CopiedSnapshotsRetentionDays)
	def get_timePoints(self): # String
		return self.get_query_params().get('timePoints')

	def set_timePoints(self, timePoints):  # String
		self.add_query_param('timePoints', timePoints)
	def get_repeatWeekdays(self): # String
		return self.get_query_params().get('repeatWeekdays')

	def set_repeatWeekdays(self, repeatWeekdays):  # String
		self.add_query_param('repeatWeekdays', repeatWeekdays)
	def get_ResourceGroupId(self): # String
		return self.get_query_params().get('ResourceGroupId')

	def set_ResourceGroupId(self, ResourceGroupId):  # String
		self.add_query_param('ResourceGroupId', ResourceGroupId)
	def get_Tags(self): # RepeatList
		return self.get_query_params().get('Tag')

	def set_Tags(self, Tag):  # RepeatList
		for depth1 in range(len(Tag)):
			if Tag[depth1].get('Value') is not None:
				self.add_query_param('Tag.' + str(depth1 + 1) + '.Value', Tag[depth1].get('Value'))
			if Tag[depth1].get('Key') is not None:
				self.add_query_param('Tag.' + str(depth1 + 1) + '.Key', Tag[depth1].get('Key'))
	def get_EnableCrossRegionCopy(self): # Boolean
		return self.get_query_params().get('EnableCrossRegionCopy')

	def set_EnableCrossRegionCopy(self, EnableCrossRegionCopy):  # Boolean
		self.add_query_param('EnableCrossRegionCopy', EnableCrossRegionCopy)
	def get_ResourceOwnerAccount(self): # String
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self, ResourceOwnerAccount):  # String
		self.add_query_param('ResourceOwnerAccount', ResourceOwnerAccount)
	def get_OwnerId(self): # Long
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self, OwnerId):  # Long
		self.add_query_param('OwnerId', OwnerId)
	def get_autoSnapshotPolicyName(self): # String
		return self.get_query_params().get('autoSnapshotPolicyName')

	def set_autoSnapshotPolicyName(self, autoSnapshotPolicyName):  # String
		self.add_query_param('autoSnapshotPolicyName', autoSnapshotPolicyName)
	def get_retentionDays(self): # Integer
		return self.get_query_params().get('retentionDays')

	def set_retentionDays(self, retentionDays):  # Integer
		self.add_query_param('retentionDays', retentionDays)
	def get_TargetCopyRegions(self): # String
		return self.get_query_params().get('TargetCopyRegions')

	def set_TargetCopyRegions(self, TargetCopyRegions):  # String
		self.add_query_param('TargetCopyRegions', TargetCopyRegions)
