from django.urls import path
from .views import AgentListView,AgentCreatView,AgentDetailView,AgentUpdateView,AgentDeleteView,UserView,YourListView
app_name = 'agents'
urlpatterns = [
    path('',UserView.as_view(),name='agents_list'),
    path('create/',AgentCreatView.as_view(),name='agents_create'),
    path('<int:pk>/',AgentDetailView.as_view(),name='agents_detail'),
    path('<int:pk>/update',AgentUpdateView.as_view(),name='agents_update'),
    path('search/', YourListView.as_view(), name='your_list_view'),
    path('<int:pk>/delete',AgentDeleteView.as_view(),name='agents_delete')

   

]