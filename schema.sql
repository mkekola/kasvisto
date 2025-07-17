CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE plants (
    id INTEGER PRIMARY KEY,
    plant_name TEXT,
    light TEXT,
    care_info TEXT,
    user_id INTEGER REFERENCES users
);