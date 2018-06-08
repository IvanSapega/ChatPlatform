from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r"^$", views.redirect_to_root_url),
    url(r"^allchats/$", views.index, name="index"),
    #url(r"^allchats/password_confirm/(?P<pk>[0-9]+)/$", views.password_confirm, name="password_confirm"),
    url(r"^allchats/(?P<pk>[0-9]+)/$", views.chat, name="chat"),
    url(r"^login/$", views.login, name="login"),
    url(r"^registration/$", views.registration, name="registration")
]
