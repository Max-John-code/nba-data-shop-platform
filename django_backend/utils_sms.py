# utils/sms.py
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_sms(phone, message):
    """
    发送短信
    这里使用阿里云短信服务作为示例
    实际使用时需要根据你选择的短信服务商修改
    """
    try:
        # 示例：使用阿里云短信服务
        # 需要安装：pip install aliyun-python-sdk-core aliyun-python-sdk-dysmsapi
        
        # 这里是伪代码，实际需要根据短信服务商的API文档实现
        # 可选的短信服务商：
        # 1. 阿里云短信
        # 2. 腾讯云短信
        # 3. 华为云短信
        # 4. 七牛云短信
        
        logger.info(f'发送短信到 {phone}: {message}')
        
        # 实际实现示例（腾讯云）：
        # from tencentcloud.common import credential
        # from tencentcloud.sms.v20210111 import sms_client
        # 
        # cred = credential.Credential(settings.SMS_API_KEY, settings.SMS_API_SECRET)
        # client = sms_client.SmsClient(cred, "ap-beijing")
        # 
        # req = models.SendSmsRequest()
        # req.PhoneNumberSet = ["+86" + phone]
        # req.TemplateID = "your_template_id"
        # req.SignName = "your_sign_name"
        # req.TemplateParamSet = [message]
        # 
        # resp = client.SendSms(req)
        
        return True
    except Exception as e:
        logger.error(f'发送短信失败: {str(e)}')
        return False
