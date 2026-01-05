# Usar imagem oficial do Python
FROM python:3.12-slim

# Definir variáveis de ambiente
# PYTHONDONTWRITEBYTECODE: Previne Python de escrever arquivos pyc
# PYTHONUNBUFFERED: Previne Python de bufferizar stdout e stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0 \
    libjpeg-dev \
    libopenjp2-7-dev \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar projeto
COPY . /app/

# Coletar arquivos estáticos (se necessário descomentar e ajustar)
# RUN python manage.py collectstatic --noinput

# Expor porta
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
