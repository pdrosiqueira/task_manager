from typing import Tuple, Union


from entities.task_status import TaskStatus
from data_access_layer.database_api_adapters.database_api_adapter import DatabaseAPIAdapter
from data_access_layer.dao.task_status_dao import TaskStatusDAO


class TaskStatusDAOImpl(TaskStatusDAO):

    def __init__(self, db_api_adapter: DatabaseAPIAdapter) -> None:

        """Inicializa um objeto TaskDAOImpl
        
        Parameters
        ----------
        db_api_adapter: data_access_layer.database_api_adapters.database_api_adapter.DatabaseAPIAdapter
            Adaptador de API de banco de dados a ser utilizado
        """

        self._db_api_adapter = db_api_adapter
        self._db_api_adapter.connect()

    def list_all(self) -> Union[Tuple[TaskStatus], None]:

        query = """
        SELECT id, name
        FROM task_status
        """

        registries = self._db_api_adapter.fetch_all(query)

        if not registries:

            return None

        tasks_status = tuple([
            TaskStatus(
                registry["id"],
                registry["name"],
            )
            for registry in registries
        ])

        return tasks_status

    def get_by_name(self, status_name: str) -> Union[TaskStatus, None]:

        query = """
        SELECT id, name
        FROM task_status
        WHERE name = ?
        """

        registry = self._db_api_adapter.fetch_one(query, (status_name,))

        if not registry:

            return None
        
        task_status = TaskStatus(
            registry["id"],
            registry["name"]
        )

        return task_status