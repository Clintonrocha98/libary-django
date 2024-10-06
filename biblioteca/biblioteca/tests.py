from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Livro, Autor, Categoria


class LivroTests(APITestCase):
    def setUp(self):

        self.autor1 = Autor.objects.create(nome="Autor 1")
        self.autor2 = Autor.objects.create(nome="Autor 2")
        self.categoria_ficcao = Categoria.objects.create(nome="Ficção")
        self.categoria_terror = Categoria.objects.create(nome="Terror")

        self.livro1 = Livro.objects.create(
            titulo="Livro 1",
            autor=self.autor1,
            categoria=self.categoria_ficcao,
            publicado_em="2023-01-01",
        )
        self.livro2 = Livro.objects.create(
            titulo="Livro 2",
            autor=self.autor2,
            categoria=self.categoria_terror,
            publicado_em="2023-02-01",
        )

    def test_livro_list(self):
        """
        Testa se a lista de livros é retornada corretamente
        """
        url = reverse("livro-list")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), Livro.objects.count())

        livro = Livro.objects.get(titulo="Livro 1")
        self.assertEqual(response.data["results"][0]["titulo"], livro.titulo)

    def test_livro_create(self):
        """
        Testa se um novo livro pode ser criado corretamente
        """
        url = reverse("livro-create")
        data = {
            "titulo": "Novo Livro",
            "autor": self.autor1.id,
            "categoria": self.categoria_ficcao.id,
            "publicado_em": "2023-10-05",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Livro.objects.count(), 3)
        novo_livro = Livro.objects.get(titulo="Novo Livro")
        self.assertEqual(novo_livro.autor.nome, "Autor 1")

    def test_livro_detail(self):
        """
        Testa se os detalhes de um livro específico são retornados corretamente
        """
        url = reverse("livro-detail", kwargs={"pk": self.livro1.pk})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        livro = Livro.objects.get(pk=self.livro1.pk)
        self.assertEqual(response.data["titulo"], livro.titulo)

    def test_livro_update(self):
        """
        Testa se um livro pode ser atualizado corretamente
        """
        url = reverse("livro-detail", kwargs={"pk": self.livro1.pk})
        data = {
            "titulo": "Livro Atualizado",
            "autor": self.autor1.id,
            "categoria": self.categoria_ficcao.id,
            "publicado_em": self.livro1.publicado_em,
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.livro1.refresh_from_db()
        self.assertEqual(self.livro1.titulo, "Livro Atualizado")

    def test_livro_delete(self):
        """
        Testa se um livro pode ser deletado corretamente
        """
        url = reverse("livro-detail", kwargs={"pk": self.livro1.pk})
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Livro.objects.count(), 1)

    def test_livro_create_invalid_data(self):
        url = reverse("livro-create")
        data = {
            "titulo": "",
            "autor": "",
            "categoria": "",
            "publicado_em": "data-invalida",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", response.data)
        self.assertIn("autor", response.data)
        self.assertIn("categoria", response.data)
        self.assertIn("publicado_em", response.data)

    def test_livro_update_invalid_data(self):
        url = reverse("livro-detail", kwargs={"pk": self.livro1.pk})
        data = {
            "titulo": "",
            "autor": "",
            "categoria": "",
            "publicado_em": "data-invalida",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", response.data)
        self.assertIn("autor", response.data)
        self.assertIn("categoria", response.data)
        self.assertIn("publicado_em", response.data)

    def test_livro_detail_not_found(self):
        url = reverse("livro-detail", kwargs={"pk": 999})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_livro_update_not_found(self):
        url = reverse("livro-detail", kwargs={"pk": 999})
        data = {
            "titulo": "Livro Não Encontrado",
            "autor": self.autor1.id,
            "categoria": self.categoria_ficcao.id,
            "publicado_em": "2023-10-05",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_livro_delete_not_found(self):
        url = reverse("livro-detail", kwargs={"pk": 999})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_livro_method_not_allowed(self):
        url = reverse("livro-list")
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
