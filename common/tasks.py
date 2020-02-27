from datetime import timedelta

from django.utils import timezone

from common.models import Record
from zufang import app


@app.task
def remove_expired_record():
    check_time = timezone.now() - timedelta(days=90)
    queryset = Record.objects.filter(recorddate__lte=check_time)
    for record in queryset:
        record.delete()
