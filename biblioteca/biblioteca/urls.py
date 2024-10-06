from django.urls import path
from .views import LivroDetail, LivroList, LivroCreate

urlpatterns = [
    path("livros/", LivroList.as_view(), name="livro-list"),
    path("livros/create/", LivroCreate.as_view(), name="livro-create"),
    path("livros/<int:pk>/", LivroDetail.as_view(), name="livro-detail"),
]
