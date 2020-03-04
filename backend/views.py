import io
from urllib.parse import quote

import xlwt
from django.http import HttpResponse

from backend.models import Emp, Dept


def export_excel(request):
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('员工信息表')
    titles = ('编号', '姓名', '职位', '主管', '工资', '部门')
    for col, title in enumerate(titles):
        sheet.write(0, col, title)
    queryset = Emp.objects.all().defer('comm')
    props = ('no', 'name', 'job', 'mgr', 'sal', 'dept')
    for row, emp in enumerate(queryset):
        for col, prop in enumerate(props):
            value = getattr(emp, prop, '')
            if isinstance(value, (Dept, Emp)):
                value = value.name
            sheet.write(row + 1, col, value)
    buffer = io.BytesIO()
    wb.save(buffer)
    resp = HttpResponse(buffer.getvalue())
    resp['content-type'] = 'application/vnd.msexecl'
    filename = quote('员工信息表.xls')
    resp['content-disposition'] = f'attachment; filename="{filename}"'
    return resp
