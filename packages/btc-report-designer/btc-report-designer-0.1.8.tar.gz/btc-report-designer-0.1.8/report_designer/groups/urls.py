from django.urls import path, include

from . import views


app_name = 'groups'


ajax_urls = [
    path('table/<str:type>/', views.PatternGroupListView.as_view(), name='list'),
    path('create/', views.PatternGroupCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.PatternGroupUpdateView.as_view(), name='update'),
]


urlpatterns = [
    path('', views.PatternGroupListView.as_view(), name='list', kwargs={'type': 'base'}),
    path('ajax/', include(ajax_urls)),
]
