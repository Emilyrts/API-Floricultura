# Usa imagem oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta configurada no Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
