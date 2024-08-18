# Projeto de CRUD de Livros

Este projeto é uma API RESTful para gerenciamento de livros, implementada usando Django e Django Rest Framework.

## Funcionalidades

- Listar todos os livros
- Criar um novo livro
- Visualizar detalhes de um livro específico
- Atualizar informações de um livro
- Deletar um livro

## Estrutura do Projeto

O projeto consiste em três modelos principais:

1. `Categoria`: Representa as categorias dos livros
2. `Autor`: Representa os autores dos livros
3. `Livro`: Representa os livros, com relações para Categoria e Autor

## Endpoints da API

- `GET /livros/`: Lista todos os livros
- `POST /livros/`: Cria um novo livro
- `GET /livros/<id>/`: Retorna detalhes de um livro específico
- `PUT /livros/<id>/`: Atualiza um livro específico
- `DELETE /livros/<id>/`: Deleta um livro específico

## Instalação e Configuração

1. Clone o repositório:
   ```
   git clone git@github.com:Clintonrocha98/libary-django.git
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute as migrações:
   ```
   python manage.py migrate
   ```

4. Inicie o servidor:
   ```
   python manage.py runserver
   ```

## Uso

Para usar a API, você pode fazer requisições HTTP para os endpoints listados acima. Por exemplo:

```python
import requests

# Listar todos os livros
response = requests.get('http://localhost:8000/livros/')
print(response.json())

# Criar um novo livro
novo_livro = {
    'titulo': 'Novo Livro',
    'autor': 1,  # ID do autor
    'categoria': 1,  # ID da categoria
    'publicado_em': '2024-08-17'
}
response = requests.post('http://localhost:8000/livros/', json=novo_livro)
print(response.json())
```
