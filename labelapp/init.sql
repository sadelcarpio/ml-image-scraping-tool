CREATE TABLE users
(
    id UUID NOT NULL,
    name VARCHAR(64) NOT NULL,
    email VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE projects
(
    id   SERIAL      NOT NULL,
    name VARCHAR(64) NOT NULL,
    keywords TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    owner_id UUID,
    PRIMARY KEY (id),
    UNIQUE (name),
    FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE urls
(
    id         SERIAL      NOT NULL,
    gcs_url    VARCHAR     NOT NULL,
    hashed_url VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    labeled    BOOLEAN,
    user_id    UUID,
    project_id INTEGER,
    PRIMARY KEY (id),
    UNIQUE (gcs_url),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL
);
