import os

from app.utils.constants import Constants


class Files:
    """
        Classe utilitária para trasformação de arquivos.
    """

    @staticmethod
    def create_folder_structure():
        """
            Cria a estrutura de pastas necessárias.

            Esta função cria as pastas especificadas na lista retornada pela função `lista_pasta` da classe `Constantes`. Se a pasta não existir, ela será criada.
        """
        for constante in Constants().folder_list():
            if not os.path.exists(constante):
                os.makedirs(constante)
