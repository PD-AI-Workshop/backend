ALTER TABLE files
    ADD CONSTRAINT fk_file FOREIGN KEY (article_id) REFERENCES articles(id);