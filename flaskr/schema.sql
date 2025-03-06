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


INSERT INTO user (id, email, username, password, role, blocked) VALUES 
(1, 'user1@example.com', 'user1', 'scrypt:32768:8:1$hashed_password_here', 'user', 0);

INSERT INTO todo (user_id, title, completed) VALUES
(1, 'Công việc 1', 0), (1, 'Công việc 2', 1), (1, 'Công việc 3', 0), (1, 'Công việc 4', 0),
(1, 'Công việc 5', 1), (1, 'Công việc 6', 0), (1, 'Công việc 7', 0), (1, 'Công việc 8', 1),
(1, 'Công việc 9', 0), (1, 'Công việc 10', 0), (1, 'Công việc 11', 0), (1, 'Công việc 12', 1),
(1, 'Công việc 13', 0), (1, 'Công việc 14', 0), (1, 'Công việc 15', 1), (1, 'Công việc 16', 0),
(1, 'Công việc 17', 0), (1, 'Công việc 18', 1), (1, 'Công việc 19', 0), (1, 'Công việc 20', 0),
(1, 'Công việc 21', 0), (1, 'Công việc 22', 1), (1, 'Công việc 23', 0), (1, 'Công việc 24', 0),
(1, 'Công việc 25', 1);