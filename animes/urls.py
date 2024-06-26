from django.urls import path
from .views import *

urlpatterns = [
    path('', AnimeListView.as_view(), name='anime_list'),
    path('search/', AnimeSrcView.as_view(), name='anime_search'),
    # path('info/', AnimeInfo.as_view(), name='anime_info'),
    path('create/', AnimeTaskCreate.as_view(),name='task_create'),
    path('api/anime-list/', AnimeListAPI.as_view(), name='api-anime-list'),
    # path('api/anime-info/', AnimeInfoAPI.as_view(), name='api-anime-info'),
    # path('api/anime-src/', AnimeSrcAPI.as_view(), name='api-anime-src'),
    path('api/anime-task-create/', AnimeTaskCreateAPI.as_view(), name='api-anime-task-create'),
]