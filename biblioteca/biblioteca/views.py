from .models import Livro
from .serializers import LivroSerializer
from rest_framework import generics
from .filters import LivroFilter


class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-list"
    search_fields = ("^titulo",)
    filterset_class = LivroFilter
    ordering_fields = ["titulo", "autor", "categoria", "publicado_em"]


class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"
    search_fields = ("^titulo",)
    filterset_class = LivroFilter
    ordering_fields = ["titulo", "autor", "categoria", "publicado_em"]


class LivroCreate(generics.CreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-create"