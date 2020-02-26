import os

import celery
import pymysql

from zufang import settings

pymysql.install_as_MySQLdb()

# 加载Django项目配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zufang.settings')

# 创建Celery对象，指定模块名、消息代理（消息队列）和持久化方式
app = celery.Celery('zufang',
                    # broker='redis://120.77.222.217:6379/1',
                    broker='amqp://luohao:1qaz2wsx@120.77.222.217:5672/zufangwang_vhost',
                    backend='redis://120.77.222.217:6379/2')
# 读取配置文件
app.config_from_object('django.conf:settings')
# 自动从所有注册的应用中发现异步任务
app.autodiscover_tasks(['common', ])
