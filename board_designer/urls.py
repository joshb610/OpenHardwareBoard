from django.urls import path
from . import views

app_name = "board_designer"

urlpatterns = [
    path("", views.home, name="home"),
    path("generate/", views.generate_board, name="generate_board"),
    path("generate-test-piece/", views.generate_test_piece, name="generate_test_piece"),
    path("download/<str:filename>/", views.download_stl, name="download_stl"),
]
