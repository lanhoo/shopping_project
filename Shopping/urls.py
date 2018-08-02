from django.conf.urls import url
from Shopping import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^forget/$', views.Forget.as_view(), name='forget'),
    url(r'^active/(?P<email>.*)/(?P<active_code>.*)/$', views.UserActiveView.as_view(), name="user_active"),


]