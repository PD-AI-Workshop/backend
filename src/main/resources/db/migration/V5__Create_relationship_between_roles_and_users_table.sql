ALTER TABLE users
    ADD CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES roles(id);