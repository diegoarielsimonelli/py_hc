DROP TABLE IF EXISTS paciente;

CREATE TABLE paciente(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL,
    [age] INTEGER NOT NULL,
    [nationality] TEXT NOT NULL,
    [diagnosis] TEXT NOT NULL,
    [telephone] INTEGER NOT NULL,
    [treatment] TEXT NOT NULL,
);