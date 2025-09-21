FROM python:3.12-slim AS builder

# Crie o diretório de trabalho no contexto de construção
WORKDIR /build

# Copie o conteúdo necessário para o contexto de construção
COPY . .

# Instale as dependências Python
RUN pip install --no-cache-dir -r /build/requirements.txt

# Comando para executar o servidor
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
