import json, requests
from tools_lyc7456.uCloudapi.signature import verify_ac

# Write by lyc at 2020-12-4
# Update by lyc at 2021-10-5：优化成包


class UNI():
    """[优刻得uni虚拟网卡 api封装]
    
    """
    def __init__(self, key):
        self.PublicKey = key['PublicKey']           # 公钥
        self.PrivateKey = key['PrivateKey']         # 私钥
        self.api_url = key['api_url']               # api接口url
        self.project_id = key['project_id']         # 项目id
        self.region = key['UHOST']['region']        # 地域
        self.zone = key['UHOST']['zone']            # 可用区
        self.vpc_id = key['UHOST']['vpc_id']        # vpc id
        self.subnet_id = key['UHOST']['subnet_id']  # subnet id


    def create_networkinterface(self):
        """[创建虚拟网卡]

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'CreateNetworkInterface',  # 接口名称
            'Region': self.region,
            'VPCId': self.vpc_id,
            'SubnetId': self.subnet_id,
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



    def delete_networkinterface(self, uni_id):
        """[删除虚拟网卡]

        Args:
            uni_id ([string]): [虚拟网卡id]

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'DeleteNetworkInterface',  # 接口名称
            'Region': self.region,
            'InterfaceId': uni_id,
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



    def grantfirewall(self, uni_id, fw_id, resource_type='uhost'):
        """[应用防火墙 - GrantFirewall]https://docs.ucloud.cn/api/unet-api/grant_firewall

        Args:
            uni_id ([string]): [虚拟网卡资源ID]
            fw_id ([string]): [防火墙资源ID]
            resource_type (str, optional): [弹性IP请求绑定的资源类型]. 枚举值为: uhost: 云主机; ulb, 负载均衡器; uni：虚拟网卡; 默认值 'uhost'.

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'GrantFirewall',  # 接口名称
            'Region': self.region,
            'FWId': fw_id,
            'ResourceType': resource_type,
            'ResourceId': uni_id,
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



    def attach_networkinterface(self, uni_id, uhost_id):
        """[虚拟网卡绑定云主机]

        Args:
            uni_id ([string]): [虚拟网卡id]
            uhost_id ([string]): [云主机资源id]

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'AttachNetworkInterface',  # 接口名称
            'Region': self.region,
            'InterfaceId': uni_id,
            'InstanceId': uhost_id,
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



    def describe_networkinterface(self, uhost_id):
        '''获取网卡绑定信息'''
        params = {
            'Action': 'DescribeNetworkInterface',  # 接口名称
            'Region': self.region,
            'Limit': 1000,  # 1000个网卡内可以获取到，1000个以上需要重写递归循环
            'Offset': 0,
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



    def detach_networkinterface(self, uni_id, uhost_id):
        """[虚拟网卡解绑云主机]

        Args:
            uni_id ([string]): [虚拟网卡id]
            uhost_id ([string]): [云主机资源id]

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'DetachNetworkInterface',  # 接口名称
            'Region': self.region,
            'InterfaceId': uni_id,
            'InstanceId': uhost_id,
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



    
