from unittest.mock import Mock


from data_access_layer.dao.task_status_dao_impl import TaskStatusDAOImpl
from entities.task import Task
from entities.task_status import TaskStatus

class TestTaskStatusDAO:

    def test_list_all(self):

        fake_db_api_adapter = Mock()

        task_status_dao = TaskStatusDAOImpl(fake_db_api_adapter)

        expected_values = [
            TaskStatus(1, "Disponível"),
            TaskStatus(2, "Fazendo"),
            TaskStatus(3, "Feita"),
        ]

        fake_db_api_adapter.fetch_all.return_value = [
            {
                "id": 1, 
                "name": "Disponível"
            },
            {
                "id": 2, 
                "name": "Fazendo"
            },
            {
                "id": 3, 
                "name": "Feita"
            },
        ]

        tasks_status = task_status_dao.list_all()

        fake_db_api_adapter.fetch_all.assert_called_once()

        args, _ = fake_db_api_adapter.fetch_all.call_args

        query_passed = args[0]

        expected_query = """
        SELECT id, name
        FROM task_status
        """

        assert query_passed == expected_query

        for task_status, expected_value in zip(tasks_status, expected_values):

            assert task_status.id == expected_value.id
            assert task_status.name == expected_value.name
    
    def test_list_all_empty(self):

        fake_db_api_adapter = Mock()

        task_status_dao = TaskStatusDAOImpl(fake_db_api_adapter)

        expected_value = None

        fake_db_api_adapter.fetch_all.return_value = None

        tasks_status = task_status_dao.list_all()

        fake_db_api_adapter.fetch_all.assert_called_once()

        args, _ = fake_db_api_adapter.fetch_all.call_args

        query_passed = args[0]

        expected_query = """
        SELECT id, name
        FROM task_status
        """

        assert query_passed == expected_query

        assert tasks_status == expected_value
    
    def test_get_by_name(self):

        fake_db_api_adapter = Mock()

        task_status_dao = TaskStatusDAOImpl(fake_db_api_adapter)

        status_name = "Disponível"

        expected_value = TaskStatus(
            1,
            status_name
        )

        fake_db_api_adapter.fetch_one.return_value = {
            "id": 1,
            "name": status_name,
        }

        task_status = task_status_dao.get_by_name(status_name)

        fake_db_api_adapter.fetch_one.assert_called_once()

        args, _ = fake_db_api_adapter.fetch_one.call_args

        query_passed = args[0]
        parameters_passed = args[1]

        expected_query = """
        SELECT id, name
        FROM task_status
        WHERE name = ?
        """

        assert query_passed == expected_query

        assert parameters_passed[0] == status_name

        assert task_status.id == expected_value.id

        assert task_status.name == expected_value.name
    
    def test_get_by_name_empty(self):

        fake_db_api_adapter = Mock()

        task_status_dao = TaskStatusDAOImpl(fake_db_api_adapter)

        status_name = "Feito"

        expected_value = None

        fake_db_api_adapter.fetch_one.return_value = None

        task_status = task_status_dao.get_by_name(status_name)

        fake_db_api_adapter.fetch_one.assert_called_once()

        args, _ = fake_db_api_adapter.fetch_one.call_args

        query_passed = args[0]
        parameters_passed = args[1]

        expected_query = """
        SELECT id, name
        FROM task_status
        WHERE name = ?
        """

        assert query_passed == expected_query

        assert parameters_passed[0] == status_name

        assert task_status == expected_value



