import json
import logging.config
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from mongoengine import disconnect, connect
from starlette.middleware.cors import CORSMiddleware

from app.utils.constants import Constants

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

root_path = os.getenv("ROOT_PATH", "")
APP_TITLE: str = "integracao_projeto_base"

# Cria uma instância do FastAPI
app = FastAPI(title="API de Automação ...",
              summary="""descrição breve""",
              description="""descrição

### Funcionalidades Principais:

- **Automação de ?**: Facilita a criação, gerenciamento e...

```Responsáveis: Danton Issler Rodrigues```""",
              version=os.environ.get("VERSION"),
              contact={"name": "Personal Finance Control APP", "email": "dantonissler18@gmail.com"},
              license_info={"name": "Copyright © Personal Finance Control APP - Todos os direitos reservados."},
              openapi_tags=[{"name": "Teste", "description": "Breve descrição."}],
              swagger_ui_parameters={"syntaxHighlight.theme": "ascetic", "deepLinking": False, "defaultModelsExpandDepth": -1, "filter": True, "docExpansion": "none"})

# Inicializa o banco de dados mongoengine
host_mongo = os.getenv("MONGO_DB_URL")
disconnect(alias='default')
connect(db=os.getenv('MONGO_DB_NAME'), host=host_mongo)

# Configura o app
app.secret_key = os.getenv('APP_SECRET_KEY')
app.max_request_size = 1000 * 1024 * 1024

if os.environ.get("ENVIRONMENT") != "development":
    try:
        multiprocessing.set_start_method("fork")
    except RuntimeError as e:
        if "context has already been set" not in str(e):
            raise
        logging.debug("Multiprocessing start method already set.")
from app.utils.files import Files

# Criar a estrutura de pastas necessárias para rodar a aplicação.
Files.create_folder_structure()

try:
    if os.path.exists('logging.json'):
        # Carrega o arquivo de configuração do logging
        with open('logging.json', 'rt') as f:
            config = json.load(f)
        # Configura o logging com base no arquivo de configuração
        logging.config.dictConfig(config)
except Exception as e:
    # Configura o logging com o nível de log INFO como padrão
    logging.basicConfig(level=logging.INFO)

from app.domain.controllers import router as teste_controller

routers = [teste_controller]

for router in routers:
    app.include_router(router)
