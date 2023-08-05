import json

import requests

'''
@author lyingOn
@desc 企业微信消息发送工具类
@date 2021-09-17
'''
class SendWechatMsg:
    def __init__(self):
        pass

    # 获取企业微信应用token
    # corpid 企业id
    # corpsecret 企业应用的Secret
    def getTokenFromWechat(self,corpid,corpsecret):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        data = {
            "corpid": corpid,
            "corpsecret": corpsecret
        }
        result = requests.get(url=url, params=data, verify=False).json()
        if result['errcode'] == 0:
            token = result['access_token']
            return token
        else:
            return False

    # 发送消息到企业微信
    # corpid 企业id
    # corpsecret 企业应用的Secret
    # topartyid 企业应用通知的部门id
    # agentid 企业应用的AgentId
    # msg 发送的消息内容
    def sendMsgToWechat(self,corpid,corpsecret,topartyid,agentid,msg):
        token = self.getTokenFromWechat(corpid, corpsecret)

        # 发送消息
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token
        data = {
            "toparty": topartyid,
            "msgtype": "text",
            "agentid": agentid,
            "text": {"content": msg},
            "safe": "0"
        }
        result = requests.post(url=url, data=json.dumps(data), verify=False).json()
        print(result)

        if result['errcode'] == 0:
            return 0
        else:
            return -1


