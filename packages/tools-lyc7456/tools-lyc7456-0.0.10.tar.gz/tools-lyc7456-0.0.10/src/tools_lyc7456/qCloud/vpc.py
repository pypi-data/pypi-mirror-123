import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.vpc.v20170312 import vpc_client, models

# Write by lyc at 2021-10-9

class VPC():
    """[腾讯云VPC私有网络 Python3 SDK方法封装]
    """
    def __init__(self, key) -> None:
        self.SecretId = key['SecretId']
        self.SecretKey = key['SecretKey']
        self.endpoint = key['VPC']['endpoint']
        self.Region = key['Region']

        # 签名
        self.cred = credential.Credential(self.SecretId, self.SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = self.endpoint

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self.client = vpc_client.VpcClient(self.cred, self.Region, clientProfile)


    def describeAddressQuota(self):
        """[查询弹性公网IP配额]https://cloud.tencent.com/document/api/215/16701
        Quota响应值解释：https://cloud.tencent.com/document/api/215/15824#Quota

        Returns:
            [json]: [json response]
        """
        try:
            req = models.DescribeAddressQuotaRequest()
            params = {

            }
            req.from_json_string(json.dumps(params))

            resp = self.client.DescribeAddressQuota(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err


    def allocateAddresses(self, AddressType='EIP', InternetMaxBandwidthOut=1, AddressCount=1, InternetChargeType='TRAFFIC_POSTPAID_BY_HOUR'):
        """[创建弹性公网IP]https://cloud.tencent.com/document/api/215/16699

        Args:
            AddressType (str, optional): [EIP类型：'EIP'、'AnycastEIP'：加速IP、'HighQualityEIP'：精品IP]. 默认值：EIP.
            InternetMaxBandwidthOut (int, optional): [EIP出带宽上限，单位：Mbps]. 默认值：1 Mbps.
            AddressCount (int, optional): [EIP数量]. 默认值：1.
            InternetChargeType (str, optional): [EIP计费方式]. 默认值：TRAFFIC_POSTPAID_BY_HOUR.
        
        Returns:
            [json]: [json response]
        """
        try:
            req = models.AllocateAddressesRequest()
            params = {
                "AddressCount": AddressCount,
                "InternetChargeType": InternetChargeType,
                "InternetMaxBandwidthOut": InternetMaxBandwidthOut,
                "AddressType": AddressType
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.AllocateAddresses(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err


    def releaseAddresses(self, AddressIds):
        """[释放弹性公网IP]https://cloud.tencent.com/document/api/215/16705

        Args:
            AddressIds ([Array of String]): [标识 EIP 的唯一 ID 列表。EIP 唯一 ID 形如：eip-11112222。]
        
        Returns:
            [json]: [json response]
        """
        try:
            req = models.ReleaseAddressesRequest()
            params = {
                "AddressIds": AddressIds,
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.ReleaseAddresses(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err


    def associateAddress(self, AddressId, NetworkInterfaceId, PrivateIpAddress):
        """[绑定弹性公网IP]https://cloud.tencent.com/document/api/215/16700

        Args:
            AddressId ([str]): [标识 EIP 的唯一 ID。EIP 唯一 ID 形如：eip-11112222]
            NetworkInterfaceId ([str]): [要绑定的弹性网卡 ID。 弹性网卡 ID 形如：eni-11112222。]
            PrivateIpAddress ([str]): [要绑定的内网 IP。如果指定了 NetworkInterfaceId 则也必须指定 PrivateIpAddress ，表示将 EIP 绑定到指定弹性网卡的指定内网 IP 上。同时要确保指定的 PrivateIpAddress 是指定的 NetworkInterfaceId 上的一个内网 IP。]
        
        Returns:
            [json]: [json response]
        """
        try:
            req = models.AssociateAddressRequest()
            params = {
                "AddressId": AddressId,
                "NetworkInterfaceId": NetworkInterfaceId,
                "PrivateIpAddress": PrivateIpAddress
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.AssociateAddress(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err


    def disassociateAddress(self, AddressId):
        """[解绑定弹性公网IP]https://cloud.tencent.com/document/api/215/16703

        Args:
            AddressId ([str]): [标识 EIP 的唯一 ID。EIP 唯一 ID 形如：eip-11112222]

        Returns:
            [json]: [json response]
        """
        try:
            req = models.DisassociateAddressRequest()
            params = {
                "AddressId": AddressId
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.DisassociateAddress(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err



    def createNetworkInterface(self, VpcId, SubnetId, SecurityGroupIds, NetworkInterfaceName='eth1'):
        """[创建弹性网卡]https://cloud.tencent.com/document/api/215/15818

        Args:
            VpcId ([str]): [VPC实例ID]
            SubnetId ([str]): [弹性网卡所在的子网实例ID]
            SecurityGroupId ([Array of String]): [指定绑定的安全组，例如：['sg-1dd51d']。]
            NetworkInterfaceName (str, optional): [弹性网卡名称]. 默认值：'eth1'.

        Returns:
            [json]: [json response]
        """
        try:
            req = models.CreateNetworkInterfaceRequest()
            params = {
                "VpcId": VpcId,
                "NetworkInterfaceName": NetworkInterfaceName,
                "SubnetId": SubnetId,
                "SecurityGroupIds": SecurityGroupIds,
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.CreateNetworkInterface(req)
            # print(resp.to_json_string())
            return resp.to_json_string()

        except TencentCloudSDKException as err:
            # print(err)
            return err


    def deleteNetworkInterface(self, NetworkInterfaceId):
        """[删除弹性网卡]https://cloud.tencent.com/document/api/215/15822

        Args:
            NetworkInterfaceId ([str]): [弹性网卡实例ID，例如：eni-m6dyj72l。]
        
        Returns:
            [json]: [json response]
        """
        try:
            req = models.DeleteNetworkInterfaceRequest()
            params = {
                "NetworkInterfaceId": NetworkInterfaceId
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.DeleteNetworkInterface(req)
            # print(resp.to_json_string())
            return resp.to_json_string()
            
        except TencentCloudSDKException as err:
            # print(err)
            return err


    def attachNetworkInterface(self, NetworkInterfaceId, InstanceId):
        """[弹性网卡绑定云服务器]https://cloud.tencent.com/document/api/215/15819

        Args:
            NetworkInterfaceId ([str]): [弹性网卡实例ID，例如：eni-m6dyj72l。]
            InstanceId ([str]): [CVM实例ID。形如：ins-r8hr2upy。]

        Returns:
            [json]: [json response]
        """
        try:
            req = models.AttachNetworkInterfaceRequest()
            params = {
                "NetworkInterfaceId": NetworkInterfaceId,
                "InstanceId": InstanceId
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.AttachNetworkInterface(req)
            # print(resp.to_json_string())
            return resp.to_json_string()
            
        except TencentCloudSDKException as err:
            # print(err)
            return err

