from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User


class CustomAuthenticationForm(AuthenticationForm):
    """Formulário de autenticação personalizado com classes Tailwind."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'appearance-none rounded-lg relative block w-full px-3 py-2 border border-input bg-background/50 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring sm:text-sm transition-colors'


class CustomUserCreationForm(UserCreationForm):
    """Formulário de criação de usuário personalizado com classes Tailwind."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'appearance-none rounded-lg relative block w-full px-3 py-2 border border-input bg-background/50 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring sm:text-sm transition-colors'

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class AdminUserCreationForm(UserCreationForm):
    """Formulário para admin criar usuários."""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ['is_staff', 'is_active']:
                field.widget.attrs['class'] = 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
            else:
                field.widget.attrs['class'] = 'appearance-none rounded-lg relative block w-full px-3 py-2 border border-input bg-background/50 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring sm:text-sm transition-colors'


class CustomUserChangeForm(UserChangeForm):
    """Formulário de alteração de usuário personalizado."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'appearance-none rounded-lg relative block w-full px-3 py-2 border border-input bg-background/50 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring sm:text-sm transition-colors'

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
