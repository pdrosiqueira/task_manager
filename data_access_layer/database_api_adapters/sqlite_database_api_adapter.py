import sqlite3
from typing import Dict, List, Tuple, Union, Any


from data_access_layer.database_api_adapters.database_api_adapter import DatabaseAPIAdapter

class SQLiteDatabaseAPIAdapter(DatabaseAPIAdapter):

    """
    Adaptador da API do SQLite
    """

    _instance = None

    def __new__(cls, *args, **kwargs) -> 'SQLiteDatabaseAPIAdapter':

        """Retorna uma instância da classe SQLiteDatabaseAPIAdapter alocada em memória

        Returns
        -------
        database.sqlite_database_adapter.SQLiteDatabaseAPIAdapter
            Objeto SQLiteDatabaseAPIAdapter alocado
        """

        if cls._instance is None:

            cls._instance = object.__new__(cls)

        return cls._instance
    
    def __init__(self, filename: str) -> None:

        """Inicializa um objeto SQLiteDatabaseAPIAdapter

        Parameters
        ----------
        filename: str
            Nome do arquivo do banco de dados
        """

        if not isinstance(filename, str) or filename == "":

            raise ValueError("O nome do arquivo do banco deve ser uma sequência de caracteres não vazio!")
        
        self._filename = filename

    def connect(self):

        self.connection = sqlite3.connect(self._filename)
    
    def execute(self, query: str, parameters: Tuple[Any]=()) -> None:

        cursor = self.connection.cursor()

        cursor.execute(query, parameters)

        self.connection.commit()

        cursor.close()
    
    def fetch_all(self, query: str, parameters: Tuple[Any]=()) -> Union[List[Dict[str, Any]], None]:

        cursor = self.connection.cursor()

        cursor = cursor.execute(query, parameters)

        rows = cursor.fetchall()

        if not rows:

            return None
        
        column_names = cursor.description

        data = [
            {column_name: value for column_name, value in zip(column_names, row)} 
            for row in rows
        ]

        return data
    
    def fetch_one(self, query: str, parameters: Tuple[Any]=()) -> Union[Dict[str, Any], None]:

        cursor = self.connection.cursor()

        cursor = cursor.execute(query, parameters)

        row = cursor.fetchone()

        if not row:

            return None
        
        column_names = cursor.description

        data = {column_name: value for column_name, value in zip(column_names, row)}

        return data

    def close_connection(self) -> None:

        self.connection.close()

