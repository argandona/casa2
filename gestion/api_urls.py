from django.urls import path
from .api_views import (
    ActividadListView,
    ProgramacionView,
    SSTDetailView,
    SSTListView,
    SuministroDetailView,
    SuministroListView,
)

urlpatterns = [
    path('suministros/', SuministroListView.as_view()),
    path('suministros/<int:pk>/', SuministroDetailView.as_view()),
    path('programacion/', ProgramacionView.as_view()),
    path('ssts/', SSTListView.as_view()),
    path('ssts/<int:pk>/', SSTDetailView.as_view()),
    path('actividades/', ActividadListView.as_view()),
]
