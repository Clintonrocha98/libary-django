from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Colecao, Livro, Autor, Categoria


class BibliotecaTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

        self.token_user1 = Token.objects.create(user=self.user1)
        self.token_user2 = Token.objects.create(user=self.user2)

        self.autor = Autor.objects.create(nome="Autor Teste")
        self.categoria = Categoria.objects.create(nome="Categoria Teste")

        self.livro1 = Livro.objects.create(
            titulo="Livro 1", autor=self.autor, categoria=self.categoria, publicado_em="2023-01-01"
        )
        self.livro2 = Livro.objects.create(
            titulo="Livro 2", autor=self.autor, categoria=self.categoria, publicado_em="2023-02-01"
        )

        self.colecao = Colecao.objects.create(
            nome="Coleção Teste",
            descricao="Descrição da coleção",
            colecionador=self.user1,
        )
        self.colecao.livros.set([self.livro1, self.livro2])

    def authenticate(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_criar_colecao_autenticado(self):
        self.authenticate(self.token_user1.key)
        data = {
            "nome": "Nova Coleção",
            "descricao": "Descrição da nova coleção",
            "livros": [self.livro1.id, self.livro2.id],
        }
        url = reverse("colecao-list-create")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome"], "Nova Coleção")
        self.assertEqual(response.data["colecionador"]["username"], self.user1.username)


    def test_criar_colecao_nao_autenticado(self):
        data = {
            "nome": "Nova Coleção",
            "descricao": "Descrição da nova coleção",
            "livros": [self.livro1.id, self.livro2.id],
        }
        url = reverse("colecao-list-create")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listar_colecoes_autenticado(self):
        self.authenticate(self.token_user1.key)
        url = reverse("colecao-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_listar_colecoes_nao_autenticado(self):
        url = reverse("colecao-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_editar_colecao_propria(self):
        self.authenticate(self.token_user1.key)
        data = {"nome": "Coleção Editada", "descricao": "Nova descrição"}
        url = reverse("colecao-detail", kwargs={"pk": self.colecao.id})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], "Coleção Editada")

    def test_editar_colecao_de_outro_usuario(self):
        self.authenticate(self.token_user2.key)
        data = {"nome": "Coleção Editada"}
        url = reverse("colecao-detail", kwargs={"pk": self.colecao.id})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deletar_colecao_propria(self):
        self.authenticate(self.token_user1.key)
        url = reverse("colecao-detail", kwargs={"pk": self.colecao.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Colecao.objects.filter(id=self.colecao.id).exists())

    def test_deletar_colecao_de_outro_usuario(self):
        self.authenticate(self.token_user2.key)
        url = reverse("colecao-detail", kwargs={"pk": self.colecao.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_livro_list(self):
        self.authenticate(self.token_user1.key)
        url = reverse("livro-list")
        response = self.client.get(url, format="json")

        if "results" in response.data:
            livros_retornados = len(response.data["results"]) 
        else:
            livros_retornados = len(response.data) 

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(livros_retornados, Livro.objects.count()) 


    def test_livro_create_unauthenticated(self):
        url = reverse("livro-create")
        data = {
            "titulo": "Novo Livro",
            "autor": self.autor.id,
            "categoria": self.categoria.id,
            "publicado_em": "2023-10-05",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
