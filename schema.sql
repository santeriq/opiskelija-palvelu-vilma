CREATE TABLE Users (id SERIAL PRIMARY KEY, username VARCHAR, password VARCHAR, visible BOOLEAN);
CREATE TABLE RoleRequests (id SERIAL PRIMARY KEY, username VARCHAR, message TEXT, sent VARCHAR);
CREATE TABLE Courses (id SERIAL PRIMARY KEY, key VARCHAR, name VARCHAR, credits INT, status BOOLEAN, visible BOOLEAN);