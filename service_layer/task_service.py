from typing import Tuple, Union
from entities.task import Task
from entities.task_status import TaskStatus
from data_access_layer.dao.task_dao import TaskDAO
from data_access_layer.dao.task_status_dao import TaskStatusDAO

class TaskService:
    """
    Serviço responsável pela lógica de negócio relacionada às tarefas
    """
    def __init__(self, task_dao: TaskDAO, task_status_dao: TaskStatusDAO) -> None:
        """Inicializa um objeto TaskService
        
        Parameters
        ----------
        task_dao: data_access_layer.dao.task_dao.TaskDAO
            DAO para operações com tarefas
        task_status_dao: data_access_layer.dao.task_status_dao.TaskStatusDAO
            DAO para operações com status de tarefas
        """
        self._task_dao = task_dao
        self._task_status_dao = task_status_dao

    def create_task(self, name: str, description: str, status_name: str) -> None:
        """Cria uma nova tarefa no sistema
        
        Parameters
        ----------
        name: str
            Nome da tarefa
        description: str
            Descrição da tarefa
        status_name: str
            Nome do status inicial da tarefa (Disponível, Fazendo ou Feita)
            
        Raises
        ------
        ValueError
            Se o nome for vazio ou se o status não existir
        """
        # Validações de regra de negócio
        if not name or not isinstance(name, str) or name.strip() == "":
            raise ValueError("O nome da tarefa não pode ser vazio!")
        
        if not isinstance(description, str):
            raise ValueError("A descrição deve ser uma sequência de caracteres!")
        
        if not status_name or not isinstance(status_name, str):
            raise ValueError("O nome do status não pode ser vazio!")
        
        # Busca o status pelo nome
        status = self._task_status_dao.get_by_name(status_name)
        
        if status is None:
            raise ValueError(f"Status '{status_name}' não encontrado! Use: Disponível, Fazendo ou Feita")
        
        # Cria a tarefa (id será gerado pelo banco)
        task = Task(
            id=0,  # Será gerado automaticamente pelo banco
            name=name.strip(),
            description=description.strip(),
            status=status
        )
        
        # Persiste no banco de dados
        self._task_dao.insert(task)

    def list_all_tasks(self) -> Union[Tuple[Task], None]:
        """Lista todas as tarefas cadastradas no sistema
        
        Returns
        -------
        Union[Tuple[Task], None]
            Tupla com todas as tarefas ou None se não houver tarefas
        """
        return self._task_dao.list_all()

    def delete_task(self, task_id: int) -> None:
        """Remove uma tarefa do sistema
        
        Parameters
        ----------
        task_id: int
            Identificador da tarefa a ser removida
            
        Raises
        ------
        ValueError
            Se o ID for inválido ou se a tarefa não existir
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("O ID da tarefa deve ser um número inteiro positivo!")
        
        # Verifica se a tarefa existe
        all_tasks = self._task_dao.list_all()
        
        if all_tasks is None:
            raise ValueError("Não há tarefas cadastradas para remover!")
        
        task_exists = any(task.id == task_id for task in all_tasks)
        
        if not task_exists:
            raise ValueError(f"Tarefa com ID {task_id} não encontrada!")
        
        # Remove a tarefa
        self._task_dao.delete(task_id)

    def update_task_status(self, task_id: int, new_status_name: str) -> None:
        """Altera o status de uma tarefa
        
        Parameters
        ----------
        task_id: int
            Identificador da tarefa
        new_status_name: str
            Nome do novo status (Disponível, Fazendo ou Feita)
            
        Raises
        ------
        ValueError
            Se o ID for inválido, se a tarefa não existir ou se o status for inválido
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("O ID da tarefa deve ser um número inteiro positivo!")
        
        if not new_status_name or not isinstance(new_status_name, str):
            raise ValueError("O nome do status não pode ser vazio!")
        
        # Verifica se a tarefa existe
        all_tasks = self._task_dao.list_all()
        
        if all_tasks is None:
            raise ValueError("Não há tarefas cadastradas!")
        
        task_exists = any(task.id == task_id for task in all_tasks)
        
        if not task_exists:
            raise ValueError(f"Tarefa com ID {task_id} não encontrada!")
        
        # Busca o novo status
        new_status = self._task_status_dao.get_by_name(new_status_name)
        
        if new_status is None:
            raise ValueError(f"Status '{new_status_name}' não encontrado! Use: Disponível, Fazendo ou Feita")
        
        # Atualiza o status da tarefa
        self._task_dao.update_status(task_id, new_status)

    def get_task_by_id(self, task_id: int) -> Union[Task, None]:
        """Busca uma tarefa específica pelo ID
        
        Parameters
        ----------
        task_id: int
            Identificador da tarefa
            
        Returns
        -------
        Union[Task, None]
            Tarefa encontrada ou None se não existir
            
        Raises
        ------
        ValueError
            Se o ID for inválido
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("O ID da tarefa deve ser um número inteiro positivo!")
        
        all_tasks = self._task_dao.list_all()
        
        if all_tasks is None:
            return None
        
        for task in all_tasks:
            if task.id == task_id:
                return task
        
        return None