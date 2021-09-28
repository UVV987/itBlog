from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

from users import views as userViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', userViews.register, name='reg'),
    path('profile/', userViews.profile, name='profile'),
    path('user/', views.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('exit/', views.LogoutView.as_view(template_name='users/exit.html'), name='exit'),

    path('pass-reset/', views.PasswordResetView.as_view(template_name='users/pass_reset.html'), name='pass-reset'),

    path('password_reset_complete/<uidb64>/<token>/', views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password_reset_done/<uidb64>/<token>/', views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),

    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
