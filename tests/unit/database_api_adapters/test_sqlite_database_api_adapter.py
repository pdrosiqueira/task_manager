import pytest


from data_access_layer.database_api_adapters.sqlite_database_api_adapter import SQLiteDatabaseAPIAdapter


class TestSQLiteDatabaseAPIAdapter:

    def test_filename(self):
        
        # String
        SQLiteDatabaseAPIAdapter("database.db")

        # String vazia
        with pytest.raises(ValueError):

            SQLiteDatabaseAPIAdapter("")
        
        # Inteiro
        with pytest.raises(ValueError):

            SQLiteDatabaseAPIAdapter(1)
        
        # Float
        with pytest.raises(ValueError):

            SQLiteDatabaseAPIAdapter(3.4)
        
        # Sequência
        with pytest.raises(ValueError):

            SQLiteDatabaseAPIAdapter([1, 2, 3])

