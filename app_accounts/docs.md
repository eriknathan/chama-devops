# Documentação do App: Contas (`app_accounts`)

## Visão Geral
O aplicativo `app_accounts` é responsável por todo o gerenciamento de identidade e acesso do sistema ChamaDevOps. Ele substitui o modelo de usuário padrão do Django para utilizar o e-mail como identificador principal, modernizando o fluxo de autenticação.

## Modelos de Dados

### `User` (Usuário Personalizado)
- **Herança**: `django.contrib.auth.models.AbstractUser`
- **Caminho**: `app_accounts.models.User`
- **Descrição**: Modelo de usuário central do sistema. Remove o campo `username` padrão e impõe o `email` como identificador único.
- **Campos Principais**:
    - `email` (EmailField): Identificador único e obrigatório. Usado para login.
    - `first_name` (CharField): Primeiro nome.
    - `last_name` (CharField): Sobrenome.
    - `is_staff` (BooleanField): Define se o usuário tem acesso às áreas administrativas/DevOps.
    - `is_active` (BooleanField): Define se a conta está ativa.
- **Gerenciador**: `UserManager` customizado para lidar com a criação de usuários e superusuários sem username.

## Funcionalidades e Views

### Autenticação
O app utiliza as views baseadas em classe do Django (`LoginView`, `LogoutView`) com templates customizados e estilizados com TailwindCSS.

- **Login**: `/accounts/login/`
    - Autenticação via Email e Senha.
    - Redirecionamento automático para o Dashboard após sucesso.
- **Logout**: `/accounts/logout/`
    - Encerra a sessão e redireciona para a página de login.

## Configuração
Para correta utilização, este app deve ser configurado no `settings.py`:
```python
AUTH_USER_MODEL = 'app_accounts.User'
```

## Permissões
O sistema baseia-se na flag `is_staff` para diferenciar perfis:
- **Usuário Comum (`is_staff=False`)**: Acesso apenas aos seus próprios tickets e abertura de novos chamados.
- **Administrador/DevOps (`is_staff=True`)**: Acesso total ao gerenciamento de projetos, tópicos e visualização de todos os tickets.
