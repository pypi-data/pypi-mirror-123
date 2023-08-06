from django.urls import path, include

from . import views


app_name = 'patterns'


ajax_urls = [
    path('table/<str:type>/', views.PatternListView.as_view(), name='list'),
    path('create/', views.PatternCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.PatternUpdateView.as_view(), name='update'),
    path('<int:pattern_pk>/tables/<int:pk>/fields/', views.TableFieldsListView.as_view(), name='fields-list'),
    path('<int:pattern_pk>/tables/', views.DBTablesTreeListView.as_view(), name='tables-list'),
    path('<int:pattern_pk>/tables/included/', views.PatternDBTablesTreeListView.as_view(), name='included-tables-list'),
    path('<int:pk>/add_table/', views.PatternDBTableAddView.as_view(), name='add-table'),
    path('<int:pk>/remove_table/', views.PatternDBTableRemoveView.as_view(), name='remove-table'),
    path('<int:pk>/fields/<str:type>/', views.PatternFieldsListView.as_view(), name='pattern-fields-list'),
    path('<int:pk>/add_fields/', views.PatternFieldsAddView.as_view(), name='add-fields'),
    path('<int:pk>/change_order/', views.PatternFieldChangeOrderView.as_view(), name='field-change-order'),
]


urlpatterns = [
    path('', views.PatternListView.as_view(), name='list', kwargs={'type': 'base'}),
    path('<int:pk>/', views.PatternDetailView.as_view(), name='detail'),
    path('ajax/', include(ajax_urls)),
]
