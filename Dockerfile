# Define a imagem base que será usada
FROM python:3.9-slim-buster

# Define o diretório de trabalho do contêiner
WORKDIR /app

# Copia o arquivo Pipfile e Pipfile.lock para o contêiner
COPY Pipfile Pipfile.lock ./

# Instala o pipenv no contêiner
RUN pip install pipenv

# Instala as dependências no contêiner
RUN pipenv install --system --deploy

# Copia os arquivos do projeto para o contêiner
COPY . .

# Define a porta que será exposta pelo contêiner
EXPOSE 80

# Define o comando que será executado quando o contêiner for iniciado
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
