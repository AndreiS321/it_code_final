from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('profile/<int:pk>', views.ProfileDetail.as_view(), name="profile"),
    path('update/<int:pk>', views.ProfileUpdate.as_view(), name="update"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('registration/', views.RegisterView.as_view(), name="registration"),
]