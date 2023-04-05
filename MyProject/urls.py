from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from UploadFiles import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('uploadfile',views.uploadfile,name="uploadfile"),
    path('deleteFile/<int:id>',views.deleteFile), 
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='login/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="login/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='login/password/password_reset_complete.html'), name='password_reset_complete'),      
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("data",views.jsondata,name = "jsondata"),
    path("user",views.jsonuserdata,name = "jsonuserdata"),
    path("show",views.show,name = "show"),

]
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)