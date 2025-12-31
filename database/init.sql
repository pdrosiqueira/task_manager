CREATE TABLE task_status(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL
);

CREATE TABLE task(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    description VARCHAR,
    status_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES task_status(id)
        ON DELETE CASCADE 
);

INSERT INTO task_status(name) VALUES ("Disponível"), ("Fazendo"), ("Feita");
