# Usa uma imagem oficial do Python leve
FROM python:3.12-slim

# Define a pasta de trabalho principal dentro do container
WORKDIR /app

# Copia o arquivo de dependências da pasta docker para o container
COPY docker/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia a pasta api inteira 
COPY api/ /app/api/

# Muda o diretório para dentro da pasta api para rodar o servidor
WORKDIR /app/api

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]