from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("about/", views.about, name="about"),
    path("register/", views.register_token, name="register_token"),
    path("live/", views.live_queue, name="live_queue"),
    path("staff/login/", views.staff_login, name="staff_login"),
    path("staff/logout/", views.staff_logout, name="staff_logout"),
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/token/<int:token_id>/<str:action>/", views.token_action, name="token_action"),
]
