from . import views
from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', views.UserProfileViewSet)


urlpatterns = [

    path('', include(router.urls)),
    # path('task', views.TaskListView.as_view()),
    # path('task/<int:id>/', views.TaskListView.as_view())
    path('task', views.TaskAPIView.as_view()),
    path('user/<int:user_id>/task/', views.TaskOfUserAPIView.as_view()),
    path('auth/login', views.LoginView.as_view()),
    path('auth/logout', views.LogoutView.as_view()),
    path('task/count/', views.task_counts),
    path('task/<int:task_id>/', views.TaskDetailAPIView.as_view())  # task_id must be parsed in view as it's written hia

    # path('hello/', views.HelloApiView.as_view()),
]
