import json
from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils import timezone

from .views import get_trends_data


METRIC_LABELS = {
    'positions': '岗位发布数',
    'applications': '申请提交数',
    'timesheets': '工时提交数',
    'salaries': '薪酬生成数/金额',
}


def admin_trends_page(request):
    """
    Django Admin 内的趋势分析页面（图表 + 表格）
    URL: /admin/reports/trends/
    """
    now = timezone.now()
    metric = request.GET.get('metric', 'positions')
    group_by = request.GET.get('group_by', 'year')
    start_year = int(request.GET.get('start_year') or (now.year - 2))
    end_year = int(request.GET.get('end_year') or now.year)

    data = get_trends_data(metric, group_by, start_year, end_year)

    labels = []
    series_count = []
    series_total = []
    for row in data:
        if group_by == 'year':
            label = str(row.get('year'))
        else:
            label = f"{row.get('year')}-{int(row.get('month')):02d}"
        labels.append(label)
        series_count.append(row.get('count', 0))
        if metric == 'salaries':
            series_total.append(row.get('total', 0))

    chart_payload = {
        'labels': labels,
        'count': series_count,
        'total': series_total,
        'metric': metric,
        'group_by': group_by,
    }

    context = {
        **admin.site.each_context(request),
        'metric': metric,
        'group_by': group_by,
        'start_year': start_year,
        'end_year': end_year,
        'metric_labels': METRIC_LABELS,
        'data': data,
        'chart_json': json.dumps(chart_payload, ensure_ascii=False),
    }
    return TemplateResponse(request, 'admin/trends.html', context)

