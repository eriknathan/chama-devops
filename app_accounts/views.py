from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, AdminUserCreationForm
from .models import User


class SignUpView(CreateView):
    """View de cadastro de usuário."""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class CustomLoginView(LoginView):
    """View de login personalizada."""
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class ProfileView(LoginRequiredMixin, UpdateView):
    """View de edição de perfil do usuário."""
    model = User
    form_class = CustomUserChangeForm
    template_name = 'app_accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Retorna o usuário atual."""
        return self.request.user


from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import SetPasswordForm
from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import get_object_or_404, redirect

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin para garantir que apenas membros da equipe acessem a view."""
    def test_func(self):
        return self.request.user.is_staff

from django.db.models import Q

class UserListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """View para listar usuários com suporte a busca e paginação."""
    model = User
    template_name = 'app_accounts/user_list.html'
    context_object_name = 'users'
    ordering = ['-date_joined']
    paginate_by = 10

    def get_queryset(self):
        """Filtra usuários baseado na busca."""
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """Adiciona termo de busca ao contexto."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class UserDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """View para detalhes do usuário."""
    model = User
    template_name = 'app_accounts/user_detail.html'
    context_object_name = 'target_user'

class UserUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """View para atualização de usuário por admin."""
    model = User
    fields = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']
    template_name = 'app_accounts/user_form.html'
    context_object_name = 'target_user'

    def get_success_url(self):
        """Retorna para detalhes do usuário após sucesso."""
        return reverse_lazy('user-detail', kwargs={'pk': self.object.pk})

class UserCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """View para criação de usuários por admin."""
    model = User
    form_class = AdminUserCreationForm
    template_name = 'app_accounts/user_create_form.html'
    success_url = reverse_lazy('user-list')

class AdminUserPasswordChangeView(LoginRequiredMixin, StaffRequiredMixin, FormView):
    """View para admin alterar senha de usuário."""
    template_name = 'app_accounts/admin_password_change.html'
    form_class = SetPasswordForm

    def get_form_kwargs(self):
        """Adiciona usuário alvo aos argumentos do formulário."""
        kwargs = super().get_form_kwargs()
        self.target_user = get_object_or_404(User, pk=self.kwargs['pk'])
        kwargs['user'] = self.target_user
        return kwargs

    def form_valid(self, form):
        """Salva a nova senha."""
        form.save()
        return redirect('user-detail', pk=self.target_user.pk)

    def get_context_data(self, **kwargs):
        """Adiciona usuário alvo ao contexto."""
        context = super().get_context_data(**kwargs)
        context['target_user'] = self.target_user
        return context
