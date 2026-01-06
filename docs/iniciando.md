# Iniciando o Projeto

Este guia descreve como configurar o ambiente de desenvolvimento para o ChamaDevOps.

## Pré-requisitos

*   **Docker** e **Docker Compose** instalados (recomendado).
*   **Python 3.12+** instalado (para desenvolvimento local sem Docker).
*   **Git** instalado.

---

## Opção 1: Setup com Docker (Recomendado)

A maneira mais rápida de rodar o projeto é utilizando Docker.

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd chama-devops
```

### 2. Inicie os containers

```bash
make restart
```

Este comando irá:
- Subir o banco PostgreSQL
- Subir o MinIO (armazenamento de arquivos)
- Subir a aplicação Django
- Subir o Nginx como proxy reverso

### 3. Aplique as migrações e crie um superusuário

```bash
make migrate
make createsuperuser
```

### 4. (Opcional) Popular com dados de teste

```bash
make populate
```

### 5. Acesse a aplicação

*   **Aplicação:** http://localhost
*   **Admin:** http://localhost/admin
*   **MinIO Console:** http://localhost:9001

---

## Opção 2: Setup Local (Sem Docker)

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd chama-devops
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados

O projeto utilizará SQLite por padrão em desenvolvimento local.

```bash
python manage.py migrate
```

### 5. Crie um Superusuário (Admin)

```bash
python manage.py createsuperuser
```

### 6. Inicie o Servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

---

## Comandos Úteis (Makefile)

O projeto inclui um `Makefile` para facilitar operações comuns:

| Comando | Descrição |
|---------|-----------|
| `make restart` | Reinicia todos os containers Docker |
| `make up` | Sobe os containers em background |
| `make down` | Para todos os containers |
| `make logs` | Mostra logs da aplicação |
| `make migrate` | Executa migrações do banco |
| `make makemigrations` | Cria novas migrações |
| `make createsuperuser` | Cria usuário administrador |
| `make populate` | Popula o banco com dados de teste |
| `make shell` | Abre shell Django interativo |

---

## Comandos Django (Sem Docker)

*   **Criar novas migrações:**
    ```bash
    python manage.py makemigrations
    ```

*   **Verificar integridade do projeto:**
    ```bash
    python manage.py check
    ```

*   **Coletar arquivos estáticos:**
    ```bash
    python manage.py collectstatic
    ```

---

## Variáveis de Ambiente

Para configuração de produção, defina as seguintes variáveis:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DEBUG` | Modo debug | `True` |
| `SECRET_KEY` | Chave secreta Django | Auto-gerada |
| `DATABASE_URL` | URL do banco PostgreSQL | SQLite |
| `MINIO_ENDPOINT` | Endpoint do MinIO | `minio:9000` |
| `MINIO_ACCESS_KEY` | Chave de acesso MinIO | `minioadmin` |
| `MINIO_SECRET_KEY` | Chave secreta MinIO | `minioadmin` |
