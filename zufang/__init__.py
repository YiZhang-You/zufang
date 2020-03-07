import os

import celery
# import sentry_sdk
# import pymysql
from celery.schedules import crontab
from django.conf import settings

# pymysql.install_as_MySQLdb()

# sentry_sdk.init("https://8afe52973694471eb1541d0eab19c517@sentry.io/3888861")
# sentry_sdk.init("http://85d9cd6310d94955b6534d87a060ace2@120.77.222.217:9000/4")

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
#
# sentry_sdk.init(
#     dsn="https://c7cc09257cea45bfb0d5ae7872a190af@sentry.io/3910331",
#     integrations=[DjangoIntegration()],
#
#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )


# 加载Django项目配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zufang.settings')

# 创建Celery对象，指定模块名、消息代理（消息队列）和持久化方式
app = celery.Celery(
    'zufang',
    broker='redis://120.77.222.217:6379/1',
    # broker='amqp://luohao:1qaz2wsx@120.77.222.217:5672/zufangwang_vhost',
    backend='redis://120.77.222.217:6379/2'
    # backend='django-db'
)

# 直接通过代码修改Celery相关配置
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
app.conf.update(
    # 接受的内容
    accept_content=['json', 'pickle'],
    # 任务序列化方式
    task_serializer='pickle',
    # 任务执行结果序列化方式
    result_serializer='json',
    # 时区设置
    timezone=settings.TIME_ZONE,
    # 启用协调世界时
    enable_utc=True,
    # 配置定时任务
    beat_schedule={
        'task1': {
            'task': 'common.tasks.remove_expired_records',
            'schedule': crontab('0', '2', '*', '*', '*'),
            'args': ()
        },
    },
)
# # 从配置文件中读取Celery相关配置
# app.config_from_object('django.conf:settings')
# 自动从指定的应用中发现任务（异步任务/定时任务）
app.autodiscover_tasks(('common', ))
# # 自动从注册的应用中发现任务（异步任务/定时任务）
# app.autodiscover_tasks(settings.INSTALLED_APPS)
