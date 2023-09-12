DROP TABLE IF EXISTS posts;

CREATE TABLE posts(
    id INTEGER PRIMARY KEY autoincrement, /* no geral é "auto_increment", mas no SQLite com PY é assim */
    titulo STRING NOT NULL,
    texto STRING NOT NULL,
    data_criacao TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
);

/* o comando sqlite3 banco.bd < esquema.sql no console python cria o BD a partir do esquema */