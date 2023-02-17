# Define a imagem base que será usada
FROM python:3.9-slim-buster

# Define o diretório de trabalho do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instala as dependências no contêiner
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto para o contêiner
COPY . .

# Define a porta que será exposta pelo contêiner
EXPOSE 80

# Define o comando que será executado quando o contêiner for iniciado
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
