from django.urls import path
from .views import ColecaoDetail, ColecaoListCreate, LivroDetail, LivroList, LivroCreate

urlpatterns = [
    path("livros/", LivroList.as_view(), name="livro-list"),
    path("livros/create/", LivroCreate.as_view(), name="livro-create"),
    path("livros/<int:pk>/", LivroDetail.as_view(), name="livro-detail"),
    path('colecoes/', ColecaoListCreate.as_view(), name='colecao-list-create'),
    path('colecoes/<int:pk>/', ColecaoDetail.as_view(), name='colecao-detail'),
]
