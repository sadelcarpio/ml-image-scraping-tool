CREATE TABLE users
(
    id UUID NOT NULL,
    username VARCHAR(64) NOT NULL,
    email VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL,
    full_name VARCHAR(64) NOT NULL,
    is_admin BOOL NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE projects
(
    id   SERIAL      NOT NULL,
    owner_id UUID,
    name VARCHAR(64) NOT NULL,
    keywords TEXT NOT NULL,
    description TEXT,
    task_type VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name),
    FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE urls
(
    id         SERIAL      NOT NULL,
    user_id    UUID,
    project_id INTEGER,
    gcs_url    VARCHAR     NOT NULL,
    hashed_url VARCHAR(64) NOT NULL,
    labeled    BOOLEAN,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (gcs_url),
    UNIQUE (hashed_url),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL
);

CREATE TABLE users_projects (
    user_id UUID,
    project_id INTEGER,
    current_url INTEGER,
    assigned_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (user_id, project_id),
    FOREIGN KEY(user_id) REFERENCES users (id),
    FOREIGN KEY(project_id) REFERENCES projects (id),
    FOREIGN KEY(current_url) REFERENCES urls (id)
);

CREATE TABLE labels (
    id SERIAL NOT NULL,
    project_id INTEGER,
    label VARCHAR(64) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);