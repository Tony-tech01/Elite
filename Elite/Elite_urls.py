from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import  LogoutView
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, TeamViewSet, PerformanceStatViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'performance-stats', PerformanceStatViewSet)


urlpatterns = [
    
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('player_list/', views.player_list, name='player_list'),
    path('player_detail/<int:pk>/', views.player_detail, name='player_detail'),
    path('add_player/', views.add_player, name='add_player'),
    path('delete_player/<int:pk>/', views.delete_player, name='delete_player'),
    path('update_stat/<int:pk>/', views.update_stat, name='update_stat'),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login_user"),
    path('logout/', LogoutView.as_view(next_page='login_user'), name='logout_user'),
    path('team_list/', views.team_list, name='team_list'),
    path('team_detail/<int:pk>/', views.team_detail, name='team_detail'),
    path('add_team/', views.add_team, name='add_team'),
    path('update_team/<int:pk>/', views.update_team, name='update_team'),
    path('delete_team/<int:pk>/', views.delete_team, name='delete_team'),
    path('profile/', views.profile, name='profile'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('donate/', views.donate, name='donate'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('update_player/<int:pk>/', views.update_player, name='update_player'),

    
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)