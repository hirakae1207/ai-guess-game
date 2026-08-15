SET NAMES utf8mb4;
CREATE TABLE Themes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    theme VARCHAR(64)
);

CREATE TABLE Topics(
    id INT AUTO_INCREMENT PRIMARY KEY,
    theme_id INT,
    topic_text VARCHAR(64),
    FOREIGN KEY (theme_id) REFERENCES Themes(id)
);

CREATE TABLE Topic_pairs(
    id INT AUTO_INCREMENT PRIMARY KEY,
    theme_id INT,
    topic1_id INT,
    topic2_id INT,
    FOREIGN KEY (theme_id) REFERENCES Themes(id),
    FOREIGN KEY (topic1_id) REFERENCES Topics(id),
    FOREIGN KEY (topic2_id) REFERENCES Topics(id)
);
-- pair_idを消去

CREATE TABLE Players(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64),
    assigned_topic_id INT,
    keyword VARCHAR(64),
    FOREIGN KEY (assigned_topic_id) REFERENCES Topics(id)
);

INSERT INTO Themes(theme)VALUES("フルーツ");
INSERT INTO Themes(theme)VALUES("動物");

INSERT INTO Topics(theme_id, topic_text)VALUES(1, "りんご");
INSERT INTO Topics(theme_id, topic_text)VALUES(1, "梨");

INSERT INTO Topics(theme_id, topic_text)VALUES(2, "犬");
INSERT INTO Topics(theme_id, topic_text)VALUES(2, "猫");

INSERT INTO Topic_pairs(theme_id, topic1_id, topic2_id)VALUES(1, 1, 2);
INSERT INTO Topic_pairs(theme_id, topic1_id, topic2_id)VALUES(2, 3, 4);