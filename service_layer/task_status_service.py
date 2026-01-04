from typing import Tuple, Union
from entities.task_status import TaskStatus
from data_access_layer.dao.task_status_dao import TaskStatusDAO

class TaskStatusService:
    """
    Serviço responsável pela lógica de negócio relacionada aos status das tarefas
    """
    def __init__(self, task_status_dao: TaskStatusDAO) -> None:
        """Inicializa um objeto TaskStatusService
        
        Parameters
        ----------
        task_status_dao: data_access_layer.dao.task_status_dao.TaskStatusDAO
            DAO para operações com status de tarefas
        """
        self._task_status_dao = task_status_dao

    def list_all_status(self) -> Union[Tuple[TaskStatus], None]:
        """Lista todos os status disponíveis no sistema
        
        Returns
        -------
        Union[Tuple[TaskStatus], None]
            Tupla com todos os status ou None se não houver status cadastrados
        """
        return self._task_status_dao.list_all()

    def get_status_by_name(self, status_name: str) -> Union[TaskStatus, None]:
        """Busca um status específico pelo nome
        Parameters
        ----------
        status_name: str
            Nome do status a ser buscado
        Returns
        -------
        Union[TaskStatus, None]
            Status encontrado ou None se não existir
        Raises
        ------
        ValueError
            Se o nome do status for inválido
        """
        if not status_name or not isinstance(status_name, str) or status_name.strip() == "":
            raise ValueError("O nome do status não pode ser vazio!")
        
        return self._task_status_dao.get_by_name(status_name.strip())

    def validate_status_name(self, status_name: str) -> bool:
        """Valida se um nome de status existe no sistema
        
        Parameters
        ----------
        status_name: str
            Nome do status a ser validado
            
        Returns
        -------
        bool
            True se o status existe, False caso contrário
        """
        if not status_name or not isinstance(status_name, str):
            return False
        
        status = self._task_status_dao.get_by_name(status_name.strip())
        
        return status is not None

    def get_available_status_names(self) -> Tuple[str]:
        """Retorna uma lista com os nomes de todos os status disponíveis
        
        Returns
        -------
        Tuple[str]
            Tupla com os nomes dos status disponíveis
        """
        all_status = self._task_status_dao.list_all()
        
        if all_status is None:
            return tuple()
        
        return tuple(status.name for status in all_status)