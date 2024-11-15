from django.urls import path
# from .views import UserListCreateView, UserDetailView, DealershipListCreateView, DealershipDetailView
from .views import RegisterView, LoginView, ResetPasswordView, CustomTokenRefreshView, CreateDealershipView


urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='register'),
    path('user/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('user/login/', LoginView.as_view(), name='register'),
    path('user/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('user/create-dealership/', CreateDealershipView.as_view(), name='reset_password'),
    # path('users/', UserListCreateView.as_view(), name='user_list_create'),
    # path('users/<str:userId>/', UserDetailView.as_view(), name='user_detail'),
    # path('dealerships/', DealershipListCreateView.as_view(), name='dealership_list_create'),
    # path('dealerships/<str:dealerId>/', DealershipDetailView.as_view(), name='dealership_detail'),
]