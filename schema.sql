CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, role TEXT, visible BOOLEAN);
CREATE TABLE RoleRequests (id SERIAL PRIMARY KEY, username TEXT, message TEXT, sent TEXT);
CREATE TABLE Courses (id SERIAL PRIMARY KEY, tag TEXT, name TEXT, credits INT, open BOOLEAN, visible BOOLEAN);

INSERT INTO Users (username, password, role, visible) VALUES ('admin1', 'pbkdf2:sha256:260000$kgyYu8LdLXAuWNvr$b15c687fbd4c5d23f6cf57f431045ea20e40ebcac5fae47dd1e0356701273fe7', 'admin', 'true');
INSERT INTO Users (username, password, role, visible) VALUES ('teacher1', 'pbkdf2:sha256:260000$kgyYu8LdLXAuWNvr$b15c687fbd4c5d23f6cf57f431045ea20e40ebcac5fae47dd1e0356701273fe7', 'teacher', 'true');
INSERT INTO Users (username, password, role, visible) VALUES ('student1', 'pbkdf2:sha256:260000$kgyYu8LdLXAuWNvr$b15c687fbd4c5d23f6cf57f431045ea20e40ebcac5fae47dd1e0356701273fe7', 'student', 'true');
INSERT INTO Users (username, password, role, visible) VALUES ('user1', 'pbkdf2:sha256:260000$kgyYu8LdLXAuWNvr$b15c687fbd4c5d23f6cf57f431045ea20e40ebcac5fae47dd1e0356701273fe7', 'none', 'true');

INSERT INTO Courses (tag, name, credits, open, visible) VALUES ('ohpe2021', 'Ohjelmoinnin perusteet 2021', 5, 'false', 'true');
INSERT INTO Courses (tag, name, credits, open, visible) VALUES ('ohja2021', 'Ohjelmoinnin jatkokurssi 2021', 5, 'false', 'true');
INSERT INTO Courses (tag, name, credits, open, visible) VALUES ('ohpe2022', 'Ohjelmoinnin perusteet 2022', 5, 'true', 'true');
INSERT INTO Courses (tag, name, credits, open, visible) VALUES ('ohja2022', 'Ohjelmoinnin jatkokurssi 2022', 5, 'true', 'true');
INSERT INTO Courses (tag, name, credits, open, visible) VALUES ('lapio2021', 'Tietokone työvälineenä 2021', 1, 'false', 'true');
INSERT INTO Courses (tag, name, credits, open, visible) VALUES ('lapio2022', 'Tietokone työvälineenä 2022', 5, 'true', 'true');

INSERT INTO RoleRequests (username, message, sent) VALUES ('user1', 'moi', '19/04/2023 15:06:08');





