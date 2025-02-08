FROM python:3.11

# Evita criação de arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Instala pacotes necessários
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependências e instala
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o código da aplicação para o container
COPY . /app/

# Copia os scripts e ajusta permissões
COPY ./scripts/bash/xvfb-run.sh /mnt/scripts/xvfb-run.sh
RUN chmod +x /mnt/scripts/xvfb-run.sh

# Define o servidor X virtual
ENV DISPLAY=:99

# Define o ponto de entrada do container
ENTRYPOINT ["/mnt/scripts/xvfb-run.sh"]

# Comando padrão do container
CMD ["python", "manage.py", "runserver", "--noreload", "0.0.0.0:8000"]
