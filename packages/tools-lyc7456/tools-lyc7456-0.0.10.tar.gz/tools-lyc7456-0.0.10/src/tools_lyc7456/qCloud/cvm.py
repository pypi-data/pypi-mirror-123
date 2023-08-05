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
        self.SecretId = key['SecretId']
        self.SecretKey = key['SecretKey']
        self.endpoint = key['CVM']['endpoint']
        self.Region = key['Region']
        self.Zone = key['Zone']

        # CVM
        self.Password = key['CVM']['Password']
        self.InstanceName = key['CVM']['InstanceName']
        self.InstanceType = key['CVM']['InstanceType']
        self.ImageId = key['CVM']['ImageId']

        # VPC
        self.VpcId = key['VPC']['VpcId']
        self.SubnetId = key['VPC']['SubnetId']
        self.InternetMaxBandwidthOut = key['VPC']['InternetMaxBandwidthOut']
        self.SecurityGroupIds = key['VPC']['SecurityGroupIds']

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



    def runInstances(self, InstanceType, InstanceChargeType='POSTPAID_BY_HOUR', InstanceCount=1, InternetChargeType='TRAFFIC_POSTPAID_BY_HOUR'):
        """[创建实例]https://cloud.tencent.com/document/api/213/15730

        Args:
            InstanceType ([str]): [实例机型。不同实例机型指定了不同的资源规格。]
            InstanceChargeType (str, optional): [实例计费类型。
                                                    PREPAID：预付费，即包年包月
                                                    POSTPAID_BY_HOUR：按小时后付费
                                                    CDHPAID：独享子机（基于专用宿主机创建，宿主机部分的资源不收费）
                                                    SPOTPAID：竞价付费
                                                    CDCPAID：专用集群付费
                                                    默认值：POSTPAID_BY_HOUR。]. 默认取值 'POSTPAID_BY_HOUR'.
            InstanceCount (int, optional): [购买实例数量。包年包月实例取值范围：[1，300]，按量计费实例取值范围：[1，100]。]. 默认取值：1
            InternetChargeType (str, optional): [网络计费类型。取值范围：
                                                    BANDWIDTH_PREPAID：预付费按带宽结算
                                                    TRAFFIC_POSTPAID_BY_HOUR：流量按小时后付费
                                                    BANDWIDTH_POSTPAID_BY_HOUR：带宽按小时后付费
                                                    BANDWIDTH_PACKAGE：带宽包用户].默认取值 'TRAFFIC_POSTPAID_BY_HOUR'.                           
        
        Returns:
            [json]: [json response]
        """
        try:
            req = models.RunInstancesRequest()
            params = {
                "InstanceChargeType": InstanceChargeType,
                "Placement": {
                    "Zone": self.Zone
                },
                "InstanceType": InstanceType,
                "ImageId": self.ImageId,
                "VirtualPrivateCloud": {
                    "VpcId": self.VpcId,
                    "SubnetId": self.SubnetId
                },
                "InternetAccessible": {
                    "InternetChargeType": InternetChargeType,
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



