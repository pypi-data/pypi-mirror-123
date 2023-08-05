import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models

# Write by lyc at 2021-10-9

class CVM():
    """[腾讯云CVM云主机 Python3 SDK方法封装]
    """
    def __init__(self, key) -> None:
        self.SecretId = key['SecretId']             # 公钥
        self.SecretKey = key['SecretKey']           # 私钥
        self.endpoint = key['CVM']['endpoint']      # 接口地址
        self.Region = key['Region']                 # 地域
        self.Zone = key['Zone']                     # 可用区
        # CVM
        self.Password = key['CVM']['Password']                      # 实例密码
        self.InstanceName = key['CVM']['InstanceName']              # 实例名称
        self.InstanceType = key['CVM']['InstanceType']              # 机型
        self.ImageId = key['CVM']['ImageId']                        # 镜像id
        self.InstanceChargeType = key['CVM']['InstanceChargeType']  # 实例计费类型
        # VPC
        self.VpcId = key['VPC']['VpcId']                                        # VPC id
        self.SubnetId = key['VPC']['SubnetId']                                  # 子网 id
        self.InternetMaxBandwidthOut = key['VPC']['InternetMaxBandwidthOut']    # EIP带宽值
        self.SecurityGroupIds = key['VPC']['SecurityGroupIds']                  # 安全组id（列表）
        self.InternetChargeType = key['VPC']['InternetChargeType']              # EIP计费类型
        # 签名
        self.cred = credential.Credential(self.SecretId, self.SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = self.endpoint

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self.client = cvm_client.CvmClient(self.cred, self.Region, clientProfile)


    def describeAccountQuota(self):
        """[查询用户配额详情]https://cloud.tencent.com/document/api/213/55628

        Returns:
            [json]: [json response]
        """
        try:
            req = models.DescribeAccountQuotaRequest()
            params = {
                "Filters": [
                    {
                        "Name": "zone",
                        "Values": [ self.Zone, ],
                    }
                ]
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.DescribeAccountQuota(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err



    def describeZones(self):
        """[查询可用区列表]https://cloud.tencent.com/document/api/213/15707

        Returns:
            [json]: [json response]
        """
        try:
            req = models.DescribeZonesRequest()
            params = {

            }
            req.from_json_string(json.dumps(params))

            resp = self.client.DescribeZones(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err



    def describeInstanceTypeConfigs(self, zone, instance_family):
        """[查询实例机型列表]https://cloud.tencent.com/document/api/213/15749

        Args:
            zone ([str]): [按照【可用区】进行过滤。可用区形如：ap-guangzhou-1。]

        Returns:
            [json]: [json response]
        """
        try:
            req = models.DescribeInstanceTypeConfigsRequest()
            params = {
                "Filters": [
                    {
                        "Name": "zone",
                        "Values": [ zone, ]
                    },
                    {
                        "Name": "instance-family",
                        "Values": [ instance_family, ],
                    }
                ]
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.DescribeInstanceTypeConfigs(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err



    def runInstances(self, InstanceCount=1):
        """[创建实例]https://cloud.tencent.com/document/api/213/15730

        Args:
            InstanceCount (int, optional): [购买实例数量。包年包月实例取值范围：[1，300]，按量计费实例取值范围：[1，100]。]. 默认取值：1                      
        
        Returns:
            [json]: [json response]
        """
        try:
            req = models.RunInstancesRequest()
            params = {
                "InstanceChargeType": self.InstanceChargeType,
                "Placement": {
                    "Zone": self.Zone
                },
                "InstanceType": self.InstanceType,
                "ImageId": self.ImageId,
                "VirtualPrivateCloud": {
                    "VpcId": self.VpcId,
                    "SubnetId": self.SubnetId
                },
                "InternetAccessible": {
                    "InternetChargeType": self.InternetChargeType,
                    "InternetMaxBandwidthOut": self.InternetMaxBandwidthOut,
                    "PublicIpAssigned": True
                },
                "InstanceCount": InstanceCount,
                "InstanceName": self.InstanceName,
                "LoginSettings": {
                    "Password": self.Password
                },
                "SecurityGroupIds": self.SecurityGroupIds
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.RunInstances(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err



    def stopInstances(self, InstanceIds=[], ForceStop=True):
        """[关闭实例]https://cloud.tencent.com/document/api/213/15743

        Args:
            InstanceIds (list): [实例ID]. 
            ForceStop (bool, optional): [是否在正常关闭失败后选择强制关闭实例
                                            TRUE：表示在正常关闭失败后进行强制关闭
                                            FALSE：表示在正常关闭失败后不进行强制关闭]. Defaults to True.
        
        Returns:
            [json]: [json response]
        """
        try:
            req = models.StopInstancesRequest()
            params = {
                "InstanceIds": InstanceIds,
                "ForceStop": ForceStop
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.StopInstances(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err



    def terminateInstances(self, InstanceIds=[]):
        """[退还实例]https://cloud.tencent.com/document/api/213/15723

        Args:
            InstanceIds (list, optional): [实例ID]. 

        Returns:
            [json]: [json response]
        """
        try:
            req = models.TerminateInstancesRequest()
            params = {
                "InstanceIds": InstanceIds
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.TerminateInstances(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err



    def describeInstances(self, InstanceIds=[]):
        """[查看实例列表]https://cloud.tencent.com/document/api/213/15728

        Args:
            InstanceIds (list, optional): [实例ID列表].

        Returns:
            [json]: [json response]
        """
        try:
            req = models.DescribeInstancesRequest()
            params = {
                "InstanceIds": InstanceIds,
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.DescribeInstances(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err


