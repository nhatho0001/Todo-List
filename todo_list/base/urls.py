from django.urls import path 
from .views import TakeList , TaskDetail , CreateTask , EditTask , DeleteTask , CustomLogin , RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/' , CustomLogin.as_view() , name = 'login'),
    path('logout/' , LogoutView.as_view(next_page = 'login') , name='logout' ),
    path('register/' , RegisterPage.as_view() , name = 'register'),
    path('' , TakeList.as_view() , name = 'base'),
    path('task/<int:id>' , TaskDetail.as_view() , name='task'),
    path('update/<int:pk>' , EditTask.as_view() , name='Edit_task' ),
    path('create-task/' , CreateTask.as_view() , name='create_task'),
    path('deletete-task/<int:pk>' , DeleteTask.as_view() , name= 'Delete_task'),
]