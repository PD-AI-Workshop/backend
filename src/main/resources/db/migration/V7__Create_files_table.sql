CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    type VARCHAR(255) NOT NULL,
    size BIGINT NOT NULL,
    article_id INTEGER REFERENCES articles (id)
);