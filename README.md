# Task Manager

Projeto que gerencia tarefas criadas pelo usuário

## Padrões de Projeto Usados

Padrão de Projeto | Localização | Motivação
----------------- | ----------- | ---------
Singleton | [Método \_\_new\_\_ da classe SQLiteDatabaseAPIAdapter](/data_access_layer/database_api_adapters/sqlite_database_api_adapter.py) | Criar uma única instância para que não haja concorrência nas transações do banco de dados
Adapter | [Classe abstrata DatabaseAPIAdapter](/data_access_layer/database_api_adapters/database_api_adapter.py) | Gerar uma interface global que lida com as diferentes APIs de diferentes SGBDs, de modo a evitar incompatibilidade

## Padrão Arquitetural

O seguinte projeto implementa um padrão arquitetural de três camadas.

- [Camada de Apresentação](/presentation_layer/)
- [Camada de Serviço](/service_layer/)
- [Camada de Acesso aos Dados](/data_access_layer/)

## Estrutura do Projeto

```
├── data_access_layer
│   ├── dao
│   │   ├── __init__.py
│   │   ├── task_dao_impl.py
│   │   ├── task_dao.py
│   │   ├── task_status_dao_impl.py
│   │   └── task_status_dao.py
│   ├── database_api_adapters
│   │   ├── database_api_adapter.py
│   │   ├── __init__.py
│   │   └── sqlite_database_api_adapter.py
│   └── __init__.py
├── database
│   ├── init.sql
│   └── schema.db
├── entities
│   ├── __init__.py
│   ├── task.py
│   └── task_status.py
├── main.py
├── presentation_layer
│   └── __init__.py
│   └── task_controller.py
├── README.md
├── requirements.txt
├── service_layer
│   └── __init__.py
│   └── task_service.py
│   └── task_status_service.py
└── tests
    ├── intregation
    └── unit
        ├── dao
        │   ├── test_task_dao.py
        │   └── test_task_status_dao.py
        ├── database_api_adapters
        │   └── test_sqlite_database_api_adapter.py
        └── entities
            ├── test_task.py
            └── test_task_status.py
```
