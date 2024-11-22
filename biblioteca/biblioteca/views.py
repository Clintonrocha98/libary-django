from .models import Livro, Colecao
from .serializers import ColecaoSerializer, LivroSerializer
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .filters import LivroFilter
from .custom_permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

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


class ColecaoListCreate(generics.ListCreateAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(colecionador=self.request.user)


class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] 

    def get_object(self):
        obj = super().get_object()
        if self.request.method not in permissions.SAFE_METHODS and obj.colecionador != self.request.user:
            raise PermissionDenied("Você não tem permissão para modificar esta coleção.")
        return obj