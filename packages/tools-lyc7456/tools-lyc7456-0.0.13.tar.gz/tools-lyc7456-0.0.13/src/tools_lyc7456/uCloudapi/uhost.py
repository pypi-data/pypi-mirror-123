import base64
import json, requests
from tools_lyc7456.uCloudapi.signature import verify_ac

# Write by lyc at 2020-12-4
# Update by lyc at 2021-2-4：增加绑定云主机告警模板id
# Update by lyc at 2021-10-4：优化成包


class UHOST():
    '''优刻得uhost云主机 api封装'''
    def __init__(self, key):
        self.PublicKey = key['PublicKey']                           # 公钥
        self.PrivateKey = key['PrivateKey']                         # 私钥
        self.api_url = key['api_url']                               # api接口url
        self.project_id = key['project_id']                         # 项目id
        self.region = key['UHOST']['region']                        # 地域
        self.zone = key['UHOST']['zone']                            # 可用区
        self.image_id = key['UHOST']['image_id']                    # 镜像id
        self.uhost_password = key['UHOST']['uhost_password']        # 密码
        self.uhost_name = key['UHOST']['uhost_name']                # 云主机名称
        self.eip_bandwidth = key['UHOST']['eip_bandwidth']          # 带宽
        self.eip_paymode = key['UHOST']['eip_paymode']              # 带宽付费类型
        self.fw_id = key['UHOST']['fw_id']                          # 防火墙id
        self.alarm_template_id = key['UHOST']['alarm_template_id']  # 云主机告警模板id



    def describe_uhostinstance(self, uhost_id):
        """[获取主机信息 - DescribeUHostInstance]https://docs.ucloud.cn/api/uhost-api/describe_uhost_instance

        Args:
            uhost_id ([string]): [UHost实例ID]

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'DescribeUHostInstance',      # 接口名称
            'Region': self.region,
            'Zone': self.zone,
            'UHostIds.0': uhost_id,
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



    def create_uhostinstance(self, uhost_cpu=1, uhost_memory=2048, uhost_disk0_size=20, uhost_disks_0_type='LOCAL_NORMAL',
                                   uhost_tag='Default', uhost_chargetype='Month', uhost_count=1, eip_operatorname='Bgp', features_uni=False):
        """[创建云主机 - CreateUHostInstance]https://docs.ucloud.cn/api/uhost-api/create_uhost_instance

        Args:
            uhost_cpu (int, optional): [虚拟CPU核数]. Defaults to 1.
            uhost_memory (int, optional): [虚拟内存大小]. Defaults to 2048.
            uhost_disk0_size (int, optional): [系统盘大小]. Defaults to 20.
            uhost_disks_0_type (str, optional): [系统盘类型]. Defaults to 'LOCAL_NORMAL'. 磁盘类型参考：https://docs.ucloud.cn/api/uhost-api/disk_type
            uhost_tag (str, optional): [业务组]. Defaults to 'Default'.
            uhost_chargetype (str, optional): [计费模式]. Defaults to 'Month'.
            uhost_count (int, optional): [本次最大创建主机数量]. Defaults to 1.
            eip_operatorname (str, optional): [弹性IP线路]. "International" 国际线路；"Bgp" 国内IP。默认为 "Bgp".
            features_uni (bool): [弹性IP线路]. 弹性网卡特性。开启了弹性网卡权限位，此特性才生效。默认 False 不开启。

        Returns:
            [type]: [description]
        """
        self.uhost_password = (base64.b64encode(self.uhost_password.encode("utf-8"))).decode('utf-8')   # 云主机密码使用base64进行编码
        params = {
            'Action': 'CreateUHostInstance',      # 接口名称
            'Region': self.region,
            'Zone': self.zone,
            'ImageId': self.image_id,
            'Password': self.uhost_password,
            'Disks.0.Type': uhost_disks_0_type,
            'Disks.0.IsBoot': 'True',
            'Disks.0.Size': uhost_disk0_size,
            'LoginMode': 'Password',
            'Name': self.uhost_name,
            'Tag': uhost_tag,
            'ChargeType': uhost_chargetype,
            'CPU': uhost_cpu,
            'Memory': uhost_memory,
            'SecurityGroupId': self.fw_id,
            'MaxCount': uhost_count,
            'NetworkInterface.0.EIP.Bandwidth': self.eip_bandwidth,
            'NetworkInterface.0.EIP.PayMode': self.eip_paymode,
            'NetworkInterface.0.EIP.OperatorName': eip_operatorname,
            'AlarmTemplateId': self.alarm_template_id,
            'ProjectId': self.project_id,
            'PublicKey': self.PublicKey,
            'Features.UNI':  features_uni,
        }
        # 签名
        signature = verify_ac(self.PublicKey, self.PrivateKey, params)
        params['Signature'] = signature

        # POST请求接口
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=self.api_url, headers=headers, data=json.dumps(params))
        response_dic = json.loads(response.content.decode('utf-8'))

        return response_dic



    def stop_uhostinstance(self, uhost_id):
        """[关闭主机 - StopUHostInstance]https://docs.ucloud.cn/api/uhost-api/stop_uhost_instance

        Args:
            uhost_id ([string]): [UHost实例ID]

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'StopUHostInstance',      # 接口名称
            'Region': self.region,
            'Zone': self.zone,
            'UHostId': uhost_id,
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



    def terminate_uhostinstance(self, uhost_id):
        """[删除云主机 - TerminateUHostInstance]https://docs.ucloud.cn/api/uhost-api/terminate_uhost_instance

        Args:
            uhost_id ([string]): [UHost实例ID]

        Returns:
            [dict]: [response]
        """
        params = {
            'Action': 'TerminateUHostInstance',      # 接口名称
            'Region': self.region,
            'UHostId': uhost_id,
            'ReleaseEIP': True,
            'ReleaseUDisk': True,
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


