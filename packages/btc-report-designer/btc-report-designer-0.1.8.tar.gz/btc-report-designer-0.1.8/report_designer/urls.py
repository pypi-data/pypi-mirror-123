from django.urls import include, path


app_name = 'report_designer'


urlpatterns = [
    path('tables/', include('report_designer.tables.urls', namespace='tables')),
    path('formats/', include('report_designer.formats.urls', namespace='formats')),
    path('groups/', include('report_designer.groups.urls', namespace='groups')),
    path('patterns/', include('report_designer.patterns.urls', namespace='patterns')),
]
