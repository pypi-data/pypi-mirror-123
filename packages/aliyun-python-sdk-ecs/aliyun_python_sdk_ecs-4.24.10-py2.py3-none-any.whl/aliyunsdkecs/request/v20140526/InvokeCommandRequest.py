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

class InvokeCommandRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ecs', '2014-05-26', 'InvokeCommand','ecs')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_ResourceOwnerId(self): # Long
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self, ResourceOwnerId):  # Long
		self.add_query_param('ResourceOwnerId', ResourceOwnerId)
	def get_CommandId(self): # String
		return self.get_query_params().get('CommandId')

	def set_CommandId(self, CommandId):  # String
		self.add_query_param('CommandId', CommandId)
	def get_Frequency(self): # String
		return self.get_query_params().get('Frequency')

	def set_Frequency(self, Frequency):  # String
		self.add_query_param('Frequency', Frequency)
	def get_RepeatMode(self): # String
		return self.get_query_params().get('RepeatMode')

	def set_RepeatMode(self, RepeatMode):  # String
		self.add_query_param('RepeatMode', RepeatMode)
	def get_WindowsPasswordName(self): # String
		return self.get_query_params().get('WindowsPasswordName')

	def set_WindowsPasswordName(self, WindowsPasswordName):  # String
		self.add_query_param('WindowsPasswordName', WindowsPasswordName)
	def get_Timed(self): # Boolean
		return self.get_query_params().get('Timed')

	def set_Timed(self, Timed):  # Boolean
		self.add_query_param('Timed', Timed)
	def get_ResourceOwnerAccount(self): # String
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self, ResourceOwnerAccount):  # String
		self.add_query_param('ResourceOwnerAccount', ResourceOwnerAccount)
	def get_OwnerAccount(self): # String
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self, OwnerAccount):  # String
		self.add_query_param('OwnerAccount', OwnerAccount)
	def get_OwnerId(self): # Long
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self, OwnerId):  # Long
		self.add_query_param('OwnerId', OwnerId)
	def get_InstanceIds(self): # RepeatList
		return self.get_query_params().get('InstanceId')

	def set_InstanceIds(self, InstanceId):  # RepeatList
		for depth1 in range(len(InstanceId)):
			self.add_query_param('InstanceId.' + str(depth1 + 1), InstanceId)
	def get_Parameters(self): # Json
		return self.get_query_params().get('Parameters')

	def set_Parameters(self, Parameters):  # Json
		self.add_query_param('Parameters', Parameters)
	def get_Username(self): # String
		return self.get_query_params().get('Username')

	def set_Username(self, Username):  # String
		self.add_query_param('Username', Username)
