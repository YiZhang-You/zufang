import logging
from concurrent.futures.thread import ThreadPoolExecutor

import boto3
import qiniu
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

MAX_READ_SIZE = 64 * 1024

QINIU_ACCESS_KEY = 'KarvlHfUdoG1mZNSfDVS5Vh3nae2jUZumTBHK-PR'
QINIU_SECRET_KEY = 'SFPFkAn5NENhdCMqMe9wd_lxGHAeFR5caXxPTtt7'
QINIU_BUCKET_NAME = 'zufangwang'

AUTH = qiniu.Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)

# AWS3_REGION = 'region_name'
# AWS3_AK = 'access_key'
# AWS3_SK = 'secret_key'
# AWS3_BUCKET = 'bucket_name'
#
# S3 = boto3.client('s3', region_name=AWS3_REGION,
#                   aws_access_key_id=AWS3_AK, aws_secret_access_key=AWS3_SK)

MAX_THREAD_WORKERS = 64
EXECUTOR = ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a',)

logger = logging.getLogger('')

# 支付宝配置对象
alipay_client_config = AlipayClientConfig()
# 支付宝分配给开发者的应用ID
alipay_client_config.app_id = '2016101800716377'
alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
alipay_client_config.app_private_key = 'MIIEowIBAAKCAQEA1NPx89jxynhQF38Qot1QUW1duHErHY3vGZgCek0GErdIKfgjJ93gHLWvKEuUEauPDW1tgXbo6+qa39OdyFQ8838g2jP519gxywHUYGgR0TKY8TlDYogII2xboY/6lPKuGTZKCd7s0UF5gZ5VxAAo7QlF8PajwlQDqD+TJPbp/tUnhAsJlqh/iLldL3SdEcdUkQ6n2Edt5/w1G8y91XbtiRc4m5hccDAmzaBMBAfzlbtc0ZwZA0A8AtdBovXgl6LjARh4OzRIg0dH4mnPOvhym70Nq+THV9Ul6gJqufyVQ+OGjJRI/OUASqonDW2h0aUGwc0/8NrWgj15kwv8/+S9fwIDAQABAoIBADohGXiszH2sltOUFQsmv4U+BdcWsdwEpEWtSx/0YbBC9ybfa1q8MzYkOY8b9XlODmhwdvRhcgTdsydnOTU6LNuk4Wg3wgm+NvtnqIYcZqFo3HUmWs1SskZaljxugtaj4gFo3pgLl0sgQvuwL2S1VnhHjB7gfqHZKJaPprT167t6JNVPY9y6CcA7cc+KG06Fjz9HtN0K6sICIIsCfHvncOA1vuAL2esp8V1mNASo9E8NXtVyITu7/z0Lrgr4qZP/CVfh6LCLa3UfOdJLo5eVTwGn7i5ATAllOxdfXiLTt34cCfEePCsoet87/Ye1xFiq+VICFmzOaX4k/zmALZ/bDKECgYEA+u/mAvARI00S27kQ9+FwojXddeQqSzrufNHbjbowi41zctl8+yt4z2uw9XqQwM/Ugw1uuKwTdQEB2tNdbkA9mkZyYPQsiLlofIx0dRe596FBcvHOrn5BwmA/Vyd7Ju2+U28EePXkhwgTgv9o6O25H+gEPTBtTMjIyESRbNK+r20CgYEA2R81/+YQQoPFXjzXKX+6qzGA4cvX6w7OpEAPK+Vxyp54QFOaEJBYbYftJNcyFCrY+sqguVPW3hqP9zhNYjMeKDGmQR4gO84QsZItGgUj9OaXEOJ++z/1Jer6blPzwQgB9aivmePPecdwTSl82wIFncihtBu3wmiHqmfxvL1qERsCgYAQ555oLkIJTcTqdnI1MMPEubo8me1behHc6MpQpu1kSVgwsYQg65HM72VRdDtSMe4QEhSWbkk1RacZVcnihoNf5EUKUQi7ATqPwWqLBNkrXHqrQqz4xlqpvJAnz+oU+kkrF7yGZZJKonmmBozLvFAPXTMD6EJEvPYBv9TILv5XlQKBgAoRb3CZW4GqGJnhGl0bRi2wEvjlefK1chGdwtZXQmqR5KOe/NLtzpvtpKqDrBfRUNR4VvGhGKKd+rUNEFGQa0KT4tC8M+RyDsYdMCg3us4dbz3iMt81vQlwFwLMs83ssCKTGul47eMIw4VgeiCxvE7vwcfXTTMfo8LcJRKKegOnAoGBAPIUmpLK/rQrU13YISil8c4VqTDiY3kZV/ZY/MOHm8ljS8nlqeUpbfglF5Y7Jgf6Cl7dP2nKAKoFSGulE/eTDz+wMrU+FCSxXf6wtgurfLuWl9sgLC5euCfYxI+kqQeRz3Apeh2Bnkc6ct/1liAi7ECZ49rOhfkuXMXddHcPs7pp'
alipay_client_config.alipay_public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIgHnOn7LLILlKETd6BFRJ0GqgS2Y3mn1wMQmyh9zEyWlz5p1zrahRahbXAfCfSqshSNfqOmAQzSHRVjCqjsAw1jyqrXaPdKBmr90DIpIxmIyKXv4GGAkPyJ/6FTFY99uhpiq0qadD/uSzQsefWo0aTvP/65zi3eof7TcZ32oWpwIDAQAB'
# 支付成功返回的页面是自己定制的 备案的域名可以跟服务器IP地址绑定（配置域名解析即可）
# 此处必须写完整的URL
alipay_client_config.return_url = 'http://jackfrued.top:8000/static/html/pay_success.html'
alipay_client_config.notify_url = 'http://jackfrued.top:8000/api/get_alipay_notification/'

# 支付宝客户端对象
alipay_client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
