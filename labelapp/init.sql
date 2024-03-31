CREATE TYPE tasktype AS ENUM ('multilabel', 'sparse', 'regression', 'detection');

CREATE TABLE users
(
    id UUID NOT NULL,
    username VARCHAR(64) NOT NULL,
    email VARCHAR(64) NOT NULL,
    hashed_password VARCHAR(64) NOT NULL,
    full_name VARCHAR(64) NOT NULL,
    is_admin BOOL NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (username),
	UNIQUE (email)
);

CREATE TABLE projects
(
    id   SERIAL      NOT NULL,
    owner_id UUID,
    name VARCHAR(64) NOT NULL,
    keywords TEXT NOT NULL,
    description TEXT,
    task_type tasktype,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name),
    FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE labels (
    id SERIAL NOT NULL,
    project_id INTEGER,
    name VARCHAR(64) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
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
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
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

CREATE TABLE labeled_urls (
	url_id INTEGER NOT NULL,
	label_id INTEGER NOT NULL,
	labeled_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (url_id, label_id),
	FOREIGN KEY(url_id) REFERENCES urls (id) ON DELETE CASCADE,
	FOREIGN KEY(label_id) REFERENCES labels (id) ON DELETE CASCADE
);

CREATE VIEW labels_for_processing
AS SELECT u.gcs_url, l.name as label, lu.labeled_at, p.name AS project
FROM labeled_urls lu
INNER JOIN urls u ON u.id = lu.url_id
INNER JOIN labels l ON l.id = lu.label_id
INNER JOIN projects p ON p.id = u.project_id;
