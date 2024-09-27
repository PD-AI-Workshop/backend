CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    views INTEGER NOT NULL DEFAULT 0,
    likes INTEGER NOT NULL DEFAULT 0,
    dislikes INTEGER NOT NULL DEFAULT 0,
    created_at DATE NOT NULL,
    content TEXT NOT NULL,
    reading_time INTEGER NOT NULL DEFAULT 0,
    image_name VARCHAR(255) NOT NULL,
    user_id INTEGER REFERENCES users (id)
)