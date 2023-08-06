import json, requests
from tools_lyc7456.uCloudapi.signature import verify_ac

# Write by lyc at 2020-12-4
# Update by lyc at 2021-10-4：优化成包


class UEIP():
    '''优刻得EIP api封装'''
    def __init__(self, key):
        self.PublicKey = key['PublicKey']           # 公钥
        self.PrivateKey = key['PrivateKey']         # 私钥
        self.api_url = key['api_url']               # api接口url
        self.project_id = key['project_id']         # 项目id
        self.region = key['UHOST']['region']        # 地域


    def allocate_eip(self, eip_bandwidth=1, eip_paymode='Bandwidth', eip_operatorname='Bgp', eip_chargetype='Month'):
        """[申请弹性IP - AllocateEIP]https://docs.ucloud.cn/api/unet-api/allocate_eip

        Args:
            eip_bandwidth (int, optional): [带宽值]. 默认值1.
            eip_paymode (str, optional): [弹性IP的计费模式]. "Traffic", 流量计费; "Bandwidth", 带宽计费; "ShareBandwidth",共享带宽模式. 默认为 "Bandwidth".
            eip_operatorname (bool, optional): [弹性IP线路]. "International" 国际线路；"Bgp" 国内IP。默认为 "Bgp".
            eip_chargetype (str, optional): [付费方式]. "Year", 按年付费; "Month", 按月付费; "Dynamic", 按需付费(需开启权限); Trial, 试用(需开启权限) 默认为按月付费.

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'AllocateEIP',            # 接口名称
            'Region': self.region,              # 地区
            'OperatorName': eip_operatorname,
            'Bandwidth': eip_bandwidth,
            'PayMode': eip_paymode,
            'ChargeType': eip_chargetype,
            'ProjectId': self.project_id,
            'PublicKey': self.PublicKey,
        }
        # 签名
        signature = verify_ac(self.PublicKey, self.PrivateKey, params)
        params['Signature'] = signature

        # POST请求接口
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=self.api_url, headers=headers, data=json.dumps(params))
        response_dic = json.loads(response.content.decode('utf-8'))

        return response_dic


    def release_eip(self, eip_id):
        """[释放弹性IP - ReleaseEIP]https://docs.ucloud.cn/api/unet-api/release_eip

        Args:
            eip_id (string): [弹性ip资源id].

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'ReleaseEIP',         # 接口名称
            'Region': self.region,
            'EIPId': eip_id,
            'ProjectId': self.project_id,
            'PublicKey': self.PublicKey,
        }
        # 签名
        signature = verify_ac(self.PublicKey, self.PrivateKey, params)
        params['Signature'] = signature

        # POST请求接口
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=self.api_url, headers=headers, data=json.dumps(params))
        response_dic = json.loads(response.content.decode('utf-8'))

        return response_dic


    def bind_eip(self, eip_id, resource_id, resource_type='uhost'):
        """[绑定弹性IP - BindEIP]https://docs.ucloud.cn/api/unet-api/bind_eip

        Args:
            eip_id ([string]): [弹性ip资源id]
            resource_id ([string]): [弹性IP请求绑定的资源id]
            resource_type (str, optional): [弹性IP请求绑定的资源类型]. 枚举值为: uhost: 云主机; ulb, 负载均衡器; uni：虚拟网卡; 默认值 'uhost'.

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'BindEIP',                # 接口名称
            'Region': self.region,
            'EIPId': eip_id,
            'ResourceType': resource_type,
            'ResourceId': resource_id,
            'ProjectId': self.project_id,
            'PublicKey': self.PublicKey,
        }
        # 签名
        signature = verify_ac(self.PublicKey, self.PrivateKey, params)
        params['Signature'] = signature

        # POST请求接口
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=self.api_url, headers=headers, data=json.dumps(params))
        response_dic = json.loads(response.content.decode('utf-8'))

        return response_dic



    def unbind_eip(self, eip_id, resource_id, resource_type='uhost'):
        """[解绑弹性IP - UnBindEIP]https://docs.ucloud.cn/api/unet-api/un_bind_eip

        Args:
            eip_id ([string]): [弹性ip资源id]
            resource_id ([string]): [弹性IP请求绑定的资源id]
            resource_type (str, optional): [弹性IP请求绑定的资源类型]. 枚举值为: uhost: 云主机; ulb, 负载均衡器; uni：虚拟网卡; 默认值 'uhost'.

        Returns:
            [dict]: [response]
        """
        '''EIP与虚拟网卡解绑'''
        params = {
            'Action': 'UnBindEIP',      # 接口名称
            'Region': self.region,
            'EIPId': eip_id,
            'ResourceId': resource_id,
            'ResourceType': resource_type,
            'ProjectId': self.project_id,
            'PublicKey': self.PublicKey,
        }
        # 签名
        signature = verify_ac(self.PublicKey, self.PrivateKey, params)
        params['Signature'] = signature

        # POST请求接口
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=self.api_url, headers=headers, data=json.dumps(params))
        response_dic = json.loads(response.content.decode('utf-8'))

        return response_dic

