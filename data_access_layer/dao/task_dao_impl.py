from typing import Tuple, Union


from entities.task import Task
from entities.task_status import TaskStatus
from data_access_layer.dao.task_dao import TaskDAO
from data_access_layer.database_api_adapters.database_api_adapter import DatabaseAPIAdapter


class TaskDAOImpl(TaskDAO):

    def __init__(self, db_api_adapter: DatabaseAPIAdapter) -> None:

        """Inicializa um objeto TaskDAOImpl
        
        Parameters
        ----------
        db_api_adapter: data_access_layer.database_api_adapters.database_api_adapter.DatabaseAPIAdapter
            Adaptador de API de banco de dados a ser utilizado
        """

        self._db_api_adapter = db_api_adapter
        self._db_api_adapter.connect()

    def insert(self, task: Task) -> None:

        query = """
        INSERT INTO task(name, description, status_id) 
        VALUES (?, ?, ?)
        """

        self._db_api_adapter.execute(
            query, (task.name, task.description, task.status.id)
        )

    def list_all(self) -> Union[Tuple[Task], None]:

        query = """
        SELECT
            t.id as task_id,
            t.name as task_name,
            t.description as task_description,
            s.id as status_id,
            s.name as status_name
        FROM task as t
        JOIN task_status as s ON t.status_id = s.id
        """

        registries = self._db_api_adapter.fetch_all(query)

        if not registries:

            return None

        tasks = tuple([
            Task(
                registry["task_id"],
                registry["task_name"],
                registry["task_description"],
                TaskStatus(
                    registry["status_id"],
                    registry["status_name"],
                )
            )
            for registry in registries
        ])

        return tasks

    def delete(self, task_id: int) -> None:

        query = """
        DELETE FROM task
        WHERE id = ?
        """

        self._db_api_adapter.execute(
            query, (task_id,)
        )

    def update_status(self, task_id: int, status: TaskStatus) -> None:

        query = """
        UPDATE task SET status_id = ?
        WHERE id = ?
        """

        self._db_api_adapter.execute(
            query, (status.id, task_id)
        )