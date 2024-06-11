from django.urls import path
from .views import *

urlpatterns = [
    path('', AnimeListView.as_view(), name='anime_list'),
    path('search/', AnimeSrcView.as_view(), name='anime_search'),
    path('info/', AnimeInfo.as_view(), name='anime_info'),
    path('create/', AnimeTaskCreate.as_view(),name='task_create')
    # path('create/', AnimeCreateView.as_view(), name='anime_create'),
    # path('edit/<int:pk>/', AnimeUpdateView.as_view(), name='anime_edit'),
]