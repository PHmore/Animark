from django.urls import path
from .views import AnimeListView, AnimeSrcView

urlpatterns = [
    path('', AnimeListView.as_view(), name='anime_list'),
    path('search/', AnimeSrcView.as_view(), name='anime_search'),
    # path('create/', AnimeCreateView.as_view(), name='anime_create'),
    # path('edit/<int:pk>/', AnimeUpdateView.as_view(), name='anime_edit'),
]