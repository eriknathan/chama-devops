# Iniciando o Projeto

Este guia descreve como configurar o ambiente de desenvolvimento para o ChamaDevOps.

## Pré-requisitos

*   **Python 3.12+** instalado.
*   **Git** instalado.

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd chama-devops
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # ou
    venv\Scripts\activate     # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados (Migrações):**
    O projeto utiliza SQLite por padrão em desenvolvimento.
    ```bash
    python manage.py migrate
    ```

5.  **Crie um Superusuário (Admin):**
    necessário para acessar a área administrativa e ter permissões de Staff.
    ```bash
    python manage.py createsuperuser
    ```

6.  **Inicie o Servidor:**
    ```bash
    python manage.py runserver
    ```
    Acesse: `http://127.0.0.1:8000/`

## Comandos Úteis

*   **Criar novas migrações (após mudar models):**
    ```bash
    python manage.py makemigrations
    ```
*   **Verificar integridade do projeto:**
    ```bash
    python manage.py check
    ```
