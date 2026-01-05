from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Modelo base com campos de timestamp automáticos."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


from django.conf import settings

class Project(BaseModel):
    """Modelo de Projeto."""
    name = models.CharField(_('Nome'), max_length=100)
    description = models.TextField(_('Descrição'), blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_projects', verbose_name=_('Gerente'))
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', verbose_name=_('Usuários'))

    class Meta:
        verbose_name = _('Projeto')
        verbose_name_plural = _('Projetos')

    def __str__(self):
        return self.name


class Topic(BaseModel):
    """Modelo de Tópico."""
    name = models.CharField(_('Nome'), max_length=100)
    template = models.TextField(_('Modelo de Descrição'), blank=True, help_text=_('Texto padrão para preencher a descrição do ticket ao selecionar este tópico.'))
    form_fields = models.JSONField(_('Campos do Formulário'), default=list, blank=True, help_text=_('Esquema JSON para campos dinâmicos.'))
    
    class Meta:
        verbose_name = _('Tópico')
        verbose_name_plural = _('Tópicos')

    def __str__(self):
        return self.name
