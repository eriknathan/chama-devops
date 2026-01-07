# Usar imagem Node.js para compilar Tailwind CSS
FROM node:20-alpine AS tailwind-builder

WORKDIR /app

# Copiar arquivos de configuração
COPY package.json tailwind.config.js postcss.config.js ./
COPY static/src ./static/src
COPY templates ./templates
COPY app_*/templates ./app_templates/

# Instalar dependências e compilar CSS
RUN npm install && npm run build

# ================================
# Imagem final Python
# ================================
FROM python:3.12-slim

# Definir variáveis de ambiente
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

# Copiar CSS compilado do estágio anterior (DEPOIS de COPY . para sobrescrever o diretório vazio)
RUN mkdir -p /app/static/css
COPY --from=tailwind-builder /app/static/css/style.css /app/static/css/style.css

# Expor porta
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
