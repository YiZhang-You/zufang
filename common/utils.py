"""
项目常用工具函数
"""
import json
import random

from hashlib import md5
from io import BytesIO

import qrcode
import requests
from qiniu import Auth, put_file, put_stream


def get_ip_address(request):
    """获得请求的IP地址"""
    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    return ip or request.META['REMOTE_ADDR']


def to_md5_hex(origin_str):
    """生成MD5摘要"""
    return md5(origin_str.encode('utf-8')).hexdigest()


def gen_mobile_code(length=6):
    """生成指定长度的手机验证码"""
    return ''.join(random.choices('0123456789', k=length))


def gen_captcha_text(length=4):
    """生成指定长度的图片验证码文字"""
    return ''.join(random.choices(
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        k=length)
    )


def gen_qrcode(data):
    """生成二维码"""
    image = qrcode.make(data)
    buffer = BytesIO()
    image.save(buffer)
    return buffer.getvalue()


def send_sms_by_luosimao(tel, message):
    """发送短信（调用螺丝帽短信网关）"""
    resp = requests.post(
        url='http://sms-api.luosimao.com/v1/send.json',
        auth=('api', 'key-'),
        data={
            'mobile': tel,
            'message': message
        },
        timeout=10,
        verify=False)
    return json.loads(resp.content)


QINIU_ACCESS_KEY = 'access_key'
QINIU_SECRET_KEY = 'secret_key'
QINIU_BUCKET_NAME = 'bucket_name'

auth = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)


def upload_filepath_to_qiniu(file_path, filename):
    """将文件上传到七牛云存储"""
    token = auth.upload_token(QINIU_BUCKET_NAME, filename)
    put_file(token, filename, file_path)


def upload_stream_to_qiniu(file_stream, filename, size):
    """将数据流上传到七牛云存储"""
    token = auth.upload_token(QINIU_BUCKET_NAME, filename)
    put_stream(token, filename, file_stream, None, size)
