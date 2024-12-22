import sqlite3

schema = """
CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY
    discord_id TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE session (
    id TEXT NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user(id),
    expires_at INTEGER NOT NULL
);

"""


def init():
    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()
    c.execute(schema)
    conn.commit()
    conn.close()
