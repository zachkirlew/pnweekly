from django.conf.urls import url

from users import views

urlpatterns = [
    # signup page
    url(r'^signup/$', views.signup, name='signup'),
    # register new user
    url(r'^register/$', views.register, name='register'),
    # login page
    url(r'^user_login/$', views.user_login, name='user_login'),
    # check email availability
    url(r'^reg_check_user/$', views.regCheckUser, name='reg_check_user'),
    # logout page
    url(r'^logout/$', views.logout, name='logout'),
    # user account page
    url(r'^account/$', views.account, name='account'),
    # edit user account details
    url(r'^edit_account/$', views.edit_account, name='edit_account'),
    # alerts page
    url(r'^alerts/$', views.alerts, name='alerts'),
    # edit alerts
    url(r'^edit_alerts/$', views.edit_alerts, name='edit_alerts'),
    # POST new profile picture
    url(r'^upload_pic/$', views.upload_pic, name='upload_pic'),
]
