DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS todo;

CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'user',
  blocked INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE todo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  completed INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

INSERT INTO user (id, email, username, password, role, blocked) VALUES (
  0, 
  'admin@example.com', 
  'admin', 
  'scrypt:32768:8:1$oVVcYjs75xgYv3ji$469abbb391ac73345e913fcb0d3a4df1d6462f83af04ac8037bd0a2552e31ddde9d1ea896c1bb2f02cfbb3026fcff2934abfe4adf89cea3056aad0c78683e990', 
  'admin', 
  0
);
