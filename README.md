# E-commerce API

Uma API REST simples para sistema de e-commerce desenvolvida em Python com Flask.

## Tecnologias Utilizadas

- **Flask 2.3.0** - Framework web minimalista
- **Flask-SQLAlchemy 3.1.1** - ORM para integração com banco de dados
- **Flask-Login 0.6.2** - Sistema de autenticação de usuários
- **Flask-CORS 3.0.10** - Suporte para Cross-Origin Resource Sharing
- **Werkzeug 2.3.0** - Biblioteca WSGI utility
- **SQLite** - Banco de dados local

## Arquitetura e Padrões

- **Padrão MVC** - Separação entre modelos, views e controllers
- **API RESTful** - Endpoints seguindo convenções REST
- **ORM Pattern** - Mapeamento objeto-relacional com SQLAlchemy
- **Authentication Pattern** - Sistema de login baseado em sessões

## Funcionalidades

- ✅ Autenticação de usuários (login/logout)
- ✅ Gerenciamento de produtos (CRUD)
- ✅ Sistema de carrinho de compras
- ✅ Busca de produtos
- ✅ Documentação da API com Swagger

## Setup e Instalação

### Pré-requisitos

- Python 3.7+
- pip

### Instalação

1. Clone o repositório:

```bash
git clone <repository-url>
cd e-commerce-api
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
```

3. Ative o ambiente virtual:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Execute a aplicação:

```bash
python app.py
```

A API estará disponível em `http://127.0.0.1:5000`

## Documentação da API

A documentação completa da API está disponível no arquivo `swagger.yaml`.

### Principais Endpoints

- `POST /login` - Autenticação do usuário
- `POST /logout` - Logout do usuário
- `GET /api/products` - Lista todos os produtos
- `GET /api/products/{id}` - Busca produto por ID
- `GET /api/products/search` - Busca produtos por termo
- `POST /api/products/add` - Adiciona novo produto (requer autenticação)

## Banco de Dados

O projeto utiliza SQLite com as seguintes entidades:

- **User** - Usuários do sistema
- **Product** - Produtos do e-commerce
- **CartItem** - Itens do carrinho de compras

O banco de dados é criado automaticamente em `instance/ecommerce.db` na primeira execução.

## Configuração

As principais configurações podem ser alteradas no arquivo `app.py`:

```python
app.config['SECRET_KEY'] = 'your_secret_key'  # Altere para produção
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
```
