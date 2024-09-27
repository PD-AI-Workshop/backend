CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    password VARCHAR(100) NOT NULL,
    role_id INTEGER REFERENCES roles (id)
);